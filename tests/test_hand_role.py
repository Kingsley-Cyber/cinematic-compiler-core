"""S08: hand roles lock for each interaction; verbs, beats, hands, grips, swaps and overlaps are checked."""

import copy
import json

import pytest
import yaml
from conftest import ROOT
from ugc_scene import glasses, ugc_plans

from compiler.passes.derived import p08_hand_role
from kernel.canonical import canonical_json
from planner import library_vocab
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = ugc_plans()["hand_role"]
PACKET = p08_hand_role.prepare(glasses("contact"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "hand_role_graph.schema.json").read_text())


def interaction(plan, identity):
    return next(i for i in plan["interactions"] if i["id"] == identity)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p08_hand_role.check(plan, PACKET)}


def test_glasses_interactions_pass():
    assert p08_hand_role.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def test_every_object_card_grip_is_a_grip_type():
    grips = set(library_vocab.load("grip_types")["fields"]["grip"]["values"])
    for path in sorted((ROOT / "library" / "ontology" / "objects").glob("*.yaml")):
        assert set(yaml.safe_load(path.read_text())["grips"]) <= grips, path.name


@pytest.mark.parametrize("code, change", [
    ("HAND_ROLE_OBJECT", lambda p: interaction(p, "i01").update(verb="zip")),
    ("HAND_ROLE_BEATS", lambda p: interaction(p, "i02").update(beats=["b02", "b04"])),
    ("HAND_ROLE_HANDS", lambda p: interaction(p, "i01").update(support_hand="left_hand")),
    ("HAND_ROLE_HANDS", lambda p: interaction(p, "i01").update(role_template="one_hand")),
    ("HAND_ROLE_GRIP", lambda p: interaction(p, "i01").update(agent_grip="handle_hook")),
    ("HAND_ROLE_GRIP", lambda p: interaction(p, "i01").update(support_hand="none", role_template="one_hand")),
    ("HAND_ROLE_SWAP", lambda p: interaction(p, "i01").update(agent_hand="right_hand", support_hand="none",
                                                              support_grip="none", role_template="one_hand")),
    ("HAND_ROLE_OVERLAP", lambda p: interaction(p, "i02").update(beats=["b02", "b03"])),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_the_support_hand_holds_or_touches_its_object():
    beats = {b["id"]: b for b in PACKET["beats"]}
    assert ["ugc_creator", "left_hand", "glasses"] not in beats["b03"]["held_at_start"]  # i02's support hand only touches
    packet = copy.deepcopy(PACKET)
    next(b for b in packet["beats"] if b["id"] == "b02")["held_at_start"].remove(["ugc_creator", "right_hand", "glasses"])
    findings = p08_hand_role.check(PLAN, packet)  # F-137: i01's support hand now holds nothing and touches nothing
    assert [(f["code"], f["slot"]) for f in findings] == [("HAND_ROLE_SWAP", "i01")] and "support hand" in findings[0]["message"]


@pytest.mark.integration
def test_s08_graph_scope_and_determinism(order):
    before = glasses("contact")
    after, _ = p08_hand_role.run(copy.deepcopy(before), PLAN, order=order)
    assert check_pass_writes(order, "hand_role", before, after) == []
    nodes, edges = after["nodes"]["hand_role"]["items"], after["edges"]["hand_role_transition"]["items"]
    validate_schema({"hand_role": nodes, "hand_role_transition": edges}, GRAPH)
    assert [(n["id"], n["t"], n["end"], n["duration"]) for n in nodes] == [("i01", 1.5, 3.5, 2.0), ("i02", 3.5, 5.5, 2.0)]
    assert edges[0]["agent_hand_changed"] and "no swap" in nodes[0]["role_invariant"]
    assert canonical_json(after) == canonical_json(p08_hand_role.run(copy.deepcopy(before), PLAN, order=order)[0])
