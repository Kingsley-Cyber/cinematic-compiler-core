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


# RV-95 (F-206, S-083): the commands that re-blocked the pickups, run from the keys S-080 committed (a62e551), whose
# bones START keeps; `--from a62e551` reads the same keys from git.
START = {"ninja_lean@b19": {"Sp": [28.375, -19.25, -13.125], "LUL": [-82.325, 0, 45.0], "RUL": [-80.0, 0, 30.0],
          "LL": [118.475, 0, 0], "RL": [124.0, 0, 0], "LA": [-60.85, 32.125, 12.25], "RA": [-103.375, 0, -0.5],
          "LFA": [-16.0, 0, 0], "RFA": [-45.375, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]},
         "ninja_lean@b20": {"Sp": [45.0, 45.0, 15.25], "LUL": [-69.975, 0, -23.5], "RUL": [-65.975, 0, -14.0],
          "LL": [102.05, 0, 0], "RL": [109.375, 0, 0], "LA": [-60.0, 0, 0.0], "RA": [-56.2, -10.575, -24.875],
          "LFA": [-30.0, 0, 0], "RFA": [-3.275, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]}}
COMMON = ["--root-y", "0.57", "--goal", "left_foot.y=0", "--goal", "right_foot.y=0", "--above", "left_leg.y=0.08",
          "--above", "right_leg.y=0.08", "--above", "left_ankle.y=0", "--above", "right_ankle.y=0", "--above", "head.y=0.77",
          "--bound", "Sp.x=-30..40"]
COMMANDS = {
    "ninja_lean@b19": ["--free", "Sp.x,Sp.y,Sp.z,LUL.x,RUL.x,LUL.z,RUL.z,LL.x,RL.x,LA.x,LA.y,LA.z,LFA.x,RA.x,RA.z,RFA.x",
                       "--goal", "left_hand=1.18,0.0,4.51", "--goal", "left_foot=0.693,0,3.724@0.01",
                       "--goal", "right_foot=0.461,0,3.852@0.01", "--above", "right_hand.y=0.3", *COMMON],
    "ninja_lean@b20": ["--free", "Sp.x,Sp.y,Sp.z,LUL.x,RUL.x,LUL.z,RUL.z,LL.x,RL.x,RA.x,RA.y,RA.z,RFA.x,LA.x,LA.z,LFA.x",
                       "--goal", "right_hand=1.4,0.0,3.77", "--goal", "left_foot=0.430,0,3.511@0.01",
                       "--goal", "right_foot=0.386,0,3.759@0.01", "--above", "left_hand.y=0.3", *COMMON],
}


def test_the_pickups_re_derive_from_their_recorded_commands(tmp_path, capsys):
    """F-206, F-207 (RV-95): each pickup's committed bones are what its recorded command gives from the key before the
    re-block."""
    plan = json.loads((EXAMPLES / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    committed = {k["slot"]: k["bones"] for k in plan["keys"] if k["slot"] in START}
    for key in plan["keys"]:
        if key["slot"] in START:
            key["bones"], key["pos"] = START[key["slot"]], [key["pos"][0], 0.40, key["pos"][2]]
    before = tmp_path / "motion.json"
    before.write_text(json.dumps(plan), encoding="utf-8")
    for slot, command in COMMANDS.items():
        assert main(["reference_fight", slot, "--plan", str(before), *command]) == 0
        assert json.loads(capsys.readouterr().out)["bones"] == committed[slot]


def test_the_pickups_crouch_on_the_feet_with_one_hand_down():
    """F-110, F-206 (RV-95, owner O18): at 7.5 and 8.0 A crouches on both soles with one hand at its prop and the other
    off the floor, every knee 0.08 m (the thigh's radius) and every ankle over the floor, the head 0.2 m over the pelvis
    and the trunk leaning 70 degrees or less; the feet bear the weight, so the hand is no support."""
    envelope = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    kinematic = {k["id"]: k for k in envelope["nodes"]["kinematic"]["items"]}
    metres = forward_kinematics.segments("anime")
    for slot, hand, other in (("ninja_lean@b19", "left_hand", "right_hand"), ("ninja_lean@b20", "right_hand", "left_hand")):
        points, key = keys[slot]["points"], keys[slot]
        joints = forward_kinematics.joints(key, metres)
        assert abs(points["left_foot"][1]) <= 0.02 and abs(points["right_foot"][1]) <= 0.02
        assert points[hand][1] <= 0.03 and points[other][1] >= 0.3
        assert min(joints["left_knee"][1], joints["right_knee"][1]) >= 0.08 - 1e-3
        assert min(joints["left_ankle"][1], joints["right_ankle"][1]) >= 0
        assert points["head"][1] - points["pelvis"][1] >= 0.2 - 1e-3
        assert (key["rot"][0] % 360) + key["bones"]["Sp"][0] <= 70  # the root's 30 degrees and the spine's lean
        assert kinematic[slot]["support"] == ["left_foot", "right_foot"]
