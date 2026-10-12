"""M8.4 final-prompt QA: the DAG's model-as-reader check (M4) on a structured-prose prompt.

`check(text, envelope, mode)` reads the prompt as a model reads it (sections, staff lines, guidance, rules) and
compares it with the envelope it was compiled from. Every finding carries a semantic code. kernel/knowledge_map.yaml
lists, per DAG row, the codes that verify it (field `codes`); tests/test_dag_conformance.py compiles every example
through every layer, requires zero findings, and proves each code fires on a prompt broken in that one way.
Codes whose atoms the repo does not have yet are listed in the map as `gaps`, never emitted here.
"""

import math
import re

from compiler.passes.derived import p11_kinematic
from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner import dynamic_beat_validator, hits
from planner.scene_view import slots
from renderers import anime_renderer, prop_samples, prose_renderer
from renderers.anime_renderer import constraint_rows
from solver import contact_world, euler_solver, shape_direction, staff_geometry
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
    "PROP_LINE_MISSING": "a line prop held by one body and fastened to another is not written as one line between them",
    "DOUBLED_WORD": "a word is written twice in a row ('rope dart dart'): the reader cannot tell what is meant",
    "COUNT_CONTRADICTION": "a stated count (fighters, props, a prop's units) disagrees with the scene",
    "VANISHED_BODY": "a substituted body has a staff line before it reappears, its vanish line carries its support or a "
                     "path into the vanish, or RULES do not say it is gone",
    "TURN_LABEL": "a line whose beat names a flip or a cartwheel does not write that turn",
    "BODY_HOLD_FRAMES": "a hold, freeze or pause is written in frames (probes R10, R11, R14 stretched each to about 1 s)",
    "EMPTY_HAND_UNSTATED": "a hand that releases a prop and then holds nothing is not said to be empty (probe R11 kept a "
                           "second kunai in the throwing hand)",
    "ROTATION_ANGLES_PRINTED": "a turn is written as angles at times or a rate, or a line inside a turn prints its "
                               "angles (probe R13 flipped twice)",
    "HIDDEN_PHRASING": "a prop is called hidden or not visible (probes R12, R17 drew it from the start anyway)",
    "IMPACT_CONTACT_SYNC": "a strike bow sits off every printed impact frame, or an impact frame has no contact on it "
                           "(one time per hit, O23; F-021)",
    "AIRBORNE_PICKUP": "a body takes a prop resting on a surface on a NO SUPPORT line (O18; renders R3, R4: F7)",
    "ROTATION_PATH_UNSTATED": "a turn run, named or not (a spin too), is not written once on its first line by axis, "
                              "plane and count with its takeoff and landing, or not continued on its later lines (FR.1 "
                              "as amended by W3)",
    "MOMENTUM_MISSING": "an anime span that hangs against gravity is not said to hang (stylised hang time) in RULES "
                        "(plan F9.2, owner O74; S11 refuses an undeclared hang)",
    "CONTACT_WORLD": "a touch or hold of a prop or a body that S13 measures does not print its two world points on its "
                     "actor's staff line (plan F5.2, owners O24, O72, O83)",
    "SHAPE_DIRECTION": "a printed Shape quality is the opposite of what the body's path and form show (plan F9.1, owner "
                       "O31, O73; airborne turns are not judged, O76)",
    "ENTRANCE_UNSTATED": "a performer who starts in the air above a raised top lacks the rule that its feet touch the "
                         "top at the landing, not earlier, or the negative against standing on it at the start "
                         "(probe V6, R19; F10)",
    "PROP_PHYSICS_UNSTATED": "a free prop's flight is not written as ballistic under gravity (or a declared float) from its "
                             "p and v (plan F2.1: the model skips between samples)",
    "PROP_VISIBILITY": "a prop's WHERE line is missing, leaves a gap, disagrees with the derived track, or a span has no "
                       "place (plan F6.1 as amended by W4, F6.2)",
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
    "HIT_HOLD": "a hit (from the contacts, or a hold on an impact frame) is not printed as a camera hold naming every body "
                "present, or its shot is a close-up, an insert or a moving camera (owner O92, R-21; F-083, F-155, F-177)",
    "PLAYBACK_RAMP": "a camera line plays at a speed other than normal x1 (owner O92: the clip has a fixed length; F-083)",
    "CAMERA_RULES": "the printed camera rules are not the genre card's, word for word; the card's rules are checked against "
                    "the grammar and owner O92 where they are written (planner/camera_library.py; F-160, F-177)",
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
    "CUSTODY_RULE_MISSING": (PROPS,), "PROP_FIRST_STATE": ("[SCENE]", PROPS), "PROP_LINE_MISSING": (PROPS,),
    "DOUBLED_WORD": (), "COUNT_CONTRADICTION": (),
    "VANISHED_BODY": (STAFF, RULES, "[IMPLIED GUIDANCE]"), "TURN_LABEL": (STAFF,),
    "BODY_HOLD_FRAMES": (), "EMPTY_HAND_UNSTATED": (STAFF,), "ROTATION_ANGLES_PRINTED": (), "HIDDEN_PHRASING": (),
    "IMPACT_CONTACT_SYNC": (STAFF, "[ANIME]", "[UGC]", "[LIVE ACTION]"), "AIRBORNE_PICKUP": (STAFF,),
    "PROP_PHYSICS_UNSTATED": (PROPS,), "PROP_VISIBILITY": (PROPS,), "ROTATION_PATH_UNSTATED": (STAFF,),
    "ENTRANCE_UNSTATED": (RULES, NEGATIVES), "SHAPE_DIRECTION": ("[IMPLIED GUIDANCE]",), "MOMENTUM_MISSING": (RULES,),
    "CONTACT_WORLD": (STAFF,),
    "CAUSAL_LIST_MISSING": ("[CAUSAL LINKS]",), "CAUSE_REASON": ("[CAUSAL LINKS]",),
    "REACTION_WITHOUT_CAUSE": (),
    "CAUSAL_RULE_MISSING": (RULES,), "CONSERVATION_RULE_MISSING": (RULES,), "SPAN_RULE_MISSING": (STAFF, RULES),
    "EVENT_SEPARATION_MISSING": (STAFF, RULES), "RULES_MISSING": (RULES,), "NEGATIVES_MISSING": (NEGATIVES,),
    "DISCONNECTED_CAMERA_MOTION": ("[CAMERA]",), "HIT_HOLD": ("[CAMERA]",), "PLAYBACK_RAMP": ("[CAMERA]",),
    "CAMERA_RULES": ("[CAMERA]",),
    "ANCHOR_PHRASE_MISSING": ("[SCENE]",),
    "RENDER_INTENT_MISSING": ("[SCENE]",), "END_STATE_MISSING": (RULES,),
}
HEADER = re.compile(r"^\[[A-Z][^\]]*\]$")
LINE = re.compile(r"^(\d+\.\d\d) ([A-Z]): SUPPORT (.*)$")
SHOT = re.compile(r"^(\d+\.\d\d)–(\d+\.\d\d) \S+(?: across the axis)? to (\w+)")
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
    _where_checks(envelope, parts, labels, add)
    _entrance_checks(envelope, parts, labels, add)
    _shape_checks(envelope, parts, labels, add)
    _world_checks(envelope, mode, parts, labels, add)
    for rule in prose_renderer.hang_rules(envelope, labels):  # MOMENTUM_MISSING (plan F9.2, owner O74)
        if rule not in _body(parts, RULES):
            add("MOMENTUM_MISSING", f"RULES do not say: {rule}")
    _first_state_checks(envelope, parts, labels, add)
    _line_and_word_checks(envelope, text, parts, labels, add)
    _count_checks(envelope, text, add)
    _vanish_checks(envelope, parts, labels, mode, add)
    _turn_checks(envelope, parts, labels, mode, add)
    _wording_checks(envelope, text, parts, labels, mode, add)
    _impact_checks(envelope, parts, mode, add)
    _pickup_checks(envelope, parts, labels, mode, add)
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
    mids = {s for run in prose_renderer.turn_runs(envelope, labels) for s in run["slots"][1:]}
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
        _euler_check(row, key, mode, first_of[row["label"]] is slot, last_of[row["label"]] is slot, add,
                     slot["slot"] in mids)
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


def _euler_check(row, key, mode, first, last, add, mid=False):
    """Euler blocks by mode (D6/D7/D10 reading): Mixed root on strikes, first and last lines; Upgraded root and joints
    on strikes and last lines; Euler-heavy everything everywhere; pure staff nothing. Numbers equal the S13 key; a line
    inside a turn writes its root position and 'EulerXYZ mid-turn' (W3)."""
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
    if root is not None and _numbers(root) != [float(v) for v in key["pos"] + ([] if mid else key["rot"])]:
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


NUMBER_WORDS = {w: i for i, w in enumerate(("zero one two three four five six seven eight nine ten eleven twelve").split())}
COUNT_WORD = rf"(?:\d+|{'|'.join(NUMBER_WORDS)})"
HOLD_FRAMES = re.compile(rf"\b(?:hold|holds|held|holding|freeze|freezes|frozen|freezing|pause|pauses|paused)\b"
                         r"(?:[^.;\n]|\.(?=\d))*?"  # one clause; a time's point (0.60) is not a full stop
                         rf"\b{COUNT_WORD}[- ]frames?\b|\b{COUNT_WORD}[- ]frames? (?:hold|freeze|pause)", re.I)
RATE = re.compile(r"degrees per second|deg/s|°/s", re.I)
ANGLE_AT = re.compile(r"-?\d+(?:\.\d+)?\s*(?:degrees|deg|°)\s+at\s+\d+\.\d\d")
INNER_ANGLE = re.compile(r"EulerXYZ \[|\d\s*(?:degrees|deg|°)|sign \([^)]*\d")
HIDDEN = re.compile(r"\b(?:hidden|not visible|invisible|concealed|out of sight)\b", re.I)


def _pickup_checks(envelope, parts, labels, mode, add):
    """AIRBORNE_PICKUP (owner O18, backlog M9-03): at the instant a body takes a prop resting on a surface, its staff
    line (the last one at or before that time) does not say NO SUPPORT."""
    rows = _staff(parts, mode)
    for c in p11_kinematic.resting_pickups(envelope):
        label = labels.get(c["a"]["id"])
        own = [r for r in rows if r["label"] == label and r["t"] <= c["t"] + EPSILON]
        if own and own[-1]["columns"][0].startswith("SUPPORT NO SUPPORT"):
            add("AIRBORNE_PICKUP", f"{label} takes the resting {c['b']['id']} at {c['t']:.2f} on a NO SUPPORT line")


BOW_TIME = re.compile(r" at (\d+\.\d\d)\]?$")
VERB_MARK = re.compile(r"^[A-Z]{3,} (?=\[|contact bow)")  # owner O22: 'DEFLECT [DOUBLE BOW + accent: ...]'


def _impact_checks(envelope, parts, mode, add):
    """IMPACT_CONTACT_SYNC (owner O23, backlog M9-02): the prompt prints one time per hit. Every strike bow sits on a
    printed impact frame; every printed impact frame has a bow on it (a strike, a contact, or a hold that starts there:
    a catch, O93), or a support onset in the envelope (a body hitting a surface; surface supports are not printed as
    bows)."""
    genre = _body(parts, GENRE_TITLES.get(envelope["scene"]["genre"], "[GENRE]"))
    line = next((x for x in genre.splitlines() if x.startswith("Impact frames:")), "")
    impacts = [float(x) for x in re.findall(r"\d+\.\d\d", line)]
    tolerance = 0.5 / envelope["scene"]["fps"] + 1e-9
    strikes, bows = [], []
    for row in _staff(parts, mode):
        if len(row["columns"]) != 5:
            continue
        for item in (VERB_MARK.sub("", x) for x in row["columns"][3].split("; ")):
            if item.startswith(("[DOUBLE BOW + accent:", "contact bow:")) or (item.startswith("[contact:")
                                                                             and item.endswith(" retained]")):
                match = BOW_TIME.search(item)
                t = float(match.group(1)) if match else row["t"]
                bows.append(t)
                if item.startswith("[DOUBLE BOW"):
                    strikes.append((row["label"], t, item))
    supports = [c["t"] for c in envelope["nodes"]["contacts"]["items"] if c["contact_type"] == "support"]
    for label, t, item in strikes:
        if not any(abs(t - i) <= tolerance for i in impacts):
            add("IMPACT_CONTACT_SYNC", f"{label} strike at {t:.2f} ({item[:40]}) is on no printed impact frame")
    for i in impacts:
        if not any(abs(t - i) <= tolerance for t in bows + supports):
            add("IMPACT_CONTACT_SYNC", f"Impact frame {i:.2f} has no contact on it")


def _wording_checks(envelope, text, parts, labels, mode, add):
    """The probe wording rules W1-W4 (owner O47-O49; docs/render_tests/2026-10-11-m9-probes): no hold or freeze in
    frames, the empty hand after a release, a turn named once without angles, no prop called hidden."""
    for match in HOLD_FRAMES.finditer(text):
        add("BODY_HOLD_FRAMES", f"'{match.group(0)[:70]}'")
    rows = _staff(parts, mode)
    staff = "\n".join(row["line"] for row in rows)
    for phrase in prose_renderer.empty_hands(envelope, labels).values():
        if phrase not in staff:
            add("EMPTY_HAND_UNSTATED", f"STAFF lacks '{phrase}'")
    for match in RATE.finditer(text):
        add("ROTATION_ANGLES_PRINTED", f"a rate is written: '{match.group(0)}'")
    for line in text.splitlines():
        if len(ANGLE_AT.findall(line)) >= 2:
            add("ROTATION_ANGLES_PRINTED", f"angles at times: '{line[:60]}'")
    times = {s["slot"]: (labels.get(s["entity"]), round(s["t"], 6)) for s in slots(envelope)}
    inside = {times[s] for run in prose_renderer.turn_runs(envelope, labels) for s in run["slots"][1:]}
    for row in rows:
        if (row["label"], round(row["t"], 6)) in inside and INNER_ANGLE.search(row["line"]):
            add("ROTATION_ANGLES_PRINTED", f"{row['label']} {row['t']:.2f} prints angles inside a turn")
    motion = next((lines for header, lines in parts if header.startswith("[MOTION CONTROL]")), [])
    turning = anime_renderer.inbetweens_turning(envelope)  # RV-59k (F-232): the in-between lines too
    for between in anime_renderer.inbetweens(envelope):
        head = f"{prose_renderer._time(between['t'])} {labels[between['entity']]}: "
        line = next((line for line in motion if line.startswith(head)), "")
        if between["id"] in turning and INNER_ANGLE.search(line):
            add("ROTATION_ANGLES_PRINTED", f"{head.rstrip(': ')} (an in-between key) prints angles inside a turn")
    props = envelope["nodes"]["props"]["items"]
    names = [p["name"].lower() for p in props] + [p["unit_name"].lower() for p in props if p.get("unit_name")]
    for header, lines in parts:
        body = "\n".join(lines)
        if header.startswith(PROPS):
            clauses = [body]
        else:
            clauses = [c for c in re.split(r"[.;\n]", body) if any(n in c.lower() for n in names)]
        for clause in clauses:
            for match in HIDDEN.finditer(clause):
                add("HIDDEN_PHRASING", f"{header}: '{match.group(0)}' near '{clause.strip()[:50]}'")




def _vanish_checks(envelope, parts, labels, mode, add):
    """VANISHED_BODY (owner O18, audit X9: the golden showed A standing at 4.00 after vanishing at 3.70)."""
    rules = _body(parts, "[RULES]")
    for rule in prose_renderer.vanish_rules(envelope, labels):
        if f"- {rule}" not in rules:
            add("VANISHED_BODY", f"RULES lack '{rule[:50]}'")
    for actor, _, start, back in dynamic_beat_validator.vanish_windows(envelope["nodes"]["beats"]["items"]):
        for row in _staff(parts, mode):
            if row["label"] == labels.get(actor) and start + EPSILON < row["t"] and (back is None or row["t"] < back - EPSILON):
                add("VANISHED_BODY", f"{row['label']} has a staff line at {row['t']:.2f} while gone")
            elif row["label"] == labels.get(actor) and abs(row["t"] - start) <= EPSILON and (  # owner O90, F-163 (RV-62)
                    f"then none: {row['label']} vanishes here" not in row["columns"][0]
                    or row["columns"][0].startswith("SUPPORT steps ")  # F-176 (RV-70): a support that travels
                    or (len(row["columns"]) > 4 and "path: " in row["columns"][4])):
                add("VANISHED_BODY", f"{row['label']}'s line at {row['t']:.2f} carries its support or a path into the vanish")
        label = labels.get(actor)
        for line in _body(parts, "[IMPLIED GUIDANCE]").splitlines():  # F-176 (RV-70): nor does the guidance move it
            span = re.match(rf"- {re.escape(label or '')} (\d+\.\d\d)–(\d+\.\d\d)\b", line) if label else None
            if span and float(span.group(1)) < (back if back is not None else math.inf) - EPSILON \
                    and float(span.group(2)) > start + EPSILON:
                add("VANISHED_BODY", f"The guidance moves {label} {span.group(1)}–{span.group(2)} while it is gone")


def _turn_checks(envelope, parts, labels, mode, add):
    """TURN_LABEL (owner O18, audit X5/X6: the golden's 'full backflip' had pitch 0, its 'cartwheel' no roll): the line
    of a beat that names a flip or a cartwheel writes that turn (W3: its run's first line names it, later lines continue
    it)."""
    rows = {(row["label"], round(row["t"], 6)): row["line"] for row in _staff(parts, mode)}
    runs = prose_renderer.turn_runs(envelope, labels)
    for slot in slots(envelope):
        turn = euler_solver.named_turn(slot["label"]) if slot["role"] == "actor" else None
        if turn is None:
            continue
        line = rows.get((labels.get(slot["entity"]), round(slot["t"], 6)), "")
        run = next((r for r in runs if slot["slot"] in r["slots"]), None)
        if run is None or run["turn"] != turn or (run["head"] if run["slots"][0] == slot["slot"] else run["more"]) not in line:
            add("TURN_LABEL", f"{labels.get(slot['entity'])} {slot['t']:.2f} ({slot['label']}) does not write its {turn}")
    at = {slot["slot"]: slot for slot in slots(envelope)}
    for run in runs:  # ROTATION_PATH_UNSTATED (FR.1 as amended by W3): every run, named by a beat or not
        for position, slot_id in enumerate(run["slots"]):
            slot, words = at[slot_id], run["head"] if position == 0 else run["more"]
            if words not in rows.get((labels.get(slot["entity"]), round(slot["t"], 6)), ""):
                add("ROTATION_PATH_UNSTATED", f"{labels.get(slot['entity'])} {slot['t']:.2f}: the {run['turn']} is not "
                                              f"written as '{words}'")


def _count_checks(envelope, text, add):
    """COUNT_CONTRADICTION (M8.12, owner O17; render finding F12: R5 drew four shuriken while the prompt said both FOUR
    props and FIVE props): every '<number> fighters|performers|characters|props' and '<number> <a prop's unit or name>'
    agrees with the scene. A number inside a time (2.50) or opening a list item (LBN-2.4's ';8 rope dart pull') is a
    time, not a count; '<n> shuriken volley' may count the units or the volleys."""
    props, people = envelope["nodes"]["props"]["items"], len(envelope["nodes"]["entities"]["items"])
    plural = {"fighters": {people}, "performers": {people}, "characters": {people}, "props": {len(props)}}
    named = {}
    for prop in props:
        unit, count = prop.get("unit_name"), prop.get("count", 1)
        named[prop["name"].lower()] = {1, count} if unit and prop["name"].lower().startswith(unit.lower()) else {1}
        if unit:
            named.setdefault(unit.lower(), {count})
    nouns = "|".join(sorted((re.escape(n) for n in [*plural, *named]), key=len, reverse=True))
    for match in re.finditer(rf"(?<![\d.;\"\[])\b(\d+|{'|'.join(NUMBER_WORDS)})\s+({nouns})\b(?!\.\d)", text, re.I):
        stated = int(match.group(1)) if match.group(1).isdigit() else NUMBER_WORDS[match.group(1).lower()]
        allowed = {**plural, **named}[match.group(2).lower()]
        if stated not in allowed:
            add("COUNT_CONTRADICTION", f"'{match.group(0)}' but the scene has {' or '.join(map(str, sorted(allowed)))}")


def _line_and_word_checks(envelope, text, parts, labels, add):
    """PROP_LINE_MISSING and DOUBLED_WORD (M8.12; render finding F8: the wrapped rope dart never one line, 'rope dart
    dart')."""
    names = {p["id"]: p["name"] for p in envelope["nodes"]["props"]["items"]}
    for prop_id, rows in prose_renderer.line_links(envelope, labels).items():
        track = _body(parts, f"[PROP STATE MACHINE – {names[prop_id]}]")
        for _, row in rows:
            if row not in track:
                add("PROP_LINE_MISSING", f"{names[prop_id]}: '{row}' is not in its state machine")
    for match in re.finditer(r"\b([A-Za-z]{2,})\s+\1\b", text, re.I):
        add("DOUBLED_WORD", f"'{match.group(0)}' near '{text[max(0, match.start() - 30):match.start()].strip()}'")


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
        everything = "\n".join(_body(parts, header) for header, _ in parts)
        for clause in re.split(r"[;\n]", everything):  # F-122: a goal the prompt denies the prop elsewhere
            if prop["name"].lower() not in clause.lower():
                continue
            for label in sorted(set(labels.values())):
                if re.search(rf"\bNOT toward {re.escape(label)}\b", clause) and \
                        re.search(rf"(?<!NOT )\btoward {re.escape(label)}\b", track):
                    add("PROMPT_CONTRADICTION", f"{prop['name']}: its track says toward {label} where the prompt says "
                                                f"NOT toward {label}")
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


def _world_point(values):
    return "[" + ", ".join(f"{round(v, 2):g}" for v in values) + "]"


def _world_checks(envelope, mode, parts, labels, add):
    """CONTACT_WORLD (plan F5.2, owners O24, O72, O83): every touch or hold of a prop or a body that S13 measures prints
    the actor's and the target's world points on the actor's staff line for that beat; S13 refuses the distance."""
    lines = {(row["t"], row["label"]): row["line"] for row in _staff(parts, mode)}
    starts = {(s["entity"], s["beat"]): round(s["t"], 2) for s in slots(envelope)}
    beat_of = {c["id"]: c["beat"] for c in envelope["nodes"]["contacts"]["items"]}
    for row in contact_world.measure(envelope):
        if not row["measurable"] or row["kind"] == contact_world.KINDS["surface"]:
            continue
        line = lines.get((starts.get((row["actor"], beat_of[row["id"]])), labels.get(row["actor"])), "")
        if f" at {_world_point(row['actor_point'])}, " not in line or f" at {_world_point(row['target_point'])}" not in line:
            add("CONTACT_WORLD", f"{labels.get(row['actor'])} {row['t']:.2f}: the staff does not print the two points of "
                                 f"{row['part'].replace('_', ' ')} on {row['target']}")


def _shape_checks(envelope, parts, labels, add):
    """SHAPE_DIRECTION (plan F9.1, owner O73): the Shape quality each IMPLIED GUIDANCE line prints is not contradicted
    by its performer's path and form over the interval (solver/shape_direction.py)."""
    printed = {(m.group(1), m.group(2)): m.group(3) for m in re.finditer(
        r"^- ([A-Z]) (\d+\.\d\d)–\d+\.\d\d: maintain [^;]*; shape (\w+)", _body(parts, "[IMPLIED GUIDANCE]"), re.M)}
    support = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
    keys = sorted(envelope["nodes"]["motion"]["items"], key=lambda k: k["t"])
    for interval in envelope["nodes"]["efforts"]["items"]:
        quality = printed.get((labels.get(interval["actor"]), f"{interval['t']:.2f}"))
        own = [k for k in keys if k["entity"] == interval["actor"]]
        ids = [f"{interval['actor']}@{b}" for b in interval["beats"]]
        inside = [i for i, k in enumerate(own) if k["id"] in ids]
        span = own[inside[0]:inside[-1] + 2] if inside else []
        if quality in shape_direction.OPPOSITE and len(span) > 1 and shape_direction.judge(
                quality, span, [support[k["id"]] for k in span]) == "contradicted":
            add("SHAPE_DIRECTION", f"{labels.get(interval['actor'])} {interval['t']:.2f}: shape {quality} is the opposite "
                                   "of what the body does")


def _entrance_checks(envelope, parts, labels, add):
    """ENTRANCE_UNSTATED (probe V6, owner O51, R19): each entrance from above has its rule and its negative."""
    rules, negatives = _body(parts, RULES), _body(parts, NEGATIVES)
    for entrance in prose_renderer.entrances(envelope, labels):
        if entrance["rule"] not in rules:
            add("ENTRANCE_UNSTATED", f"RULES do not say when {entrance['label']}'s feet first touch the top")
        if entrance["negative"] not in negatives:
            add("ENTRANCE_UNSTATED", f"NEGATIVES do not forbid {entrance['label']} standing on the top at the start")


def _where_checks(envelope, parts, labels, add):
    """Plan F2.1, F6.1 (as amended by W4) and F6.2: each prop block's WHERE line tiles 0 to the end with the derived
    track; flights state their physics (PROP_PHYSICS_UNSTATED), every other span its place (PROP_VISIBILITY)."""
    end = f"{envelope['scene']['duration_s']:.2f}"
    for prop in envelope["nodes"]["props"]["items"]:
        block = _body(parts, f"[PROP STATE MACHINE – {prop['name']}]")
        if not block:
            continue  # PROP_TRACK_MISSING
        line = next((row for row in block.splitlines() if row.startswith("WHERE: ")), "")
        items = line[len("WHERE: "):].split(" · ") if line else []
        for start, stop, kind, text in prop_samples.track(envelope, labels, prop["id"]):
            item = f"{start:.2f}-{stop:.2f} {text}"
            if kind == "flight" and item not in items:
                add("PROP_PHYSICS_UNSTATED", f"{prop['name']}: the flight {start:.2f}-{stop:.2f} is not stated as {text}")
            elif kind == "unplaced":
                add("PROP_VISIBILITY", f"{prop['name']}: nothing says where it is {start:.2f}-{stop:.2f}")
            elif kind != "flight" and line and item not in items:
                add("PROP_VISIBILITY", f"{prop['name']}: the WHERE line does not say '{item}'")
        if not line:
            add("PROP_VISIBILITY", f"{prop['name']} has no WHERE line")
            continue
        times = [re.match(r"(\d+\.\d\d)-(\d+\.\d\d) ", item) for item in items]
        spans = [(m.group(1), m.group(2)) for m in times if m]
        if len(spans) < len(items) or not spans or spans[0][0] != "0.00" or spans[-1][1] != end or any(
                a[1] != b[0] for a, b in zip(spans, spans[1:], strict=False)):
            add("PROP_VISIBILITY", f"{prop['name']}: the WHERE spans do not run from 0.00 to {end} without a gap")


def _lasting_expected(envelope, labels):
    """Each property's last S06 change at the instant it took effect (F-132), when known and before the end: the
    time-bounded rule it needs (read here from S06, not through the renderer)."""
    subjects = {s["id"]: s["subject"] for s in envelope["nodes"]["states"]["items"]}
    names = {p["id"]: p["name"] for p in envelope["nodes"]["props"]["items"]}
    last = {}
    for edge in envelope["edges"]["state_transition"]["items"]:
        subject = subjects[edge["to_state"]]
        for change in edge["changes"]:
            key = (subject["kind"], subject["id"], change["property"])
            if key not in last or change["t"] >= last[key][0]:
                last[key] = (change["t"], change["to"])
    return [(t, labels.get(identity) or names.get(identity) or identity.replace("_", " "), prop, value)
            for (_, identity, prop), (t, value) in last.items()
            if value != "unknown" and t < envelope["scene"]["duration_s"] - EPSILON]


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
    lines = [line for line in _body(parts, "[CAMERA]").splitlines()
             if line and not line.startswith(("Camera rules:", "Holds on hits:"))]
    shots = envelope["nodes"]["camera"]["items"]
    if len(lines) != len(shots):
        add("DISCONNECTED_CAMERA_MOTION", f"{len(lines)} camera lines for {len(shots)} shots")
    for line in lines:
        if "; motivated by " not in line or "; shows " not in line:
            add("DISCONNECTED_CAMERA_MOTION", f"Camera line lacks its motivation or its beats: {line[:40]}")
        played = re.search(r"; (\w+) x([0-9.]+); shows ", line)
        if played and (played.group(1), float(played.group(2))) != ("normal", 1.0):
            add("PLAYBACK_RAMP", f"A camera line plays {played.group(1)} x{played.group(2)}: {line[:40]}")
    camera = _body(parts, "[CAMERA]")
    printed = next((line for line in camera.splitlines() if line.startswith("Camera rules: ")), None)
    if printed != "Camera rules: " + " ".join(prose_renderer.camera_rules(envelope)):  # F-177 (RV-71b): word for word
        add("CAMERA_RULES", "The printed camera rules are not the genre card's, word for word")
    held = camera.split("Holds on hits: ", 1)[1].split("\n", 1)[0] if "Holds on hits: " in camera else ""
    frame_parts = envelope["nodes"]["render"]["items"][0]["frame_parts"]
    for t in hits.hold_times(envelope, frame_parts):  # every hit, from the contacts or S17's holds (owner O92, F-155)
        shot = next((m for m in map(SHOT.match, lines) if m and float(m.group(1)) - EPSILON <= t < float(m.group(2)) - EPSILON),
                    None)
        if (f"{t:.2f} impact: hold with " not in held or shot is None or "; static: " not in shot.string
                or any(word in shot.group(3) for word in ("close", "insert"))):
            add("HIT_HOLD", f"The hit at {t:.2f} is not a camera hold with the bodies in frame")
            continue
        entry = held.split(f"{t:.2f} impact: hold with ", 1)[1].split("; ", 1)[0]  # F-177 (RV-71a): the bodies it names
        named = set(re.split(r", | and ", entry[entry.find("(") + 1:entry.find(")")])) if "(" in entry else set()
        present = {labels[e["id"]] for e in envelope["nodes"]["entities"]["items"]
                   if not any(actor == e["id"] and start < t - EPSILON and (back is None or t < back - EPSILON)
                              for actor, _, start, back in dynamic_beat_validator.vanish_windows(
                                  envelope["nodes"]["beats"]["items"]))}
        if not present <= named:
            add("HIT_HOLD", f"The hold at {t:.2f} leaves out {', '.join(sorted(present - named))}")
