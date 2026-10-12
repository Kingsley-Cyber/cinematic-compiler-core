"""solver/interpolation.py and the between-keys report (RV-59a; F-159, F-089): poses between keys as the source declares
them ("Use slerp on all joint rotations. Root positions are exact."), measured at every frame."""

import pytest

from solver import interpolation
from solver.quaternion import matrix, unit_quaternion

pytestmark = pytest.mark.unit


def _same_rotation(a, b):
    """The same rotation matrix (what forward kinematics turns a body by), to 1e-9."""
    return max(abs(u - v) for ra, rb in zip(matrix(a), matrix(b), strict=True) for u, v in zip(ra, rb, strict=True)) < 1e-9


def test_euler_round_trips_the_kernel_convention():
    """`euler` reads a quaternion back as intrinsic XYZ degrees (R = Rx Ry Rz), so a slerped pose feeds forward
    kinematics unchanged; at Y = +-90 degrees (A's root in the fight) the shared X and Z turn is kept as X."""
    for rot in ([30, -20, 15], [-60, 40, 0], [0, 0, -110], [120, 10, -45], [-330, 30, -360],
                [25, 90, 0], [20, -90, 0], [-280, -270, 0], [-340, -90, -360], [-330, 90, -360], [15, 90, 40], [15, -90, 40]):
        assert _same_rotation(interpolation.euler(unit_quaternion(rot)), rot), rot


def test_every_span_of_the_examples_starts_and_ends_on_its_keys():
    """At its two keys an interpolated pose is the key: forward kinematics gives the same points (to a micrometre) for
    every entity's every span in the four examples, so the frames between run from what S13 checks."""
    import json

    from compiler.examples import EXAMPLES
    from solver import forward_kinematics
    for example in ("reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo"):
        envelope = json.loads((EXAMPLES / example / "envelope.json").read_text(encoding="utf-8"))
        metres, keys = forward_kinematics.segments(envelope["scene"]["genre"]), {}
        for key in sorted(envelope["nodes"]["motion"]["items"], key=lambda k: (k["t"], k["id"])):
            keys.setdefault(key["entity"], []).append(key)
        for own in keys.values():
            for a, b in zip(own, own[1:], strict=False):
                for key in (a, b):
                    want = forward_kinematics.points(key, metres)
                    got = forward_kinematics.points(interpolation.pose(a, b, key["t"]), metres)
                    assert max(abs(u - v) for name in want for u, v in zip(want[name], got[name], strict=True)) < 1e-6, \
                        (example, key["id"], a["t"], b["t"])


def test_a_pose_between_keys_runs_from_one_key_to_the_next():
    """At its ends the pose is its keys; between them the root runs straight and every joint is slerped."""
    a = {"t": 1.0, "pos": [0.0, 1.0, 0.0], "rot": [0, 0, 0], "turn": "none", "bones": {"LL": [10, 0, 0], "Sp": [0, 20, 0]}}
    b = {"t": 2.0, "pos": [2.0, 1.0, 4.0], "rot": [0, 90, 0], "turn": "none", "bones": {"LL": [90, 0, 0], "Sp": [0, -20, 0]}}
    start, end, middle = interpolation.pose(a, b, 1.0), interpolation.pose(a, b, 2.0), interpolation.pose(a, b, 1.5)
    assert start["pos"] == a["pos"] and end["pos"] == b["pos"] and middle["pos"] == [1.0, 1.0, 2.0]
    for joint in a["bones"]:
        assert _same_rotation(start["bones"][joint], a["bones"][joint]) and _same_rotation(end["bones"][joint], b["bones"][joint])
    assert _same_rotation(middle["bones"]["LL"], [50, 0, 0]) and _same_rotation(middle["rot"], [0, 45, 0])


def test_a_declared_turn_runs_its_angles_straight():
    """Across a declared flip the root's Euler angles run straight (the S13 edge's euler_axis): halfway through a
    backflip the body is upside down, where a slerp from 0 to -360 would not move it."""
    a = {"t": 5.1, "pos": [0, 2, 4], "rot": [0, 0, 0], "turn": "flip", "bones": {}}
    b = {"t": 5.5, "pos": [0, 2, 4], "rot": [-360, 0, 0], "turn": "none", "bones": {}}
    assert interpolation.pose(a, b, 5.3)["rot"] == [-180.0, 0.0, 0.0]


def test_frames_leave_out_the_keys_and_a_vanished_window():
    """Frames lie strictly between consecutive keys, at the scene's fps, and a vanished body's window has none."""
    keys = {"a": [{"t": 0.0, "pos": [0, 1, 0], "rot": [0, 0, 0], "bones": {}},
                  {"t": 1.0, "pos": [0, 1, 1], "rot": [0, 0, 0], "bones": {}}]}
    assert sorted(t for _, t in interpolation.frames(keys, 4)) == [0.25, 0.5, 0.75]
    assert sorted(t for _, t in interpolation.frames(keys, 4, [("a", 0.4, 0.8)])) == [0.25]


def test_the_report_measures_the_fight_between_keys():
    """RV-59a, RV-59e (F-159, F-089): between keys the fight's bodies no longer overlap nor sink: S13 refuses an overlap
    at any frame (RV-59e) and B's in-between keys clear its side."""
    from validators import between_keys_report
    found = between_keys_report.measure("reference_fight")
    # the crash sank 0.385 m (S-086) and 0.209 m on its tip (S-096); the overlaps were 38 frames (S-086) and 24 (S-096);
    # B's in-between keys (RV-59e, S-097) clear both, with nothing placed on A's rows
    assert found["sinks"] == [] and found["overlaps"] == []


def test_a_declared_turn_under_a_half_turn_is_slerped():
    """RV-108 (F-225): a declared turn under a half turn about its own axis is drawn as the shortest arc; only a half
    turn or more keeps its angles straight. B's 8.5 crash ("flip", from a key at gimbal lock) is the 90-degree tip the
    prompt prints: halfway it has turned 45 degrees about B's side axis, where straight angles strayed 34 degrees."""
    import json

    from compiler.examples import EXAMPLES
    from solver.quaternion import arc_degrees
    envelope = json.loads((EXAMPLES / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    a, b = keys["ninja_broad@b21"], keys["ninja_broad@b22"]
    assert a["turn"] == "flip" and not interpolation.straight(a, b)
    middle = interpolation.pose(a, b, (a["t"] + b["t"]) / 2)["rot"]
    assert abs(arc_degrees(a["rot"], middle) - 45) < 1e-3 and abs(arc_degrees(middle, b["rot"]) - 45) < 1e-3
    flip = {"t": 5.1, "pos": [0, 2, 4], "rot": [0, 0, 0], "turn": "flip", "bones": {}}
    assert interpolation.straight(flip, {**flip, "t": 5.5, "rot": [-360, 0, 0]})

