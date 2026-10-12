"""Forward kinematics for S13 key poses (owner O24: world contact points come from the pose; O72: the root is the pelvis).

The Q6 chain with the hips read from the trunk (owner O84, rule R-35): root -> Sp -> (NK -> HD, LA -> LFA, RA -> RFA,
LUL -> LL, RUL -> RL), each joint's Euler rotation local to its parent; at rest the body is upright and every limb
hangs straight down; +X is the performer's left. The hip joints sit on the pelvis (the root's frame) and the thighs
turn with the trunk, as the owner's source writes its crouches (S-029). Segment lengths come from
library/body_segments.yaml (draft), the body each genre profile names (owner O85). `points` gives each key's named world
points; `part_point` maps a contact's body part onto one of them.
Interpretation (Claude's, for owner review): the hip joints sit on the pelvis while the thighs turn with the trunk
(O84 sets the trunk reading, not where the joint sits); a foot's point is its sole, below the ankle along the shin; a
hand's is the palm's centre at the end of the forearm; a leg's is the knee and an arm's the elbow; the torso's lies
at `torso_point` of the spine from the pelvis; the head's at its centre.
Capsules (RV-49, F-144): each segment is a capsule, its axis between its two joints and its radius from the body card
(draft); `capsules` gives them for one key, `surface_gap` the distance between a part's surface and a target's.
Interpretation (Claude's, for owner review): the trunk is one capsule from the pelvis to the shoulder line, with a thinner
one across the shoulders and one across the hips; the head is a sphere about its centre; a part's point carries the
radius of the segment it ends (a hand the forearm's, a foot the foot's, a knee the thigh's, an elbow the upper arm's).
"""

import json
import math

import yaml

from planner import genre_profile
from planner.dependency_graph import ROOT
from solver.quaternion import apply, matrix
from validators.schema_validator import validate_schema

POINTS = ("pelvis", "torso", "head", "left_arm", "left_hand", "right_arm", "right_hand", "left_leg", "left_foot",
          "right_leg", "right_foot")
CAPSULES = {"trunk": ("pelvis", "chest", "trunk"), "girdle": ("left_shoulder", "right_shoulder", "girdle"),
            "hips": ("left_hip", "right_hip", "hips"), "neck": ("chest", "neck", "neck"), "head": ("head", "head", "head"),
            **{f"{side}_{name}": (f"{side}_{a}", f"{side}_{b}", name) for side in ("left", "right")
               for name, a, b in (("upper_arm", "shoulder", "elbow"), ("forearm", "elbow", "hand"), ("thigh", "hip", "knee"),
                                  ("shin", "knee", "ankle"), ("foot", "ankle", "sole"))}}
PART_RADIUS = {"hand": "forearm", "arm": "upper_arm", "leg": "thigh", "foot": "foot"}  # the segment a point ends
PART_CAPSULES = {"hand": ("forearm",), "arm": ("upper_arm", "forearm"), "leg": ("thigh", "shin"), "foot": ("foot",)}


def _card():
    card = yaml.safe_load((ROOT / "library" / "body_segments.yaml").read_text(encoding="utf-8"))
    validate_schema(card, json.loads((ROOT / "schemas" / "cards" / "body_segments.schema.json").read_text(encoding="utf-8")))
    return card


def segments(genre):
    """The metres of the body the genre's profile names (owner O85: library/genre_profiles/<genre>.yaml body_type)."""
    return _card()["bodies"][genre_profile.body_type(genre)]["metres"]


def radii(genre):
    """The capsule radii of the body the genre's profile names (RV-49, draft)."""
    return _card()["bodies"][genre_profile.body_type(genre)]["radii"]


def standing_leg(metres):
    """The pelvis's height over the soles with the legs straight (thigh, shin and ankle)."""
    return round(metres["thigh"] + metres["shin"] + metres["ankle"], 6)


def _turn(chain, vector):
    for rot in reversed(chain):
        vector = apply(matrix(rot), vector)
    return vector


def _at(base, chain, vector):
    return [round(b + d, 6) + 0.0 for b, d in zip(base, _turn(chain, vector), strict=True)]


def joints(key, metres):
    """{joint: [x, y, z]} in the scene frame for one key (root position and rotation, joints in `bones`): the pelvis,
    chest (the shoulder line's centre), neck, head, and each side's hip, knee, ankle, sole, shoulder, elbow and hand."""
    root, bones, pelvis = key["rot"], key["bones"], list(key["pos"])
    out = {"pelvis": [float(v) for v in pelvis]}
    trunk = [root, bones["Sp"]]  # owner O84: the hips are read from the trunk
    for side, sign, upper, lower in (("left", 1, "LUL", "LL"), ("right", -1, "RUL", "RL")):
        out[f"{side}_hip"] = hip = _at(pelvis, [root], (sign * metres["hip"], 0.0, 0.0))  # the hip joint sits on the pelvis
        out[f"{side}_knee"] = knee = _at(hip, [*trunk, bones[upper]], (0.0, -metres["thigh"], 0.0))
        out[f"{side}_ankle"] = ankle = _at(knee, [*trunk, bones[upper], bones[lower]], (0.0, -metres["shin"], 0.0))
        out[f"{side}_sole"] = _at(ankle, [*trunk, bones[upper], bones[lower]], (0.0, -metres["ankle"], 0.0))
    out["chest"] = chest = _at(pelvis, [root, bones["Sp"]], (0.0, metres["spine"], 0.0))
    out["torso"] = _at(pelvis, [root, bones["Sp"]], (0.0, metres["torso_point"] * metres["spine"], 0.0))
    for side, sign, upper, lower in (("left", 1, "LA", "LFA"), ("right", -1, "RA", "RFA")):
        out[f"{side}_shoulder"] = shoulder = _at(chest, [root, bones["Sp"]], (sign * metres["shoulder"], 0.0, 0.0))
        out[f"{side}_elbow"] = elbow = _at(shoulder, [root, bones["Sp"], bones[upper]], (0.0, -metres["upper_arm"], 0.0))
        out[f"{side}_hand"] = _at(elbow, [root, bones["Sp"], bones[upper], bones[lower]], (0.0, -metres["forearm"], 0.0))
    out["neck"] = neck = _at(chest, [root, bones["Sp"], bones["NK"]], (0.0, metres["neck"], 0.0))
    out["head"] = _at(neck, [root, bones["Sp"], bones["NK"], bones["HD"]], (0.0, metres["head"], 0.0))
    return out


def points(key, metres):
    """{name: [x, y, z]} in the scene frame for one key: the contact points (a leg's is the knee, an arm's the elbow, a
    foot's the sole)."""
    named = joints(key, metres)
    out = {name: named[name] for name in ("pelvis", "torso", "head")}
    for side in ("left", "right"):
        out |= {f"{side}_leg": named[f"{side}_knee"], f"{side}_foot": named[f"{side}_sole"],
                f"{side}_arm": named[f"{side}_elbow"], f"{side}_hand": named[f"{side}_hand"]}
    return out


def capsules(key, metres, radii):
    """{segment: (start, end, radius)} for one key (RV-49): each segment's axis between its two joints."""
    named = joints(key, metres)
    return {name: (named[a], named[b], radii[r]) for name, (a, b, r) in CAPSULES.items()}


def part_radius(part, radii):
    """The radius of a contact part's point: the segment it ends (RV-49)."""
    side, _, name = part.partition("_")
    if side in ("left", "right"):
        return radii[PART_RADIUS["hand" if name in ("palm", "fingers", "fist") else name]]
    return radii["head"] if part == "head" else radii["hips"] if part == "pelvis" else radii["trunk"]


def part_capsules(part):
    """The segments that make up a target part (RV-49); a torso, chest, back, spine or shoulder is the trunk and the
    shoulders."""
    side, _, name = part.partition("_")
    if side in ("left", "right"):
        return [f"{side}_{n}" for n in PART_CAPSULES["hand" if name in ("palm", "fingers", "fist") else name]]
    return ["head", "neck"] if part == "head" else ["hips", "trunk"] if part == "pelvis" else ["trunk", "girdle"]


def closest(point, start, end):
    """The point of the segment start-end nearest `point`."""
    axis = [b - a for a, b in zip(start, end, strict=True)]
    length = sum(v * v for v in axis)
    share = 0.0 if length <= 1e-12 else min(1.0, max(0.0, sum((p - a) * v for p, a, v in zip(point, start, axis,
                                                                                            strict=True)) / length))
    return [a + share * v for a, v in zip(start, axis, strict=True)]


def segment_distance(p1, q1, p2, q2):
    """The least distance between the segments p1-q1 and p2-q2."""
    d1, d2, r = ([b - a for a, b in zip(x, y, strict=True)] for x, y in ((p1, q1), (p2, q2), (p2, p1)))
    a, e, f = sum(v * v for v in d1), sum(v * v for v in d2), sum(u * v for u, v in zip(d2, r, strict=True))
    if a <= 1e-12 and e <= 1e-12:
        return math.dist(p1, p2)
    if a <= 1e-12:
        s, t = 0.0, min(1.0, max(0.0, f / e))
    else:
        c = sum(u * v for u, v in zip(d1, r, strict=True))
        if e <= 1e-12:
            s, t = min(1.0, max(0.0, -c / a)), 0.0
        else:
            b = sum(u * v for u, v in zip(d1, d2, strict=True))
            denominator = a * e - b * b
            s = min(1.0, max(0.0, (b * f - c * e) / denominator)) if denominator > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0.0:
                s, t = min(1.0, max(0.0, -c / a)), 0.0
            elif t > 1.0:
                s, t = min(1.0, max(0.0, (b - c) / a)), 1.0
    return math.dist([p + s * v for p, v in zip(p1, d1, strict=True)], [p + t * v for p, v in zip(p2, d2, strict=True)])


def surface_gap(point, radius, target_capsules):
    """(gap, surface point): the distance from the surface of a part (its point and radius) to the nearest of the
    target's capsules, never below zero (a part inside the target is BODY_OVERLAP's to refuse), and the target's surface
    point facing it (RV-49, F-144: a strike is measured to the target's surface)."""
    best = None
    for start, end, r in target_capsules:
        axis = closest(point, start, end)
        apart = math.dist(point, axis)
        if best is None or apart - r < best[0]:
            toward = [(p - a) / apart for p, a in zip(point, axis, strict=True)] if apart > 1e-9 else [0.0, 0.0, 0.0]
            best = (apart - r, [round(a + r * u, 6) + 0.0 for a, u in zip(axis, toward, strict=True)])
    return round(max(0.0, best[0] - radius), 3), best[1]


def part_point(named, part):
    """The world point a contact's body part touches with, or None for a part with no point."""
    if part in named:
        return named[part]
    side, _, name = part.partition("_")
    return named.get(f"{side}_{'hand' if name in ('palm', 'fingers', 'fist') else name}") if side in ("left", "right") else (
        named["torso"] if part in ("chest", "back", "spine", "shoulder") else None)
