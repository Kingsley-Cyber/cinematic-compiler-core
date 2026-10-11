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
"""

import hashlib

from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner import camera_library
from planner.scene_view import slots
from renderers import ugc_renderer
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
GAP_S = 1.5  # C2: never more than 1.5 s without an explicit key or strong implied guidance
EPSILON = 1e-6
GENRE_BLOCKS = {"anime": "ANIME", "ugc_ad": "UGC", "live_action": "LIVE ACTION"}
LOOSE = ("scarf", "coat", "robe", "robes", "sleeves", "hem", "cape", "cloak", "hair", "hood", "hoodie", "skirt", "ribbon",
         "sash", "tassel", "trousers")
CONSERVATION = (  # T10, six of seven laws (PRESERVE_AXIS left out, P3.2-6); in the rules layer, not first (P3.2-7)
    "Identity is immutable: every performer and prop stays itself for the whole scene.",
    "Spatial continuity: a body travels through space between lines; no teleporting unless a rule declares a substitution.",
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
        lines.append({"text": text, "strike": strike, "key": key, "entity": entity, "kin": kin,
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


def _scene(envelope, frame_parts, lines, labels, rows):
    scene = envelope["scene"]
    entities = _items(envelope, "nodes", "entities")
    props = _items(envelope, "nodes", "props")
    out = [envelope["provenance"]["source_prompt"].strip(),
           f"{_num(scene['duration_s'])} s {GENRES.get(scene['genre'], scene['genre'])} scene, {_num(scene['fps'])} fps,"
           f" setting: {scene.get('setting') or _words(scene.get('world') or 'unspecified')}."]
    cast = [f"{labels[e['id']]} = {e['name']}: {e['silhouette'].rstrip('.')}; {e['costume'].rstrip('.')}." for e in entities]
    out.append("Cast: " + " ".join(cast))
    out.append("Props: " + (", ".join(f"{p['name']}" + (f" ({p['count']} {p['unit_name']})" if p.get("count", 1) > 1
                                                        else "") for p in props) if props else "none") + ".")
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
        action = "" if e["effort_action"] == "none" else f" ({e['effort_action']})"
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
                out.append(f"{label} after the {_time(line['key']['t'])} strike: a short natural recovery before the next "
                           f"phrase.")
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
        count = prop.get("count", 1)
        lines = [" · ".join(text for _, text in sorted(rows, key=lambda r: r[0]))]
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
    return "[CAUSAL LINKS]\n" + "\n".join([legend] + (threads or ["none: the beats are independent."]))


def _camera(envelope, labels):
    beats = {b["id"]: b for b in _items(envelope, "nodes", "beats")}

    def name(identifier):
        return labels.get(identifier, _words(identifier))

    out = []
    for s in _items(envelope, "nodes", "camera"):
        f, a, lens, mv, pb = s["framing"], s["angle"], s["lens"], s["movement"], s["playback"]
        cross = " across the axis" if s["editing"]["axis"] == "cross" else ""
        shows = ", ".join(f"{labels.get(beats[b]['actor'], beats[b]['actor'])} {_words(beats[b]['label'])}" for b in s["beats"])
        out.append(f"{_time(s['t'])}–{_time(s['t'] + s['dur'])} {s['editing']['transition_in']}{cross} to {f['scale']}"
                   f"{' insert on ' + f['detail'] if f['detail'] else ''} on {', '.join(name(x) for x in f['subjects'])}: "
                   f"{f['visible_action'].rstrip('.')}; elevation {_num(a['elevation_deg'])}, azimuth "
                   f"{_num(a['azimuth_deg'])}, roll {_num(a['roll_deg'])}; {_num(lens['focal_length_mm'])} mm "
                   f"{lens['perspective']}; {mv['kind']}: {mv['path'].rstrip('.')}; {pb['treatment']} x{_num(pb['speed'])}; "
                   f"shows {shows}; motivated by {_words(s['motivation']['kind'])} {name(s['motivation']['ref'])}.")
    card = camera_library.convention(envelope["scene"]["genre"])
    rules = [c["statement"] for c in card["conventions"]] + [
        f"Shots last {_num(card['shot_duration_s'][0])}-{_num(card['shot_duration_s'][1])} s.",
        "Crossing the action axis is " + ("allowed when a cut declares it." if card["cross_line"] == "allowed"
                                          else "never allowed.")]
    return "[CAMERA]\n" + "\n".join(out + ["Camera rules: " + " ".join(rules)])


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
           "Holds: " + ("; ".join(f"{_time(h['t'])} for {h['frames']} frames" for h in frame_parts["holds"]) or "none")
           + ".",
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


def _rules(envelope, mode, rows, lines, labels):
    lead = ("Follow the SUPPORT column and the contact bows strictly; they are the movement authority."
            if mode == "pure_staff" else "Laban support and contacts are primary; Euler numbers are precision override only.")
    kept = []
    for section, text, _, ref in rows:
        if section == "rules" and ref != ROOT_EXACT and text not in kept:
            kept.append(text)
    rules = ([lead] + kept + list(CONSERVATION) + _lasting(envelope, labels) + _end_states(envelope, lines, labels)
             + _spans(envelope, lines, labels) + _separations(lines, labels))
    return "[RULES]\n" + "\n".join(f"- {r}" for r in rules)


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
    shared = {"scene": _scene(envelope, frame_parts, lines, labels, rows), "implied": _implied(envelope, lines, labels),
              "motion": _motion_control(lines, labels), "spatial": _spatial(envelope, lines, labels, rows),
              "props": _props(envelope, labels), "causal": _causal(envelope, labels), "camera": _camera(envelope, labels),
              "genre": _genre_block(envelope, frame_parts, labels), "negatives": _negatives(rows)}
    result = {}
    for mode, (title, _) in MODES.items():
        staff = "\n".join(line["text"] + _euler(line, mode) for line in lines)
        blocks = [shared["scene"], _movement_language(mode, rows), f"[LABAN STAFF – {title}]\n{staff}", shared["implied"],
                  shared["motion"], shared["spatial"], *shared["props"], shared["causal"], shared["camera"],
                  shared["genre"], _rules(envelope, mode, rows, lines, labels), shared["negatives"]]
        text = "\n\n".join(blocks) + "\n"
        result[mode] = {"target": TARGET, "variant": f"DAG-PROSE-{title.replace(' ', '-')}", "text": text,
                        "sha256": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
                        "omitted_constraints": omitted}
    return result
