"""S13 checks on authored key poses (owner Q2, Q5, Q6).

- bones are exactly the kernel joints (names from the kernel `key` items, e.g. "LUL/RUL=UpLeg");
- root pos equals the S04 anchor exactly;
- root heading agrees with the S04 facing within 1 degree. An upright root (rotated up axis y >= 0.5) is read from
  its forward axis (+Z). A root that is not upright inside a declared flip or cartwheel is read from that turn's
  invariant axis (a flip about X keeps the lateral axis, a cartwheel about Z keeps the forward axis); otherwise
  (a slide, a fall) from whichever of the two is more horizontal;
- Euler angles are continuous per entity (never wrapped), so the change between consecutive keys is the rotation
  performed. A change of 90 degrees or more on any axis must be declared; a declared turn uses the convention axis
  (flip X, spin Y, cartwheel Z) and that axis changes most, by at least 90 degrees, before the entity's next key.
- the root agrees with the S06 posture when no posture change is in progress: standing/crouching/kneeling are
  upright, inverted has the up axis at y <= -0.5, prone/supine have it level with the chest down/up (agent addition).
A mismatch is a finding (the step fails and is re-authored); nothing is corrected silently.
"""

from solver.quaternion import angle_between, apply, heading_degrees, horizontal, lateral_heading, matrix, uprightness

UPRIGHT = 0.5
HEADING_TOLERANCE = 1.0
TURN_MINIMUM = 90
AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}
INVARIANT_BASIS = {"X": "lateral", "Z": "forward"}


def posture_problem(rot, posture):
    up, forward = uprightness(rot), apply(matrix(rot), (0, 0, 1))[1]
    expected = {"standing": up >= UPRIGHT, "crouching": up >= UPRIGHT, "kneeling": up >= UPRIGHT, "inverted": up <= -UPRIGHT,
                "prone": abs(up) < UPRIGHT and forward <= -UPRIGHT, "supine": abs(up) < UPRIGHT and forward >= UPRIGHT}
    return posture in expected and not expected[posture]


def kernel_joints(kernel):
    joints = []
    for item in kernel["items"]:
        if item["field"] == "key":
            joints.extend(item["text"].split("=")[0].split("/"))
    return joints


def sequences(keys, slots):
    by_entity = {}
    for slot_id in sorted(keys, key=lambda s: (slots[s]["t"], s)):
        by_entity.setdefault(slots[slot_id]["entity"], []).append(slot_id)
    return by_entity


def heading(rot, basis):
    if basis == "lateral":
        return lateral_heading(rot)
    return heading_degrees(apply(matrix(rot), (0, 0, 1)))


def basis_for(key, previous, turns):
    """Which axis reads the heading: forward when upright, the invariant axis of a flip or cartwheel in progress,
    else the more horizontal of the lateral and forward axes."""
    if uprightness(key["rot"]) >= UPRIGHT:
        return "forward"
    for candidate in (previous, key):
        if candidate is not None and turns.get(candidate["turn"]) in INVARIANT_BASIS:
            return INVARIANT_BASIS[turns[candidate["turn"]]]
    m = matrix(key["rot"])
    lateral, forward = apply(m, (1, 0, 0)), apply(m, (0, 0, 1))
    return "lateral" if horizontal(lateral) > horizontal(forward) else "forward"


def check(keys, slots, joints, turns):
    """keys/slots keyed by slot id. Returns (findings, heading basis per slot)."""
    findings, bases = [], {}
    for entity_keys in sequences(keys, slots).values():
        for position, slot_id in enumerate(entity_keys):
            key, slot = keys[slot_id], slots[slot_id]
            previous = keys[entity_keys[position - 1]] if position else None
            following = keys[entity_keys[position + 1]] if position + 1 < len(entity_keys) else None
            missing = [j for j in joints if j not in key["bones"]]
            extra = [j for j in key["bones"] if j not in joints]
            if missing or extra:
                findings.append({"code": "MOTION_JOINTS", "message": "Bones must be exactly the kernel joints", "slot": slot_id,
                                 "detail": {"missing": missing, "extra": extra}})
            if key["pos"] != slot["pos"]:
                findings.append({"code": "MOTION_POS", "message": "Root pos must equal the S04 anchor exactly",
                                 "slot": slot_id, "detail": [key["pos"], slot["pos"]]})
            basis = bases[slot_id] = basis_for(key, previous, turns)
            if horizontal(slot["facing"]) > 0:
                off = angle_between(heading(key["rot"], basis), heading_degrees(slot["facing"]))
                if off > HEADING_TOLERANCE:
                    findings.append({"code": "MOTION_FACING", "message": f"Root heading ({basis} axis) disagrees with the "
                                     "S04 facing", "slot": slot_id, "detail": round(off, 3)})
            postures = slot["allowed_postures"]
            if len(postures) == 1 and posture_problem(key["rot"], postures[0]):
                findings.append({"code": "MOTION_POSTURE", "message": f"Root rotation disagrees with the S06 posture "
                                 f"{postures[0]}", "slot": slot_id})
            findings.extend(_turn_findings(slot_id, key, following, turns))
    return findings, bases


def _turn_findings(slot_id, key, following, turns):
    turn, axis = key["turn"], key["axis_declaration"]
    deltas = [abs(b - a) for a, b in zip(key["rot"], following["rot"], strict=True)] if following else [0, 0, 0]
    if turn == "none":
        if axis != "none":
            return [{"code": "MOTION_AXIS", "message": "No turn means axis_declaration none", "slot": slot_id}]
        if max(deltas) >= TURN_MINIMUM:
            return [{"code": "MOTION_AXIS", "message": "A root rotation of 90 degrees or more before the next key must be "
                     "declared (flip X, spin Y, cartwheel Z)", "slot": slot_id, "detail": deltas}]
        return []
    if axis != turns[turn]:
        return [{"code": "MOTION_AXIS", "message": f"A {turn} turns about {turns[turn]}", "slot": slot_id}]
    if following is None:
        return [{"code": "MOTION_AXIS", "message": "A declared turn needs a following key", "slot": slot_id}]
    index = AXIS_INDEX[axis]
    if deltas[index] < TURN_MINIMUM or deltas[index] < max(deltas):
        return [{"code": "MOTION_AXIS", "message": "The declared axis is not the dominant rotation before the next key",
                 "slot": slot_id, "detail": deltas}]
    return []
