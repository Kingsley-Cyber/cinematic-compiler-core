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
"""

import json

import yaml

from planner import modality
from planner.dependency_graph import ROOT
from solver.quaternion import apply, matrix
from validators.schema_validator import validate_schema

POINTS = ("pelvis", "torso", "head", "left_arm", "left_hand", "right_arm", "right_hand", "left_leg", "left_foot",
          "right_leg", "right_foot")


def _card():
    card = yaml.safe_load((ROOT / "library" / "body_segments.yaml").read_text(encoding="utf-8"))
    validate_schema(card, json.loads((ROOT / "schemas" / "cards" / "body_segments.schema.json").read_text(encoding="utf-8")))
    return card


def segments(genre):
    """The metres of the body the genre's profile names (owner O85: schemas/modality/<genre>.schema.json body_type)."""
    return _card()["bodies"][modality.body_type(genre)]["metres"]


def standing_leg(metres):
    """The pelvis's height over the soles with the legs straight (thigh, shin and ankle)."""
    return round(metres["thigh"] + metres["shin"] + metres["ankle"], 6)


def _turn(chain, vector):
    for rot in reversed(chain):
        vector = apply(matrix(rot), vector)
    return vector


def _at(base, chain, vector):
    return [round(b + d, 6) + 0.0 for b, d in zip(base, _turn(chain, vector), strict=True)]


def points(key, metres):
    """{name: [x, y, z]} in the scene frame for one key (root position and rotation, joints in `bones`)."""
    root, bones, pelvis = key["rot"], key["bones"], list(key["pos"])
    out = {"pelvis": [float(v) for v in pelvis]}
    trunk = [root, bones["Sp"]]  # owner O84: the hips are read from the trunk
    for side, sign, upper, lower in (("left", 1, "LUL", "LL"), ("right", -1, "RUL", "RL")):
        hip = _at(pelvis, [root], (sign * metres["hip"], 0.0, 0.0))  # the hip joint sits on the pelvis
        out[f"{side}_leg"] = knee = _at(hip, [*trunk, bones[upper]], (0.0, -metres["thigh"], 0.0))
        ankle = _at(knee, [*trunk, bones[upper], bones[lower]], (0.0, -metres["shin"], 0.0))
        out[f"{side}_foot"] = _at(ankle, [*trunk, bones[upper], bones[lower]], (0.0, -metres["ankle"], 0.0))
    chest = _at(pelvis, [root, bones["Sp"]], (0.0, metres["spine"], 0.0))
    out["torso"] = _at(pelvis, [root, bones["Sp"]], (0.0, metres["torso_point"] * metres["spine"], 0.0))
    for side, sign, upper, lower in (("left", 1, "LA", "LFA"), ("right", -1, "RA", "RFA")):
        shoulder = _at(chest, [root, bones["Sp"]], (sign * metres["shoulder"], 0.0, 0.0))
        out[f"{side}_arm"] = elbow = _at(shoulder, [root, bones["Sp"], bones[upper]], (0.0, -metres["upper_arm"], 0.0))
        out[f"{side}_hand"] = _at(elbow, [root, bones["Sp"], bones[upper], bones[lower]], (0.0, -metres["forearm"], 0.0))
    neck = _at(chest, [root, bones["Sp"], bones["NK"]], (0.0, metres["neck"], 0.0))
    out["head"] = _at(neck, [root, bones["Sp"], bones["NK"], bones["HD"]], (0.0, metres["head"], 0.0))
    return out


def part_point(named, part):
    """The world point a contact's body part touches with, or None for a part with no point."""
    if part in named:
        return named[part]
    side, _, name = part.partition("_")
    return named.get(f"{side}_{'hand' if name in ('palm', 'fingers', 'fist') else name}") if side in ("left", "right") else (
        named["torso"] if part in ("chest", "back", "spine", "shoulder") else None)
