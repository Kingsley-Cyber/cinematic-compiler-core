"""The automatic author (PLAN-008, owner ADR-O112): an idea in, a prompt out.

`author(query, backend)` runs the pipeline. At each authored step it hands the step's sealed packet to the backend
(one call per step; the packet, with its instructions, is the prompt), binds the returned document to the packet,
and lets the step's own checks judge it. A refusal goes back to the step that can fix it (compiler/replan_trigger.py:
a derived step's failure to the nearest authored step upstream) with its findings, and every document written after
that step is dropped, since it was sealed to a packet that may change. Each step has its first attempt and two more
(replan_trigger.MAX_ATTEMPTS); a third refusal stops the run with AuthorFailed, naming the step and its findings.
Every call is logged: the step, the backend and model, the attempt, its size, tokens and cost, its time and whether
the checks passed it.

A backend has `name` and `write(node, step_id, packet, findings) -> (document, usage)`; `usage` holds model,
tokens_in, tokens_out and cost_usd. `Replay` is the offline backend: an example's committed plans, which proves the
loop without a model (AA-1). Live backends are AA-2 and AA-5.
"""

import json
import re
import time
from pathlib import Path

from compiler import pipeline, replan_trigger
from compiler.authoring import AuthorRequired, GateFailed, StepFailed
from kernel.canonical import ContractError, canonical_json
from planner.dependency_graph import node_index
from planner.intent_parser import parse_intent


class AuthorFailed(ContractError):
    """A step was refused on every attempt; `node`, `findings` and `calls` say where and why."""

    def __init__(self, node, findings, calls):
        super().__init__("AUTHOR_FAILED", f"{node} was refused on all {replan_trigger.MAX_ATTEMPTS} attempts", findings)
        self.node, self.findings, self.calls = node, findings, calls


class Replay:
    """The offline backend (AA-1): an example's committed plans, written back as they are."""

    name = "replay"

    def __init__(self, folder):
        self.plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(folder).glob("*.json"))}

    def write(self, node, step_id, packet, findings=None):
        return dict(self.plans[node]), {"model": "replay", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0}


class BackendError(ContractError):
    """The backend could not return a document (the model or its CLI failed, not the checks)."""

    def __init__(self, node, detail):
        super().__init__("BACKEND_FAILED", f"the backend wrote no document for {node}", detail)


ROOT = Path(__file__).resolve().parents[1]
GUIDES = {"anime": "reference_fight", "live_action": "live_action_standoff", "ugc_ad": "ugc_glasses_demo"}  # AA-8
FRONTIER = ("temporal",)  # the frontier model's first attempts (PLAN-008, AA-8)
RETRY_FRONTIER = ("temporal", "motion", "effort", "camera")  # its retries
PIECE = 5  # AA-9: about the most slots one S13 piece writes (a beat's slots stay together)
ROUTES = {"HIT_HOLD": "camera"}  # a refusal some later step finds, fixed where its content is written (AA-8)
FILLED = ("step_id", "band", "packet_sha256", "author", "attempt")  # the author sets these; the model never copies them
ENV = ("HOME", "PATH", "USER", "LOGNAME", "SHELL", "TMPDIR", "LANG")


def _schema(node):
    """The step's document schema without the fields the author fills."""
    schema = json.loads(pipeline.AUTHORED[node].PLAN_SCHEMA.read_text(encoding="utf-8"))
    schema["required"] = [f for f in schema.get("required", []) if f not in FILLED]
    schema["properties"] = {k: v for k, v in schema.get("properties", {}).items() if k not in FILLED}
    for key in ("$schema", "$id"):
        schema.pop(key, None)
    return schema


class ClaudeCLI:
    """The subscription backend (AA-2, owner's choice 2026-10-12): one `claude -p` call per step on the owner's Claude
    login, no per-call bill. Isolated: an empty working folder, an allowlisted environment, no tools, no settings,
    hooks, skills, MCP or memory (--safe-mode, --setting-sources project, --strict-mcp-config), no session kept. The
    model reads the step's packet (its instructions are the brief), the step's schema, and one document of the same
    step that passed in an example of the scene's genre (its shape, not its content); a retry adds the refused
    document and the findings. The frontier model writes the creative steps, a faster one the rest."""

    name = "claude-cli"

    def __init__(self, genre, frontier="claude-opus-5-5", other="claude-sonnet-5-5", timeout_s=1800, split=True):
        self.genre, self.frontier, self.other, self.timeout_s, self.split = genre, frontier, other, timeout_s, split
        self.previous = {}

    def _guide(self, node):
        path = ROOT / "examples" / GUIDES.get(self.genre, "wizard_vs_acrobat") / "plans" / f"{node}.json"
        if not path.exists():
            path = next((ROOT / "examples").glob(f"*/plans/{node}.json"), None)
        if path is None:
            return None
        return {k: v for k, v in json.loads(path.read_text(encoding="utf-8")).items() if k not in FILLED}

    def write(self, node, step_id, packet, findings=None):
        whole = any(f.get("code", "").startswith(("ROTATION", "TURN")) for f in findings or [])  # a turn spans pieces
        if node == "motion" and self.split and not whole:
            document, usage = self._split_motion(step_id, packet, findings)
        else:
            document, usage = self._call(node, step_id, packet, findings, self.previous.get(node, {}))
        self.previous[node] = document
        return ({**document, "step_id": packet.get("step_id", step_id), "band": packet.get("band"),
                 "author": {"host": "cinematic author (claude -p, subscription)", "model": usage["model"]}}, usage)

    def _split_motion(self, step_id, packet, findings):
        """AA-9: S13 in parallel pieces, each one time window holding every fighter's keys in it (a beat never split,
        about PIECE slots a piece), merged into one document. Fighters stay in one piece so a strike and its target are
        posed together: split by fighter, the pieces met 18 refusals where one call met 6 (S-112). On a retry only the
        pieces that hold a refused slot are written again, with their findings and their own previous keys."""
        from concurrent.futures import ThreadPoolExecutor

        beats = {}
        for slot in sorted(packet["slots"], key=lambda s: (s["t"], s["slot"])):
            beats.setdefault(slot["t"], []).append(slot)
        pieces, piece = [], []
        for group in beats.values():
            if piece and len(piece) + len(group) > PIECE:
                pieces.append(piece)
                piece = []
            piece = piece + group
        if piece:
            pieces.append(piece)
        bounds = [p[0]["t"] for p in pieces] + [float("inf")]
        previous = self.previous.get("motion") or {}

        def span(index):
            return bounds[index], bounds[index + 1]

        def holds(index, finding):
            low, high = span(index)
            slot = finding.get("slot") or ""
            if slot in {s["slot"] for s in pieces[index]}:
                return True
            tail = slot.partition("@")[2]
            return bool(tail) and not tail.startswith("b") and low <= float(tail) < high

        redo = [i for i in range(len(pieces)) if not findings or not previous or any(holds(i, f) for f in findings)]
        redo = redo or list(range(len(pieces)))

        def write(index):
            low, high = span(index)
            slots = {s["slot"] for s in pieces[index]}
            mine = [f for f in findings or [] if holds(index, f)] or findings
            own = {"keys": [k for k in previous.get("keys", []) if k["slot"] in slots],
                   "inbetweens": [b for b in previous.get("inbetweens", []) if low < b["t"] < high]}
            note = (f"WRITE ONLY THE KEYS OF THESE SLOTS: {', '.join(sorted(slots))} (every fighter, {low:g} s to "
                    f"{'the end' if high == float('inf') else f'{high:g} s'}). Other authors write the other times at "
                    "the same time from the same packet: keep every key on its packet anchor and facing, and add "
                    "in-betweens only inside that time.")
            return self._call("motion", step_id, packet, mine, own if findings else {}, note)

        with ThreadPoolExecutor(max_workers=len(redo)) as pool:
            written = dict(zip(redo, pool.map(write, redo), strict=True))
        keys, inbetweens, usage = [], {}, {"model": None, "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0,
                                           "list_cost_usd": 0.0, "billing": "subscription", "pieces": len(redo)}
        for index, piece in enumerate(pieces):
            low, high = span(index)
            slots = {s["slot"] for s in piece}
            document, used = written.get(index, (previous, None))
            keys += [k for k in document.get("keys", []) if k["slot"] in slots]
            for b in document.get("inbetweens", []):
                if low < b["t"] < high:
                    inbetweens[(b["entity"], round(b["t"], 4))] = b  # one per entity and instant
            if used:
                usage["model"] = used["model"]
                for field in ("tokens_in", "tokens_out", "list_cost_usd"):
                    usage[field] = round(usage[field] + used[field], 4)
        return {"keys": keys, "inbetweens": sorted(inbetweens.values(), key=lambda b: (b["t"], b["entity"]))}, usage

    def _call(self, node, step_id, packet, findings, previous, note=None):
        """One `claude -p` call: (the model's document, usage)."""
        model = self.frontier if node in FRONTIER or (findings and node in RETRY_FRONTIER) else self.other
        parts = [f"STEP {step_id} ({node}). THE PACKET (its `instructions` are your brief; follow them exactly):",
                 canonical_json(packet)]
        guide = self._guide(node)
        if guide is not None:
            parts += ["A DOCUMENT FOR THIS STEP THAT PASSED IN ANOTHER SCENE (its shape and level of detail, not its "
                      "content; write yours for this packet's slots):", canonical_json(guide)]
        if note:
            parts.append(note)
        if findings:
            parts += ["YOUR PREVIOUS DOCUMENT:", canonical_json(previous),
                      "THE STEP'S CHECKS REFUSED IT FOR THESE FINDINGS. Fix every one and return the whole document:",
                      canonical_json(findings)]
        system = ("You author one step of a cinematic compiler. Write the step's document for the packet you are given, "
                  "exactly as its instructions say, as JSON matching the schema. Where the packet lists the allowed "
                  "values (its vocabulary, slots, ids, modes and their allowed combinations), use only those, copied "
                  "exactly, and check every combination against the packet before you answer. Return only the "
                  "document.")
        return self._run(node, parts, _schema(node), system, model)

    def _run(self, label, parts, schema, system, model):
        """One isolated `claude -p` call: (the structured reply, usage), or BackendError."""
        import os
        import subprocess
        import tempfile

        env = {k: os.environ[k] for k in ENV if k in os.environ}
        argv = ["claude", "-p", "--output-format", "json", "--json-schema", json.dumps(schema),
                "--system-prompt", system, "--tools", "", "--safe-mode", "--setting-sources", "project",
                "--strict-mcp-config", "--no-session-persistence", "--model", model]
        detail = None
        for _ in range(2):  # one more try when the CLI itself fails
            with tempfile.TemporaryDirectory() as folder:
                try:
                    done = subprocess.run(argv, input="\n\n".join(parts), capture_output=True, text=True, cwd=folder,
                                          env=env, timeout=self.timeout_s)
                except subprocess.TimeoutExpired:
                    detail = f"timed out after {self.timeout_s} s"
                    continue
            try:
                reply = json.loads(done.stdout)
            except json.JSONDecodeError:
                detail = (done.stderr or done.stdout)[-500:]
                continue
            document = reply.get("structured_output")
            if reply.get("is_error") or not isinstance(document, dict):
                detail = str(reply.get("result"))[-500:]
                continue
            usage = reply.get("usage", {})
            return document, {"model": model, "tokens_out": usage.get("output_tokens", 0),
                              "tokens_in": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
                              + usage.get("cache_read_input_tokens", 0), "cost_usd": 0.0,
                              "list_cost_usd": round(reply.get("total_cost_usd") or 0.0, 4), "billing": "subscription"}
        raise BackendError(label, detail)

    def cast(self, idea, index, schemas, findings=None):
        """AA-6: the idea rewritten in the forms S01 reads (a cast line per performer, `holding a <prop>`, `on a
        <setting>`), every detail kept, and a draft card for each performer, prop or place the library lacks."""
        parts = ["THE IDEA:", idea,
                 "THE LIBRARY'S CARDS (reuse one when it fits; its names are what the query must say):", canonical_json(index),
                 "THE CARD SCHEMAS (one per kind; a new card must match its kind's schema):", canonical_json(schemas),
                 "THE QUERY FORM THE PARSER READS, EXACTLY: '<n> seconds <genre>. A: <performer card name>, <looks and "
                 "actions>. B: <performer card name>, <looks and actions>. On a <place card name>, holding a <prop card "
                 "name>.' Each cast line starts right after a full stop and a space ('. A: '), never after a colon. The "
                 "place must be a world card's name (write a world card, with a floor surface at y=0 and any obstacles, "
                 "when no library world fits); each performer and prop must be a card's name. Example: '6 seconds "
                 "anime. A: kunoichi, slim woman in a dark blue outfit, sprints and vaults the chimney, landing crouched "
                 "as she draws her kunai. On a moonlit rooftop, holding a kunai.' Name the place once, only in that "
                 "last sentence: the parser refuses a place it reads twice (no 'across the rooftop' in the actions)."]
        if findings:
            parts += ["YOUR PREVIOUS ANSWER WAS REFUSED:", canonical_json(findings)]
        schema = {"type": "object", "additionalProperties": False, "required": ["query", "cards"],
                  "properties": {"query": {"type": "string", "minLength": 10},
                                 "cards": {"type": "array", "items": {"type": "object"}}}}
        system = ("You cast a scene for a cinematic compiler. Rewrite the idea as one query in the parser's forms, "
                  "keeping every detail of the idea (looks, actions, timing, mood) in its words, and write a new draft "
                  "card only for a performer, prop or place no library card covers. Return only the JSON.")
        return self._run("cast", parts, schema, system, self.other)



REPAIRABLE = ("CONTACT_WORLD", "BODY_OVERLAP", "FLOOR_PENETRATION")  # in the order they are repaired
ARMS_SPINE = ["LA.x", "LA.y", "LA.z", "LFA.x", "RA.x", "RA.y", "RA.z", "RFA.x", "Sp.x", "Sp.z"]
LEGS = ["LUL.x", "LUL.y", "LUL.z", "RUL.x", "RUL.y", "RUL.z", "LL.x", "RL.x"]
BETWEEN = re.compile(r"at (\d+(?:\.\d+)?) between keys")


def repair_motion(document, findings, envelope, rounds=None):
    """AA-4 (PLAN-008): S13's overlap and floor refusals repaired by the re-block solver before the model retries,
    one finding at a time, S13 re-checking after each (`rounds` at most). A refusal at a key re-blocks the key: its arms
    and spine free inside the joint limits, its root on its S04 anchor, its soles and every part it touches something
    with at that instant held. A refusal between keys places an in-between key at that frame (ADR-O109): its arms,
    spine, legs and root free, its soles held where the declared interpolation puts them when both its keys stand on
    them. Each is kept clear of every other body between its keys and, for a floor refusal, over the floor. Findings of
    another kind are left for the model, which then reads the repaired document. A missed contact at a key re-blocks
    that key the same way, its touching part placed on the target's surface (a body's: touching, its radius off the
    surface, not inside; a surface's top; a prop's point). Returns the repaired document, or None when no finding is of
    these kinds."""
    import copy

    from compiler.passes.derived import p13_motion
    from solver import contact_world, floor_penetration, forward_kinematics, reblock

    if not any(f.get("code") in REPAIRABLE for f in findings or []):
        return None
    packet = p13_motion.prepare(envelope)
    plan, genre = copy.deepcopy(document), envelope["scene"]["genre"]
    metres = forward_kinematics.segments(genre)
    entities = sorted({k["slot"].split("@")[0] for k in plan["keys"]})
    floor = floor_penetration.floor_level(envelope["nodes"]["surfaces"]["items"], envelope["scene"]["ax"].get("ground"))
    claims = {k["id"]: set(k["support"]) for k in envelope["nodes"]["kinematic"]["items"]}
    contacts = {c["id"]: c for c in envelope["nodes"]["contacts"]["items"]}
    radii = forward_kinematics.radii(genre)
    slots = {s["slot"]: s for s in packet["slots"]}

    def touch_goals(entity, t, key):
        """(goals, parts) placing each part the entity touches something with at instant t on its target."""
        rows = {r["id"]: r for r in contact_world.measure_plan({k["slot"]: k for k in plan["keys"]}, slots, packet,
                                                               plan.get("inbetweens", []))}
        goals, parts = [], set()
        for c in contacts.values():
            row = rows.get(c["id"])
            if c["a"]["id"] != entity or abs(c["t"] - t) > 1e-6 or not row or not row["measurable"]:
                continue
            name = c["body_part"] if c["body_part"] in forward_kinematics.POINTS else None
            point = forward_kinematics.points(key, metres).get(name) if name else None
            if point is None:
                continue
            target = row["target_point"]
            if c["b"]["kind"] == "entity":  # touching the body's surface, not inside it
                away = [a - b for a, b in zip(point, target, strict=True)]
                length = sum(v * v for v in away) ** 0.5
                if length < 1e-9:
                    continue
                reach = forward_kinematics.part_radius(c["body_part"], radii) + 0.005
                target = [b + v / length * reach for b, v in zip(target, away, strict=True)]
            goals.append((name, list(target)))
            parts.add(name)
        return goals, parts

    skipped = set()
    rounds = rounds or min(40, 2 * len(findings) + 4)  # enough for every finding, its repair re-checked
    for _ in range(rounds):
        mine = sorted((f for f in findings if f.get("code") in REPAIRABLE and canonical_json(f) not in skipped),
                      key=lambda f: REPAIRABLE.index(f["code"]))
        if not mine:
            break
        finding = mine[0]
        if finding["code"] == "CONTACT_WORLD":  # the actor's key at the contact's instant
            contact = contacts.get(finding.get("contact"))
            slot = f"{contact['a']['id']}@{contact['beat']}" if contact else None
            if not contact or not any(k["slot"] == slot for k in plan["keys"]):
                skipped.add(canonical_json(finding))  # between keys or unknown: the model's
                continue
            finding = {**finding, "slot": slot, "message": ""}
        entity = finding["slot"].split("@")[0]
        between = BETWEEN.search(finding.get("message", ""))
        others = [e for e in entities if e != entity]
        sinks = finding["code"] == "FLOOR_PENETRATION"
        if between:  # an in-between key at the frame the refusal names
            t, fps = float(between.group(1)), envelope["scene"]["fps"]
            own = reblock._scene_keys(plan, envelope)[entity]
            taken = {round(k["t"] * fps) for k in own}
            frame, lo, hi = round(t * fps), max(k["t"] for k in own if k["t"] < t), min(k["t"] for k in own if k["t"] > t)
            step = 1 if t - lo < hi - t else -1  # a frame a key holds: one toward the span's middle
            while frame in taken and lo < (frame + step) / fps < hi:
                frame += step
            if frame in taken:
                break
            t = round(frame / fps, 6)
            slot = f"{entity}@{t:g}"
            plan = reblock._start_inbetween(plan, envelope, slot)
            own = reblock._scene_keys(plan, envelope)[entity]
            key = copy.deepcopy(next(k for k in own if k["slot"] == slot))
            before = max((k for k in own if k["t"] < t and "@b" in k["slot"]), key=lambda k: k["t"], default=None)
            after = min((k for k in own if k["t"] > t and "@b" in k["slot"]), key=lambda k: k["t"], default=None)
            stood = claims.get(before["slot"], set()) & claims.get(after["slot"], set()) if before and after else set()
            points = forward_kinematics.points(key, metres)
            goals = [(part, [points[part][0], 0.0, points[part][2]]) for part in sorted(stood) if part in points]
            free = ARMS_SPINE + LEGS + ["pos.x", "pos.y", "pos.z"]
        else:  # the key itself, its root on its anchor
            slot = finding["slot"]
            key = copy.deepcopy(next(k for own in reblock._scene_keys(plan, envelope).values() for k in own
                                     if k["slot"] == slot))
            points = forward_kinematics.points(key, metres)
            goals, parts = touch_goals(entity, key["t"], key)
            goals += [(sole, points[sole]) for sole in ("left_foot", "right_foot") if sole not in parts]
            legs = any(p.endswith(("_foot", "_leg")) for p in parts)
            free = ARMS_SPINE + (LEGS if legs else [])
        extra = reblock.clearance(plan, envelope, slot, others, floor=floor if sinks else None)
        solved, _ = reblock.solve_key(key, metres, goals, free, {}, (), reblock.limits(genre), extra)
        for item in plan["keys"]:
            if item["slot"] == slot:
                item["bones"] = solved["bones"]
        for item in plan.get("inbetweens", []):
            if f"{item['entity']}@{item['t']:g}" == slot:
                item.update(pos=solved["pos"], rot=solved["rot"], bones=solved["bones"],
                            name=f"clear_of_{others[0]}" if others else "clear",
                            description=f"{entity} kept clear of {' and '.join(others)} between keys (placed by the solver).")
        findings = p13_motion.check(plan, packet)
    return plan


def casting(idea, backend, *, genre=None, attempts=3, progress=None):
    """AA-6: (query, cards, new_cards) for any idea. When S01 and S02 already cast the idea from the library (a performer
    and a place), it stands as written. Otherwise the backend rewrites it in the parser's forms and drafts a card for
    each performer, prop or place the library lacks; a new card is checked against its kind's schema, marked a draft
    for the owner (R-30), and the cast is refused until S02 finds a performer and a place."""
    import copy
    import datetime

    from planner.card_loader import FOLDERS, load_cards
    from planner.query_expander import expand
    from validators.schema_validator import validate_schema

    library = load_cards()

    def cast_of(query, cards):
        intent = {"raw_query": query, **parse_intent(query)}
        if genre:
            intent["parsed"]["genre"] = genre
        result = expand(intent, cards)
        return result["entities"], result["surfaces"]

    try:
        entities, surfaces = cast_of(idea, library)
    except ContractError:
        entities, surfaces = [], []
    if entities and surfaces:
        return idea, library, []
    schemas = {kind: json.loads((ROOT / "schemas" / "cards" / f"{kind}_card.schema.json").read_text(encoding="utf-8"))
               for kind in FOLDERS}
    index = [{"card_id": c["card_id"], "kind": c["kind"], "names": c["names"], "description": c.get("description")}
             for c in library.values()]
    from kernel import kernel_files

    conventions = kernel_files.load("conventions")
    axes = {"up": conventions["up"], "forward": conventions["forward"], "ground": conventions["ground"], "unit": "m"}
    findings, kept = None, {}
    for _ in range(attempts):
        started = time.perf_counter()
        answer, usage = backend.cast(idea, index, schemas, findings)
        if progress:
            progress(f"cast written by {usage['model']} in {time.perf_counter() - started:.0f} s")
        cards, findings = copy.deepcopy(library), []
        cards.update(kept)  # cards an earlier attempt wrote that passed their schema
        for card in answer.get("cards", []):
            if card.get("kind") == "world":  # the kernel's axes; match terms only (S02 reads required_terms against
                card = {k: v for k, v in card.items() if k != "required_terms"} | {"ax": dict(axes)}  # raw query words)
            card = {**card, "status": "draft", "card_version": 1,
                    "provenance": {"authored_by": "cinematic author (claude -p)",
                                   "date": datetime.date.today().isoformat(),
                                   "basis": "Drafted for this idea by the automatic author (AA-6); needs owner review."}}
            try:
                if card.get("kind") not in schemas or card.get("card_id") in library:
                    raise ContractError("CARD", "unknown kind or a card_id the library already uses", card.get("card_id"))
                validate_schema(card, schemas[card["kind"]])
            except ContractError as refused:
                findings.append({"code": "CARD", "card": card.get("card_id"), "message": str(refused)})
                continue
            cards[card["card_id"]] = kept[card["card_id"]] = card
        if not findings:
            try:
                entities, surfaces = cast_of(answer["query"], cards)
            except ContractError as refused:
                entities, surfaces = [], []
                findings.append({"code": "CAST", "message": str(refused)})
            if entities and surfaces:
                return answer["query"], cards, list(kept.values())
            read = parse_intent(answer["query"])
            parsed, unsure = read["parsed"], [a for a in read.get("ambiguous", []) if a["field"] == "setting"]
            findings.append({"code": "CAST", "message": f"S02 cast {len(entities)} performer(s) and "
                             f"{len(surfaces)} surface(s) from {answer['query']!r}: it needs a performer and a place. The "
                             f"parser read performers {parsed.get('entities_hinted')}, props {parsed.get('props_hinted')} "
                             f"and the place {parsed.get('setting')!r}; a performer needs a cast line after '. ' naming a "
                             "card, the place a world card whose name it is"
                             + (f"; the parser read the place twice ({', '.join(repr(c['text']) for c in seen)}) "
                                "and so took neither: name it once" if (seen := unsure[0]["candidates"] if unsure else [])
                                else "")})
        if progress:
            progress("cast refused: " + "; ".join(f["message"][:120] for f in findings))
    raise AuthorFailed("cast", findings, [])


FAR_M = 0.3  # a contact still this far off after the solver's repair goes back to S04's anchors (AA-10)
MISS = re.compile(r"by (\d+(?:\.\d+)?) m")


REACH_M = 1.5  # two bodies' anchors farther apart than this, on the ground plane, cannot meet by a limb


def _out_of_reach(envelope, findings):
    """Whether every missed contact in `findings` joins two bodies whose S04 anchors are over REACH_M apart at its
    instant (the target at its nearest slot in time): S13 cannot close that with a key's root fixed on its anchor."""
    from planner.scene_view import slots

    contacts = {c["id"]: c for c in envelope["nodes"]["contacts"]["items"]}
    by_entity = {}
    for slot in slots(envelope):
        by_entity.setdefault(slot["entity"], []).append(slot)
    for finding in findings:
        contact = contacts.get(finding.get("contact"))
        if not contact or contact["b"]["kind"] != "entity":
            return False
        mine, theirs = by_entity.get(contact["a"]["id"]), by_entity.get(contact["b"]["id"])
        if not mine or not theirs:
            return False
        a = min(mine, key=lambda s: abs(s["t"] - contact["t"]))["pos"]
        b = min(theirs, key=lambda s: abs(s["t"] - contact["t"]))["pos"]
        if ((a[0] - b[0]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5 <= REACH_M:
            return False
    return True


def _miss(finding):
    found = MISS.search(finding.get("message", ""))
    return float(found.group(1)) if found else 0.0


def _keep(cache, plans):
    """AA-7: each document under its packet's hash (the steps before a refusal passed; at the end, all of them)."""
    if cache is None:
        return
    cache.mkdir(parents=True, exist_ok=True)
    for document in plans.values():
        (cache / f"{document['packet_sha256'].split(':')[1]}.json").write_text(canonical_json(document), encoding="utf-8")


def _sequence(query, genre):
    return pipeline.sequence_for(pipeline.load(), genre or parse_intent(query)["parsed"]["genre"])


def author(query, backend, *, genre=None, duration_s=None, until="render", load_bearing=False, progress=None,
           cache=None, cards=None):
    """(envelope, calls): the compiled envelope with every authored step written by `backend`, and the call log;
    `progress(line)`, when given, hears each call as it returns and each refusal. `cache` (a folder, AA-7) keeps each
    accepted document under its packet's hash, so a re-run writes only the steps whose packets changed."""
    cache = Path(cache) if cache else None
    order = pipeline.load()
    index = node_index(order)
    node_of = {spec["step_id"]: node for node, spec in index.items()}
    sequence = _sequence(query, genre)
    resolved = genre or parse_intent(query)["parsed"]["genre"]
    plans, attempts, calls, last, repairs = {}, {}, [], None, {}

    def run(target):
        return pipeline.run(query, genre=genre, duration_s=duration_s, until=target, plans=plans,
                            load_bearing=load_bearing, cards=cards)

    def refuse(node, findings):
        if progress:
            progress(f"{index[node]['step_id']} {node} refused: " + ", ".join(sorted({f.get('code', '?') for f in findings})))
        for call in calls:  # the model's call and any solver repair of the same attempt
            if call["node"] == node and call["attempt"] == attempts.get(node) and "result" not in call:
                call.update(result="refused", findings=[f.get("code", "?") for f in findings])
        if attempts.get(node, 0) >= replan_trigger.MAX_ATTEMPTS:
            raise AuthorFailed(node, findings, calls)

    while True:
        try:
            envelope = run(until)
        except AuthorRequired as needed:
            node, packet, findings = node_of[needed.step_id], needed.packet, None
        except StepFailed as failed:  # an authored step's gate (GateFailed) or a derived step's check
            node = replan_trigger.owning_step(node_of[failed.step_id], resolved)
            findings = failed.findings
            far = [f for f in findings if f.get("code") == "CONTACT_WORLD" and _miss(f) > FAR_M]
            if (node == "motion" and far and repairs.get(attempts.get(node)) is not None
                    and attempts.get("temporal", 0) < replan_trigger.MAX_ATTEMPTS
                    and _out_of_reach(run(sequence[sequence.index("motion") - 1]), far)):
                node = "temporal"  # the solver could not reach: S04 placed the bodies out of reach (AA-10)
                findings = [{**f, "message": f["message"] + "; the beat's anchors put the two bodies out of reach: "
                             "place them so this contact can land"} for f in far]
            routed = {ROUTES.get(f.get("code")) for f in findings}
            if len(routed) == 1 and None not in routed and next(iter(routed)) in plans:
                node = next(iter(routed))  # AA-8: e.g. HIT_HOLD at S18 is the camera's to fix
            if node == "motion" and repairs.get(attempts.get(node)) is None:  # AA-4: the solver first
                started = time.perf_counter()
                repaired = repair_motion(plans[node], findings, run(sequence[sequence.index(node) - 1]))
                repairs[attempts.get(node)] = repaired or {}
                if repaired is not None:
                    plans[node] = repaired
                    calls.append({"step_id": index[node]["step_id"], "node": node, "attempt": attempts[node],
                                  "backend": "reblock-solver", "model": "solver", "tokens_in": 0, "tokens_out": 0,
                                  "cost_usd": 0.0, "input_chars": 0, "output_chars": 0,
                                  "duration_s": round(time.perf_counter() - started, 3)})
                    if progress:
                        progress(f"{index[node]['step_id']} {node} refused for {len(findings)} overlap or floor "
                                 f"finding(s); the solver re-blocked them in {calls[-1]['duration_s']:.0f} s")
                    if hasattr(backend, "previous"):
                        backend.previous[node] = {k: v for k, v in repaired.items() if k not in FILLED}
                    continue
            refuse(node, findings)
            own = isinstance(failed, GateFailed) and node_of[failed.step_id] == node
            packet = failed.packet if own else pipeline.AUTHORED[node].prepare(run(sequence[sequence.index(node) - 1]))
        except ContractError as error:  # a document the schema or the packet binding refuses: the step just written
            if last is None:
                raise
            node, findings = last, [{"code": error.code, "message": str(error)}]
            refuse(node, findings)
            packet = pipeline.AUTHORED[node].prepare(run(sequence[sequence.index(node) - 1]))
        else:
            for call in calls:
                call.setdefault("result", "passed")
            _keep(cache, plans)
            return envelope, calls
        for later in sequence[sequence.index(node) + 1:]:
            if plans.pop(later, None) is not None:  # written for a packet this step may change
                next(c for c in reversed(calls) if c["node"] == later).setdefault("result", "dropped")
                attempts.pop(later, None)  # a new packet: its attempts start again
                if later == "motion":
                    repairs.clear()
        attempts[node] = attempts.get(node, 0) + 1
        started = time.perf_counter()
        kept = cache / f"{packet['packet_sha256'].split(':')[1]}.json" if cache and not findings else None
        if kept is not None and kept.exists():  # AA-7: this packet's document was accepted before
            document = json.loads(kept.read_text(encoding="utf-8"))
            usage = {"model": "cache", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0}
        else:
            _keep(cache, {n: d for n, d in plans.items() if sequence.index(n) < sequence.index(node)})
            document, usage = backend.write(node, index[node]["step_id"], packet, findings)
        plans[node] = {**document, "packet_sha256": packet["packet_sha256"], "attempt": attempts[node]}
        last = node
        calls.append({"step_id": index[node]["step_id"], "node": node, "attempt": attempts[node],
                      "backend": backend.name, **usage, "input_chars": len(canonical_json(packet)),
                      "output_chars": len(canonical_json(plans[node])),
                      "duration_s": round(time.perf_counter() - started, 3)})
        if progress:
            progress(f"{index[node]['step_id']} {node} attempt {attempts[node]} written by {usage.get('model')} in "
                     f"{calls[-1]['duration_s']:.0f} s")
