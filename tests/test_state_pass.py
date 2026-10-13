"""S06: replay rules, starting values, conflicts, continuity and possession, write scope, determinism."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, cup
from ugc_scene import glasses as ugc

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


def test_pos_is_authoritative_from_the_beat_and_otherwise_carried():
    """S-123: the label (pos_source) is gone, no layer read it; the carry itself stays."""
    by_id = states(courtyard("state"))
    assert by_id["acrobat@b01"]["pos"] == [0, 0.96, 0]  # from its beat: the anime pelvis, O72, O85
    assert by_id["acrobat@b09"]["pos"] == by_id["acrobat@b08"]["pos"]  # carried
    assert by_id["wizard@b01"]["pos"] is None and "pos_source" not in by_id["wizard@b01"]


def test_starting_values_come_only_from_a_first_requirement():
    by_id = states(cup("state"))
    assert by_id["coffee_cup@b01"]["conditions"]["fill"] == "full"
    # a free prop must start somewhere since RV-48a (F-139), so the property without a first requirement is the wizard's
    assert by_id["wizard@b01"]["conditions"]["possession"] == "unknown"
    assert by_id["coffee_cup@end"]["conditions"] == {"fill": "partly_full", "holder": "none", "location": "ground"}


def test_a_free_prop_starts_somewhere():
    """PROP_FIRST_STATE (F-139, RV-48a): a prop that nobody holds or carries needs its first place; the cup without its
    first location is refused."""
    with pytest.raises(ContractError) as error:
        cup("state", edit=lambda p: p["beats"][0]["requires"].pop())
    assert error.value.code == "GATE_FAILED" and error.value.path[0]["code"] == "PROP_FIRST_STATE"


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
    # O23 (RV-48a): the cup is let go on b03's key pose, its start, so b03 joins the transition into b03
    assert edges["coffee_cup@b03"]["trigger_event"] == ["b02", "b03"]
    assert {c["property"] for c in edges["coffee_cup@b03"]["changes"]} == {"fill", "holder"}
    assert "coffee_cup@end" not in edges                       # it already lay on the ground (F-139: it starts there)


def test_a_change_of_hands_takes_effect_at_its_contact():
    """F-061 (RV-08): a possess at its beat's start hands the prop over at that instant, while the beat's own
    requirement (nobody holds it) still holds; a release at a beat's start frees it then; any other effect waits for
    the beat's end; each transition records the instant its changes take effect."""
    hand, cup_ = {"kind": "entity", "id": "a", "part": "right_hand"}, {"kind": "prop", "id": "cup", "part": None}
    take = {"subject": {"kind": "prop", "id": "cup"}, "property": "holder", "value": "a"}
    beats = [{"id": "b01", "t": 0, "dur": 1, "pos": {}, "facing": {}, "requires": [dict(take, value="none")],
              "effects": [take, dict(take, property="fill", value="empty")],
              "contacts": [{"contact_type": "possess", "a": hand, "b": cup_, "at": "start"}]},
             {"id": "b02", "t": 1, "dur": 1, "pos": {}, "facing": {}, "requires": [take],
              "effects": [dict(take, value="none")],
              "contacts": [{"contact_type": "release", "a": hand, "b": cup_, "at": "start"}]}]
    snapshots, transitions, findings = replay(beats, [("prop", "cup")], {("prop", "cup"): ["fill", "holder"]}, 3)
    by_id = {s["id"]: s["conditions"] for s in snapshots}
    assert findings == [] and by_id["cup@b01"] == {"fill": "unknown", "holder": "a"}
    assert by_id["cup@b02"] == {"fill": "empty", "holder": "none"}
    assert [(e["to_state"], e["t"]) for e in transitions] == [("cup@b02", 1.0)]
    late = [dict(b, contacts=[dict(c, at="end") for c in b["contacts"]]) for b in beats]
    snapshots, _, findings = replay(late, [("prop", "cup")], {("prop", "cup"): ["fill", "holder"]}, 3)
    assert findings == [] and {s["id"]: s["conditions"]["holder"] for s in snapshots}["cup@b01"] == "none"

def test_an_effect_marked_at_start_takes_effect_at_its_beat_start():
    """O91 (RV-07): an effect marked `at: start` commits at its beat's start, any other at its end; each change in a
    transition carries its own instant, and the transition the last of them (F-132)."""
    pellet = {"kind": "prop", "id": "pellet"}
    burst = {"subject": pellet, "property": "smoke", "value": "burst", "at": "start"}
    beats = [{"id": "b01", "t": 0, "dur": 1, "pos": {}, "facing": {}, "contacts": [], "effects": [],
              "requires": [{"subject": pellet, "property": "smoke", "value": "sealed"}]},
             {"id": "b02", "t": 1, "dur": 0.5, "pos": {}, "facing": {}, "contacts": [], "requires": [],
              "effects": [burst, {"subject": pellet, "property": "location", "value": "ground"}]},
             {"id": "b03", "t": 1.2, "dur": 0.6, "pos": {}, "facing": {}, "contacts": [], "requires": [],
              "effects": [{"subject": pellet, "property": "spent", "value": "yes"}]}]
    tables = {("prop", "pellet"): ["location", "smoke", "spent"]}
    snapshots, transitions, findings = replay(beats, [("prop", "pellet")], tables, 3)
    assert findings == [] and {s["id"]: s["conditions"]["smoke"] for s in snapshots}["pellet@b02"] == "burst"
    assert [(e["to_state"], e["t"], [(c["property"], c["t"]) for c in e["changes"]]) for e in transitions] == [
        ("pellet@b02", 1.0, [("smoke", 1.0)]), ("pellet@end", 1.8, [("location", 1.5), ("spent", 1.8)])]
    late = [dict(b, effects=[{k: v for k, v in f.items() if k != "at"} for f in b["effects"]]) for b in beats]
    snapshots, transitions, _ = replay(late, [("prop", "pellet")], tables, 3)
    assert {s["id"]: s["conditions"]["smoke"] for s in snapshots}["pellet@b02"] == "sealed"
    assert [(c["property"], c["t"]) for c in transitions[-1]["changes"]] == [("location", 1.5), ("smoke", 1.5),
                                                                             ("spent", 1.8)]


def test_a_beat_s_own_start_effects_are_kept_apart_in_its_state():
    """F-161 (RV-61): a beat's snapshot holds the values after its own at-start effects, and before_own_effects the
    values before them, which its requirements read (REPLAY_REQUIRES); a change of hands at an at-start contact counts."""
    pellet = {"kind": "prop", "id": "pellet"}
    beats = [{"id": "b01", "t": 0, "dur": 1, "pos": {}, "facing": {}, "contacts": [], "effects": [],
              "requires": [{"subject": pellet, "property": "smoke", "value": "sealed"}]},
             {"id": "b02", "t": 1, "dur": 0.5, "pos": {}, "facing": {}, "contacts": [],
              "requires": [{"subject": pellet, "property": "smoke", "value": "sealed"}],
              "effects": [{"subject": pellet, "property": "smoke", "value": "burst", "at": "start"}]},
             {"id": "b03", "t": 1.5, "dur": 0.5, "pos": {}, "facing": {}, "contacts": [], "requires": [], "effects": []}]
    snapshots, _, findings = replay(beats, [("prop", "pellet")], {("prop", "pellet"): ["smoke"]}, 3)
    by_id = {s["id"]: s for s in snapshots}
    assert findings == [] and by_id["pellet@b02"]["conditions"] == {"smoke": "burst"}
    assert by_id["pellet@b02"]["before_own_effects"] == {"smoke": "sealed"}
    assert [s["id"] for s in snapshots if "before_own_effects" in s] == ["pellet@b02"]
    glasses = states(ugc("state"))["glasses@b01"]  # the creator holds the glasses from the first frame (M8.12)
    assert glasses["conditions"]["holder"] == "ugc_creator" and glasses["before_own_effects"] == {"holder": "none"}


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
