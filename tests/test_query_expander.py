"""S02 gates: schema, determinism, completeness, non-invention; pass write scope; pipeline order."""

import copy
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.passes.mandatory import p02_brief
from kernel.canonical import ContractError, canonical_json
from planner.card_loader import load_cards
from planner.intent_parser import parse_intent
from planner.query_expander import NEVER_RESOLVED, SCENE_FIELDS, expand
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
CARDS = load_cards()
QUERIES = ["10s anime fight, 24fps, moonlit bamboo courtyard", "ugc 15s, glasses product demo, kitchen counter",
           "wizard vs superman variant", "", "dark knight vs ninja in a castle",
           "10 seconds choreographed wizard versus acrobat fight scene in a stone courtyard, wizard with a staff",
           "glasses product demo, kitchen counter", "ninja vs ninja on the rooftop, 12 fps"]


def test_owner_scenarios():
    anime = expand(parse_intent(QUERIES[0]), CARDS)["scene"]
    assert (anime["world"], anime["genre"], anime["fps"]) == ("bamboo_courtyard", "anime", 24)
    assert anime["sources"]["world"] == "card:bamboo_courtyard" and anime["sources"]["fps"] == "intent:query"
    duel = expand(parse_intent("wizard vs superman variant"), CARDS)
    assert [e["id"] for e in duel["entities"]] == ["wizard", "superman_variant"]
    assert {"duration_s", "fps", "genre", "world", "ax"} <= set(duel["scene"]["missing"])
    twins = expand(parse_intent(QUERIES[7]), CARDS)
    assert [e["id"] for e in twins["entities"]] == ["ninja"]
    staff = expand(parse_intent(QUERIES[5]), CARDS)["scene"]["unresolved_hints"]
    assert staff == [{"hint": "staff", "field": "props_hinted", "reason": "No card matches this hint."}]


def test_genre_only_from_intent_or_a_single_genre_world_card():
    scene = expand(parse_intent("glasses product demo, kitchen counter"), CARDS)["scene"]
    assert (scene["genre"], scene["sources"]["genre"]) == ("ugc_ad", "card:modern_ugc")
    scene = expand(parse_intent("castle duel"), CARDS)["scene"]
    assert scene["genre"] is None and "genre" in scene["missing"]
    flagged = expand(parse_intent("castle duel", genre="anime"), CARDS)["scene"]
    assert (flagged["genre"], flagged["sources"]["genre"]) == ("anime", "intent:flag")


@pytest.mark.parametrize("query", QUERIES)
def test_schema_gate(query):
    result = expand(parse_intent(query), CARDS)
    envelope_schema = json.loads((ROOT / "schemas" / "cinematic_ir.schema.json").read_text())
    validate_schema(result["scene"], {"$ref": "#/$defs/Scene", "$defs": envelope_schema["$defs"]})
    nodes = json.loads((ROOT / "schemas" / "graphs" / "brief_nodes.schema.json").read_text())
    validate_schema({k: result[k] for k in ("entities", "props", "surfaces")}, nodes)


@pytest.mark.parametrize("query", QUERIES)
def test_completeness_gate(query):
    intent = parse_intent(query)
    result = expand(intent, CARDS)
    scene = result["scene"]
    for field in SCENE_FIELDS:
        assert (scene[field] is None) == (field in scene["missing"]) == (field not in scene["sources"]), field
    assert scene["missing"][-3:] == list(NEVER_RESOLVED)
    placed = [i["hint"] for i in result["entities"] + result["props"]] + [u["hint"] for u in scene["unresolved_hints"]]
    hints = intent["parsed"]["entities_hinted"] + intent["parsed"]["props_hinted"]
    assert sorted(placed) == sorted(h for h in hints if h in placed) and set(placed) == set(hints)


@pytest.mark.parametrize("query", QUERIES)
def test_non_invention_gate(query):
    intent = parse_intent(query)
    result = expand(intent, CARDS)
    scene = result["scene"]
    for field, source in scene["sources"].items():
        if source.startswith("intent:"):
            assert scene[field] == intent["parsed"][field]
        else:
            card = CARDS[source.split(":", 1)[1]]
            expected = {"world": card["card_id"], "ax": card["ax"], "genre": (card.get("genres") or [None])[0]}[field]
            assert scene[field] == expected
    for item in result["entities"] + result["props"]:
        card = CARDS[item["card_id"]]
        for key, value in item.items():
            if key in card:
                assert value == card[key], (item["id"], key)
        assert query[slice(*item["hint_evidence"]["span"])] == item["hint_evidence"]["text"] == item["hint"]
    for surface in result["surfaces"]:
        assert any(s["id"] == surface["id"] and s["description"] == surface["description"]
                   for s in CARDS[surface["world_card_id"]]["surfaces"])


@pytest.mark.integration
def test_determinism_gate_is_byte_identical_across_processes():
    outputs = set()
    for seed in ("0", "7", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outputs.add(subprocess.run([sys.executable, "-m", "planner.query_expander", QUERIES[5]], cwd=ROOT,
                                   capture_output=True, text=True, env=env, check=True).stdout)
    assert outputs == {canonical_json(expand(parse_intent(QUERIES[5]), CARDS))}


@pytest.mark.integration
def test_s02_pass_writes_only_its_paths_and_needs_s01(order):
    after_s01 = pipeline.run(QUERIES[0], until="intent")
    snapshot = copy.deepcopy(after_s01)
    after_s02 = p02_brief.run(after_s01, cards=CARDS, order=order)
    assert after_s01 == snapshot
    assert check_pass_writes(order, "brief", after_s01, after_s02) == []
    assert after_s02["nodes"]["surfaces"]["band"] == "L0.5" and after_s02["nodes"]["surfaces"]["step_id"] == "S02"
    with pytest.raises(ContractError) as error:
        p02_brief.run(pipeline.skeleton(), cards=CARDS, order=order)
    assert error.value.code == "MISSING_INPUT"


@pytest.mark.integration
def test_pipeline_runs_in_dag_order_and_assumes_no_genre():
    envelope = pipeline.run(QUERIES[5])
    assert envelope["intent"]["step_id"] == "S01" and envelope["scene"]["genre"] is None
    with pytest.raises(ContractError) as error:
        pipeline.run(QUERIES[1], until="hand_role")
    assert error.value.code == "PIPELINE_TARGET"
    with pytest.raises(ContractError) as error:
        pipeline.run(QUERIES[0], genre="anime", until="constraint")
    assert error.value.code == "PASS_MISSING"
