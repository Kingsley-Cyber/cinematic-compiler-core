"""S12: one node per slot, closed values, body-mode coherence, cpcs: extensions labelled."""

import copy

import pytest
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p12_bartenieff
from validators.layer_dependency_validator import check_pass_writes

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["bartenieff"]
PACKET = p12_bartenieff.prepare(courtyard("kinematic"))


def node(plan, slot):
    return next(n for n in plan["nodes"] if n["slot"] == slot)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p12_bartenieff.check(plan, PACKET)}


def test_courtyard_plan_passes():
    assert p12_bartenieff.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


@pytest.mark.parametrize("code, change", [
    ("BARTENIEFF_SLOT", lambda p: p["nodes"].pop(0)),
    ("BARTENIEFF_VOCABULARY", lambda p: node(p, "acrobat@b01").update(connectivity="spiral")),
    ("BARTENIEFF_VOCABULARY", lambda p: node(p, "acrobat@b01").update(initiation="tail")),
    ("BARTENIEFF_VOCABULARY", lambda p: node(p, "acrobat@b01").update(follow_through=["wing"])),
    ("BARTENIEFF_VOCABULARY", lambda p: node(p, "acrobat@b01").update(body_mode="floating")),
    ("BODY_MODE_COHERENCE", lambda p: node(p, "acrobat@b01").update(body_mode="same_side")),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


@pytest.mark.integration
def test_extensions_are_labelled_and_scope_is_respected(order):
    before = courtyard("kinematic")
    after, _ = p12_bartenieff.run(before, PLAN, order=order)
    assert check_pass_writes(order, "bartenieff", before, after) == []
    flagged = {n["id"]: n["extensions"] for n in after["nodes"]["bartenieff"]["items"] if n["extensions"]}
    assert flagged == {"acrobat@b05": ["connectivity"], "wizard@b11": ["connectivity"]}
    assert all(n["connectivity"].startswith("cpcs:") == bool(n["extensions"]) for n in after["nodes"]["bartenieff"]["items"])
