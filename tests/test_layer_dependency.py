"""The layer DAG, envelope layer tags and pass write scopes obey kernel/layer_order.yaml."""

import copy

import pytest
from conftest import empty_envelope

from kernel.canonical import ContractError
from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION
from planner.topological_sort import build_order
from validators.layer_dependency_validator import check_envelope, check_layer_order, check_pass_writes

pytestmark = pytest.mark.unit


def codes(findings):
    return {row["code"] for row in findings}


def node(order, identity):
    return next(row for row in order["nodes"] if row["id"] == identity)


def test_committed_layer_order_passes_every_check(order):
    assert check_layer_order(order) == []
    assert (order["kernel"], order["envelope"], order["version"]) == (KERNEL_VERSION, ENVELOPE_VERSION,
                                                                       LAYER_ORDER_VERSION)


def test_owner_order_effort_before_camera_and_constraint_before_its_checks(order):
    for modality in order["modalities"]:
        sequence = build_order(order, modality)
        position = sequence.index
        assert position("motion") < position("effort") < position("camera") < position("render")
        assert position("kinematic") < position("bartenieff") < position("motion")
        for row in order["nodes"]:
            if "constraint" in row["validated_by"] and row["id"] in sequence:
                assert position("constraint") < position(row["id"])


def test_ugc_layers_run_only_for_ugc_and_feed_kinematics(order):
    ugc = build_order(order, "ugc_ad")
    assert ugc.index("contact") < ugc.index("hand_role") < ugc.index("affordance") < ugc.index("kinematic")
    assert ugc.index("object_state") < ugc.index("affordance")
    for modality in ("anime", "live_action"):
        assert not {"hand_role", "object_state", "affordance"} & set(build_order(order, modality))


def test_build_order_is_deterministic(order):
    assert build_order(order, "anime") == build_order(copy.deepcopy(order), "anime")


def test_cycle_is_refused(order):
    node(order, "effort")["depends_on"].append("camera")
    assert "LAYER_CYCLE" in codes(check_layer_order(order))
    with pytest.raises(ContractError) as error:
        build_order(order, "anime")
    assert error.value.code == "LAYER_CYCLE"


def test_shared_nested_and_unknown_writes_are_refused(order):
    node(order, "causal")["writes"].append("/nodes/beats")
    node(order, "post_generation")["writes"].append("/validation")
    node(order, "render")["writes"].append("/prompt")
    found = codes(check_layer_order(order))
    assert {"SHARED_WRITE", "OVERLAPPING_WRITE", "UNKNOWN_PATH"} <= found


def test_unknown_dependency_validator_modality_and_version_are_refused(order):
    node(order, "camera")["depends_on"].append("lighting")
    node(order, "camera")["validated_by"].append("vibes")
    node(order, "hand_role")["when"] = ["ugc"]
    order["kernel"] = "LBN-2.5"
    assert {"UNKNOWN_DEPENDENCY", "UNKNOWN_VALIDATOR", "UNKNOWN_MODALITY", "VERSION_DRIFT"} <= codes(
        check_layer_order(order))


def test_conditional_node_cannot_depend_on_a_layer_missing_in_its_modality(order):
    node(order, "hand_role")["when"] = ["ugc_ad", "anime"]
    assert "CONDITIONAL_DEPENDENCY" not in codes(check_layer_order(order))
    node(order, "object_state")["when"] = ["ugc_ad", "anime"]
    node(order, "hand_role")["depends_on"].append("affordance")
    node(order, "affordance")["when"] = ["ugc_ad"]
    assert "CONDITIONAL_DEPENDENCY" in codes(check_layer_order(order))


@pytest.mark.parametrize("modality", ["anime", "live_action", "ugc_ad"])
def test_empty_envelope_for_each_modality_has_correct_tags(order, modality):
    assert check_envelope(empty_envelope(order, modality), order) == []


def test_wrong_layer_tag_inactive_data_missing_and_unknown_groups(order):
    envelope = empty_envelope(order, "anime")
    envelope["nodes"]["camera"]["band"] = "L5"
    envelope["nodes"]["hand_role"] = {"band": "L2.5", "items": [{"id": "agent_right"}]}
    envelope["edges"]["lighting"] = {"band": "L4.5", "items": []}
    assert {"LAYER_TAG", "INACTIVE_LAYER_DATA", "UNKNOWN_GROUP"} <= codes(check_envelope(envelope, order))
    ugc = empty_envelope(order, "ugc_ad")
    del ugc["nodes"]["object_state"]
    assert "MISSING_GROUP" in codes(check_envelope(ugc, order))


def test_a_pass_may_change_only_its_own_paths(order):
    before = empty_envelope(order, "anime")
    after = copy.deepcopy(before)
    after["nodes"]["beats"]["items"].append({"id": "beat_1"})
    after["edges"]["temporal"]["items"].append({"id": "beat_1_precedes_beat_2"})
    assert check_pass_writes(order, "temporal", before, after) == []
    after["nodes"]["states"]["items"].append({"id": "staff_held"})
    found = check_pass_writes(order, "temporal", before, after)
    assert [row["subject"][1] for row in found] == ["/nodes/states/items"]
    assert check_pass_writes(order, "lighting", before, after)[0]["code"] == "UNKNOWN_NODE"


def test_owner_decisions_2026_10_10_fix_the_exact_order(order):
    anime, ugc = build_order(order, "anime"), build_order(order, "ugc_ad")
    # F1/F2 (2026-10-11) and S-125 (owner, PLAN-009 naming A): S14 the pose mechanics (every genre), S15 the face
    # (live_action and ugc_ad); effort, camera, render, post-generation S16-S19.
    steps = [f"S{n:02d}" for n in range(1, 20)]
    assert [node(order, n)["step_id"] for n in ugc] == steps
    assert [node(order, n)["step_id"] for n in anime] == steps[:7] + steps[10:14] + steps[15:]
    assert [node(order, n)["step_id"] for n in build_order(order, "live_action")] == steps[:7] + steps[10:]
    assert [node(order, n)["band"] for n in ugc] == [
        "L0", "L0.5", "constraint", "L1", "L1", "L2", "L2", "L2.5", "L2.6", "L2.7",
        "L4a", "L4b", "L4c", "L4e", "L4d", "L5", "L5.5", "L6", "L6.5"]
    assert node(order, "brief")["writes"] == ["/scene", "/nodes/entities", "/nodes/props", "/nodes/surfaces"]
    assert node(order, "temporal")["writes"] == ["/nodes/beats", "/edges/temporal", "/edges/beat_constraint",
                                                 "/scene/duration_s", "/scene/duration_source"]
    assert node(order, "causal")["writes"] == ["/edges/causal", "/scene/quadrant"]
    assert node(order, "intent")["writes"] == ["/intent"]
    assert "/edges/constraint_application" in node(order, "constraint")["writes"]
    assert node(order, "render")["writes"] == ["/nodes/render"]


def test_step_ids_must_be_well_formed_unique_and_rise_with_build_order(order):
    node(order, "temporal")["step_id"], node(order, "causal")["step_id"] = "S05", "S04"
    assert "STEP_ORDER" in codes(check_layer_order(order))
    node(order, "temporal")["step_id"] = "L1.1"
    node(order, "causal")["step_id"] = "S03"
    assert {"STEP_ID", "STEP_ORDER"} <= codes(check_layer_order(order))


def test_step_and_item_layer_tags_are_checked_against_the_owner(order):
    envelope = empty_envelope(order, "anime")
    envelope["edges"]["causal"]["step_id"] = "S04"
    envelope["nodes"]["states"]["items"].append({"id": "staff_held", "band": "L1"})
    found = [row for row in check_envelope(envelope, order) if row["code"] == "LAYER_TAG"]
    assert {row["subject"][0] for row in found} == {"/edges/causal", "/nodes/states"}


def test_edge_groups_need_declared_endpoints_built_no_later(order):
    del order["edge_endpoints"]["causal"]
    assert "EDGE_ENDPOINTS" in codes(check_layer_order(order))
    order = copy.deepcopy(order)
    order["edge_endpoints"]["causal"] = {"from": ["beats"], "to": ["beats"]}
    order["edge_endpoints"]["beat_constraint"]["to"] = ["kinematic"]
    order["edge_endpoints"]["temporal"]["to"] = ["render"]
    found = [row for row in check_layer_order(order) if row["code"] == "EDGE_ENDPOINTS"]
    assert {row["subject"][1] for row in found} >= {"kinematic", "render"}


def test_carve_outs_need_a_later_owner_and_the_most_specific_owner_wins(order):
    before = empty_envelope(order, "anime")
    after = copy.deepcopy(before)
    after["scene"]["quadrant"]["quadrant"] = "A"
    assert check_pass_writes(order, "causal", before, after) == []
    assert check_pass_writes(order, "brief", before, after)[0]["code"] == "WRITE_SCOPE"
    after = copy.deepcopy(before)
    after["scene"]["fps"] = 30
    assert check_pass_writes(order, "brief", before, after) == []
    assert check_pass_writes(order, "causal", before, after)[0]["code"] == "WRITE_SCOPE"
    node(order, "intent")["writes"].append("/scene/genre")
    assert "OVERLAPPING_WRITE" in codes(check_layer_order(order))


def test_projection_steps_write_node_groups_only(order):
    node(order, "render")["writes"].append("/edges/render_links")
    order["edge_endpoints"]["render_links"] = {"from": ["render"], "to": ["render"]}
    assert "PROJECTION" in codes(check_layer_order(order))
