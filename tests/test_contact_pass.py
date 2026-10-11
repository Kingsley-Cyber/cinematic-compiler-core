"""S07: contact lifecycle (release, duplicates, one thing per hand) and cross-checks with S06."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, cup

from compiler.passes.mandatory import p07_contact
from kernel.canonical import ContractError, canonical_json
from planner import dynamic_beat_validator
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


def test_a_contact_marked_at_start_happens_when_its_beat_starts():
    """M8.12: a prop already in hand at t=0 — the cup's possess contact moved to the start of b01."""
    def in_hand_from_the_start(plan):
        first = plan["beats"][0]
        first["contacts"][0]["at"] = "start"
        first["requires"][0]["value"] = "wizard"  # in hand from the start; its effect still enables the hard cause

    plan_check = {}
    envelope = cup("contact", edit=lambda p: (in_hand_from_the_start(p), plan_check.update(p)))
    assert [c["t"] for c in envelope["nodes"]["contacts"]["items"] if c["beat"] == "b01"] == [0.0]
    assert dynamic_beat_validator.holds(plan_check["beats"])["coffee_cup"][0][0] == 0.0  # held from t=0, not 1.5
    assert next(s for s in envelope["nodes"]["states"]["items"] if s["id"] == "coffee_cup@b01")["conditions"]["holder"] == \
        "wizard"


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


def _held_then_released(release_beat):
    """x holds prop k from 0.0; the release at 1.0 belongs to `release_beat`; b2 starts at 1.0 with holder x."""
    hand = {"kind": "entity", "id": "x"}, {"kind": "prop", "id": "k", "part": "handle"}
    events = [{"id": "b1_c1", "t": 0.0, "beat": "b1", "contact_type": "possess", "body_part": "right_hand", "a": hand[0],
               "b": hand[1]},
              {"id": f"{release_beat}_c1", "t": 1.0, "beat": release_beat, "contact_type": "release",
               "body_part": "right_hand", "a": hand[0], "b": hand[1]}]
    _, findings, intervals = p07_contact.lifecycle(events)
    assert findings == []
    state = {"id": "k@b2", "beat": "b2", "t": 1.0, "subject": {"kind": "prop", "id": "k"}, "conditions": {"holder": "x"}}
    beats = [{"id": "b1", "t": 0.0, "dur": 1.0}, {"id": "b2", "t": 1.0, "dur": 0.5}]
    return p07_contact.cross_check(events, intervals, [state], [], beats)


def test_a_release_at_its_own_beats_start_still_holds_at_that_instant():
    """O23 (M9-02): a throw lets go at its pose (`at: start`), so at the beat's first instant the prop is still in the
    hand; a release that ended the hold in the previous beat does not count (the holder there must be none)."""
    assert _held_then_released("b2") == []
    assert [f["code"] for f in _held_then_released("b1")] == ["HOLDER_CONTACT"]
