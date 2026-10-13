"""Pose mechanics (PLAN-009): what makes a pose read, computed from a key's world points (forward kinematics, the 11
points S13 writes: pelvis, torso, head, each elbow and hand, each knee and foot). Pure functions of the points; S14
writes them, S18 prints them.

Line of action (PM-3, S-126): the curve the body makes from the head through the chest and the pelvis to its base, the
foot farthest from the head. The chord runs from the head to that foot; each inner point's offset from the chord,
signed along the side the largest offset bulges to, gives the shape: `straight` when no offset reaches STRAIGHT of the
chord's length, `c` when every offset bulges to one side, `s` when they bulge to both. `tension` is the largest offset
over the chord's length (how hard the body bends), `apex` the point that bulges most, `bulge` the unit direction it
bulges toward, `chord` the unit direction from the head to the base, and `inverted` whether the head is INVERTED_M or more
below the pelvis (a flip, a takedown; a body laid flat is not). The thresholds are Claude's interpretation,
for the owner's review (PLAN-009 section 8).

Centre of mass (S-127): the mass-weighted centre of the body's segments, each segment's share and the place of its
centre along it from library/body_segments.yaml `masses` (Dempster via Winter), on the key's joints (forward
kinematics).

Counterbalance (PM-3, S-127): a limb is extended when it runs nearly straight (its ends at EXTENDED_STRAIGHT of its
length or more) and its end lies REACH_M or more from the centre of mass across the floor; the limb that reaches
furthest leads, and the limbs whose ends lie COUNTER_M or more across the floor on the other side of the centre of
mass counter it. A lead with no counter is a reach the body does not balance.
"""

import math

STRAIGHT = 0.08  # an offset under 8 % of the chord reads as a straight line (a standing body bends ~5 %)
INVERTED_M = 0.15  # the head this far below the hips: upside down (a body laid flat is not)
SPINE = ("head", "torso", "pelvis")
FEET = ("left_foot", "right_foot")


def _sub(a, b):
    return [x - y for x, y in zip(a, b, strict=True)]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def _unit(v):
    length = math.sqrt(_dot(v, v))
    return [x / length for x in v] if length > 1e-9 else [0.0, 0.0, 0.0]


def _round(v):
    return [round(x, 3) + 0.0 for x in v]


def line_of_action(points):
    """{shape, apex, tension, bulge, chord, base} for one key's world points, or None without a head, a chest, a
    pelvis and a foot."""
    if not all(p in points for p in SPINE) or not any(f in points for f in FEET):
        return None
    head = points["head"]
    base = max((f for f in FEET if f in points), key=lambda f: (math.dist(head, points[f]), f))
    chord = _sub(points[base], head)
    length = math.sqrt(_dot(chord, chord))
    if length < 1e-9:
        return None
    axis = _unit(chord)
    offsets = {}
    for name in ("torso", "pelvis"):
        rel = _sub(points[name], head)
        offsets[name] = _sub(rel, [axis[i] * _dot(rel, axis) for i in range(3)])
    apex = max(offsets, key=lambda n: (_dot(offsets[n], offsets[n]), n))
    largest = math.sqrt(_dot(offsets[apex], offsets[apex]))
    bulge = _unit(offsets[apex])
    signed = [_dot(offsets[n], bulge) for n in offsets]
    tension = largest / length
    if tension < STRAIGHT:
        shape = "straight"
    elif all(d >= -STRAIGHT * length for d in signed):
        shape = "c"
    else:
        shape = "s"
    return {"shape": shape, "apex": apex, "tension": round(tension, 3), "bulge": _round(bulge),
            "chord": _round(axis), "base": base, "inverted": head[1] < points["pelvis"][1] - INVERTED_M}


EXTENDED_STRAIGHT = 0.85  # a limb whose ends span 85 % of its length or more runs nearly straight
REACH_M = 0.4  # an extended limb's end this far from the centre of mass across the floor reaches out
COUNTER_M = 0.25  # a limb's end this far across the floor on the other side counters it
LIMBS = {"left_arm": ("left_shoulder", "left_elbow", "left_hand"), "right_arm": ("right_shoulder", "right_elbow",
                                                                                "right_hand"),
         "left_leg": ("left_hip", "left_knee", "left_ankle", "left_sole"),
         "right_leg": ("right_hip", "right_knee", "right_ankle", "right_sole")}


def centre_of_mass(joints, masses):
    """[x, y, z]: the segments' centres weighted by their share of the body (`masses`, body_segments.yaml)."""
    total, weighted = 0.0, [0.0, 0.0, 0.0]
    for row in masses.values():
        for side in ("left_", "right_") if row.get("sided") else ("",):
            a, b = joints[side + row["from"]], joints[side + row["to"]]
            centre = [x + row["at"] * (y - x) for x, y in zip(a, b, strict=True)]
            weighted = [w + row["fraction"] * c for w, c in zip(weighted, centre, strict=True)]
            total += row["fraction"]
    return _round([w / total for w in weighted])


def _across(a, b):
    """The vector from b to a across the floor (x, z): the vertical (y) dropped."""
    return [a[0] - b[0], 0.0, a[2] - b[2]]


def counterbalance(joints, com):
    """{extended: [limbs], lead: limb or None, reach_m, counter: [limbs]} for one key's joints and its centre of mass."""
    extended, reach = [], {}
    for limb, chain in LIMBS.items():
        length = sum(math.dist(joints[a], joints[b]) for a, b in zip(chain, chain[1:], strict=False))
        span = math.dist(joints[chain[0]], joints[chain[-1]])
        out = _across(joints[chain[-1]], com)
        reach[limb] = math.sqrt(_dot(out, out))
        if length > 1e-9 and span / length >= EXTENDED_STRAIGHT and reach[limb] >= REACH_M:
            extended.append(limb)
    lead = max(extended, key=lambda limb: (reach[limb], limb)) if extended else None
    counter = []
    if lead is not None:
        way = _unit(_across(joints[LIMBS[lead][-1]], com))
        counter = [limb for limb, chain in LIMBS.items() if limb != lead
                   and _dot(_across(joints[chain[-1]], com), way) <= -COUNTER_M]
    return {"extended": extended, "lead": lead, "reach_m": round(reach[lead], 3) if lead else 0.0, "counter": counter}
