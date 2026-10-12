"""S11 pass (band L4a, authored): visible bodily organization per entity per beat.

Checks: one node per slot; cue values from library/kinematic_cues.yaml; support parts are the entity's own;
support agrees with S07 (when supports are active they must match exactly) or else with S06 (airborne means no
support, grounded/braced/lying means some support; a support change in progress allows either side); AIRBORNE_PICKUP
(owner O18, M9-03): a prop resting on a surface is taken only by a supported body within reach (S11 is the first step
that knows every genre's support).
"""

import math

from compiler.authoring import run_authored, seal
from planner import library_vocab
from planner.dependency_graph import ROOT, load
from planner.dynamic_beat_validator import GRAVITY, REACH_M
from planner.scene_view import slots, values_in_progress

NODE, STEP = "kinematic", "S11"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "kinematic_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "kinematic_organization.txt"
ARC_TOLERANCE_M = 0.3  # interpretation (Claude's, for owner review): a root this far off the gravity arc hangs
CUES = ("balance", "loading", "bracing", "yielding", "weight_transfer", "tension", "release", "strain", "restraint", "breathing")


def prepare(envelope):
    vocabulary = library_vocab.load("kinematic_cues")
    parts = {e["id"]: e["parts"] for e in envelope["nodes"]["entities"]["items"]}
    view = [{**s, "allowed_support_states": values_in_progress(envelope, s, "support")} for s in slots(envelope)]
    return seal({"step_id": STEP, "band": "L4a", "kind": "kinematic_plan",
                 "schema": "urn:cinematic-compiler:schema:kinematic_plan:1.1",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "genre": envelope["scene"]["genre"],
                 "slots": view, "parts": parts, "vocabulary": vocabulary["fields"]})


def check(document, packet):
    findings, seen = [], {}
    slots_by_id = {s["slot"]: s for s in packet["slots"]}
    vocabulary = {"fields": packet["vocabulary"]}
    for node in document["nodes"]:
        seen[node["slot"]] = seen.get(node["slot"], 0) + 1
        slot = slots_by_id.get(node["slot"])
        if slot is None:
            findings.append({"code": "KINEMATIC_SLOT", "message": "Node names no packet slot", "slot": node["slot"]})
            continue
        parts = packet["parts"][slot["entity"]]
        for field in ("support", *CUES):
            for problem in library_vocab.problems(vocabulary, field, node[field], parts):
                findings.append({"code": "KINEMATIC_VOCABULARY", "message": problem, "slot": node["slot"]})
        support, active, allowed = set(node["support"]), set(slot["active_supports"]), set(slot["allowed_support_states"])
        if active and support != active:
            findings.append({"code": "KINEMATIC_SUPPORT", "message": "Support must match the active support contacts",
                             "slot": node["slot"]})
        elif not active and "unknown" not in allowed:
            if allowed == {"airborne"} and support:
                findings.append({"code": "KINEMATIC_SUPPORT", "message": "An airborne body has no support", "slot": node["slot"]})
            if "airborne" not in allowed and not support:
                findings.append({"code": "KINEMATIC_SUPPORT", "message": "A supported body needs support parts",
                                 "slot": node["slot"]})
    for slot_id in slots_by_id:
        if seen.get(slot_id, 0) != 1:
            findings.append({"code": "KINEMATIC_SLOT", "message": "Every slot needs exactly one node", "slot": slot_id})
    return findings + momentum_findings(document, packet)


def float_spans(nodes, slots):
    """[(entity, takeoff slot, airborne slots, landing slot)] for each run of airborne keys (no support) between a
    supported key before it and one after it; `nodes` and `slots` keyed by slot id."""
    own, spans = {}, []
    for slot in sorted(slots.values(), key=lambda s: s["t"]):
        own.setdefault(slot["entity"], []).append(slot)
    for entity, seq in own.items():
        i = 0
        while i < len(seq):
            if nodes[seq[i]["slot"]]["support"]:
                i += 1
                continue
            j = i
            while j < len(seq) and not nodes[seq[j]["slot"]]["support"]:
                j += 1
            if i > 0 and j < len(seq):
                spans.append((entity, seq[i - 1], seq[i:j], seq[j]))
            i = j
    return spans


def momentum_findings(document, packet):
    """MOMENTUM_MISSING (plan F9.2, owner O74): an airborne span keeps each root within 0.3 m of the gravity arc
    through its takeoff and landing roots, unless (anime only) a key of the span floats: stylised hang time. A float
    outside anime or on a supported key is refused. Interpretation (Claude's, for owner review): the arc and the
    0.3 m; a span with no takeoff or no landing key (a fall into the clip, a clip ending in the air) is not judged."""
    nodes = {n["slot"]: n for n in document["nodes"]}
    slots = {s["slot"]: s for s in packet["slots"] if s["slot"] in nodes}
    findings = [{"code": "MOMENTUM_MISSING", "message": "Only an airborne key in anime may float (O74)", "slot": n["slot"]}
                for n in document["nodes"] if n.get("float") and (packet["genre"] != "anime" or n["support"])]
    for entity, takeoff, airborne, landing in float_spans(nodes, slots):
        if any(nodes[s["slot"]].get("float") for s in airborne):
            continue
        t0, y0, span = takeoff["t"], takeoff["pos"][1], landing["t"] - takeoff["t"]
        launch = (landing["pos"][1] - y0 + 0.5 * GRAVITY * span * span) / span
        for slot in airborne:
            dt = slot["t"] - t0
            arc = y0 + launch * dt - 0.5 * GRAVITY * dt * dt
            if abs(slot["pos"][1] - arc) > ARC_TOLERANCE_M:
                findings.append({"code": "MOMENTUM_MISSING", "message": f"{entity} at {slot['t']} is at y={slot['pos'][1]:g}, "
                                 f"{abs(slot['pos'][1] - arc):.2f} m off the gravity arc from {t0} to {landing['t']} "
                                 "(re-time it, or in anime declare the span's hang time)", "slot": slot["slot"]})
    return findings


def resting_pickups(envelope):
    """The possess contacts that take a prop resting on a surface (S06 at that beat: holder none, a known location)."""
    resting = {(s["subject"]["id"], s["beat"]) for s in envelope["nodes"]["states"]["items"] if s["subject"]["kind"] == "prop"
               and s["conditions"].get("holder") == "none" and s["conditions"].get("location") not in (None, "unknown")}
    return [c for c in envelope["nodes"]["contacts"]["items"] if c["contact_type"] == "possess" and c["b"]["kind"] == "prop"
            and (c["b"]["id"], c["beat"]) in resting]


def pickup_findings(document, packet, envelope):
    """AIRBORNE_PICKUP (owner O18, backlog M9-03; audit X2/X3, render finding F7): a possess on a prop that rests on a
    surface needs its possessor supported at that instant, and within the 2 m reach of PROP_KINEMATICS of the prop's last
    sample. Fix the S04 plan: land first, then take. Interpretations (Claude's, for owner review): a prop "rests" when
    S06 has it with holder none and a known location at the contact's beat; the possessor's support "at that instant" is
    the support of its last slot at or before the contact (this plan); the 2 m reach."""
    support = {node["slot"]: node["support"] for node in document["nodes"]}
    own = {}
    for slot in sorted(packet["slots"], key=lambda s: s["t"]):
        own.setdefault(slot["entity"], []).append(slot)
    samples = sorted((x["t"], x["prop"], x["p"]) for b in envelope["nodes"]["beats"]["items"] for x in b.get("prop_samples", []))
    findings = []
    for c in resting_pickups(envelope):
        prop, entity, t = c["b"]["id"], c["a"]["id"], c["t"]
        slot = next((s for s in reversed(own.get(entity, [])) if s["t"] <= t + 1e-9), None)
        if slot is None:
            continue
        if not support.get(slot["slot"]):
            findings.append({"code": "AIRBORNE_PICKUP", "message": f"{entity} takes the resting {prop} at {t} with no support",
                             "slot": slot["slot"]})
        rest = next((p for at, what, p in reversed(samples) if what == prop and at <= t + 1e-9), None)
        if slot.get("pos") and rest and math.dist(slot["pos"], rest) > REACH_M:
            findings.append({"code": "AIRBORNE_PICKUP", "message": f"{entity} takes {prop} at {t} from "
                             f"{math.dist(slot['pos'], rest):.2f} m away", "slot": slot["slot"]})
    return findings


def build(envelope, document, packet):
    slots_by_id = {s["slot"]: s for s in packet["slots"]}
    nodes = []
    for node in sorted(document["nodes"], key=lambda n: (slots_by_id[n["slot"]]["t"], n["slot"])):
        slot = slots_by_id[node["slot"]]
        nodes.append({"id": node["slot"], "entity": slot["entity"], "beat": slot["beat"], "t": slot["t"],
                      **{k: v for k, v in node.items() if k != "slot"}})
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            changes = [f for f in ("support", *CUES) if prior[f] != node[f]]
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"], "changes": changes})
        last[node["entity"]] = node
    return {"/nodes/kinematic": nodes, "/edges/kinematic_transition": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=lambda doc, packet: check(doc, packet) + pickup_findings(doc, packet, envelope), build=build,
                        order=order or load())
