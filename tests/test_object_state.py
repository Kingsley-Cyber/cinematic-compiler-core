"""S09: object internals per beat; each change is tied to a hand contact (or a holding hand) and an S08 interaction."""

import copy
import json

import pytest
from conftest import ROOT
from ugc_scene import glasses

from compiler.authoring import StepFailed
from compiler.passes.derived import p09_object_state
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
BEFORE = glasses("hand_role")
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "object_state_graph.schema.json").read_text())


def test_glasses_internals_and_their_triggers():
    graph, findings = p09_object_state.build(BEFORE)
    validate_schema(graph, GRAPH)
    names = [n["state_name"] for n in graph["object_state"]]
    assert findings == [] and names == ["temples:folded|worn:no", "temples:folded|worn:no", "temples:open|worn:no",
                                        "temples:open|worn:yes", "temples:open|worn:yes"]
    assert [(e["trigger_beat"], e["trigger_contact"], e["interaction"]) for e in graph["object_state_transition"]] == [
        ("b02", "b02_c1", "i01"), ("b03", "b03_c1", "i02")]


def without_contacts(envelope, beat_ids):
    envelope = copy.deepcopy(envelope)
    for beat in envelope["nodes"]["beats"]["items"]:
        if beat["id"] in beat_ids:
            beat["contacts"] = []
    envelope["nodes"]["contacts"]["items"] = [c for c in envelope["nodes"]["contacts"]["items"] if c["beat"] not in beat_ids]
    return envelope


def test_a_holding_hand_is_the_trigger_when_no_hand_touches():
    graph, findings = p09_object_state.build(without_contacts(BEFORE, {"b02"}))
    assert findings == [] and graph["object_state_transition"][0]["trigger_contact"] == "held:ugc_creator.right_hand"


def test_changes_without_a_hand_or_outside_an_interaction_are_refused():
    codes = {f["code"] for f in p09_object_state.build(without_contacts(BEFORE, {"b01", "b02", "b03"}))[1]}
    assert "OBJECT_STATE_TRIGGER" in codes
    envelope = copy.deepcopy(BEFORE)
    envelope["nodes"]["hand_role"]["items"] = []
    assert {f["code"] for f in p09_object_state.build(envelope)[1]} == {"OBJECT_STATE_INTERACTION"}
    with pytest.raises(StepFailed):
        p09_object_state.run(envelope)


@pytest.mark.integration
def test_s09_scope(order):
    after = p09_object_state.run(copy.deepcopy(BEFORE), order=order)
    assert check_pass_writes(order, "object_state", BEFORE, after) == []
