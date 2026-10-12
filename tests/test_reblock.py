"""solver/reblock.py (RV-35a, F-127): a re-block is re-derived from stated goals, free joints and bounds; and the
pickups it re-derived crouch on the feet with one hand down (F-110)."""

import json

import pytest
from conftest import ROOT

from solver import forward_kinematics
from solver.reblock import solve

pytestmark = pytest.mark.unit
EXAMPLES = ROOT / "examples"


def _key(example, slot):
    plan = json.loads((EXAMPLES / example / "plans" / "motion.json").read_text(encoding="utf-8"))
    return next(k for k in plan["keys"] if k["slot"] == slot)


def test_the_solver_meets_a_goal_by_the_least_change_inside_its_bounds():
    """A sole lifted 0.3 m comes back to the floor through the free knee and hip only, inside their bounds, and a
    start outside a bound is moved into it."""
    metres = forward_kinematics.segments("anime")
    key = _key("wizard_vs_acrobat", "acrobat@b11")
    lifted = {**key, "bones": {**key["bones"], "LL": [110, 0, 0]}}
    bones, misses = solve(lifted, metres, [("left_foot", 0.0)], ["LUL.x", "LL.x"], {"LL.x": (0, 80)})
    assert misses < 1e-4 and 0 <= bones["LL"][0] <= 80
    assert {joint: bones[joint] for joint in bones if joint not in ("LUL", "LL")} == \
        {joint: lifted["bones"][joint] for joint in bones if joint not in ("LUL", "LL")}
    assert abs(forward_kinematics.points({**lifted, "bones": bones}, metres)["left_foot"][1]) < 0.01


def test_s078_s_re_blocks_are_re_derived_from_their_goals():
    """B's lunge at 3.4 (S-078) comes back from the hip alone with its sole's height as the goal."""
    metres = forward_kinematics.segments("anime")
    key = _key("reference_fight", "ninja_broad@b08")
    before = {**key, "bones": {**key["bones"], "LUL": [-85.17, 1.29, 22.95]}}  # the key before S-078
    bones, misses = solve(before, metres, [("left_foot", 0.034)], ["LUL.x"], {})
    assert misses < 1e-6 and abs(bones["LUL"][0] - key["bones"]["LUL"][0]) <= 1


def test_the_pickups_crouch_on_the_feet_with_one_hand_down():
    """F-110 (RV-35a, owner O18): at 7.5 and 8.0 A crouches on both soles with one hand on the floor at its prop and the
    other off it, the head clear of the pelvis and the trunk short of flat; S11 names the hand's support."""
    envelope = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    kinematic = {k["id"]: k for k in envelope["nodes"]["kinematic"]["items"]}
    for slot, hand, other in (("ninja_lean@b19", "left_hand", "right_hand"), ("ninja_lean@b20", "right_hand", "left_hand")):
        points, key = keys[slot]["points"], keys[slot]
        assert abs(points["left_foot"][1]) <= 0.03 and abs(points["right_foot"][1]) <= 0.03
        assert points[hand][1] <= 0.03 and points[other][1] >= 0.3
        assert points["head"][1] - points["pelvis"][1] >= 0.2
        assert (key["rot"][0] % 360) + key["bones"]["Sp"][0] < 80  # the root's 30 degrees and the spine's lean
        assert hand in kinematic[slot]["support"]
