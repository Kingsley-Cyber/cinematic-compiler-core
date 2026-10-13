"""S03 gates: schema, determinism, completeness, non-invention; write scope; reference rules stay out."""

import copy
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.passes.mandatory import p03_constraint
from kernel.canonical import ContractError, canonical_json
from planner.card_loader import load_cards
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
CARDS = load_cards()
KERNEL = p03_constraint.load_kernel()
SCHEMA = json.loads((ROOT / "schemas" / "graphs" / "constraint_graph.schema.json").read_text())
QUERIES = ["10 seconds choreographed wizard versus acrobat fight scene in a stone courtyard",
           "ugc 15s, glasses product demo, kitchen counter", "", "dark knight vs ninja in a castle",
           "ninja vs ninja on the rooftop"]


def run(query, **kwargs):
    genre = None if ("ugc" in query or "anime" in query) else "anime"
    return pipeline.run(query, genre=genre, cards=CARDS, **kwargs)


def graph_of(envelope):
    return {"constraints": envelope["nodes"]["constraints"]["items"],
            "applications": envelope["edges"]["constraint_application"]["items"],
            "invariants": envelope["invariants"]}


@pytest.mark.parametrize("query", QUERIES)
def test_schema_gate(query):
    validate_schema(graph_of(run(query)), SCHEMA)


@pytest.mark.parametrize("query", QUERIES)
def test_completeness_and_non_invention(query):
    envelope = run(query)
    graph = graph_of(envelope)
    entities = envelope["nodes"]["entities"]["items"]
    props = envelope["nodes"]["props"]["items"]
    by_id = {c["id"]: c for c in graph["constraints"]}
    targets = {}
    for row in graph["applications"]:
        targets.setdefault(row["constraint_id"], []).append((row["target"]["kind"], row["target"]["id"]))
    assert set(targets) == set(by_id)
    for item in KERNEL["items"]:
        named = all(p03_constraint._held(label, props) for label in item["reference_labels"])  # F-234 (S-121)
        expected = {"kernel": [("scene", "scene")], "scene_reference": [],
                    "kernel_actor": [("entity", e["id"]) for e in entities],
                    "kernel_prop": [("prop", p["id"]) for p in props] if named else []}[item["scope"]]
        cid = "c_" + item["id"].lower()
        assert targets.get(cid, []) == expected, item["id"]
        if expected:
            assert by_id[cid]["rule"] == item["text"]
    world = envelope["scene"]["world"]
    for row in CARDS[world]["invariants"] if world else []:
        assert by_id[f"c_world_{world}_{row['id']}"]["rule"] == row["rule"]
    for card_id in {e["card_id"] for e in entities}:
        for row in CARDS[card_id]["invariants"]:
            constraint = f"c_arch_{card_id}_{row['id']}"
            needed = row.get("requires_prop")  # S-121: a rule that needs a prop the scene lacks is not applied
            if needed and not any(needed in ("any", p["card_id"]) for p in props):
                assert constraint not in by_id
                continue
            assert by_id[constraint]["rule"] == row["rule"]
            expected = sorted(("entity", e["id"]) for e in entities if e["card_id"] == card_id)
            assert sorted(targets[constraint]) == expected
    assert [i["id"] for i in graph["invariants"]] == [c["id"] for c in graph["constraints"]]


def test_reference_fight_rules_are_never_applied():
    for query in QUERIES:
        constraints = graph_of(run(query))["constraints"]
        assert not [c for c in constraints if c["scope"] == "scene_reference"]


@pytest.mark.integration
def test_determinism_gate_is_byte_identical_across_processes():
    outputs = set()
    for seed in ("0", "11", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outputs.add(subprocess.run([sys.executable, "-m", "compiler.pipeline", QUERIES[0], "--genre", "anime"], cwd=ROOT,
                                   capture_output=True, text=True, env=env, check=True).stdout)
    assert outputs == {canonical_json(pipeline.run(QUERIES[0], genre="anime"))}


@pytest.mark.integration
def test_s03_pass_writes_only_its_paths_and_needs_s02(order):
    before = run(QUERIES[0], until="brief")
    snapshot = copy.deepcopy(before)
    after = p03_constraint.run(before, cards=CARDS, kernel=KERNEL, order=order)
    assert before == snapshot
    assert check_pass_writes(order, "constraint", before, after) == []
    assert after["nodes"]["constraints"]["band"] == "constraint" and after["nodes"]["constraints"]["step_id"] == "S03"
    with pytest.raises(ContractError) as error:
        p03_constraint.run(run(QUERIES[0], until="intent"), cards=CARDS, kernel=KERNEL, order=order)
    assert error.value.code == "MISSING_INPUT"


def test_a_rule_naming_a_prop_the_scene_lacks_is_not_applied():
    """F-234 and R20's kunai (S-121): the reference fight's five-prop rule and its no-duplicated-kunai negative stay
    off the glasses; a thrown-weapon rule stays off a ninja with no prop."""
    glasses = graph_of(run("ugc 15s, glasses product demo, kitchen counter"))
    ids = {c["id"] for c in glasses["constraints"]}
    assert not ids & {"c_k_rules_24", "c_k_negative_08", "c_k_negative_09", "c_k_negative_10", "c_k_negative_11"}
    bare = graph_of(run("6 seconds anime fight scene: ninja versus knight in a moonlit bamboo courtyard"))
    assert "c_arch_ninja_thrown_weapon_leaves_hand" not in {c["id"] for c in bare["constraints"]}
