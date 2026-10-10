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
    ("MOTION_ORIENTATION", lambda p: [key(p, s).update(turn="none", axis_declaration="none")
                                      for s in ("acrobat@b03", "acrobat@b04")]),
    ("MOTION_POSTURE", lambda p: key(p, "acrobat@b12").update(rot=[460, -389.055, 0])),
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
