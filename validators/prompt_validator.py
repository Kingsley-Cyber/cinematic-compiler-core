"""M8.4 final-prompt QA: the DAG's model-as-reader check (M4) on a structured-prose prompt.

`check(text, envelope, mode)` reads the prompt as a model reads it (sections, staff lines, guidance, rules) and
compares it with the envelope it was compiled from. Every finding carries a semantic code. kernel/knowledge_map.yaml
lists, per DAG row, the codes that verify it (field `codes`); tests/test_dag_conformance.py compiles every example
through every layer, requires zero findings, and proves each code fires on a prompt broken in that one way.
Codes whose atoms the repo does not have yet are listed in the map as `gaps`, never emitted here.
"""

import re

from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner.scene_view import slots
from renderers import prop_samples, prose_renderer
from renderers.anime_renderer import constraint_rows
from solver import staff_geometry
from validators import cause_reason

CODES = {
    "SECTION_MISSING": "a Master Template section is absent",
    "SECTION_ORDER": "sections are out of order, or the query is not the first line (intent first, rules and negatives last)",
    "PROSE_STALE": "the text is not the projection of the current envelope",
    "PRECEDENCE_RULE_MISSING": "the precedence rule for the mode is missing from RULES",
    "ROOT_EXACT_PRESENT": "the prose carries the root-exact rule (owner O3)",
    "PROMPT_CONTRADICTION": "two sections of the prompt disagree",
    "KEY_LINE_MISSING": "a slot has no staff line, or has more than one",
    "STAFF_FORMAT": "a staff line breaks FORMAT",
    "SUPPORT_MISMATCH": "SUPPORT disagrees with S11",
    "AIRBORNE_UNBOOKENDED": "an airborne span lacks its takeoff or its landing",
    "GESTURE_MISMATCH": "a limb, body or head word disagrees with the key pose",
    "EULER_MODE_MISMATCH": "Euler blocks sit on the wrong lines for the mode, or their numbers differ from S13",
    "SKELETON_KEY_MISSING": "a mode with joints lacks the skeleton key",
    "EFFORT_UNDECLARED": "a staff line's time has no declared Effort for its performer",
    "KINETIC_CHAIN_MISSING": "a strike line lacks its follow-through chain",
    "KEY_GAP_UNGUIDED": "a gap over 1.5 s without a line has no implied guidance",
    "IMPLIED_GUIDANCE_MISSING": "implied guidance lacks the general line, a lag line, a recovery line or an airborne line",
    "INTERPOLATION_UNDECLARED": "MOTION CONTROL does not declare the interpolation",
    "CONVENTION_MISSING": "the frame line lacks a part of the coordinate and rotation convention",
    "SPATIAL_ANCHOR_MISSING": "a surface or a performer's start is missing from SPATIAL ANCHORS",
    "PROP_TRACK_MISSING": "a prop has no state machine, or a state change is missing from it",
    "PROP_STATE_ORDER": "a prop's states are out of time order or its holders disagree with S06",
    "PROP_INVARIANT_MISSING": "a prop lacks its never-duplicated / never-two-hands / never-lost line",
    "CUSTODY_RULE_MISSING": "a prop that never changes holder lacks its CUSTODY rule",
    "PROP_FIRST_STATE": "a prop's state at the start is unknown, or SCENE or its state machine does not say it",
    "CAUSAL_LIST_MISSING": "a causal edge is absent from CAUSAL LINKS",
    "CAUSE_REASON": "a causal link's reason is not printed in CAUSAL LINKS, or does not state a cause",
    "REACTION_WITHOUT_CAUSE": "a hard effect's line comes before its cause's contact",
    "CAUSAL_RULE_MISSING": "a lasting effect has no time-bounded rule",
    "CONSERVATION_RULE_MISSING": "one of the six conservation laws is absent from RULES",
    "SPAN_RULE_MISSING": "a support held across lines on anything but the ground has no span rule",
    "EVENT_SEPARATION_MISSING": "consecutive strikes by one performer lack a separation rule",
    "RULES_MISSING": "a rule constraint (other than root exact) is absent from RULES",
    "NEGATIVES_MISSING": "a negative constraint is absent from NEGATIVES",
    "DISCONNECTED_CAMERA_MOTION": "a shot is missing, or a camera line lacks its motivation or the beats it shows",
    "ANCHOR_PHRASE_MISSING": "an entity lacks its appearance phrase in SCENE",
    "RENDER_INTENT_MISSING": "SCENE lacks the motion, animation or choreography intent",
    "END_STATE_MISSING": "a performer lacks its end state (position and support)",
    "STACKED_GRAPHS": "a section other than the Master Template's is embedded (only prop state machines and causal links)",
}
STAFF, PROPS, RULES, NEGATIVES = "[LABAN STAFF", "[PROP STATE MACHINE", "[RULES]", "[NEGATIVES]"
# The Master Template sections (header prefixes) each code reads. A prompt without one of them cannot pass the code
# (M8.10 checklist): silence is not a pass. Layout codes read the whole text (SECTION_ORDER also the query in SCENE);
# REACTION_WITHOUT_CAUSE reads the envelope's beats and contacts only.
READS = {
    "SECTION_MISSING": (), "SECTION_ORDER": ("[SCENE]",), "PROSE_STALE": (), "ROOT_EXACT_PRESENT": (), "STACKED_GRAPHS": (),
    "PRECEDENCE_RULE_MISSING": (RULES,), "PROMPT_CONTRADICTION": (STAFF, PROPS, NEGATIVES), "KEY_LINE_MISSING": (STAFF,),
    "STAFF_FORMAT": (STAFF,), "SUPPORT_MISMATCH": (STAFF,), "AIRBORNE_UNBOOKENDED": (STAFF, RULES),
    "GESTURE_MISMATCH": (STAFF,), "EULER_MODE_MISMATCH": (STAFF,), "SKELETON_KEY_MISSING": ("[MOVEMENT LANGUAGE]",),
    "EFFORT_UNDECLARED": (STAFF,), "KINETIC_CHAIN_MISSING": (STAFF,), "KEY_GAP_UNGUIDED": (STAFF, "[IMPLIED GUIDANCE]"),
    "IMPLIED_GUIDANCE_MISSING": (STAFF, "[IMPLIED GUIDANCE]"), "INTERPOLATION_UNDECLARED": ("[MOTION CONTROL]",),
    "CONVENTION_MISSING": ("[SPATIAL ANCHORS]",), "SPATIAL_ANCHOR_MISSING": ("[SPATIAL ANCHORS]",),
    "PROP_TRACK_MISSING": (PROPS,), "PROP_STATE_ORDER": (PROPS,), "PROP_INVARIANT_MISSING": (PROPS,),
    "CUSTODY_RULE_MISSING": (PROPS,), "PROP_FIRST_STATE": ("[SCENE]", PROPS),
    "CAUSAL_LIST_MISSING": ("[CAUSAL LINKS]",), "CAUSE_REASON": ("[CAUSAL LINKS]",),
    "REACTION_WITHOUT_CAUSE": (),
    "CAUSAL_RULE_MISSING": (RULES,), "CONSERVATION_RULE_MISSING": (RULES,), "SPAN_RULE_MISSING": (STAFF, RULES),
    "EVENT_SEPARATION_MISSING": (STAFF, RULES), "RULES_MISSING": (RULES,), "NEGATIVES_MISSING": (NEGATIVES,),
    "DISCONNECTED_CAMERA_MOTION": ("[CAMERA]",), "ANCHOR_PHRASE_MISSING": ("[SCENE]",),
    "RENDER_INTENT_MISSING": ("[SCENE]",), "END_STATE_MISSING": (RULES,),
}
HEADER = re.compile(r"^\[[A-Z][^\]]*\]$")
LINE = re.compile(r"^(\d+\.\d\d) ([A-Z]): SUPPORT (.*)$")
NUMBERS = re.compile(r"-?\d+(?:\.\d+)?")
GENRE_TITLES = {"anime": "[ANIME]", "ugc_ad": "[UGC]", "live_action": "[LIVE ACTION]"}
LAWS = ("Identity is immutable", "Spatial continuity", "Momentum is conserved", "Ground force needs support",
        "Contact before effect", "Rotation is continuous")
EPSILON = 1e-6


def sections(text):
    """[(header, [lines])] in order; a header is a whole line in square brackets."""
    out = []
    for line in text.splitlines():
        if HEADER.match(line):
            out.append((line, []))
        elif out:
            out[-1][1].append(line)
    return out


def _body(parts, header):
    return "\n".join(next((lines for h, lines in parts if h == header or h.startswith(header)), []))


def _numbers(text):
    return [float(n) for n in NUMBERS.findall(text)]


def _staff(parts, mode):
    title = prose_renderer.MODES[mode][0]
    rows = []
    for line in next((lines for h, lines in parts if h == f"[LABAN STAFF – {title}]"), []):
        match = LINE.match(line)
        if match:
            rows.append({"t": float(match.group(1)), "label": match.group(2), "line": line,
                         "columns": ("SUPPORT " + match.group(3)).split(" | ")})
    return rows


def _expected_headers(envelope, mode):
    return (["[SCENE]", "[MOVEMENT LANGUAGE]", f"[LABAN STAFF – {prose_renderer.MODES[mode][0]}]", "[IMPLIED GUIDANCE]",
             "[MOTION CONTROL]", "[SPATIAL ANCHORS]"]
            + [f"[PROP STATE MACHINE – {p['name']}]" for p in envelope["nodes"]["props"]["items"]]
            + ["[CAUSAL LINKS]", "[CAMERA]", GENRE_TITLES.get(envelope["scene"]["genre"], "[GENRE]"), "[RULES]", "[NEGATIVES]"])


def unread(text, envelope, mode):
    """{code: [headers]}: the expected sections a code reads that this prompt lacks, so the code cannot pass on it."""
    expected = _expected_headers(envelope, mode)
    present = {h for h, _ in sections(text)}
    out = {}
    for code, kinds in READS.items():
        missing = [h for h in expected if h.startswith(kinds) and h not in present] if kinds else []
        if missing:
            out[code] = missing
    return out


def check(text, envelope, mode):
    """Findings [{code, message}] for one prose prompt of `mode` compiled from `envelope`."""
    findings = []

    def add(code, message):
        findings.append({"code": code, "message": message})

    render = envelope["nodes"]["render"]["items"][0]
    labels, frame_parts = render["labels"], render["frame_parts"]
    parts = sections(text)
    headers = [h for h, _ in parts]
    expected = _expected_headers(envelope, mode)
    for header in expected:
        if header not in headers:
            add("SECTION_MISSING", f"{header} is missing")
    present = [h for h in headers if h in expected]
    if present != [h for h in expected if h in headers]:
        add("SECTION_ORDER", "Sections are out of the Master Template order")
    for header in headers:
        if header not in expected:
            add("STACKED_GRAPHS", f"{header} is not a Master Template section")
    scene = _body(parts, "[SCENE]")
    if not scene.startswith(envelope["provenance"]["source_prompt"].strip()):
        add("SECTION_ORDER", "The query (the intent) is not the first line of the prompt")
    fresh = prose_renderer.render_all(envelope, frame_parts, labels)[mode]["text"]
    if text != fresh or render["prose"][mode]["text"] != text:
        add("PROSE_STALE", "The text differs from the projection of the current envelope")
    if re.search(r"root exact", text, re.I):
        add("ROOT_EXACT_PRESENT", "The prose carries 'root exact' (owner O3 leaves it to LBN-2.4)")

    _staff_checks(envelope, mode, parts, labels, frame_parts, add)
    _guidance_checks(envelope, parts, labels, mode, add)
    _scene_and_space(envelope, parts, labels, add)
    _props_and_causes(envelope, parts, labels, mode, add)
    _first_state_checks(envelope, parts, labels, add)
    _rules_checks(envelope, parts, labels, mode, add)
    _camera_checks(envelope, parts, labels, add)
    return findings


def _staff_checks(envelope, mode, parts, labels, frame_parts, add):
    rows = _staff(parts, mode)
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    kinematic = {k["id"]: k for k in envelope["nodes"]["kinematic"]["items"]}
    expected = [(round(s["t"], 2), labels[s["entity"]], s) for s in slots(envelope)]
    by_place = {}
    for row in rows:
        by_place.setdefault((row["t"], row["label"]), []).append(row)
    for t, label, _ in expected:
        found = by_place.get((t, label), [])
        if len(found) != 1:
            add("KEY_LINE_MISSING", f"{label} at {t:.2f} has {len(found)} staff lines")
    if len(rows) != len(expected):
        add("KEY_LINE_MISSING", f"{len(rows)} staff lines for {len(expected)} slots")
    slot_of = {(t, label): slot for t, label, slot in expected}
    first_of, last_of = {}, {}
    for _, label, slot in expected:
        first_of.setdefault(label, slot)
        last_of[label] = slot
    for row in rows:
        slot = slot_of.get((row["t"], row["label"]))
        if slot is None:
            continue
        columns = row["columns"]
        if len(columns) != 5 or not columns[0].startswith("SUPPORT "):
            add("STAFF_FORMAT", f"{row['label']} {row['t']:.2f}: {len(columns)} columns, FORMAT has 5")
            continue
        key, support = keys[slot["slot"]], kinematic[slot["slot"]]["support"]
        said = columns[0][len("SUPPORT "):]
        airborne = said.startswith("NO SUPPORT")
        if airborne != (not support):
            add("SUPPORT_MISMATCH", f"{row['label']} {row['t']:.2f}: SUPPORT '{said}' but S11 support is {support or 'none'}")
        elif support and not said.startswith("steps "):
            for part in support:
                noun = part.split("_", 1)[-1]
                if noun not in said and {"foot": "feet", "hand": "hands"}.get(noun, noun) not in said:
                    add("SUPPORT_MISMATCH", f"{row['label']} {row['t']:.2f}: SUPPORT does not name {part}")
        words = staff_geometry.pose_words(key)
        for side, column, initial in (("left", columns[1], "L"), ("right", columns[2], "R")):
            for limb in ("arm", "leg"):
                if f"{initial} {limb} {words[side][limb]}," not in column + ",":
                    add("GESTURE_MISMATCH", f"{row['label']} {row['t']:.2f}: {initial} {limb} should read {words[side][limb]}")
                if f"lower {limb} {words[side]['lower_' + limb]}" not in column:
                    add("GESTURE_MISMATCH", f"{row['label']} {row['t']:.2f}: lower {limb} should read "
                                            f"{words[side]['lower_' + limb]}")
        for part, word in (("body", words["body"]), ("head", words["head"])):
            if (word is not None) != (f", {part} " in columns[1]) or (word and f", {part} {word}" not in columns[1]):
                add("GESTURE_MISMATCH", f"{row['label']} {row['t']:.2f}: {part} should read {word or 'nothing (upright)'}")
        _euler_check(row, key, mode, first_of[row["label"]] is slot, last_of[row["label"]] is slot, add)
        if "[DOUBLE BOW + accent:" in columns[3] and "chain " not in columns[4]:
            add("KINETIC_CHAIN_MISSING", f"{row['label']} {row['t']:.2f}: the strike line has no chain")
    labels_in = {row["label"] for row in rows}
    for label in sorted(labels_in):
        own = [row for row in rows if row["label"] == label]
        _airborne(own, label, envelope, parts, add)
    if mode in ("upgraded_mixed", "euler_heavy"):
        key_line = next((line for line in _body(parts, "[MOVEMENT LANGUAGE]").splitlines()
                         if line.startswith("Skeleton key:")), "")
        missing = [j for j in prose_renderer.JOINTS if not re.search(rf"(^|[ /]){j}[=/]", key_line[13:])]
        if not key_line or missing:
            add("SKELETON_KEY_MISSING", f"The mode carries joints but the skeleton key lacks {missing or 'everything'}")


def _euler_check(row, key, mode, first, last, add):
    """Euler blocks by mode (D6/D7/D10 reading): Mixed root on strikes, first and last lines; Upgraded root and joints
    on strikes and last lines; Euler-heavy everything everywhere; pure staff nothing. Numbers equal the S13 key."""
    blocks = row["columns"][4].split(" · ")[1:]
    root = next((b for b in blocks if b.startswith("Root [")), None)
    joints = next((b for b in blocks if b.startswith("Joints {")), None)
    strike = "[DOUBLE BOW + accent:" in row["columns"][3]
    want_root = {"pure_staff": False, "mixed": strike or first or last, "upgraded_mixed": strike or last,
                 "euler_heavy": True}[mode]
    want_joints = {"pure_staff": False, "mixed": False, "upgraded_mixed": strike or last, "euler_heavy": True}[mode]
    label = f"{row['label']} {row['t']:.2f}"
    if (root is not None) != want_root:
        add("EULER_MODE_MISMATCH", f"{label}: Root block {'missing' if want_root else 'not allowed'} in {mode}")
    if (joints is not None) != want_joints:
        add("EULER_MODE_MISMATCH", f"{label}: Joints block {'missing' if want_joints else 'not allowed'} in {mode}")
    if root is not None and _numbers(root) != [float(v) for v in key["pos"] + key["rot"]]:
        add("EULER_MODE_MISMATCH", f"{label}: Root/EulerXYZ numbers differ from the S13 key")
    if joints is not None:
        expected = [float(v) for j in prose_renderer.JOINTS for v in key["bones"][j]]
        if _numbers(joints) != expected:
            add("EULER_MODE_MISMATCH", f"{label}: joint numbers differ from the S13 key")


def _airborne(own, label, envelope, parts, add):
    rules = _body(parts, "[RULES]")
    run = []
    for i, row in enumerate(own + [None]):
        flying = row is not None and row["columns"][0].startswith("SUPPORT NO SUPPORT")
        if flying:
            run.append(i)
            continue
        if run:
            start = own[run[0]]
            if run[0] == 0 and start["t"] > EPSILON:
                add("AIRBORNE_UNBOOKENDED", f"{label} is airborne at {start['t']:.2f} with no takeoff line")
            if row is None:
                landed = re.search(rf"^- End state: {label} .*support (grounded|braced|lying|both feet|[A-Z]+ foot)", rules,
                                   re.M)
                if not landed:
                    add("AIRBORNE_UNBOOKENDED", f"{label} is airborne from {start['t']:.2f} with no landing line or end state")
            run = []


def _guidance_checks(envelope, parts, labels, mode, add):
    guidance = _body(parts, "[IMPLIED GUIDANCE]")
    rows = _staff(parts, mode)
    duration = envelope["scene"]["duration_s"]
    if "Between lines every performer keeps the declared Effort" not in guidance:
        add("IMPLIED_GUIDANCE_MISSING", "The general between-lines statement is missing")
    intervals = {}
    for match in re.finditer(r"^- ([A-Z]) (\d+\.\d\d)–(\d+\.\d\d): maintain ", guidance, re.M):
        intervals.setdefault(match.group(1), []).append((float(match.group(2)), float(match.group(3))))
    for row in rows:
        spans = intervals.get(row["label"], [])
        if not any(a - EPSILON <= row["t"] < b + EPSILON for a, b in spans):
            add("EFFORT_UNDECLARED", f"{row['label']} {row['t']:.2f}: no declared Effort covers this line")
    for label in sorted(set(labels.values())):
        if f"- {label}: secondary motion of the " not in guidance:
            add("IMPLIED_GUIDANCE_MISSING", f"{label} has no secondary-motion line")
    for row in rows:
        if "[DOUBLE BOW + accent:" in row["columns"][3] and f"- {row['label']} after the {row['t']:.2f} strike" not in guidance:
            add("IMPLIED_GUIDANCE_MISSING", f"{row['label']} {row['t']:.2f}: no recovery line after the strike")
    for label in sorted({r["label"] for r in rows}):
        own = [r for r in rows if r["label"] == label]
        for i, row in enumerate(own):
            flying = row["columns"][0].startswith("SUPPORT NO SUPPORT")
            before = i > 0 and own[i - 1]["columns"][0].startswith("SUPPORT NO SUPPORT")
            if flying and not before and f"- {label} airborne {row['t']:.2f}–" not in guidance:
                add("IMPLIED_GUIDANCE_MISSING", f"{label} {row['t']:.2f}: no airborne-arc line")
        for a, b in zip([r["t"] for r in own], [r["t"] for r in own[1:]] + [duration], strict=True):
            if b - a > prose_renderer.GAP_S + EPSILON and f"- {label} {a:.2f}–{b:.2f} (" not in guidance:
                add("KEY_GAP_UNGUIDED", f"{label} {a:.2f}–{b:.2f}: {b - a:.1f} s with neither a line nor guidance")
    if "Interpolation:" not in _body(parts, "[MOTION CONTROL]"):
        add("INTERPOLATION_UNDECLARED", "MOTION CONTROL does not declare the interpolation")


def _scene_and_space(envelope, parts, labels, add):
    scene, spatial = _body(parts, "[SCENE]"), _body(parts, "[SPATIAL ANCHORS]")
    for entity in envelope["nodes"]["entities"]["items"]:
        if f"{labels[entity['id']]} = {entity['name']}: {entity['silhouette'].rstrip('.')}" not in scene:
            add("ANCHOR_PHRASE_MISSING", f"{labels[entity['id']]} ({entity['id']}) has no appearance phrase")
    for piece in ("Render intent. Motion:", "Animation:", "Choreography:", "final instruction: end on"):
        if piece not in scene:
            add("RENDER_INTENT_MISSING", f"SCENE lacks '{piece}'")
    ax = envelope["scene"]["ax"]
    c = ax["rotation_convention"]
    frame = next((line for line in spatial.splitlines() if line.startswith("Frame:")), "")
    for piece in (f"up {ax['up']}", f"forward {ax['forward']}", f"ground {ax['ground']}", f"Euler {c['euler_order']}",
                  c["kind"], f"{c['handedness']}-handed", c["units"], "+X = the performer's left",
                  "joints local to their parent"):
        if piece not in frame:
            add("CONVENTION_MISSING", f"The frame line lacks '{piece}'")
    for surface in envelope["nodes"]["surfaces"]["items"]:
        if not re.search(rf"^{re.escape(surface['id'].replace('_', ' '))} \(", spatial, re.M):
            add("SPATIAL_ANCHOR_MISSING", f"Surface {surface['id']} is missing")
    for label in sorted({labels[s["entity"]] for s in slots(envelope)}):
        if f"{label} starts at [" not in spatial:
            add("SPATIAL_ANCHOR_MISSING", f"{label}'s start position is missing")


def _first_state_checks(envelope, parts, labels, add):
    """PROP_FIRST_STATE (M8.12; owner renders R4 and R1-R5: B's kunai in A's hand at 0.0, the log drawn before its use)."""
    scene = _body(parts, "[SCENE]")
    first = prose_renderer.first_states(envelope, labels)
    states = envelope["nodes"]["states"]["items"]
    for prop in envelope["nodes"]["props"]["items"]:
        own = sorted((s for s in states if s["subject"] == {"kind": "prop", "id": prop["id"]}), key=lambda s: (s["t"], s["id"]))
        gaps = sorted(k for k, v in (own[0]["conditions"] if own else {}).items() if v == "unknown" and k != "location")
        if not own or gaps:
            add("PROP_FIRST_STATE", f"{prop['name']}: {', '.join(gaps) or 'state'} unknown at the start")
        if f"{prop['name']} (" not in scene or not all(phrase in scene for phrase in first[prop["id"]]):
            add("PROP_FIRST_STATE", f"SCENE does not give {prop['name']}'s state at the start")
        track = _body(parts, f"[PROP STATE MACHINE – {prop['name']}]").split(" · ")[0]
        if "unknown" in track:
            add("PROP_FIRST_STATE", f"{prop['name']}'s state machine starts '{track[:40]}'")


def _prop_holders(envelope, prop_id):
    own = sorted((s for s in envelope["nodes"]["states"]["items"] if s["subject"] == {"kind": "prop", "id": prop_id}),
                 key=lambda s: (s["t"], s["id"]))
    return [s["conditions"].get("holder") for s in own], own


def _props_and_causes(envelope, parts, labels, mode, add):
    who = {**labels}
    for prop in envelope["nodes"]["props"]["items"]:
        block = _body(parts, f"[PROP STATE MACHINE – {prop['name']}]")
        holders, own = _prop_holders(envelope, prop["id"])
        if not block:
            add("PROP_TRACK_MISSING", f"{prop['name']} has no state machine")
            continue
        track = block.splitlines()[0] if block else ""
        stamps = [float(s.split(" ", 1)[0]) for s in track.split(" · ") if s]
        if stamps != sorted(stamps):
            add("PROP_STATE_ORDER", f"{prop['name']}: states are out of time order")
        changes = sum(1 for a, b in zip(own, own[1:], strict=False) if a["conditions"] != b["conditions"])
        if track.count(" -> ") < changes:
            add("PROP_TRACK_MISSING", f"{prop['name']}: {changes} state changes, {track.count(' -> ')} written")
        for t, row in prop_samples.rows(envelope, labels, prop["id"], compact=False):
            if row.split(" moving")[0].split(" held")[0].split(" at rest")[0] not in track:
                add("PROP_TRACK_MISSING", f"{prop['name']}: the sample at {t:.2f} (position, velocity) is missing")
        said = re.findall(r"holder (\S+) -> (\S+?)(?:,| ·|$)", track)
        actual = [(a, b) for a, b in zip(holders, holders[1:], strict=False) if a != b]
        if [(x, y) for x, y in said] != [(who.get(a, a), who.get(b, b)) for a, b in actual]:
            add("PROP_STATE_ORDER", f"{prop['name']}: holder changes {said} disagree with S06 {actual}")
        if "never duplicated, never in two hands at once, never lost" not in block:
            add("PROP_INVARIANT_MISSING", f"{prop['name']} has no invariant line")
        if len(set(holders)) == 1 and holders[0] in labels and f"CUSTODY: {labels[holders[0]]}.{prop['name']}" not in block:
            add("CUSTODY_RULE_MISSING", f"{prop['name']} never changes hands but has no CUSTODY rule")
        for row in _staff(parts, mode):
            for match in re.finditer(r"\[contact: [^\]]*?-?" + re.escape(prop["name"]) + r"[^\]]*?(retained|ENDS)[^\]]*?"
                                     r"(?: at (\d+\.\d\d))?\]", row["columns"][3] if len(row["columns"]) == 5 else ""):
                t = match.group(2) or f"{row['t']:.2f}"
                verb = "held by" if match.group(1) == "retained" else "released by"
                if f"{t} {verb} {row['label']}" not in track:
                    add("PROMPT_CONTRADICTION", f"Staff says {prop['name']} {match.group(1)} by {row['label']} at {t}; "
                                                f"its state machine does not")
    causal = _body(parts, "[CAUSAL LINKS]")
    beats = {b["id"]: b for b in envelope["nodes"]["beats"]["items"]}

    def name(beat_id):
        beat = beats[beat_id]
        return f"{labels.get(beat['actor'], beat['actor'])} {' '.join(beat['label'].replace('_', ' ').split())}"

    printed = set(causal.splitlines())
    for edge in envelope["edges"]["causal"]["items"]:
        arrow = "→" if edge["causal_strength"] == "hard" else "⇢"
        if f"{name(edge['from'])} {arrow} {name(edge['to'])}" not in causal:
            add("CAUSAL_LIST_MISSING", f"{edge['id']} is not in CAUSAL LINKS")
        if f"{name(edge['from'])} {arrow} {name(edge['to'])}: {edge['why']}" not in printed:
            add("CAUSE_REASON", f"{edge['id']}: its reason is not printed in CAUSAL LINKS")
        if beats[edge["to"]]["t"] + EPSILON < beats[edge["from"]]["t"]:
            add("PROMPT_CONTRADICTION", f"CAUSAL LINKS put {edge['from']} before {edge['to']} against their times")
        if edge["causal_strength"] == "hard":
            touches = [c["t"] for c in envelope["nodes"]["contacts"]["items"] if c["beat"] == edge["from"]
                       and c["contact_type"] in ("touch", "possess")]
            if touches and beats[edge["to"]]["t"] + EPSILON < min(touches):
                add("REACTION_WITHOUT_CAUSE", f"{edge['to']} starts at {beats[edge['to']]['t']} before the contact of "
                                              f"{edge['from']} at {min(touches)}")
    for edge_id, message in cause_reason.problems(envelope["edges"]["causal"]["items"], envelope["nodes"]["beats"]["items"],
                                                  envelope):
        add("CAUSE_REASON", f"{edge_id}: {message}")
    fx = " ".join(f["text"] for f in envelope["nodes"]["render"]["items"][0]["frame_parts"]["fx"]).lower()
    negatives = _body(parts, "[NEGATIVES]").lower()
    for word in ("ring", "halo", "full circle"):
        if f"no {word}" in negatives and re.search(rf"\b{word}\b", fx):
            add("PROMPT_CONTRADICTION", f"FX draws a {word} while NEGATIVES forbid it (audit X29)")


def _lasting_expected(envelope, labels):
    ends = {(s["subject"]["kind"], s["subject"]["id"]): s["conditions"] for s in envelope["nodes"]["states"]["items"]
            if s["id"].endswith("@end")}
    last = {}
    for beat in sorted(envelope["nodes"]["beats"]["items"], key=lambda b: (b["t"] + b["dur"], b["t"], b["id"])):
        for effect in beat["effects"]:
            last[(effect["subject"]["kind"], effect["subject"]["id"], effect["property"])] = (beat, effect["value"])
    names = {p["id"]: p["name"] for p in envelope["nodes"]["props"]["items"]}
    out = []
    for (kind, identity, prop), (beat, value) in last.items():
        commit = beat["t"] + beat["dur"]
        if value != "unknown" and ends.get((kind, identity), {}).get(prop) == value and \
                commit < envelope["scene"]["duration_s"] - EPSILON:
            out.append((commit, labels.get(identity) or names.get(identity) or identity.replace("_", " "), prop, value))
    return out


def _rules_checks(envelope, parts, labels, mode, add):
    rules, negatives = _body(parts, "[RULES]"), _body(parts, "[NEGATIVES]")
    lead = ("Follow the SUPPORT column and the contact bows strictly" if mode == "pure_staff"
            else "Laban support and contacts are primary; Euler numbers are precision override only.")
    if lead not in rules:
        add("PRECEDENCE_RULE_MISSING", f"RULES lack the {mode} precedence rule")
    for law in LAWS:
        if f"- {law}" not in rules:
            add("CONSERVATION_RULE_MISSING", f"RULES lack '{law}'")
    _, rows = constraint_rows(envelope, labels)
    for section, text, cid, ref in rows:
        if section == "rules" and ref != prose_renderer.ROOT_EXACT and f"- {text}" not in rules:
            add("RULES_MISSING", f"{cid} '{text}' is missing")
        if section == "negative" and text not in negatives:
            add("NEGATIVES_MISSING", f"{cid} '{text}' is missing")
    for commit, who, prop, value in _lasting_expected(envelope, labels):
        if not re.search(rf"^- From {commit:.2f} to the end, {re.escape(who)} ", rules, re.M):
            add("CAUSAL_RULE_MISSING", f"{who}: {prop} = {value} from {commit:.2f} has no time-bounded rule")
    for label in sorted({labels[s["entity"]] for s in slots(envelope)}):
        if not re.search(rf"^- End state: {label} at \[[^\]]*\].*support ", rules, re.M):
            add("END_STATE_MISSING", f"{label} has no end state with position and support")
    rows_staff = _staff(parts, mode)
    times = {}
    for row in rows_staff:
        times.setdefault(row["label"], []).append(row["t"])
    _, _, intervals = lifecycle(events_for(envelope))
    duration = envelope["scene"]["duration_s"]
    for (entity, part, _, target, _), kind, start, end in intervals:
        if kind != "support" or target == "ground" or entity not in labels:
            continue
        stop = duration if end is None else end
        held = [t for t in times.get(labels[entity], []) if start - EPSILON <= t < stop - EPSILON]
        if len(held) >= 2 and not re.search(rf"^- {labels[entity]} .* stays on the .* from {start:.2f} to {stop:.2f}",
                                            rules, re.M):
            add("SPAN_RULE_MISSING", f"{labels[entity]} {part} on {target} {start:.2f}-{stop:.2f} has no span rule")
    strikes = {}
    for row in rows_staff:
        if "[DOUBLE BOW + accent:" in row["columns"][3]:
            strikes[row["label"]] = strikes.get(row["label"], 0) + 1
    for label, count in strikes.items():
        if count >= 2 and rules.count(f"- TWO SEPARATE STRIKES: {label} ") < count - 1:
            add("EVENT_SEPARATION_MISSING", f"{label} has {count} strikes and fewer than {count - 1} separation rules")


def _camera_checks(envelope, parts, labels, add):
    lines = [line for line in _body(parts, "[CAMERA]").splitlines() if line and not line.startswith("Camera rules:")]
    shots = envelope["nodes"]["camera"]["items"]
    if len(lines) != len(shots):
        add("DISCONNECTED_CAMERA_MOTION", f"{len(lines)} camera lines for {len(shots)} shots")
    for line in lines:
        if "; motivated by " not in line or "; shows " not in line:
            add("DISCONNECTED_CAMERA_MOTION", f"Camera line lacks its motivation or its beats: {line[:40]}")
