"""S10: every functional verb is proven from the library: preconditions, postconditions, grip and duration."""

import copy
import json

import pytest
import yaml
from conftest import ROOT
from ugc_scene import glasses

from compiler.authoring import StepFailed
from compiler.passes.derived import p10_affordance
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
BEFORE = glasses("object_state")
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "affordance_graph.schema.json").read_text())


def test_glasses_verbs_are_proven_and_linked():
    graph, findings = p10_affordance.build(BEFORE)
    validate_schema(graph, GRAPH)
    assert findings == [] and [(a["id"], a["action"], a["after"]) for a in graph["affordance"]] == [
        ("i01", "unfold", {"temples": "open", "worn": "no"}), ("i02", "put_on", {"temples": "open", "worn": "yes"})]
    assert graph["affordance_dependency"] == [{"id": "i01__enables__i02", "from": "i01", "to": "i02", "relation": "enables",
                                               "via": ["temples"]}]


def test_library_entries_match_their_object_cards():
    cards = {p.stem: yaml.safe_load(p.read_text()) for p in (ROOT / "library" / "ontology" / "objects").glob("*.yaml")}
    for (obj, action), entry in p10_affordance.library().items():
        assert (entry["card"] == "present") == (obj in cards), obj
        if obj in cards:
            states = {s["property"]: s["values"] for s in cards[obj]["states"]}
            assert action in cards[obj]["affordances"] and entry["required_grip"] in cards[obj]["grips"]
            for condition in entry["preconditions"] + entry["postconditions"]:
                assert set(condition["values"]) <= set(states[condition["property"]]), (obj, action)


def edited(change):
    envelope = copy.deepcopy(BEFORE)
    change(envelope)
    return {f["code"] for f in p10_affordance.build(envelope)[1]}


def node(envelope, group, identity):
    return next(n for n in envelope["nodes"][group]["items"] if n["id"] == identity)


@pytest.mark.parametrize("code, change", [
    ("AFFORDANCE_MISSING", lambda e: node(e, "hand_role", "i01").update(verb="polish")),
    ("AFFORDANCE_GRIP", lambda e: node(e, "hand_role", "i01").update(agent_grip="two_hand_temple")),
    ("AFFORDANCE_DURATION", lambda e: node(e, "hand_role", "i02").update(duration=5.0)),
    ("AFFORDANCE_PRECONDITION", lambda e: node(e, "object_state", "glasses@b02")["state"].update(temples="open")),
    ("AFFORDANCE_POSTCONDITION", lambda e: node(e, "object_state", "glasses@b04")["state"].update(worn="no")),
])
def test_each_failure_is_named(code, change):
    assert code in edited(change)


@pytest.mark.integration
def test_s10_scope_and_refusal(order):
    after = p10_affordance.run(copy.deepcopy(BEFORE), order=order)
    assert check_pass_writes(order, "affordance", BEFORE, after) == []
    broken = copy.deepcopy(BEFORE)
    node(broken, "hand_role", "i01").update(verb="polish")
    with pytest.raises(StepFailed):
        p10_affordance.run(broken, order=order)
