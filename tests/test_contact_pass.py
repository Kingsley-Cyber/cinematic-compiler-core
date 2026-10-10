"""S07: contact lifecycle (release, duplicates, one thing per hand) and cross-checks with S06."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, cup

from compiler.passes.mandatory import p07_contact
from kernel.canonical import ContractError, canonical_json
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
SCHEMA = json.loads((ROOT / "schemas" / "graphs" / "contact_graph.schema.json").read_text())


def failure_codes(edit):
    with pytest.raises(ContractError) as error:
        cup("contact", edit=edit)
    assert error.value.code == "GATE_FAILED"
    return {row["code"] for row in error.value.path}


def test_courtyard_lifecycle_links_every_release_to_what_it_ends():
    envelope = courtyard("contact")
    events = {e["id"]: e for e in envelope["nodes"]["contacts"]["items"]}
    edges = envelope["edges"]["contact"]["items"]
    validate_schema({"contacts": list(events.values()), "contact": edges}, SCHEMA)
    releases = [e for e in edges if e["relation"] == "releases"]
    assert len(releases) == sum(e["contact_type"] == "release" for e in events.values()) == 5
    for edge in releases:
        release, opened = events[edge["from"]], events[edge["to"]]
        assert p07_contact._pair(release) == p07_contact._pair(opened) and opened["t"] <= release["t"]
    assert all(e["t"] == round(next(b for b in envelope["nodes"]["beats"]["items"] if b["id"] == e["beat"])["t"] +
                               next(b for b in envelope["nodes"]["beats"]["items"] if b["id"] == e["beat"])["dur"], 6)
               for e in events.values())


def test_cup_possession_matches_holder():
    envelope = cup("contact")
    kinds = [e["contact_type"] for e in envelope["nodes"]["contacts"]["items"]]
    assert kinds == ["possess", "release", "support"]


@pytest.mark.parametrize("code, edit", [
    ("CONTACT_RELEASE", lambda p: p["beats"][0]["contacts"].clear()),
    ("HOLDER_CONTACT", lambda p: p["beats"][0]["contacts"].clear()),
    ("CONTACT_DUPLICATE", lambda p: p["beats"][1]["contacts"].append(copy.deepcopy(p["beats"][0]["contacts"][0]))),
    ("CONTACT_HAND", lambda p: p["beats"][1]["contacts"].append({
        "contact_type": "possess", "a": {"kind": "entity", "id": "wizard", "part": "right_hand"},
        "b": {"kind": "entity", "id": "knight", "part": "torso"}})),
])
def test_each_contact_rule_rejects_its_violation(code, edit):
    assert code in failure_codes(edit)


def test_prop_change_without_any_contact_is_refused():
    events = []
    states = [{"id": "cup@b01", "subject": {"kind": "prop", "id": "cup"}, "t": 0, "conditions": {"holder": "unknown"}},
              {"id": "cup@end", "subject": {"kind": "prop", "id": "cup"}, "t": 2, "conditions": {"holder": "unknown"}}]
    transitions = [{"id": "x", "from_state": "cup@b01", "to_state": "cup@end", "trigger_event": ["b01"],
                    "changes": [{"property": "fill", "from": "full", "to": "empty"}]}]
    beats = [{"id": "b01", "t": 0, "dur": 1}]
    findings = p07_contact.cross_check(events, [], states, transitions, beats)
    assert [f["code"] for f in findings] == ["PROP_CHANGE_CONTACT"]


@pytest.mark.integration
def test_s07_writes_only_its_paths_and_is_deterministic(order):
    before = courtyard("state")
    snapshot = copy.deepcopy(before)
    after = p07_contact.run(before, order=order)
    assert before == snapshot and check_pass_writes(order, "contact", before, after) == []
    assert canonical_json(after) == canonical_json(p07_contact.run(courtyard("state"), order=order))
    with pytest.raises(ContractError) as error:
        p07_contact.run(courtyard("causal"), order=order)
    assert error.value.code == "MISSING_INPUT"
