"""S09: object internals per beat; each change is tied to a hand contact (or a holding hand) and an S08 interaction."""

import copy
import json

import pytest
from conftest import ROOT
from ugc_scene import glasses, ugc_plans

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


def at_start_unfold():
    """F-161's case: b02 opens the temples as it starts, 1.5, while its hand touch lands at its end, 3.5."""
    plan = copy.deepcopy(ugc_plans()["temporal"])
    next(f for f in next(b for b in plan["beats"] if b["id"] == "b02")["effects"] if f["property"] == "temples")["at"] = "start"
    return glasses("hand_role", temporal=plan)


def test_a_change_carries_its_instant_and_a_hand_arriving_after_it_is_no_trigger():
    """F-161 (RV-61): each change keeps its instant; a hand counts only if it touches the object by then, or holds it."""
    envelope = at_start_unfold()
    graph, findings = p09_object_state.build(envelope)
    assert findings == [] and [(e["trigger_contact"], [c["t"] for c in e["changes"]])
                               for e in graph["object_state_transition"]] == [("held:ugc_creator.right_hand", [1.5]),
                                                                              ("b03_c1", [5.5])]
    unheld = copy.deepcopy(envelope)  # the right hand never takes the glasses: only the 3.5 touch is left in b02
    for beat in unheld["nodes"]["beats"]["items"]:
        beat["contacts"] = [c for c in beat["contacts"] if c["a"]["part"] != "right_hand"]
    unheld["nodes"]["contacts"]["items"] = [c for c in unheld["nodes"]["contacts"]["items"] if c["body_part"] != "right_hand"]
    assert {f["code"] for f in p09_object_state.build(unheld)[1]} == {"OBJECT_STATE_TRIGGER"}


def test_a_release_before_the_change_is_no_trigger():
    """F-173 (RV-72): a hand that let go of the glasses at 3.5 is not on them when they become worn at 5.5; with no other
    hand there, S09 refuses the change (OBJECT_STATE_TRIGGER)."""
    early = copy.deepcopy(BEFORE)
    for beat in early["nodes"]["beats"]["items"]:
        if beat["id"] == "b03":
            beat["contacts"] = [dict(c, at="start") for c in beat["contacts"] if c["contact_type"] == "release"]
    early["nodes"]["contacts"]["items"] = [dict(c, t=3.5) if c["id"] == "b03_c3" else c
                                           for c in early["nodes"]["contacts"]["items"] if c["id"] not in ("b03_c1", "b03_c2")]
    assert [f["code"] for f in p09_object_state.build(early)[1]] == ["OBJECT_STATE_TRIGGER"]


@pytest.mark.integration
def test_s09_scope(order):
    after = p09_object_state.run(copy.deepcopy(BEFORE), order=order)
    assert check_pass_writes(order, "object_state", BEFORE, after) == []
