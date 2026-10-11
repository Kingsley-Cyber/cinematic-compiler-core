"""S13: convention math, key-pose checks against S04/S06, turn axes, derived quaternions/edges, write scope."""

import copy
import json
import math

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p13_motion
from kernel.canonical import ContractError, canonical_json
from solver import quaternion
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["motion"]
PACKET = p13_motion.prepare(courtyard("bartenieff"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "motion_graph.schema.json").read_text())


def rounded(vector):
    return [round(v, 6) + 0.0 for v in vector]


@pytest.mark.parametrize("rot, vector, expected", [
    ([90, 0, 0], (0, 0, 1), [0, -1, 0]),   # +X pitches the nose down
    ([0, 90, 0], (0, 0, 1), [1, 0, 0]),    # +Y yaws the nose to the performer's left (+X)
    ([0, 0, 90], (1, 0, 0), [0, 1, 0]),    # +Z rolls clockwise: left side up, right shoulder down
])
def test_convention_directions(rot, vector, expected):
    assert rounded(quaternion.apply(quaternion.matrix(rot), vector)) == expected


@pytest.mark.parametrize("rot", [[0, 0, 0], [90, 0, 0], [0, 90, 0], [0, 0, 90], [30, -45, 60], [180, -389.055, 0],
                                 [-120, 75, 200]])
def test_quaternion_round_trips_to_the_same_rotation(rot):
    w, x, y, z = quaternion.quaternion(rot)
    assert w >= 0 and math.isclose(w * w + x * x + y * y + z * z, 1, abs_tol=1e-8)
    from_quat = ((1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)),
                 (2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)),
                 (2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)))
    for row_a, row_b in zip(from_quat, quaternion.matrix(rot), strict=True):
        assert all(math.isclose(a, b, abs_tol=1e-7) for a, b in zip(row_a, row_b, strict=True))


def test_other_conventions_are_refused():
    with pytest.raises(ContractError) as error:
        quaternion.require({"euler_order": "YXZ", "kind": "intrinsic", "handedness": "right", "units": "degrees"})
    assert error.value.code == "ROTATION_CONVENTION"


def key(plan, slot):
    return next(k for k in plan["keys"] if k["slot"] == slot)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p13_motion.check(plan, PACKET)}


def test_a_tipped_root_without_a_turn_reads_its_more_horizontal_axis():
    from solver.euler_solver import basis_for
    turns = PACKET["rotation_convention"]["turns"]
    slide = {"rot": [80, 0, 0], "turn": "none"}          # pitched 80 degrees: the lateral axis stays level
    on_side = {"rot": [0, 0, 80], "turn": "none"}        # rolled 80 degrees: the forward axis stays level
    assert basis_for(slide, None, turns) == "lateral" and basis_for(on_side, None, turns) == "forward"
    assert basis_for({"rot": [0, 30, 0], "turn": "none"}, None, turns) == "forward"


def test_courtyard_keys_pass_and_the_joints_come_from_the_kernel():
    assert p13_motion.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]
    assert PACKET["joints"] == ["Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK"]


@pytest.mark.parametrize("code, change", [
    ("MOTION_SLOT", lambda p: p["keys"].pop(0)),
    ("MOTION_JOINTS", lambda p: key(p, "wizard@b03")["bones"].pop("NK")),
    ("MOTION_JOINTS", lambda p: key(p, "wizard@b03")["bones"].update(TAIL=[0, 0, 0])),
    ("MOTION_POS", lambda p: key(p, "acrobat@b05").update(pos=[1.0, 0, 4.3])),
    ("MOTION_FACING", lambda p: key(p, "wizard@b11").update(rot=[0, 175, 0])),
    ("MOTION_FACING", lambda p: key(p, "acrobat@b13").update(rot=[180, -330, 0])),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b02").update(axis_declaration="Y")),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b02").update(turn="none", axis_declaration="none")),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b05").update(turn="cartwheel", axis_declaration="Z")),
    ("MOTION_AXIS", lambda p: key(p, "wizard@b11").update(turn="spin", axis_declaration="Y")),
    ("MOTION_POSTURE", lambda p: key(p, "acrobat@b12").update(rot=[460, -389.055, 0])),
    ("TURN_LABEL", lambda p: key(p, "acrobat@b12").update(turn="spin", axis_declaration="Y")),  # dodge_flip as a spin
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(LL=[-30, 0, 0])),   # knee hyperextension (O7)
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(LFA=[-170, 0, 0])),  # elbow past 150, no anime allowance
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(NK=[40, 0, 0], HD=[40, 0, 0])),  # neck 80 > 45 + 30
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


@pytest.mark.integration
def test_derived_graph_scope_and_determinism(order):
    before = courtyard("bartenieff")
    snapshot = copy.deepcopy(before)
    after, _ = p13_motion.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "motion", before, after) == []
    nodes, edges = after["nodes"]["motion"]["items"], after["edges"]["motion"]["items"]
    validate_schema({"motion": nodes, "motion_edges": edges}, GRAPH)
    bases = {n["id"]: n["heading_basis"] for n in nodes}
    assert {s for s, b in bases.items() if b == "lateral"} == {"acrobat@b03", "acrobat@b04", "acrobat@b13"}
    assert len(edges) == len(nodes) - len({n["entity"] for n in nodes})
    by_id = {n["id"]: n for n in nodes}
    for edge in edges:
        start, end = by_id[edge["from"]], by_id[edge["to"]]
        assert edge["interpolation"] == ("slerp" if start["turn"] == "none" else "euler_axis")
        assert edge["euler_delta"] == rounded([b - a for a, b in zip(start["rot"], end["rot"], strict=True)])
        assert math.isclose(edge["trajectory"]["distance"], math.dist(start["pos"], end["pos"]), abs_tol=1e-6)
    spin = next(e for e in edges if e["turn"] == "spin")
    assert spin["euler_delta"][1] == -367.26 and spin["slerp_angle"] == 7.26  # slerp alone would lose the full turn
    assert canonical_json(after) == canonical_json(p13_motion.run(courtyard("bartenieff"), PLAN, order=order)[0])


def test_joint_limits_follow_the_owner_table_and_widen_for_anime():
    from compiler.passes.derived.p13_motion import joint_limits
    from solver.euler_solver import limit_findings
    human, anime = joint_limits("live_action"), joint_limits("anime")
    assert human["LL"]["x"] == [0, 135] and anime["LL"]["x"] == [0, 165]       # a hinge stop stays at 0
    assert human["LA"]["x"] == [-180, 60] and anime["LA"]["x"] == [-210, 90]
    assert human["LFA"]["x"] == anime["LFA"]["x"] == [-150, 0]                 # the elbow gets no anime allowance
    pose = {"bones": {j: [0, 0, 0] for j in ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")}}
    pose["bones"]["LL"] = [150, 0, 0]
    assert [f["code"] for f in limit_findings(pose, "s", human)] == ["JOINT_LIMIT"]
    assert limit_findings(pose, "s", anime) == []
