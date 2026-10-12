"""S06: replay rules, starting values, conflicts, continuity and possession, write scope, determinism."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, cup

from compiler.passes.mandatory import p06_state
from kernel.canonical import ContractError, canonical_json
from solver.prop_state_machine import replay
from validators import continuity_validator
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
SCHEMA = json.loads((ROOT / "schemas" / "graphs" / "state_graph.schema.json").read_text())


def states(envelope):
    return {s["id"]: s for s in envelope["nodes"]["states"]["items"]}


def test_courtyard_damage_persists_and_every_subject_is_present_at_every_beat():
    envelope = courtyard("state")
    by_id = states(envelope)
    assert by_id["ground@end"]["conditions"]["damage"] == "scorched"
    assert by_id["stone_pillar@end"]["conditions"]["damage"] == "cracked"
    assert by_id["bamboo_wall@end"]["conditions"]["damage"] == "cut"
    assert len(by_id) == (len(envelope["nodes"]["beats"]["items"]) + 1) * 5
    validate_schema({"states": envelope["nodes"]["states"]["items"],
                     "state_transition": envelope["edges"]["state_transition"]["items"]}, SCHEMA)


def test_pos_is_authoritative_from_the_beat_and_otherwise_labelled_carried():
    by_id = states(courtyard("state"))
    assert by_id["acrobat@b01"]["pos_source"] == "beat" and by_id["acrobat@b01"]["pos"] == [0, 0.96, 0]  # anime pelvis, O72, O85
    assert by_id["acrobat@b09"]["pos_source"] == "carried"
    assert by_id["acrobat@b09"]["pos"] == by_id["acrobat@b08"]["pos"]
    assert by_id["wizard@b01"]["pos"] is None and by_id["wizard@b01"]["pos_source"] is None


def test_starting_values_come_only_from_a_first_requirement():
    by_id = states(cup("state"))
    assert by_id["coffee_cup@b01"]["conditions"]["fill"] == "full"
    assert by_id["coffee_cup@b01"]["conditions"]["location"] == "unknown"
    assert by_id["coffee_cup@end"]["conditions"] == {"fill": "partly_full", "holder": "none", "location": "ground"}


def test_every_prop_state_is_known_at_the_first_beat():
    """PROP_FIRST_STATE (M8.12): without the first beat's requirement the cup's holder is unknown at the start."""
    assert continuity_validator.first_states(cup("state")["nodes"]["states"]["items"], ["b01", "b02", "b03"]) == []
    with pytest.raises(ContractError) as error:
        cup("state", edit=lambda p: p["beats"][0]["requires"].pop(0))
    assert [f["code"] for f in error.value.path] == ["PROP_FIRST_STATE"]
    assert "holder unknown at the first beat" in error.value.path[0]["message"]


def test_transitions_name_their_triggering_beats():
    envelope = cup("state")
    edges = {e["to_state"]: e for e in envelope["edges"]["state_transition"]["items"]}
    assert edges["coffee_cup@b03"]["trigger_event"] == ["b02"]
    assert {c["property"] for c in edges["coffee_cup@end"]["changes"]} == {"holder", "location"}


def test_unmet_requirement_and_same_time_conflict_are_refused():
    with pytest.raises(ContractError) as error:
        cup("state", edit=lambda p: p["beats"][2]["requires"].__setitem__(0, {
            "subject": {"kind": "prop", "id": "coffee_cup"}, "property": "holder", "value": "knight"}))
    assert error.value.code == "GATE_FAILED" and error.value.path[0]["code"] == "REPLAY_REQUIRES"
    beats = [{"id": "b01", "t": 0, "dur": 1, "requires": [], "pos": {}, "facing": {},
              "effects": [{"subject": {"kind": "surface", "id": "ground"}, "property": "damage", "value": "cut"}]},
             {"id": "b02", "t": 0.5, "dur": 0.5, "requires": [], "pos": {}, "facing": {},
              "effects": [{"subject": {"kind": "surface", "id": "ground"}, "property": "damage", "value": "scorched"}]}]
    findings = replay(beats, [("surface", "ground")], {("surface", "ground"): ["damage"]}, 1)[2]
    assert [f["code"] for f in findings] == ["STATE_CONFLICT"]


def test_continuity_catches_missing_subjects_and_possession_mismatch():
    envelope = cup("state")
    snapshots = copy.deepcopy(envelope["nodes"]["states"]["items"])
    transitions = envelope["edges"]["state_transition"]["items"]
    subjects = sorted({(s["subject"]["kind"], s["subject"]["id"]) for s in snapshots})
    beat_ids = [b["id"] for b in envelope["nodes"]["beats"]["items"]]
    assert continuity_validator.check(snapshots, transitions, subjects, beat_ids) == []
    next(s for s in snapshots if s["id"] == "coffee_cup@b02")["conditions"]["holder"] = "knight"
    dropped = [s for s in snapshots if s["id"] != "knight@b03"]
    codes = {f["code"] for f in continuity_validator.check(dropped, transitions, subjects, beat_ids)}
    assert codes == {"POSSESSION_MISMATCH", "CONTINUITY_PRESENCE"}


@pytest.mark.integration
def test_s06_writes_only_its_paths_and_is_deterministic(order):
    before = courtyard("causal")
    snapshot = copy.deepcopy(before)
    after = p06_state.run(before, order=order)
    assert before == snapshot and check_pass_writes(order, "state", before, after) == []
    assert canonical_json(after) == canonical_json(p06_state.run(courtyard("causal"), order=order))
    with pytest.raises(ContractError) as error:
        p06_state.run(courtyard("temporal"), order=order)
    assert error.value.code == "MISSING_INPUT"
