"""S17 structured-prose prompts (M8; owner O1-O3): the knowledge DAG's Master Template in four movement modes.

Compiled alongside the LBN-2.4 prompt, which stays the uncompressed projection (no_render_compression). Derived only:
a pure function of the envelope and the S17 frame parts. Spec: docs/plans/M8_DAG_PROSE.md (Master Template C19, D8
wrapper, D9 blocks, FORMAT line L507, precision tags L522).

Sections (M8.2): [SCENE], [MOVEMENT LANGUAGE] + FORMAT, [LABAN STAFF – <MODE>], [RULES], [NEGATIVES]. Staff words come
from solver/staff_geometry.py; one line per slot (performer x beat). SUPPORT reads 'steps <direction> alternating'
only when this line and the next stand on the ground on feet with no height change between them. A strike is a touch
whose beat holds an S17 impact frame (contacts are stamped at their beat's end, impact frames where the hit reads), on
anything but a prop the performer holds (touching your own held prop is handling, e.g. a throw, not a hit).
Modes differ only in the Euler blocks:
pure staff none; Mixed root + EulerXYZ on strike lines and each performer's first and last line; Upgraded Mixed
root + EulerXYZ + joints on strike lines and each performer's last line; Euler-heavy everything on every line
(the key choice reads D6/D7/D10's instances; interpretation). The prose leaves out the kernel rule
'<label> root exact' (owner O3) and lists the constraints it leaves out.
"""

import hashlib

from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner.scene_view import slots
from renderers.anime_renderer import _face_words, _items, _num, constraint_rows
from solver import staff_geometry

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
EPSILON = 1e-6


def _words(identifier):
    return identifier.replace("_", " ")


def _part(part):
    side, _, name = part.partition("_")
    return f"{side[0].upper()} {name}" if side in ("left", "right") and name else _words(part)


def _target(end, labels, names):
    who = labels.get(end["id"]) or names.get(end["id"]) or _words(end["id"])
    return f"{who} {_words(end['part'])}" if end.get("part") else who


def _time(t):
    return f"{t:.2f}"


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


def staff_lines(envelope, frame_parts, labels):
    """One line per slot with the facts the modes need: text without Euler blocks, strike flag, the key."""
    keys = {k["id"]: k for k in _items(envelope, "nodes", "motion")}
    kinematic = {k["id"]: k for k in _items(envelope, "nodes", "kinematic")}
    bartenieff = {b["id"]: b for b in _items(envelope, "nodes", "bartenieff")}
    facial = {f["id"]: f for f in _items(envelope, "nodes", "facial")}
    names = {p["id"]: p["name"] for p in _items(envelope, "nodes", "props")}
    contacts = _items(envelope, "nodes", "contacts")
    holders = {s["id"]: s["conditions"].get("holder") for s in _items(envelope, "nodes", "states")}
    tolerance = 0.5 / envelope["scene"]["fps"] + 1e-9
    impacts = frame_parts["impact"]
    spans = _supports(envelope, labels)
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
            own_prop = holders.get(f"{c['b']['id']}@{slot['beat']}") == entity
            if c["contact_type"] == "touch" and not own_prop and any(
                    slot["t"] - tolerance <= t <= slot["t"] + slot["dur"] + tolerance for t in impacts):
                strike = True
                relationship.append(f"[DOUBLE BOW + accent: {part} > {target}{at}]")
            elif c["contact_type"] == "touch":
                relationship.append(f"contact bow: {part} > {target}{at}")
            elif c["contact_type"] == "possess":
                relationship.append(f"[contact: {part}-{target} retained{at}]")
            elif c["contact_type"] == "release" and c["b"]["kind"] != "surface":
                relationship.append(f"[contact: {target} ENDS – released{at}]")
            elif c["contact_type"] == "support" and c["b"]["kind"] != "surface":
                relationship.append(f"support bow: {part} on {target}{at}")
        left = (f"L arm {words['left']['arm']}, lower arm {words['left']['lower_arm']}, L leg {words['left']['leg']}, "
                f"lower leg {words['left']['lower_leg']}")
        left += f", body {words['body']}" if words["body"] else ""
        left += f", head {words['head']}" if words["head"] else ""
        right = (f"R arm {words['right']['arm']}, lower arm {words['right']['lower_arm']}, R leg {words['right']['leg']}, "
                 f"lower leg {words['right']['lower_leg']}")
        notes = [n for n in (_path(horizontal, rise),
                             staff_geometry.turn_words(key, keys[following["slot"]] if following else None)) if n]
        if strike:
            b = bartenieff[slot["slot"]]
            notes.append(f"chain {_words(b['initiation'])} > {' > '.join(_words(p) for p in b['follow_through'])}")
        if slot["role"] == "actor":
            notes.append(slot["action"].rstrip("."))
        if slot["slot"] in facial:
            notes.append(_face_words(facial[slot["slot"]], labels))
        if following is None:
            notes.append("hold sign to the end")
        text = (f"{_time(slot['t'])} {labels[entity]}: SUPPORT {support['words']}"
                f"{' ' + support['tags'] if support['tags'] else ''} | {left} | {right} | "
                f"{'; '.join(relationship) or '-'} | {'; '.join(notes) or '-'}")
        lines.append({"text": text, "strike": strike, "key": key, "entity": entity,
                      "first": index == 0, "last": following is None})
    return lines


def _euler(line, mode):
    key = line["key"]
    root = f"Root {_numbers(key['pos'])} EulerXYZ {_numbers(key['rot'])}"
    joints = "Joints {" + ", ".join(f"{j}: {_numbers(key['bones'][j])}" for j in JOINTS) + "}"
    if mode == "euler_heavy":
        return f" · {root} · {joints}"
    if mode == "upgraded_mixed" and (line["strike"] or line["last"]):
        return f" · {root} · {joints}"
    if mode == "mixed" and (line["strike"] or line["first"] or line["last"]):
        return f" · {root}"
    return ""


def _scene(envelope, labels, rows):
    scene = envelope["scene"]
    entities = _items(envelope, "nodes", "entities")
    props = _items(envelope, "nodes", "props")
    lines = [envelope["provenance"]["source_prompt"].strip(),
             f"{_num(scene['duration_s'])} s {GENRES.get(scene['genre'], scene['genre'])} scene, {_num(scene['fps'])} fps,"
             f" setting: {scene.get('setting') or _words(scene.get('world') or 'unspecified')}."]
    cast = [f"{labels[e['id']]} = {e['name']}: {e['silhouette'].rstrip('.')}; {e['costume'].rstrip('.')}." for e in entities]
    lines.append("Cast: " + " ".join(cast))
    if props:
        lines.append("Props: " + ", ".join(
            f"{p['name']}" + (f" ({p['count']} {p['unit_name']})" if p.get("count", 1) > 1 else "") for p in props) + ".")
    else:
        lines.append("Props: none.")
    frame = [text for section, text, _, _ in rows if section == "ax"]
    convention = scene["ax"]["rotation_convention"]
    frame.append(f"Euler {convention['euler_order']} {convention['kind']} {convention['handedness']}-handed "
                 f"{convention['units']}, +X performer's left")
    lines.append("Frame: " + ", ".join(frame) + ".")
    for text in (t for s, t, _, _ in rows if s == "preface"):
        if text not in lines[0]:
            lines.append(text.rstrip(".") + ".")
    return "[SCENE]\n" + "\n".join(lines)


def _movement_language(mode, rows):
    lines = [
        f"Labanotation written as words. Mode: {MODES[mode][1]}.",
        "Each line = one measure for one performer; time in seconds; a symbol lasts until the next line.",
        "SUPPORT names what bears the weight; NO SUPPORT = airborne.",
        "Contact bow = touch; [contact: X-Y retained] = held; [contact: Y ENDS – released] = let go; "
        "DOUBLE BOW + accent = a strike (interp.: a momentary contact with a strong accent).",
        "Directions are relative to the performer's front: forward, back, left, right and the diagonals between them; "
        "levels high, mid, low; place-high / place-low = straight up / down. A limb reads mid while within 45 degrees "
        "of horizontal (interp.). Lower arm and lower leg: straight, or folded by degrees.",
        "Turn signs name the axis: flip = lateral axis, turn = vertical axis, cartwheel = sagittal axis.",
        "Precision tags: [f:L|R|both] feet, [h:L|R|both] hands, [f:alt] stepping, _on_<surface> when the support is "
        "not the ground.",
        "Explicit = the written lines (every support change, contact and accent has one); implied = everything "
        "between lines.",
    ]
    if mode != "pure_staff":
        lines.append("Root [x, y, z] is the scene position in metres; EulerXYZ and joints are degrees.")
    if mode in ("upgraded_mixed", "euler_heavy"):
        lines.append("Skeleton key: " + " ".join(t for s, t, _, _ in rows if s == "key"))
    lines.append("FORMAT: TIME PERFORMER: SUPPORT [precision tags] | LEFT | RIGHT | relationship | path/notes")
    return "[MOVEMENT LANGUAGE]\n" + "\n".join(lines)


def _rules(mode, rows):
    lead = ("Follow the SUPPORT column and the contact bows strictly; they are the movement authority."
            if mode == "pure_staff" else "Laban support and contacts are primary; Euler numbers are precision override only.")
    kept = []
    for section, text, _, ref in rows:
        if section == "rules" and ref != ROOT_EXACT and text not in kept:
            kept.append(text)
    return "[RULES]\n" + "\n".join(f"- {r}" for r in [lead] + kept)


def _negatives(rows):
    kept = []
    for section, text, _, _ in rows:
        if section == "negative" and text not in kept:
            kept.append(text)
    return "[NEGATIVES]\n" + "; ".join(kept)


def render_all(envelope, frame_parts, labels):
    """The four prose prompts: {mode: {target, variant, text, sha256, omitted_constraints}}."""
    _, rows = constraint_rows(envelope, labels)
    omitted = sorted({cid for _, _, cid, ref in rows if ref == ROOT_EXACT})
    lines = staff_lines(envelope, frame_parts, labels)
    result = {}
    for mode, (title, _) in MODES.items():
        staff = "\n".join(line["text"] + _euler(line, mode) for line in lines)
        text = "\n\n".join([_scene(envelope, labels, rows), _movement_language(mode, rows),
                            f"[LABAN STAFF – {title}]\n{staff}", _rules(mode, rows), _negatives(rows)]) + "\n"
        result[mode] = {"target": TARGET, "variant": f"DAG-PROSE-{title.replace(' ', '-')}", "text": text,
                        "sha256": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "omitted_constraints": omitted}
    return result
