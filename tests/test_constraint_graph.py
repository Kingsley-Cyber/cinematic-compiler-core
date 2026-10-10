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


def graph_of(envelope):
    return {"constraints": envelope["nodes"]["constraints"]["items"],
            "applications": envelope["edges"]["constraint_application"]["items"],
            "invariants": envelope["invariants"]}


@pytest.mark.parametrize("query", QUERIES)
def test_schema_gate(query):
    validate_schema(graph_of(pipeline.run(query, cards=CARDS)), SCHEMA)


@pytest.mark.parametrize("query", QUERIES)
def test_completeness_and_non_invention(query):
    envelope = pipeline.run(query, cards=CARDS)
    graph = graph_of(envelope)
    entities = envelope["nodes"]["entities"]["items"]
    props = envelope["nodes"]["props"]["items"]
    by_id = {c["id"]: c for c in graph["constraints"]}
    targets = {}
    for row in graph["applications"]:
        targets.setdefault(row["constraint_id"], []).append((row["target"]["kind"], row["target"]["id"]))
    assert set(targets) == set(by_id)
    for item in KERNEL["items"]:
        expected = {"kernel": [("scene", "scene")], "scene_reference": [],
                    "kernel_actor": [("entity", e["id"]) for e in entities],
                    "kernel_prop": [("prop", p["id"]) for p in props]}[item["scope"]]
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
            assert by_id[constraint]["rule"] == row["rule"]
            expected = sorted(("entity", e["id"]) for e in entities if e["card_id"] == card_id)
            assert sorted(targets[constraint]) == expected
    assert [i["id"] for i in graph["invariants"]] == [c["id"] for c in graph["constraints"]]


def test_reference_fight_rules_are_never_applied():
    for query in QUERIES:
        constraints = graph_of(pipeline.run(query, cards=CARDS))["constraints"]
        assert not [c for c in constraints if c["scope"] == "scene_reference"]


@pytest.mark.integration
def test_determinism_gate_is_byte_identical_across_processes():
    outputs = set()
    for seed in ("0", "11", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outputs.add(subprocess.run([sys.executable, "-m", "compiler.pipeline", QUERIES[0]], cwd=ROOT,
                                   capture_output=True, text=True, env=env, check=True).stdout)
    assert outputs == {canonical_json(pipeline.run(QUERIES[0]))}


@pytest.mark.integration
def test_s03_pass_writes_only_its_paths_and_needs_s02(order):
    before = pipeline.run(QUERIES[0], until="brief", cards=CARDS)
    snapshot = copy.deepcopy(before)
    after = p03_constraint.run(before, cards=CARDS, kernel=KERNEL, order=order)
    assert before == snapshot
    assert check_pass_writes(order, "constraint", before, after) == []
    assert after["nodes"]["constraints"]["band"] == "constraint" and after["nodes"]["constraints"]["step_id"] == "S03"
    with pytest.raises(ContractError) as error:
        p03_constraint.run(pipeline.run(QUERIES[0], until="intent"), cards=CARDS, kernel=KERNEL, order=order)
    assert error.value.code == "MISSING_INPUT"
