"""solver/reblock.py (RV-35a, F-127): a re-block is re-derived from stated goals, free joints and bounds; and the
pickups it re-derived crouch on the feet with one hand down (F-110)."""

import json

import pytest
from conftest import ROOT

from solver import forward_kinematics
from solver.reblock import limits, main, solve

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


def test_the_answer_does_not_depend_on_the_order_of_the_free_joints():
    """F-207 (RV-96): the search takes the best move among all free components, ties broken by their names, so any
    order of the free list gives the same bones."""
    metres = forward_kinematics.segments("anime")
    key = _key("wizard_vs_acrobat", "acrobat@b11")
    lifted = {**key, "bones": {**key["bones"], "LL": [110, 0, 0], "LUL": [-80, 0, 8]}}
    goals = [("left_foot", 0.0), ("left_hand", [1.0, 0.6, 5.2])]
    free = ["Sp.x", "LUL.x", "LUL.z", "LL.x", "LA.x", "LFA.x"]
    answers = [solve(lifted, metres, goals, order, {}, (), limits("anime"))
               for order in (free, list(reversed(free)), free[2:] + free[:2])]
    assert answers[0] == answers[1] == answers[2]


def test_the_genre_s_joint_limits_bound_the_free_joints():
    """F-207 (RV-96, owner O11): the genre's joint limits bound every free component; a goal past them is left unmet
    rather than met through a bent-back knee."""
    metres = forward_kinematics.segments("anime")
    key = _key("wizard_vs_acrobat", "acrobat@b11")
    assert limits("anime")["LL.x"] == (0.0, 165.0) and limits("adult")["LL.x"] == (0.0, 135.0)
    unbound, _ = solve(key, metres, [("left_foot", 1.6)], ["LL.x"])
    bound, misses = solve(key, metres, [("left_foot", 1.6)], ["LL.x"], None, (), limits("anime"))
    assert unbound["LL"][0] > 165 and bound["LL"][0] == 165 and misses > 0


def test_the_cli_re_derives_a_solve_from_its_start_key_and_weighted_goals(tmp_path, capsys):
    """F-207 (RV-96): the command takes the start key from a plan file (or a git revision), the root's height, weighted
    goals and the free set, and prints itself with the result that `solve` gives for the same inputs."""
    plan = json.loads((EXAMPLES / "wizard_vs_acrobat" / "plans" / "motion.json").read_text(encoding="utf-8"))
    key = next(k for k in plan["keys"] if k["slot"] == "acrobat@b11")
    key["bones"]["LL"] = [110, 0, 0]
    start = tmp_path / "motion.json"
    start.write_text(json.dumps(plan), encoding="utf-8")
    argv = ["wizard_vs_acrobat", "acrobat@b11", "--plan", str(start), "--root-y", "1.05", "--free", "LUL.x,LL.x",
            "--goal", "left_foot.y=0", "--goal", "left_foot=1.29,0,5.12@0.01", "--above", "head.y=1.5"]
    assert main(argv) == 0
    printed = json.loads(capsys.readouterr().out)
    key["pos"] = [key["pos"][0], 1.05, key["pos"][2]]
    bones, misses = solve(key, forward_kinematics.segments("anime"), [("left_foot", 0.0), ("left_foot", [1.29, 0, 5.12], 0.01)],
                          ["LUL.x", "LL.x"], {}, [("head", 1.5)], limits("anime"))
    assert printed["bones"] == bones and printed["misses_m2"] == round(misses, 6)
    assert printed["command"] == "python -m solver.reblock " + " ".join(argv)


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
