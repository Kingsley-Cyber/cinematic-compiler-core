"""S17 structured-prose prompts (M8; owner O1-O3): the knowledge DAG's Master Template in four movement modes.

Compiled alongside the LBN-2.4 prompt, which stays the uncompressed projection (no_render_compression). Derived only:
a pure function of the envelope and the S17 frame parts. Spec: docs/plans/M8_DAG_PROSE.md (Master Template C19, D8
wrapper, D9 blocks, FORMAT line L507, precision tags L522).

Sections in order: [SCENE] (with the render intent), [MOVEMENT LANGUAGE] + FORMAT, [LABAN STAFF – <MODE>], [IMPLIED
GUIDANCE], [MOTION CONTROL], [SPATIAL ANCHORS], [PROP STATE MACHINE – <prop>] per prop, [CAUSAL LINKS], [CAMERA], the
genre block ([ANIME], [UGC], [LIVE ACTION]), [RULES], [NEGATIVES]. Staff words come
from solver/staff_geometry.py; one line per slot (performer x beat). SUPPORT reads 'steps <direction> alternating'
only when this line and the next stand on the ground on feet with no height change between them. A strike is a touch
whose beat holds an S17 impact frame (contacts are stamped at their beat's end, impact frames where the hit reads), on
anything but a prop the performer holds (touching your own held prop is handling, e.g. a throw, not a hit).
Modes differ only in the Euler blocks:
pure staff none; Mixed root + EulerXYZ on strike lines and each performer's first and last line; Upgraded Mixed
root + EulerXYZ + joints on strike lines and each performer's last line; Euler-heavy everything on every line
(the key choice reads D6/D7/D10's instances; interpretation). The prose leaves out the kernel rule
'<label> root exact' (owner O3) and lists the constraints it leaves out.
Probe wording rules W1-W4 (owner O47-O49, renders R10-R18): no hold or freeze in frames (a hit gets a camera hold with
the bodies in frame); a hand that releases and then holds nothing is said to be empty; a turn is named once by axis,
plane and count, and the lines inside it write 'EulerXYZ mid-turn'; no prop is called hidden.
"""

import hashlib

from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner import camera_library, dynamic_beat_validator
from planner.scene_view import slots
from renderers import prop_samples, ugc_renderer
from renderers.anime_renderer import NUMBERS, _face_words, _items, _num, constraint_rows
from solver import euler_solver, staff_geometry

TARGET = "structured-prose"
MODES = {
    "pure_staff": ("PURE STAFF", "pure staff: the staff words carry the movement; no numbers"),
    "mixed": ("MIXED MODE", "Mixed: staff lines primary; Root [x, y, z] + EulerXYZ [x, y, z] on strike lines and on "
                            "each performer's first and last line, as precision override"),
    "upgraded_mixed": ("UPGRADED MIXED", "Upgraded Mixed: staff lines primary; Root, EulerXYZ and the full Joints "
                                         "dictionary on strike lines and on each performer's last line, as precision "
                                         "override"),
    "euler_heavy": ("EULER-HEAVY", "Euler-heavy: every line carries Root, EulerXYZ and the full Joints dictionary; the "
                                   "staff words stay primary"),
}
JOINTS = ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")
ROOT_EXACT = "k_rules_01"  # '<label> root exact': left out of the prose (owner O3)
GENRES = {"anime": "anime", "live_action": "live-action", "ugc_ad": "UGC ad"}
TRAVEL_M = 0.2
HANDS = ("left_hand", "right_hand")
# W3 (owner O47; probes R13, R18): each turn is named once with its axis and plane. (noun, tail, partial verb) per side.
TURN_TEXT = {
    "flip": ("side-to-side axis (sagittal plane)", {"forward": ("front flip", "", "tips forward"),
                                                    "backward": ("backflip", "", "tips backward")}),
    "spin": ("vertical axis (transverse plane)", {"to the left": ("spin", " to the left", "turns to the left"),
                                                 "to the right": ("spin", " to the right", "turns to the right")}),
    "cartwheel": ("front-to-back axis (frontal plane)",
                  {"toward the performer's right": ("cartwheel", " toward the performer's right",
                                                    "tilts toward the performer's right"),
                   "toward the performer's left": ("cartwheel", " toward the performer's left",
                                                   "tilts toward the performer's left")}),
}
FULL_TURN_SLACK = euler_solver.FULL_TURN_SLACK  # one number with S13's ROTATION_INCOMPLETE (interpretation)
LABAN_WORDS = {"punch": "thrust"}  # owner O22, plan F4.2: an action prints as a quality; 'punch' reads as a fist
GAP_S = 1.5  # C2: never more than 1.5 s without an explicit key or strong implied guidance
EPSILON = 1e-6
GENRE_BLOCKS = {"anime": "ANIME", "ugc_ad": "UGC", "live_action": "LIVE ACTION"}
LOOSE = ("scarf", "coat", "robe", "robes", "sleeves", "hem", "cape", "cloak", "hair", "hood", "hoodie", "skirt", "ribbon",
         "sash", "tassel", "trousers")
CONSERVATION = (  # T10, six of seven laws (PRESERVE_AXIS left out, P3.2-6); in the rules layer, not first (P3.2-7)
    "Identity is immutable: every performer and prop stays itself for the whole scene.",
    "Spatial continuity: a body travels through space between lines, never faster than 25 m/s; only a declared "
    "substitution may jump (the decoy is revealed and the body reappears at its next line).",
    "Momentum is conserved: a body keeps moving the way the last force sent it until something stops it.",
    "Ground force needs support: pushing, bracing and striking from the ground need a supporting part.",
    "Contact before effect: nothing reacts to a hit before the contact.",
    "Rotation is continuous: turns, flips and cartwheels sweep through every angle in between.",
)


def _words(identifier):
    return " ".join(identifier.replace("_", " ").split())


def _part(part):
    side, _, name = part.partition("_")
    return f"{side[0].upper()} {name}" if side in ("left", "right") and name else _words(part)


def _target(end, labels, names):
    who = labels.get(end["id"]) or names.get(end["id"]) or _words(end["id"])
    if not end.get("part"):
        return who
    part = _words(end["part"])
    return f"{who} ({part} end)" if part in who.split() else f"{who} {part}"  # never "rope dart dart" (F8)


def line_links(envelope, labels):
    """{prop id: [(t, text)]}: a line prop (its card has a 'line' state) held by one body and touched or taken by another
    is one line between them (M8.12, PROP_LINE_MISSING; owner render R3 pulled the rope two ways, audit X4)."""
    out = {}
    for prop in _items(envelope, "nodes", "props"):
        if not any(s.get("property") == "line" for s in prop.get("states", [])):
            continue
        held, rows = {}, []
        for c in sorted((c for c in _items(envelope, "nodes", "contacts") if c["b"]["kind"] == "prop"
                         and c["b"]["id"] == prop["id"]), key=lambda c: (c["t"], c["id"])):
            other = c["a"]["id"]
            for holder, part in held.items():
                if holder != other and c["contact_type"] in ("touch", "possess"):
                    rows.append((c["t"], f"{_time(c['t'])} one line from {labels.get(holder, holder)} {_part(part)} to "
                                         f"{labels.get(other, other)} {_part(c['body_part'])}"))
            if c["contact_type"] == "possess":
                held[other] = c["body_part"]
            elif c["contact_type"] == "release":
                held.pop(other, None)
        out[prop["id"]] = rows
    return out


def _time(t):
    return f"{t:.2f}"


def empty_hands(envelope, labels):
    """{contact id: phrase}: W2 (owner O47; probes R11, R16: unstated, B kept a second kunai; stated, it held one). A hand
    that releases a prop and then holds nothing is said to be empty: "B's right hand is empty from 2.50", with "until
    <t>" when it grips again."""
    _, _, intervals = lifecycle(events_for(envelope))
    out = {}
    for c in _items(envelope, "nodes", "contacts"):
        entity, part, t = c["a"]["id"], c["body_part"], c["t"]
        if c["contact_type"] != "release" or part not in HANDS or entity not in labels or not any(
                pair[:2] == (entity, part) and pair[3] == c["b"]["id"] and kind == "possess" and end is not None
                and abs(end - t) <= EPSILON for pair, kind, start, end in intervals):
            continue
        grips = [(start, end) for pair, kind, start, end in intervals if pair[:2] == (entity, part) and kind == "possess"]
        if any(start <= t + EPSILON and (end is None or end > t + EPSILON) for start, end in grips):
            continue  # the hand still holds something else
        later = [start for start, _ in grips if start > t + EPSILON]
        out[c["id"]] = (f"{labels[entity]}'s {part.split('_')[0]} hand is empty from {_time(t)}"
                        + (f" until {_time(min(later))}" if later else ""))
    return out


def turn_runs(envelope, labels):
    """W3 (owner O47; probes R13 vs R18: an angle list gave two flips, plain words one): consecutive lines of one
    performer whose keys declare the same turn in the same direction are one turn, written once on its first line:
    'ONE backflip about the side-to-side axis (sagittal plane), 5.10–5.50; takeoff 4.70, landing 5.90'. The angles in
    between stay in the graph and in LBN-2.4. [{entity, slots, head, more}]: `more` is written on the run's later lines."""
    keys = {k["id"]: k for k in _items(envelope, "nodes", "motion")}
    support = {k["id"]: k["support"] for k in _items(envelope, "nodes", "kinematic")}
    by_entity = {}
    for slot in sorted(slots(envelope), key=lambda s: (s["t"], labels[s["entity"]])):
        by_entity.setdefault(slot["entity"], []).append(slot)
    runs = []
    for entity, own in by_entity.items():
        current = None
        for i, slot in enumerate(own):
            key = keys[slot["slot"]]
            following = keys[own[i + 1]["slot"]] if i + 1 < len(own) else None
            if key.get("turn", "none") == "none":
                current = None
                continue
            axis, _, sides = staff_geometry.TURNS[key["turn"]]
            delta = following["rot"][axis] - key["rot"][axis] if following else 0.0
            side = sides[0] if delta >= 0 else sides[1]
            if current is not None and (current["turn"], current["side"]) == (key["turn"], side):
                current["slots"].append(slot["slot"])
            else:
                current = {"entity": entity, "turn": key["turn"], "side": side, "index": i, "total": 0.0,
                           "slots": [slot["slot"]]}
                runs.append(current)
            current["total"] += abs(delta)
            current["end"] = following["t"] if following else None
        for run in (r for r in runs if r["entity"] == entity):
            run.update(_turn_text(run, own, keys, support))
    return runs


def _turn_text(run, own, keys, support):
    axis, sides = TURN_TEXT[run["turn"]]
    noun, tail, verb = sides[run["side"]]
    start = keys[own[run["index"]]["slot"]]["t"]
    count = round(run["total"] / 360)
    whole = count >= 1 and abs(run["total"] - 360 * count) <= FULL_TURN_SLACK
    if run["end"] is None:
        head = f"{verb} about the {axis} from {_time(start)} to the end"
    elif whole:
        head = f"{NUMBERS[count]} {noun}{'s' if count > 1 else ''}{tail} about the {axis}, {_time(start)}–{_time(run['end'])}"
    else:
        head = f"{verb} {round(run['total'])} degrees about the {axis}, {_time(start)}–{_time(run['end'])}"
    span = range(run["index"], run["index"] + len(run["slots"]))
    i = next((j for j in span if not support[own[j]["slot"]]), None)  # the first airborne line of the turn
    if i is not None:
        first = i
        while first > 0 and not support[own[first - 1]["slot"]]:
            first -= 1
        last = i
        while last < len(own) and not support[own[last]["slot"]]:
            last += 1
        took = keys[own[first]["slot"]]["t"]
        head += f"; {'takeoff' if first > 0 else 'airborne from'} {_time(took)}, " + (
            f"landing {_time(keys[own[last]['slot']]['t'])}" if last < len(own) else "no landing before the end")
    return {"head": head, "more": f"continues the {noun if whole else 'turn'} begun at {_time(start)}"}


CLOSE = ("insert", "close")


def hit_holds(envelope, frame_parts, labels):
    """W1 (owner O47; probes R10, R11, R14 stretched every hold or freeze given in frames to 0.85-1.75 s; R15 held a hit
    as V5 wrote it): an S17 hold on an impact frame is printed as the camera holding the hit with the bodies in frame,
    never as a body freeze in frames, and only where the shot covering it frames two or more bodies (or the only one)
    without a close-up; holds elsewhere stay in the graph and in LBN-2.4."""
    tolerance = 0.5 / envelope["scene"]["fps"] + 1e-9
    entities = [e["id"] for e in _items(envelope, "nodes", "entities")]
    out = []
    for hold in frame_parts["holds"]:
        t = hold["t"]
        if not any(abs(t - i) <= tolerance for i in frame_parts["impact"]):
            continue
        shot = next((s for s in _items(envelope, "nodes", "camera") if s["t"] - tolerance <= t < s["t"] + s["dur"] - tolerance),
                    None)
        if shot is None or any(word in shot["framing"]["scale"] for word in CLOSE):
            continue
        bodies = [labels[x] for x in shot["framing"]["subjects"] if x in labels]
        if len(bodies) >= 2:
            who = (f"{'BOTH' if len(bodies) == 2 else 'ALL ' + NUMBERS[len(bodies)]} bodies in frame "
                   f"({', '.join(bodies[:-1])} and {bodies[-1]})")
        elif len(bodies) == 1 and len(entities) == 1:
            who = f"the whole body in frame ({bodies[0]})"
        else:
            continue
        out.append(f"{_time(t)} impact: hold with {who}, no close-up")
    return out


def _supports(envelope, labels):
    """(entity, body part) -> list of (start, end, what it rests on) for support contacts (S07 lifecycle)."""
    _, _, intervals = lifecycle(events_for(envelope))
    spans = {}
    for (entity, part, _, target, _), contact_type, start, end in intervals:
        if contact_type == "support":
            spans.setdefault((entity, part), []).append((start, end, labels.get(target, target)))
    return spans


def _surface_at(spans, entity, part, t):
    for start, end, target in spans.get((entity, part), []):
        if start <= t + EPSILON and (end is None or t < end - EPSILON):
            return target
    return "ground"


def _travel(slot, following):
    """Travel to the performer's next line, relative to its facing: (direction word, metres) and the height change."""
    if following is None or slot["pos"] is None or following["pos"] is None or slot["facing"] is None:
        return None, 0.0
    dx, dy, dz = (b - a for a, b in zip(slot["pos"], following["pos"], strict=True))
    fx, _, fz = slot["facing"]
    length = (fx * fx + fz * fz) ** 0.5 or 1.0
    fx, fz = fx / length, fz / length
    forward, left = dx * fx + dz * fz, dx * fz - dz * fx
    flat = (forward * forward + left * left) ** 0.5
    horizontal = None
    if flat >= TRAVEL_M:
        horizontal = (staff_geometry.direction_word((left, 0.0, forward)).rsplit("-", 1)[0], flat)
    return horizontal, (dy if abs(dy) >= TRAVEL_M else 0.0)


def _path(horizontal, rise):
    parts = ([f"{horizontal[0]} {horizontal[1]:.1f} m"] if horizontal else []) + (
        [f"{'rising' if rise > 0 else 'dropping'} {abs(rise):.1f} m"] if rise else [])
    return "path: " + ", ".join(parts) if parts else None


def _numbers(values):
    return "[" + ", ".join(str(_num(v)) for v in values) + "]"


def strike_contacts(envelope, impacts):
    """{contact id}: the strikes. A strike is a touch in a beat that holds an S17 impact frame, on anything but a prop
    the performer holds (touching your own held prop is handling, e.g. a throw, not a hit). Shared by the staff's
    DOUBLE BOW and IMPACT_CONTACT_SYNC (S17 and the prompt)."""
    tolerance = 0.5 / envelope["scene"]["fps"] + 1e-9
    beats = {b["id"]: b for b in _items(envelope, "nodes", "beats")}
    holders = {s["id"]: s["conditions"].get("holder") for s in _items(envelope, "nodes", "states")}
    out = set()
    for c in _items(envelope, "nodes", "contacts"):
        beat = beats.get(c["beat"])
        if beat is None or c["contact_type"] != "touch" or holders.get(f"{c['b']['id']}@{c['beat']}") == c["a"]["id"]:
            continue
        if any(beat["t"] - tolerance <= t <= beat["t"] + beat["dur"] + tolerance for t in impacts):
            out.add(c["id"])
    return out


def staff_lines(envelope, frame_parts, labels):
    """One line per slot with the facts the modes need: text without Euler blocks, strike flag, the key."""
    keys = {k["id"]: k for k in _items(envelope, "nodes", "motion")}
    kinematic = {k["id"]: k for k in _items(envelope, "nodes", "kinematic")}
    bartenieff = {b["id"]: b for b in _items(envelope, "nodes", "bartenieff")}
    facial = {f["id"]: f for f in _items(envelope, "nodes", "facial")}
    names = {p["id"]: p["name"] for p in _items(envelope, "nodes", "props")}
    contacts = _items(envelope, "nodes", "contacts")
    strikes = strike_contacts(envelope, frame_parts["impact"])
    spans = _supports(envelope, labels)
    empty = empty_hands(envelope, labels)
    runs = turn_runs(envelope, labels)
    heads = {r["slots"][0]: r["head"] for r in runs}
    mids = {s: r["more"] for r in runs for s in r["slots"][1:]}
    ordered = sorted(slots(envelope), key=lambda s: (s["t"], labels[s["entity"]]))
    by_entity = {}
    for slot in ordered:
        by_entity.setdefault(slot["entity"], []).append(slot)
    lines = []
    for slot in ordered:
        entity, own = slot["entity"], by_entity[slot["entity"]]
        index = own.index(slot)
        following = own[index + 1] if index + 1 < len(own) else None
        key, kin = keys[slot["slot"]], kinematic[slot["slot"]]
        words = staff_geometry.pose_words(key)
        folds = {side: staff_geometry.bend_degrees(key["bones"][j]) for side, j in (("left", "LL"), ("right", "RL"))}
        surfaces = {part: _surface_at(spans, entity, part, slot["t"]) for part in kin["support"]}
        support = staff_geometry.support_words(kin["support"], posture=slot["state"].get("posture"), knee_folds=folds,
                                               surfaces=surfaces)
        horizontal, rise = _travel(slot, following)
        grounded = [kin["support"]] + ([kinematic[following["slot"]]["support"]] if following else [])
        if horizontal and not rise and following and all(
                parts and all(p.endswith("_foot") for p in parts) for parts in grounded) and all(
                s == "ground" for s in surfaces.values()):
            support = {"words": f"steps {horizontal[0]} alternating", "tags": "[f:alt]"}
        relationship, strike = [], False
        for c in sorted((c for c in contacts if c["beat"] == slot["beat"] and c["a"]["id"] == entity),
                        key=lambda c: (c["t"], c["id"])):
            at = "" if abs(c["t"] - slot["t"]) < EPSILON else f" at {_time(c['t'])}"
            part, target = _part(c["body_part"]), _target(c["b"], labels, names)
            verb = f"{c['verb'].upper()} " if c.get("verb") else ""  # owner O22, plan F4.1: the combat verb
            if c["id"] in strikes:
                strike = True
                relationship.append(f"{verb}[DOUBLE BOW + accent: {part} > {target}{at}]")
            elif c["contact_type"] == "touch":
                relationship.append(f"{verb}contact bow: {part} > {target}{at}")
            elif c["contact_type"] == "possess":
                relationship.append(f"{verb}[contact: {part}-{target} retained{at}]")
            elif c["contact_type"] == "release" and c["b"]["kind"] != "surface":
                relationship.append(f"{verb}[contact: {target} ENDS – released{at}]")
                if c["id"] in empty:
                    relationship.append(empty[c["id"]])
            elif c["contact_type"] == "support" and c["b"]["kind"] != "surface":
                relationship.append(f"support bow: {part} on {target}{at}")
        left = (f"L arm {words['left']['arm']}, lower arm {words['left']['lower_arm']}, L leg {words['left']['leg']}, "
                f"lower leg {words['left']['lower_leg']}")
        left += f", body {words['body']}" if words["body"] else ""
        left += f", head {words['head']}" if words["head"] else ""
        right = (f"R arm {words['right']['arm']}, lower arm {words['right']['lower_arm']}, R leg {words['right']['leg']}, "
                 f"lower leg {words['right']['lower_leg']}")
        notes = [n for n in (_path(horizontal, rise), heads.get(slot["slot"]) or mids.get(slot["slot"])) if n]
        if strike:
            b = bartenieff[slot["slot"]]
            notes.append(f"chain {_words(b['initiation'])} > {' > '.join(_words(p) for p in b['follow_through'])}")
        if slot["role"] == "actor":
            notes.append(slot["action"].rstrip("."))
        if slot["role"] == "actor" and slot["event_type"] == "substitution":
            notes.append("SUBSTITUTION: the decoy takes this place and the body reappears at its next line (teleport "
                         "allowed here only)")
        if slot["slot"] in facial:
            notes.append(_face_words(facial[slot["slot"]], labels))
        if following is None:
            notes.append("hold sign to the end")
        text = (f"{_time(slot['t'])} {labels[entity]}: SUPPORT {support['words']}"
                f"{' ' + support['tags'] if support['tags'] else ''} | {left} | {right} | "
                f"{'; '.join(relationship) or '-'} | {'; '.join(notes) or '-'}")
        lines.append({"text": text, "strike": strike, "key": key, "entity": entity, "kin": kin,
                      "first": index == 0, "last": following is None, "mid_turn": slot["slot"] in mids})
    return lines


def _euler(line, mode):
    key = line["key"]
    # W3: inside a turn the root's angles would read as an angle list (R13); the run is named on its first line
    root = f"Root {_numbers(key['pos'])} EulerXYZ " + ("mid-turn" if line["mid_turn"] else _numbers(key["rot"]))
    joints = "Joints {" + ", ".join(f"{j}: {_numbers(key['bones'][j])}" for j in JOINTS) + "}"
    if mode == "euler_heavy":
        return f" · {root} · {joints}"
    if mode == "upgraded_mixed" and (line["strike"] or line["last"]):
        return f" · {root} · {joints}"
    if mode == "mixed" and (line["strike"] or line["first"] or line["last"]):
        return f" · {root}"
    return ""


def _movement_language(mode, rows, verbs=False):
    lines = [
        f"Labanotation written as words. Mode: {MODES[mode][1]}.",
        "Each line = one measure for one performer; time in seconds; a symbol lasts until the next line.",
        "SUPPORT names what bears the weight; NO SUPPORT = airborne.",
        "Contact bow = touch; [contact: X-Y retained] = held; [contact: Y ENDS – released] = let go; "
        "DOUBLE BOW + accent = a strike (interp.: a momentary contact with a strong accent).",
        "Directions are relative to the performer's front: forward, back, left, right and the diagonals between them; "
        "levels high, mid, low; place-high / place-low = straight up / down. A limb reads mid while within 45 degrees "
        "of horizontal (interp.). Lower arm and lower leg: straight, or folded by degrees.",
        "Turns name the axis and the plane: a flip turns about the side-to-side axis (sagittal plane), a spin about the "
        "vertical axis (transverse plane), a cartwheel about the front-to-back axis (frontal plane); each turn is written "
        "once, on the line where it starts, with its count.",
        "Precision tags: [f:L|R|both] feet, [h:L|R|both] hands, [f:alt] stepping, _on_<surface> when the support is "
        "not the ground.",
        "Explicit = the written lines (every support change, contact and accent has one); implied = everything "
        "between lines.",
    ]
    if mode != "pure_staff":
        lines.append("Root [x, y, z] is the scene position in metres; EulerXYZ and joints are degrees.")
    if mode in ("upgraded_mixed", "euler_heavy"):
        lines.append("Skeleton key: " + " ".join(t for s, t, _, _ in rows if s == "key"))
    if verbs:  # owner O22: only prompts whose contacts carry a combat verb
        lines.append("A word in capitals before a bow or contact (THROW, DEFLECT, STRIKE ...) names the combat action it "
                     "performs; the Effort below stays Laban.")
    lines.append("FORMAT: TIME PERFORMER: SUPPORT [precision tags] | LEFT | RIGHT | relationship | path/notes")
    return "[MOVEMENT LANGUAGE]\n" + "\n".join(lines)


def _held_at_end(envelope, entity):
    ends = [s for s in _items(envelope, "nodes", "states") if s["id"].endswith("@end") and s["subject"]["kind"] == "prop"]
    names = {p["id"]: p["name"] for p in _items(envelope, "nodes", "props")}
    return [names.get(s["subject"]["id"], s["subject"]["id"]) for s in ends if s["conditions"].get("holder") == entity]


def _gaps(lines, labels):
    """(label, t0, t1) between consecutive lines of each performer."""
    times = {}
    for line in lines:
        times.setdefault(labels[line["entity"]], []).append(line["key"]["t"])
    return [(label, a, b) for label, ts in sorted(times.items()) for a, b in zip(ts, ts[1:], strict=False)]


def _render_intent(envelope, frame_parts, lines, labels):
    scene = envelope["scene"]
    efforts = _items(envelope, "nodes", "efforts")

    def share(field, value):
        return sum(e["effort"][field] == value for e in efforts) / max(1, len(efforts))

    speed = "fast" if share("time", "sudden") >= 0.5 else "measured" if share("time", "sustained") >= 0.5 else "mixed"
    weight = "strong, heavy" if share("weight", "strong") >= 0.5 else "light" if share("weight", "light") >= 0.5 else (
        "mixed")
    accel = ("sudden accelerations into the accents" if any(e["effort"]["time"] == "sudden" for e in efforts)
             else "smooth, sustained acceleration")
    shots = _items(envelope, "nodes", "camera")
    every = f"one shot every {scene['duration_s'] / max(1, len(shots)):.1f} s on average"
    style = GENRES.get(scene["genre"], scene["genre"]) + (f", in the spirit of {scene['style_reference']}"
                                                          if scene.get("style_reference") else "")
    gaps = [b - a for _, a, b in _gaps(lines, labels)]
    spacing = (f"{sum(g < 0.6 for g in gaps)} dense, {sum(0.6 <= g <= 0.9 for g in gaps)} medium and "
               f"{sum(g > 0.9 for g in gaps)} sparse gaps between lines") if gaps else "one line per performer"
    finals = []
    for label in sorted({labels[line["entity"]] for line in lines}):
        last = [line for line in lines if labels[line["entity"]] == label][-1]
        finals.append(f"{label} {_words(last['key']['name'])}")
    return (f"Render intent. Motion: {speed}, {weight}, {accel}; readable at {every}. Animation: {style}; spacing: "
            f"{spacing}; {len(frame_parts['smear'])} smears on declared limbs or props, {len(frame_parts['impact'])} impact "
            f"frames. Choreography: every effect follows its cause along the causal links; final instruction: end on "
            f"{', '.join(finals)}.")


def first_states(envelope, labels):
    """{prop id: [phrase]}: each prop at the first beat, from S06 and S07 (M8.12, PROP_FIRST_STATE): who holds it with
    which part, where it rests, or who carries it (S02 carried_by, O63) when it is neither held nor anywhere known, and
    each card state with the time it first changes ('line coiled until 8.00')."""
    states = _items(envelope, "nodes", "states")
    ends = {b["id"]: round(b["t"] + b["dur"], 6) for b in _items(envelope, "nodes", "beats")}
    caused = {e["to_state"]: max(ends[b] for b in e["trigger_event"])
              for e in _items(envelope, "edges", "state_transition") if e["trigger_event"]}
    out = {}
    for prop in _items(envelope, "nodes", "props"):
        own = sorted((s for s in states if s["subject"] == {"kind": "prop", "id": prop["id"]}), key=lambda s: (s["t"], s["id"]))
        if not own:
            out[prop["id"]] = ["state unknown"]
            continue
        start, phrases = own[0], []
        holders = [c for c in _items(envelope, "nodes", "contacts") if c["b"]["kind"] == "prop"
                   and c["b"]["id"] == prop["id"] and c["contact_type"] == "possess" and c["t"] <= start["t"] + 1e-9]
        phrases += [f"held by {labels.get(c['a']['id'], c['a']['id'])} {_part(c['body_part'])}" for c in holders]
        location = start["conditions"].get("location", "unknown")
        if location != "unknown" and not holders:
            phrases.append(f"on the {_words(location)}")
        elif location == "unknown" and not holders and prop.get("carried_by") in labels:
            # Interpretation (Claude's, for owner review): a prop with no holder and no known place at the start is gear on
            # its carrier's body (S02 carried_by, O63), so the prompt says where it is (W4).
            phrases.append(f"carried by {labels[prop['carried_by']]}")
        for key, value in sorted(start["conditions"].items()):
            if key in ("holder", "location") or value == "unknown":
                continue
            change = next((s for s in own[1:] if s["conditions"].get(key) != value), None)
            phrases.append(f"{key} {_words(str(value))}" + (f" until {_time(caused.get(change['id'], change['t']))}"
                                                            if change else ""))
        out[prop["id"]] = phrases or ["state unknown"]
    return out


def _scene(envelope, frame_parts, lines, labels, rows):
    scene = envelope["scene"]
    entities = _items(envelope, "nodes", "entities")
    props = _items(envelope, "nodes", "props")
    out = [envelope["provenance"]["source_prompt"].strip(),
           f"{_num(scene['duration_s'])} s {GENRES.get(scene['genre'], scene['genre'])} scene, {_num(scene['fps'])} fps,"
           f" setting: {scene.get('setting') or _words(scene.get('world') or 'unspecified')}."]
    cast = [f"{labels[e['id']]} = {e['name']}: {e['silhouette'].rstrip('.')}; {e['costume'].rstrip('.')}." for e in entities]
    out.append("Cast: " + " ".join(cast))
    first = first_states(envelope, labels)
    out.append("Props at the start: " + ("; ".join(
        f"{p['name']} (" + ", ".join(([f"{p['count']} {p['unit_name']}"] if p.get("count", 1) > 1 else [])
                                     + first[p["id"]]) + ")" for p in props) if props else "none") + ".")
    out.append(_render_intent(envelope, frame_parts, lines, labels))
    for text in (t for s, t, _, _ in rows if s == "preface"):
        if text not in out[0]:
            out.append(text.rstrip(".") + ".")
    return "[SCENE]\n" + "\n".join(out)


def _active(effort):
    return ", ".join(f"{effort['effort'][f]} {f}" for f in ("weight", "time", "space", "flow")
                     if effort["effort"][f] != "latent") or "latent effort"


def _implied(envelope, lines, labels):
    duration = envelope["scene"]["duration_s"]
    out = ["Between lines every performer keeps the declared Effort below, preserves momentum and a clear weight "
           "transfer, and travels through space between positions."]
    for e in sorted(_items(envelope, "nodes", "efforts"), key=lambda e: (labels[e["actor"]], e["t"])):
        action = "" if e["effort_action"] == "none" else f" ({LABAN_WORDS.get(e['effort_action'], e['effort_action'])} quality)"
        out.append(f"{labels[e['actor']]} {_time(e['t'])}–{_time(e['end'])}: maintain {_active(e)}{action}; shape "
                   f"{e['shape']['quality']}, {_words(e['shape']['mode'])}; {e['space']['kinesphere']} reach.")
    for entity in _items(envelope, "nodes", "entities"):
        text = f"{entity['silhouette']} {entity['costume']}".lower()
        loose = [g for g in LOOSE if g in text.replace(",", " ").replace(";", " ").replace(".", " ").split()]
        lag = " and ".join(loose) if loose else "hair and clothing"
        out.append(f"{labels[entity['id']]}: secondary motion of the {lag} lags the body slightly.")
    by_label = {}
    for line in lines:
        by_label.setdefault(labels[line["entity"]], []).append(line)
    for label, own in sorted(by_label.items()):
        for line in own:
            if line["strike"]:
                out.append(f"{label} after the {_time(line['key']['t'])} strike: one instant contact, the limb does not stay "
                           f"on the target (R16), then a short natural recovery before the next phrase.")
        span = None
        for i, line in enumerate(own + [None]):
            airborne = line is not None and " SUPPORT NO SUPPORT " in line["text"]
            if airborne and span is None:
                span = (line["key"]["t"], i > 0)
            elif not airborne and span is not None:
                end = f"the landing at {_time(line['key']['t'])}" if line else "the end of the scene"
                start = f"the takeoff at {_time(span[0])}" if span[1] else f"airborne from {_time(span[0])}"
                out.append(f"{label} airborne {_time(span[0])}–{_time(line['key']['t'] if line else duration)}: a "
                           f"realistic trajectory and rotation from {start} to {end}.")
                span = None
        for a, b in zip(own, own[1:] + [None], strict=False):
            t0, t1 = a["key"]["t"], b["key"]["t"] if b else duration
            if t1 - t0 > GAP_S + EPSILON:
                kin = a["kin"]
                what = "hold the final pose with micro-motion" if b is None else f"carry '{_words(a['key']['name'])}' through"
                out.append(f"{label} {_time(t0)}–{_time(t1)} ({t1 - t0:.1f} s without a line): {what}; weight transfer "
                           f"{kin['weight_transfer']}, breathing {kin['breathing']}, tension {kin['tension']}.")
    return "[IMPLIED GUIDANCE]\n" + "\n".join(f"- {line}" for line in out)


def _motion_control(lines, labels):
    gaps = _gaps(lines, labels)
    sizes = [b - a for _, a, b in gaps]
    text = ["Interpolation: slerp joint rotations between lines; the root follows its derived path between positions; "
            "support and the declared Effort hold at all times."]
    if gaps:
        label, a, b = max(gaps, key=lambda g: (g[2] - g[1], g[0]))
        text.append(f"Density (measured): {sum(g < 0.6 for g in sizes)} dense gaps under 0.6 s, "
                    f"{sum(0.6 <= g <= 0.9 for g in sizes)} medium from 0.6 to 0.9 s, {sum(g > 0.9 for g in sizes)} sparse "
                    f"over 0.9 s; the longest is {b - a:.2f} s ({label} {_time(a)}–{_time(b)}).")
    text.append("Explicit = the staff lines; implied = everything between them (IMPLIED GUIDANCE).")
    return "[MOTION CONTROL]\n" + "\n".join(text)


def _spatial(envelope, lines, labels, rows):
    scene = envelope["scene"]
    c = scene["ax"]["rotation_convention"]
    out = [f"Frame: up {scene['ax']['up']}, forward {scene['ax']['forward']}, ground {scene['ax']['ground']}, units "
           f"{scene['ax'].get('unit', 'm')}; Euler {c['euler_order']} {c['kind']}, {c['handedness']}-handed, {c['units']}; "
           f"+X = the performer's left; joints local to their parent (root -> Sp -> arms, NK -> HD; root -> legs), "
           f"root in the scene frame.",
           "Axes: " + ", ".join(t for s, t, _, _ in rows if s == "ax") + "."]
    for surface in _items(envelope, "nodes", "surfaces"):
        out.append(f"{_words(surface['id'])} ({surface['kind']}): {surface['description'].rstrip('.')}"
                   f"{'; ' + surface['ax'] if surface.get('ax') else ''}; solid.")
    firsts = {}
    for line in lines:
        firsts.setdefault(line["entity"], line)
    for entity, line in firsts.items():
        out.append(f"{labels[entity]} starts at {_numbers(line['key']['pos'])}.")
    positions = [line["key"]["pos"] for line in lines]
    if positions:
        ys, zs = [p[1] for p in positions], [p[2] for p in positions]
        out.append(f"Height used: y {_num(min(ys))} to {_num(max(ys))} m; depth used: z {_num(min(zs))} to {_num(max(zs))} m.")
    return "[SPATIAL ANCHORS]\n" + "\n".join(out)


def _props(envelope, labels):
    blocks = []
    states = _items(envelope, "nodes", "states")
    ends = {b["id"]: round(b["t"] + b["dur"], 6) for b in _items(envelope, "nodes", "beats")}
    caused = {e["to_state"]: max(ends[b] for b in e["trigger_event"])
              for e in _items(envelope, "edges", "state_transition") if e["trigger_event"]}

    def who(value):
        return labels.get(value, _words(str(value)))

    lines_of = line_links(envelope, labels)
    for prop in _items(envelope, "nodes", "props"):
        own = sorted((s for s in states if s["subject"] == {"kind": "prop", "id": prop["id"]}), key=lambda s: (s["t"], s["id"]))
        rows, previous = [], None
        for snap in own:
            if previous is None:
                known = [f"{k} {who(v)}" for k, v in sorted(snap["conditions"].items()) if v != "unknown"]
                rows.append((snap["t"], f"{_time(snap['t'])} " + (", ".join(known) or "state unknown")))
            else:
                changes = [f"{k} {who(previous['conditions'].get(k))} -> {who(v)}"
                           for k, v in sorted(snap["conditions"].items()) if previous["conditions"].get(k) != v]
                if changes:
                    t = caused.get(snap["id"], snap["t"])
                    rows.append((t, f"{_time(t)} " + ", ".join(changes)))
            previous = snap
        for c in _items(envelope, "nodes", "contacts"):
            if c["b"]["kind"] == "prop" and c["b"]["id"] == prop["id"]:
                verb = {"possess": "held by", "release": "released by", "touch": "touched by", "support": "supports"}
                rows.append((c["t"], f"{_time(c['t'])} {verb[c['contact_type']]} {who(c['a']['id'])} {_part(c['body_part'])}"))
        rows += prop_samples.rows(envelope, labels, prop["id"], compact=False)  # owner O8: p and v
        rows += lines_of.get(prop["id"], [])
        count = prop.get("count", 1)
        lines = [" · ".join(text for _, text in sorted(rows, key=lambda r: r[0]))]
        lines.append(prop_samples.where_line(prop_samples.track(envelope, labels, prop["id"])))  # plan F2.1, F6.1, F6.2
        lines.append((f"ONE {prop['name']} only" if count == 1 else f"Exactly {count} {prop['unit_name']} in the "
                      f"{prop['group_name']}") + ": never duplicated, never in two hands at once, never lost.")
        holders = {s["conditions"].get("holder") for s in own}
        if len(holders) == 1 and next(iter(holders)) in labels:
            lines.append(f"CUSTODY: {labels[next(iter(holders))]}.{prop['name']} (it never changes hands).")
        blocks.append(f"[PROP STATE MACHINE – {prop['name']}]\n" + "\n".join(lines))
    return blocks


def _causal(envelope, labels):
    edges = _items(envelope, "edges", "causal")
    beats = {b["id"]: b for b in _items(envelope, "nodes", "beats")}
    outgoing = {e["from"]: e for e in edges}
    incoming = {e["to"] for e in edges}

    def name(beat_id):
        beat = beats[beat_id]
        return f"{labels.get(beat['actor'], beat['actor'])} {_words(beat['label'])}"

    threads = []
    for start in sorted((b for b in outgoing if b not in incoming), key=lambda b: (beats[b]["t"], b)):
        parts, current = [name(start)], start
        while current in outgoing:
            edge = outgoing[current]
            parts.append(("→ " if edge["causal_strength"] == "hard" else "⇢ ") + name(edge["to"]))
            current = edge["to"]
        threads.append(" ".join(parts))
    legend = "→ hard cause (the effect starts after the cause ends); ⇢ soft cause (it may start while the cause runs)."
    reasons = [f"{name(e['from'])} {'→' if e['causal_strength'] == 'hard' else '⇢'} {name(e['to'])}: {e['why']}"
               for e in sorted(edges, key=lambda e: (beats[e["from"]]["t"], e["from"]))]
    return "[CAUSAL LINKS]\n" + "\n".join([legend] + (threads or ["none: the beats are independent."])
                                          + (["Why each link holds:"] + reasons if reasons else []))


def _camera(envelope, frame_parts, labels):
    beats = {b["id"]: b for b in _items(envelope, "nodes", "beats")}

    def name(identifier):
        return labels.get(identifier, _words(identifier))

    out = []
    for s in _items(envelope, "nodes", "camera"):
        f, a, lens, mv, pb = s["framing"], s["angle"], s["lens"], s["movement"], s["playback"]
        cross = " across the axis" if s["editing"]["axis"] == "cross" else ""
        shows = ", ".join(f"{labels.get(beats[b]['actor'], beats[b]['actor'])} {_words(beats[b]['label'])}" for b in s["beats"])
        detail = ((" of " if f["scale"] == "insert" else " with an insert of ") + _words(f["detail"])) if f["detail"] else ""
        out.append(f"{_time(s['t'])}–{_time(s['t'] + s['dur'])} {s['editing']['transition_in']}{cross} to {f['scale']}"
                   f"{detail} on {', '.join(name(x) for x in f['subjects'])}: "
                   f"{f['visible_action'].rstrip('.')}; elevation {_num(a['elevation_deg'])}, azimuth "
                   f"{_num(a['azimuth_deg'])}, roll {_num(a['roll_deg'])}; {_num(lens['focal_length_mm'])} mm "
                   f"{lens['perspective']}; {mv['kind']}: {mv['path'].rstrip('.')}; {pb['treatment']} x{_num(pb['speed'])}; "
                   f"shows {shows}; motivated by {_words(s['motivation']['kind'])} {name(s['motivation']['ref'])}.")
    card = camera_library.convention(envelope["scene"]["genre"])
    rules = [c["statement"] for c in card["conventions"]] + [
        f"Shots last {_num(card['shot_duration_s'][0])}-{_num(card['shot_duration_s'][1])} s.",
        "Crossing the action axis is " + ("allowed when a cut declares it." if card["cross_line"] == "allowed"
                                          else "never allowed.")]
    holds = hit_holds(envelope, frame_parts, labels)
    return "[CAMERA]\n" + "\n".join(out + (["Holds on hits: " + "; ".join(holds) + "."] if holds else [])
                                     + ["Camera rules: " + " ".join(rules)])


class _Unseen:
    def mark(self, group, identity):
        pass


def _genre_block(envelope, frame_parts, labels):
    title = GENRE_BLOCKS.get(envelope["scene"]["genre"], envelope["scene"]["genre"].upper())

    def who(identifier):
        return labels.get(identifier, _words(identifier))

    def span(item):
        return f"{_time(item['t0'])}–{_time(item['t1'])}"

    out = ["Impact frames: " + (", ".join(_time(t) for t in frame_parts["impact"]) or "none") + ".",
           "Smears, only on the declared limb or prop (the body does not smear): " + ("; ".join(
               f"{span(x)} {who(x['subject'])}{' ' + _words(x['part']) if x['part'] else ''}, {x['note']}"
               for x in frame_parts["smear"]) or "none") + ".",
           "Speedlines: " + ("; ".join(f"{span(x)} {who(x['subject'])}" for x in frame_parts["speedlines"]) or "none") + ".",
           "FX: " + ("; ".join(f"{_time(x['t'])}{'–' + _time(x['t_end']) if x['t_end'] is not None else ''} {x['text']}"
                              for x in frame_parts["fx"]) or "none") + ".",
           f"Ink: {frame_parts['ink']}."]
    if envelope["scene"]["genre"] == "ugc_ad":
        ugc = ugc_renderer._ugc(envelope, frame_parts, labels, _Unseen())
        out += ["Hand roles: " + "; ".join(ugc["hand_roles"]) + ".",
                "Object states: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in sorted(ugc["object_states"].items())) + ".",
                "Affordances: " + "; ".join(ugc["affordances"]) + ".",
                "Enables: " + ("; ".join(ugc["enables"]) or "none") + "."]
    return f"[{title}]\n" + "\n".join(out)


def _lasting(envelope, labels):
    """Time-bounded rules (C13, T9): the last effect on a property, when its value is still the value at the end."""
    ends = {(s["subject"]["kind"], s["subject"]["id"]): s["conditions"] for s in _items(envelope, "nodes", "states")
            if s["id"].endswith("@end")}
    names = {p["id"]: p["name"] for p in _items(envelope, "nodes", "props")}
    last = {}
    for beat in sorted(_items(envelope, "nodes", "beats"), key=lambda b: (b["t"] + b["dur"], b["t"], b["id"])):
        for effect in beat["effects"]:
            last[(effect["subject"]["kind"], effect["subject"]["id"], effect["property"])] = (beat, effect["value"])
    rules = []
    for (kind, identity, prop), (beat, value) in sorted(last.items(), key=lambda kv: (kv[1][0]["t"] + kv[1][0]["dur"],
                                                                                         kv[0])):
        if (value == "unknown" or ends.get((kind, identity), {}).get(prop) != value
                or beat["t"] + beat["dur"] >= envelope["scene"]["duration_s"] - EPSILON):
            continue
        who = labels.get(identity) or names.get(identity) or _words(identity)
        shown = _words(labels.get(value, str(value)))
        keeps = f"stays {shown}" if shown == _words(prop) else f"keeps {_words(prop)} {shown}"
        rules.append(f"From {_time(beat['t'] + beat['dur'])} to the end, {who} {keeps}.")
    return rules


def _end_states(envelope, lines, labels):
    """C22: each performer's S06 end snapshot (position, support, posture, location, what it holds); when S06 does not
    know the support, the SUPPORT words of the performer's last staff line (S11)."""
    last = {line["entity"]: line for line in lines}
    rules = []
    for s in sorted((s for s in _items(envelope, "nodes", "states") if s["id"].endswith("@end")
                     and s["subject"]["kind"] == "entity" and s["subject"]["id"] in labels),
                    key=lambda s: labels[s["subject"]["id"]]):
        entity = s["subject"]["id"]
        known = [f"{_words(k)} {_words(labels.get(v, str(v)))}" for k, v in sorted(s["conditions"].items())
                 if v not in ("unknown", None) and k != "possession"]
        if s["conditions"].get("support", "unknown") == "unknown" and entity in last:
            known.append("support " + last[entity]["text"].split(" SUPPORT ", 1)[1].split(" | ", 1)[0].split(" [", 1)[0])
        held = _held_at_end(envelope, entity)
        where = f" at {_numbers(s['pos'])}" if s.get("pos") else ""
        rules.append(f"End state: {labels[entity]}{where}" + (", " + ", ".join(known) if known else "")
                     + (f", holding {', '.join(held)}" if held else "") + ".")
    return rules


def _spans(envelope, lines, labels):
    """C30: a support on anything but the ground held across two or more of the performer's lines."""
    _, _, intervals = lifecycle(events_for(envelope))
    duration = envelope["scene"]["duration_s"]
    times = {}
    for line in lines:
        times.setdefault(line["entity"], []).append(line["key"]["t"])
    rules = []
    for (entity, part, _, target, _), kind, start, end in intervals:
        if kind != "support" or target == "ground" or entity not in labels:
            continue
        stop = duration if end is None else end
        held = [t for t in times.get(entity, []) if start - EPSILON <= t < stop - EPSILON]
        if len(held) >= 2:
            rules.append(f"{labels[entity]} {_part(part)} stays on the {_words(labels.get(target, target))} from "
                         f"{_time(start)} to {_time(stop)}: one continuous contact, no relaunch in between.")
    return rules


def _separations(lines, labels):
    """C32: consecutive strikes by one performer stay two events."""
    rules, by_label = [], {}
    for line in lines:
        if line["strike"]:
            by_label.setdefault(labels[line["entity"]], []).append(line)

    def what(line):
        return line["text"].split("[DOUBLE BOW + accent: ", 1)[1].split("]", 1)[0]

    for label, strikes in sorted(by_label.items()):
        for a, b in zip(strikes, strikes[1:], strict=False):
            rules.append(f"TWO SEPARATE STRIKES: {label} {what(a)} and {what(b)}; do not merge them or swap the limbs.")
    return rules


def vanish_rules(envelope, labels):
    """One rule per substitution (owner O18, audit X9): the actor is gone until it reappears, with nothing in between."""
    out = []
    for actor, _, start, back in dynamic_beat_validator.vanish_windows(_items(envelope, "nodes", "beats")):
        who = labels.get(actor, actor)
        out.append(f"{who} is gone from {_time(start)} " + (f"until {who} reappears at {_time(back)}" if back is not None
                                                             else "to the end") + f" (substitution): no {who} body, pose or "
                   "support in between.")
    return out


def _rules(envelope, mode, rows, lines, labels):
    lead = ("Follow the SUPPORT column and the contact bows strictly; they are the movement authority."
            if mode == "pure_staff" else "Laban support and contacts are primary; Euler numbers are precision override only.")
    kept = []
    for section, text, _, ref in rows:
        if section == "rules" and ref != ROOT_EXACT and text not in kept:
            kept.append(text)
    rules = ([lead] + kept + list(CONSERVATION) + _lasting(envelope, labels) + _end_states(envelope, lines, labels)
             + _spans(envelope, lines, labels) + _separations(lines, labels) + vanish_rules(envelope, labels)
             + [entrance["rule"] for entrance in entrances(envelope, labels)] + hang_rules(envelope, labels))
    return "[RULES]\n" + "\n".join(f"- {r}" for r in rules)


def _negatives(rows, envelope=None, labels=None):
    kept = []
    for section, text, _, _ in rows:
        if section == "negative" and text not in kept:
            kept.append(text)
    kept += [entrance["negative"] for entrance in (entrances(envelope, labels) if envelope else [])]
    return "[NEGATIVES]\n" + "; ".join(kept)


def hang_rules(envelope, labels):
    """Owner O74 (plan F9.2): an anime span that floats is said to hang, once per span, takeoff to landing."""
    from compiler.passes.derived.p11_kinematic import float_spans

    nodes = {n["id"]: n for n in _items(envelope, "nodes", "kinematic")}
    view = {s["slot"]: s for s in slots(envelope) if s["slot"] in nodes}
    return [f"{labels[entity]} hangs in the air {_time(airborne[0]['t'])}–{_time(landing['t'])}, longer than a real jump "
            "(stylised anime hang time)." for entity, takeoff, airborne, landing in float_spans(nodes, view)
            if any(nodes[s["slot"]].get("float") for s in airborne)]


def entrances(envelope, labels):
    """Probe V6 (owner O51; R19 kept A off the pillar at the start): a performer whose first line is airborne and whose
    first support is its feet on a raised top drops in onto it. Interpretation (Claude's, for owner review): a raised
    top is a surface whose top (its world card's geometry) lies above the ground. [{label, rule, negative}]."""
    tops = dynamic_beat_validator.surface_tops(_items(envelope, "nodes", "surfaces"), envelope["scene"]["ax"].get("ground"))
    ground = tops.get("ground", 0.0)
    support = {k["id"]: k["support"] for k in _items(envelope, "nodes", "kinematic")}
    contacts = sorted(_items(envelope, "nodes", "contacts"), key=lambda c: (c["t"], c["id"]))
    out = []
    for entity in _items(envelope, "nodes", "entities"):
        own = sorted((s for s in slots(envelope) if s["entity"] == entity["id"]), key=lambda s: s["t"])
        first = next((c for c in contacts if c["contact_type"] == "support" and c["a"]["id"] == entity["id"]), None)
        if not own or support.get(own[0]["slot"]) or first is None or not first["body_part"].endswith("_foot") \
                or first["b"]["kind"] != "surface" or tops.get(first["b"]["id"], ground) <= ground:
            continue
        label, surface = labels[entity["id"]], _words(first["b"]["id"])
        out.append({"label": label, "negative": f"no {label} standing on the {surface} at the start",
                    "rule": f"{label} starts in the air above the {surface}, drops in feet first, and {label}'s feet "
                            f"touch the {surface} top at {_time(first['t'])}, not earlier."})
    return out


def render_all(envelope, frame_parts, labels):
    """The four prose prompts: {mode: {target, variant, text, sha256, omitted_constraints}}."""
    _, rows = constraint_rows(envelope, labels)
    omitted = sorted({cid for _, _, cid, ref in rows if ref == ROOT_EXACT})
    lines = staff_lines(envelope, frame_parts, labels)
    shared = {"scene": _scene(envelope, frame_parts, lines, labels, rows), "implied": _implied(envelope, lines, labels),
              "motion": _motion_control(lines, labels), "spatial": _spatial(envelope, lines, labels, rows),
              "props": _props(envelope, labels), "causal": _causal(envelope, labels),
              "camera": _camera(envelope, frame_parts, labels),
              "genre": _genre_block(envelope, frame_parts, labels), "negatives": _negatives(rows, envelope, labels)}
    result = {}
    for mode, (title, _) in MODES.items():
        staff = "\n".join(line["text"] + _euler(line, mode) for line in lines)
        verbs = any(c.get("verb") for c in _items(envelope, "nodes", "contacts"))
        blocks = [shared["scene"], _movement_language(mode, rows, verbs), f"[LABAN STAFF – {title}]\n{staff}", shared["implied"],
                  shared["motion"], shared["spatial"], *shared["props"], shared["causal"], shared["camera"],
                  shared["genre"], _rules(envelope, mode, rows, lines, labels), shared["negatives"]]
        text = "\n\n".join(blocks) + "\n"
        result[mode] = {"target": TARGET, "variant": f"DAG-PROSE-{title.replace(' ', '-')}", "text": text,
                        "sha256": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "omitted_constraints": omitted}
    return result
