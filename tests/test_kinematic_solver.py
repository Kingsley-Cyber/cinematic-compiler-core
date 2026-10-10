"""S11: one node per slot, closed cue vocabulary, support agrees with contacts and state."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.authoring import GateFailed
from compiler.passes.derived import p11_kinematic
from kernel.canonical import canonical_json
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["kinematic"]
PACKET = p11_kinematic.prepare(courtyard("contact"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "kinematic_graph.schema.json").read_text())


def node(plan, slot):
    return next(n for n in plan["nodes"] if n["slot"] == slot)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p11_kinematic.check(plan, PACKET)}


def test_courtyard_plan_passes_and_packet_is_stable():
    assert p11_kinematic.check(PLAN, PACKET) == []
    assert canonical_json(PACKET) == canonical_json(p11_kinematic.prepare(courtyard("contact")))
    assert PACKET["packet_sha256"] == PLAN["packet_sha256"]


@pytest.mark.parametrize("code, change", [
    ("KINEMATIC_SLOT", lambda p: p["nodes"].pop()),
    ("KINEMATIC_SLOT", lambda p: p["nodes"].append(copy.deepcopy(p["nodes"][0]))),
    ("KINEMATIC_SLOT", lambda p: p["nodes"][0].update(slot="acrobat@b09")),
    ("KINEMATIC_VOCABULARY", lambda p: node(p, "acrobat@b01").update(balance="wobbly")),
    ("KINEMATIC_VOCABULARY", lambda p: node(p, "acrobat@b01").update(support=["tail"])),
    ("KINEMATIC_SUPPORT", lambda p: node(p, "acrobat@b05").update(support=["left_foot"])),
    ("KINEMATIC_SUPPORT", lambda p: node(p, "acrobat@b04").update(support=["left_foot"])),
    ("KINEMATIC_SUPPORT", lambda p: node(p, "acrobat@b01").update(support=[])),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_a_support_change_in_progress_allows_either_side():
    assert codes(lambda p: node(p, "acrobat@b03").update(support=["left_foot"])) == set()


@pytest.mark.integration
def test_s11_writes_only_its_paths_and_refuses_failed_gates(order):
    before = courtyard("contact")
    snapshot = copy.deepcopy(before)
    after, _ = p11_kinematic.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "kinematic", before, after) == []
    validate_schema({"kinematic": after["nodes"]["kinematic"]["items"],
                     "kinematic_transition": after["edges"]["kinematic_transition"]["items"]}, GRAPH)
    bad = copy.deepcopy(PLAN)
    node(bad, "acrobat@b05").update(support=[])
    with pytest.raises(GateFailed) as failed:
        p11_kinematic.run(before, bad, order=order)
    assert failed.value.step_id == "S11"
