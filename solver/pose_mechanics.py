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
