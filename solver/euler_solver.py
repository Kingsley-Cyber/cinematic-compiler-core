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
  A substitution's actor is gone until its next key (owner O12, O18), so no rotation is performed across that gap.
  A beat whose label names a flip or a cartwheel has its actor declare that turn (TURN_LABEL, owner O18, audit X5/X6).
- the root agrees with the S06 posture when no posture change is in progress: standing/crouching/kneeling are
  upright, inverted has the up axis at y <= -0.5, prone/supine have it level with the chest down/up (agent addition).
- every joint's local Euler components lie inside library/joint_limits.yaml for the scene's genre (owner O11; knee
  flexion +X per O7; NK and HD summed as the neck; anime widens the listed joints by 30 degrees): JOINT_LIMIT.
- runs (plan FR.3): the consecutive keys of one performer that declare one turn are a run, ending at the first key that
  does not. The angle about the turn's axis moves one way through it (ROTATION_NOT_MONOTONIC); a run whose beat names a
  flip or a cartwheel ends inside the clip on a whole number of turns (ROTATION_INCOMPLETE, owner O38); where a flip or
  a cartwheel passes 180 + 360k degrees, the root interpolated linearly between its keys is upside down
  (INVERSION_MISSING; derived and checked, not printed, W3). Interpretation (Claude's, for owner review): a whole turn
  is within 30 degrees of a multiple of 360, and the inversion is read on linear Euler interpolation (FR.1's spacing).
A mismatch is a finding (the step fails and is re-authored); nothing is corrected silently.
"""

from solver.quaternion import angle_between, apply, heading_degrees, horizontal, lateral_heading, matrix, uprightness

UPRIGHT = 0.5
HEADING_TOLERANCE = 1.0
TURN_MINIMUM = 90
AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}
INVARIANT_BASIS = {"X": "lateral", "Z": "forward"}
FULL_TURN_SLACK = 30  # interpretation (Claude's, for owner review): degrees off a whole number of turns still whole
EPSILON = 1e-9


def effective_limits(card, genre):
    """{joint: {axis: [low, high]}} for the genre: anime moves each nonzero bound of the listed joints further out."""
    extra = card["anime"]["extra_deg"] if genre in card["anime"]["genres"] else 0
    limits = {}
    for joint, row in card["joints"].items():
        wide = extra if joint in card["anime"]["joints"] else 0
        limits[joint] = {axis: [row[axis][0] - wide if row[axis][0] < 0 else row[axis][0],
                                row[axis][1] + wide if row[axis][1] > 0 else row[axis][1]] for axis in ("x", "y", "z")}
    return limits


def limit_findings(key, slot_id, limits):
    findings = []
    for joint, bounds in sorted(limits.items()):
        parts = joint.split("+")
        if not all(p in key["bones"] for p in parts):
            continue
        values = [sum(key["bones"][p][i] for p in parts) for i in range(3)]
        for i, axis in enumerate(("x", "y", "z")):
            low, high = bounds[axis]
            if not low - 1e-9 <= values[i] <= high + 1e-9:
                findings.append({"code": "JOINT_LIMIT", "message": f"{joint} {axis} = {values[i]} is outside [{low}, {high}]",
                                 "slot": slot_id})
    return findings


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


def check(keys, slots, joints, turns, limits=None):
    """keys/slots keyed by slot id; `limits` from effective_limits. Returns (findings, heading basis per slot)."""
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
            if limits:
                findings += limit_findings(key, slot_id, limits)
            postures = slot["allowed_postures"]
            if len(postures) == 1 and posture_problem(key["rot"], postures[0]):
                findings.append({"code": "MOTION_POSTURE", "message": f"Root rotation disagrees with the S06 posture "
                                 f"{postures[0]}", "slot": slot_id})
            if not (slot["event_type"] == "substitution" and slot["role"] == "actor" and key["turn"] == "none"):
                findings.extend(_turn_findings(slot_id, key, following, turns))
            findings.extend(named_turn_findings(slot_id, slot, key, following))
    findings.extend(run_findings(keys, slots, turns))
    return findings, bases


def turn_runs(keys, slots):
    """[{entity, turn, slots, rots, end}]: consecutive keys of one performer declaring one turn; `rots` adds the key
    that ends the run (`end`, None when the clip ends first)."""
    runs = []
    for entity_keys in sequences(keys, slots).values():
        current = None
        for position, slot_id in enumerate(entity_keys):
            key = keys[slot_id]
            after = entity_keys[position + 1] if position + 1 < len(entity_keys) else None
            if key["turn"] == "none":
                current = None
                continue
            if current is None or current["turn"] != key["turn"]:
                current = {"entity": slots[slot_id]["entity"], "turn": key["turn"], "slots": [], "rots": [key["rot"]]}
                runs.append(current)
            current["slots"].append(slot_id)
            current["end"] = after
            if after is not None:
                current["rots"].append(keys[after]["rot"])
    return runs


def run_findings(keys, slots, turns):
    """FR.3: ROTATION_NOT_MONOTONIC, ROTATION_INCOMPLETE (owner O38), INVERSION_MISSING over each turn run."""
    findings = []
    for run in turn_runs(keys, slots):
        index, first = AXIS_INDEX[turns[run["turn"]]], run["slots"][0]
        angles = [rot[index] for rot in run["rots"]]
        deltas = [b - a for a, b in zip(angles, angles[1:], strict=False)]
        if len({delta > 0 for delta in deltas if abs(delta) > EPSILON}) > 1:
            findings.append({"code": "ROTATION_NOT_MONOTONIC", "message": f"The {run['turn']} turns both ways across its "
                             "keys", "slot": first, "detail": angles})
        total = abs(sum(deltas))
        count = round(total / 360)
        named = any(slots[s]["role"] == "actor" and named_turn(slots[s]["label"]) == run["turn"] for s in run["slots"])
        if named and (run["end"] is None or count < 1 or abs(total - 360 * count) > FULL_TURN_SLACK):
            findings.append({"code": "ROTATION_INCOMPLETE", "message": f"The named {run['turn']} turns {round(total)} "
                             "degrees" + (" and the clip ends first" if run["end"] is None else ", not a whole turn"),
                             "slot": first, "detail": angles})
        if run["turn"] in ("flip", "cartwheel"):
            findings.extend(_inversion_findings(run, first, deltas))
    return findings


def _inversion_findings(run, first, deltas):
    """At each crossing of 180 + 360k the root, interpolated linearly between the bracketing keys, is upside down."""
    findings, done, target = [], 0.0, 180.0
    for (a, b), delta in zip(zip(run["rots"], run["rots"][1:], strict=False), deltas, strict=True):
        while abs(delta) > EPSILON and done + abs(delta) >= target - EPSILON:
            share = (target - done) / abs(delta)
            rot = [x + (y - x) * share for x, y in zip(a, b, strict=True)]
            if uprightness(rot) > -UPRIGHT:
                findings.append({"code": "INVERSION_MISSING", "message": f"The {run['turn']} passes {round(target)} "
                                 "degrees with the root not upside down", "slot": first,
                                 "detail": [round(x, 3) for x in rot]})
            target += 360.0
        done += abs(delta)
    return findings


FLIP_WORDS, CARTWHEEL_WORDS = {"flip", "backflip", "frontflip", "somersault"}, {"cartwheel"}


def named_turn(label):
    """'flip' or 'cartwheel' when a beat label names one, else None."""
    words = set(label.split("_"))
    return "flip" if words & FLIP_WORDS else "cartwheel" if words & CARTWHEEL_WORDS else None


def named_turn_findings(slot_id, slot, key, following):
    """TURN_LABEL (owner O18, audit X5/X6): a beat that names a flip or a cartwheel has its actor's root declare that
    turn (flip about X, cartwheel about Z); _turn_findings then makes that axis rotate most, by 90 degrees or more."""
    turn = named_turn(slot["label"]) if slot["role"] == "actor" else None
    if turn is not None and key["turn"] != turn:
        return [{"code": "TURN_LABEL", "message": f"The beat names a {turn} but the root declares {key['turn']}",
                 "slot": slot_id, "detail": [key["rot"], following["rot"] if following else None]}]
    return []


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
