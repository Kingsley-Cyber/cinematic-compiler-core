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
    # plan F9.2, owner O74: the dodge flip without its declared hang time leaves the gravity arc; a float on a grounded key
    ("MOMENTUM_MISSING", lambda p: node(p, "acrobat@b13").pop("float")),
    ("MOMENTUM_MISSING", lambda p: node(p, "acrobat@b01").update(float=True)),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_a_support_change_in_progress_allows_either_side():
    """S11 allows either side of a support change a beat has in progress at the slot. Since O80 (S-022) no wizard slot
    has one, so the test gives acrobat@b03 an airborne-to-grounded change in progress."""
    packet = copy.deepcopy(PACKET)
    next(s for s in packet["slots"] if s["slot"] == "acrobat@b03")["allowed_support_states"] = ["airborne", "grounded"]
    for support in ([], ["left_foot"]):
        plan = copy.deepcopy(PLAN)
        node(plan, "acrobat@b03").update(support=support, float=False)
        assert not [f for f in p11_kinematic.check(plan, packet) if f["code"] == "KINEMATIC_SUPPORT"]


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


def test_airborne_pickup_needs_a_supported_body_within_reach():
    """AIRBORNE_PICKUP (owner O18, M9-03): the reference fight takes the rope dart (7.5) and the kunai (8.0) from the
    ground crouched; the same pickups with no support, or from out of reach, are refused."""
    from planner.scene_view import slots

    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    document = {"nodes": [{"slot": n["id"], "support": n["support"]} for n in envelope["nodes"]["kinematic"]["items"]]}
    packet = {"slots": slots(envelope)}
    assert p11_kinematic.pickup_findings(document, packet, envelope) == []
    airborne = copy.deepcopy(document)
    next(n for n in airborne["nodes"] if n["slot"] == "ninja_lean@b19")["support"] = []
    refused = p11_kinematic.pickup_findings(airborne, packet, envelope)
    assert [(f["code"], f["message"]) for f in refused] == [
        ("AIRBORNE_PICKUP", "ninja_lean takes the resting rope_dart at 7.5 with no support")]
    far = copy.deepcopy(packet)
    next(s for s in far["slots"] if s["slot"] == "ninja_lean@b20")["pos"] = [-3.0, 0.6, 5.1]
    assert [f["message"] for f in p11_kinematic.pickup_findings(document, far, envelope)] == [
        "ninja_lean takes kunai at 8.0 from 3.81 m away"]  # the kunai rests on [0.6, 0, 4.0] since O77


def test_hang_time_is_anime_only_and_said_in_the_prompt():
    """MOMENTUM_MISSING (plan F9.2, owner O74): live action and UGC follow the arc; anime's hang is printed once a span."""
    from validators import prompt_validator
    live = {**PACKET, "genre": "live_action"}
    assert "MOMENTUM_MISSING" in {f["code"] for f in p11_kinematic.check(PLAN, live)}
    envelope = json.loads((ROOT / "examples" / "wizard_vs_acrobat" / "envelope.json").read_text(encoding="utf-8"))
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    line = "- B hangs in the air 8.60–9.80, longer than a real jump (stylised anime hang time).\n"
    assert line in text
    assert "MOMENTUM_MISSING" in {f["code"] for f in prompt_validator.check(text.replace(line, ""), envelope, "mixed")}

