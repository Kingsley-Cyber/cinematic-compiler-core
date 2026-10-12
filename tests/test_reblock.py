"""solver/reblock.py (RV-35a, F-127): a re-block is re-derived from stated goals, free joints and bounds; the pickups
it re-derived crouch on the feet with one hand down (F-110); and a clearance goal keeps a key's spans clear of another
body between keys (RV-59b, F-159)."""

import json
import math

import pytest
from conftest import ROOT

from solver import forward_kinematics
from solver.reblock import _capsules, clearance, limits, main, solve, solve_key

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


def test_s078_s_lunge_height_is_reached_by_the_hip_alone():
    """B's lunge at 3.4 (S-078): its front sole's height is a hand choice (DEV-33, F-207), given here as the goal; from
    the key before, the hip alone reaches it within a degree of the committed angle. This shows the solver's reach, not
    a re-derivation of the choice (F-226)."""
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


# RV-95 (F-206, S-083), re-solved in RV-95b (F-223, F-226, S-093): the commands that re-blocked the pickups, run from
# the keys S-080 committed (a62e551), whose bones START keeps; `--from a62e551` reads the same keys from git. They state
# every bound S-083's plan stated, each floor with the solver's 1 mm margin (its floors are soft): the knees over 0.08
# m, the ankles over 0.045 m, the head 0.2 m over the pelvis, the trunk within 70 degrees of vertical (the chest over
# the pelvis by 0.5 * cos 70 = 0.171 m); the spine inside the anime limits (O11).
START = {"ninja_lean@b19": {"Sp": [28.375, -19.25, -13.125], "LUL": [-82.325, 0, 45.0], "RUL": [-80.0, 0, 30.0],
          "LL": [118.475, 0, 0], "RL": [124.0, 0, 0], "LA": [-60.85, 32.125, 12.25], "RA": [-103.375, 0, -0.5],
          "LFA": [-16.0, 0, 0], "RFA": [-45.375, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]},
         "ninja_lean@b20": {"Sp": [45.0, 45.0, 15.25], "LUL": [-69.975, 0, -23.5], "RUL": [-65.975, 0, -14.0],
          "LL": [102.05, 0, 0], "RL": [109.375, 0, 0], "LA": [-60.0, 0, 0.0], "RA": [-56.2, -10.575, -24.875],
          "LFA": [-30.0, 0, 0], "RFA": [-3.275, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]}}
COMMON = ["--root-y", "0.57", "--goal", "left_foot.y=0", "--goal", "right_foot.y=0", "--above", "left_leg.y=0.081",
          "--above", "right_leg.y=0.081", "--above", "left_ankle.y=0.046", "--above", "right_ankle.y=0.046",
          "--above", "head.y=0.771", "--above", "chest.y=0.742"]
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
    """F-110, F-206, F-223, F-226 (RV-95, RV-95b; owner O18, R-34): at 7.5 and 8.0 A crouches on both soles with one hand
    at its prop and the other off the floor, every knee 0.08 m (the thigh's radius) over the floor and the head 0.2 m
    over the pelvis; the feet bear the weight, so the hand is no support. The lean is read from the trunk's own vector
    (pelvis to chest). Two stated bounds are not met and are pinned as drawn, for the owner: the trunk leans 70.2 and
    71.2 degrees, over 70, since the hand cannot reach the ground from A's own 0.57 m within it (F-223); the 7.5 ankles
    sit 0.0385 and 0.0263 m over the floor and the 8.0 right 0.0449, under the foot's 0.045 m radius (F-215, F-219)."""
    envelope = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    kinematic = {k["id"]: k for k in envelope["nodes"]["kinematic"]["items"]}
    metres = forward_kinematics.segments("anime")
    drawn = {}
    for slot, hand, other in (("ninja_lean@b19", "left_hand", "right_hand"), ("ninja_lean@b20", "right_hand", "left_hand")):
        points, key = keys[slot]["points"], keys[slot]
        joints = forward_kinematics.joints(key, metres)
        assert abs(points["left_foot"][1]) <= 0.02 and abs(points["right_foot"][1]) <= 0.02
        assert points[hand][1] <= 0.03 and points[other][1] >= 0.3
        assert min(joints["left_knee"][1], joints["right_knee"][1]) >= 0.08
        assert points["head"][1] - points["pelvis"][1] >= 0.2
        trunk = [c - p for c, p in zip(joints["chest"], joints["pelvis"], strict=True)]
        drawn[slot] = (round(math.degrees(math.acos(trunk[1] / math.hypot(*trunk))), 1),
                       round(joints["left_ankle"][1], 4), round(joints["right_ankle"][1], 4))
        assert kinematic[slot]["support"] == ["left_foot", "right_foot"]
    assert drawn == {"ninja_lean@b19": (70.2, 0.0385, 0.0263), "ninja_lean@b20": (71.2, 0.0484, 0.0449)}


def test_the_solver_s_capsules_are_forward_kinematics():
    """The clearance composes each chain's rotations once; on every key of the four examples its capsules are forward
    kinematics' to 2 micrometres (forward kinematics rounds each joint to a micrometre), far under CLEARANCE_M."""
    for example in ("reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo"):
        envelope = json.loads((EXAMPLES / example / "envelope.json").read_text(encoding="utf-8"))
        genre = envelope["scene"]["genre"]
        metres, radii = forward_kinematics.segments(genre), forward_kinematics.radii(genre)
        for key in envelope["nodes"]["motion"]["items"]:
            exact, fast = forward_kinematics.capsules(key, metres, radii), _capsules(key, metres, radii)
            assert max(abs(u - v) for name in exact for end in (0, 1)
                       for u, v in zip(exact[name][end], fast[name][end], strict=True)) < 2e-6, key["id"]


def test_a_root_component_moves_the_root_inside_its_bound_in_metres():
    """RV-59b: `pos.x` moves the key's root, its change counted in centimetres, its bound stated in metres."""
    metres = forward_kinematics.segments("anime")
    key = _key("wizard_vs_acrobat", "acrobat@b11")
    x = key["pos"][0]
    goal = [("pelvis", [x + 0.05, key["pos"][1], key["pos"][2]])]
    free, _ = solve_key(key, metres, goal, ["pos.x"], {"pos.x": (x - 0.1, x + 0.1)})
    bound, _ = solve_key(key, metres, goal, ["pos.x"], {"pos.x": (x, x + 0.02)})
    assert abs(free["pos"][0] - (x + 0.05)) < 0.001 and free["bones"] == key["bones"]
    assert abs(bound["pos"][0] - (x + 0.02)) < 1e-9


# RV-59b (F-159, S-087): the commands that re-blocked B's paths, run from the keys at 76da0e5, whose values PATH_START
# keeps; `--from 76da0e5` reads the same keys from git.
PATH_START = {"ninja_broad@b09": {"bones": {"LA": [-25.2, 1.2, 14], "LFA": [-29.2, 0, 0]}},
              "ninja_broad@b11": {"pos": [-0.39, 1.07, 4.51],
                                  "bones": {"LUL": [-74.7, -0.1, 10.3], "RUL": [-14.8, -0.4, -4.5], "LL": [50, 0, 0],
                                            "RL": [31.1, 0, 0]}}}
PATH_COMMANDS = {
    "ninja_broad@b09": ["--free", "LA.x,LA.z,LFA.x", "--goal", "left_foot=1.005,0.0392,4.8579",
                        "--goal", "right_foot=1.8882,-0.0003,4.2357", "--bound", "LA.x=-70.2..19.8", "--bound", "LA.z=-31..59",
                        "--bound", "LFA.x=-74.2..15.8", "--clear", "ninja_lean"],
    "ninja_broad@b11": ["--free", "pos.x,pos.z,LUL.x,LUL.z,RUL.x,RUL.z,LL.x,RL.x", "--goal", "left_foot=-0.6198,0.0022,4.7869",
                        "--goal", "right_foot=0.3178,0.1352,4.3241", "--bound", "pos.x=-0.54..-0.24",
                        "--bound", "pos.z=4.36..4.66",
                        "--bound", "LUL.x=-119.7..-29.7", "--bound", "LUL.z=-34.7..55.3", "--bound", "RUL.x=-59.8..30.2",
                        "--bound", "RUL.z=-49.5..40.5", "--bound", "LL.x=5..95", "--bound", "RL.x=-13.9..76.1",
                        "--clear", "ninja_lean"],
}


def _path_start_plan():
    plan = json.loads((EXAMPLES / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    for key in plan["keys"]:
        if key["slot"] in PATH_START:
            start = PATH_START[key["slot"]]
            key["pos"] = start.get("pos", key["pos"])
            key["bones"] = {**key["bones"], **start["bones"]}
    return plan


def test_b_s_paths_re_derive_from_their_recorded_commands(tmp_path, capsys):
    """F-159 (RV-59b): each re-blocked key of B is what its recorded command gives from the key before the re-block, the
    feet held where they stood and every angle within 45 degrees of its start."""
    plan = json.loads((EXAMPLES / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    committed = {k["slot"]: k for k in plan["keys"] if k["slot"] in PATH_START}
    before = tmp_path / "motion.json"
    before.write_text(json.dumps(_path_start_plan()), encoding="utf-8")
    for slot, command in PATH_COMMANDS.items():
        assert main(["reference_fight", slot, "--plan", str(before), *command]) == 0
        printed = json.loads(capsys.readouterr().out)
        assert (printed["pos"], printed["bones"]) == (committed[slot]["pos"], committed[slot]["bones"]), slot


def test_the_re_blocked_paths_clear_a_between_keys():
    """F-159 (RV-59b): before the re-block B overlapped A between its keys at 3.7 and 4.4 along the declared
    interpolation; after it, no capsule of B meets one of A at any frame of those keys' spans."""
    envelope = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    after = json.loads((EXAMPLES / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    before = _path_start_plan()
    for slot in PATH_START:
        old, new = (next(k for k in plan["keys"] if k["slot"] == slot) for plan in (before, after))
        assert clearance(before, envelope, slot, ["ninja_lean"], margin=0.0)(old) > 0, slot
        assert clearance(after, envelope, slot, ["ninja_lean"], margin=0.0)(new) == 0, slot


def test_the_floor_term_counts_a_point_under_the_floor_between_keys():
    """RV-59c (F-089): with a floor, the clearance counts each contact point deeper than FLOOR_PENETRATION's 0.15 m
    under it at the key and every frame of its spans. The acrobat standing at 7.6 is clear; dropped 0.3 m its soles
    are 0.3 m under. B's crash from 8.5 to 9.0 sinks a sole whatever B's legs at 9.0 do (measured on S-089: within 45
    degrees of their start the right sole stayed 0.218 m under on straight angles; on the tip RV-108 draws, 0.209 m;
    F-220)."""
    import copy
    wizard = json.loads((EXAMPLES / "wizard_vs_acrobat" / "envelope.json").read_text(encoding="utf-8"))
    plan = json.loads((EXAMPLES / "wizard_vs_acrobat" / "plans" / "motion.json").read_text(encoding="utf-8"))
    cost = clearance(plan, wizard, "acrobat@b11", [], margin=0.0, floor=0.0)
    key = _key("wizard_vs_acrobat", "acrobat@b11")
    dropped = copy.deepcopy(key)
    dropped["pos"][1] -= 0.3
    assert cost(key) == 0 and cost(dropped) > (0.3 - 0.15 - 0.02) ** 2
    fight = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    motion = json.loads((EXAMPLES / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    assert clearance(motion, fight, "ninja_broad@b22", [], margin=0.0, floor=0.0)(_key("reference_fight", "ninja_broad@b22")) > 0

