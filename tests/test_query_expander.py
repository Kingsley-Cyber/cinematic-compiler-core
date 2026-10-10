"""S02 gates: schema, determinism, completeness, non-invention; genre required; write scope; pipeline order."""

import copy
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.passes.mandatory import p02_brief
from kernel import kernel_files
from kernel.canonical import ContractError, canonical_json
from planner import modality
from planner.card_loader import load_cards
from planner.intent_parser import parse_intent
from planner.query_expander import NEVER_RESOLVED, RESOLVABLE, expand
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
CARDS = load_cards()
CONVENTIONS = kernel_files.load("conventions")
CASES = [("10s anime fight, 24fps, moonlit bamboo courtyard", None),
         ("ugc 15s, glasses product demo, kitchen counter", None),
         ("wizard vs superman variant", "anime"), ("", "live_action"),
         ("dark knight vs ninja in a castle", "anime"),
         ("10 seconds choreographed wizard versus acrobat fight scene in a stone courtyard, wizard with a staff", "anime"),
         ("glasses product demo, kitchen counter", "ugc_ad"), ("ninja vs ninja on the rooftop, 12 fps", "anime")]
SCENE_SCHEMA = {"$ref": "#/$defs/SceneS02",
                "$defs": json.loads((ROOT / "schemas" / "cinematic_ir.schema.json").read_text())["$defs"]}


def brief(query, genre):
    return expand(parse_intent(query, genre=genre), CARDS)


def test_owner_scenarios():
    scene = brief(*CASES[0])["scene"]
    assert (scene["world"], scene["genre"], scene["fps"]) == ("bamboo_courtyard", "anime", 24)
    assert (scene["genre_source"], scene["fps_source"], scene["world_source"]) == ("user", "user", "card:bamboo_courtyard")
    duel = brief(*CASES[2])
    assert [e["id"] for e in duel["entities"]] == ["wizard", "superman_variant"]
    assert {"world", "setting"} <= set(duel["scene"]["missing"])
    assert [e["id"] for e in brief(*CASES[7])["entities"]] == ["ninja"]
    assert brief(*CASES[5])["scene"]["unresolved_hints"] == [
        {"hint": "staff", "field": "props_hinted", "reason": "No card matches this hint."}]


def test_genre_is_required_and_never_inferred():
    for query in ("wizard vs superman variant", "glasses product demo, kitchen counter"):
        with pytest.raises(ContractError) as error:
            expand(parse_intent(query), CARDS)
        assert error.value.code == "GENRE_REQUIRED" and "--genre" in error.value.message
    flagged = brief("castle duel", "anime")["scene"]
    assert (flagged["genre"], flagged["genre_source"]) == ("anime", "flag")


def test_fps_defaults_come_from_the_genre_schema_and_are_marked():
    for genre in ("anime", "live_action", "ugc_ad"):
        scene = brief("castle duel", genre)["scene"]
        assert (scene["fps"], scene["fps_source"]) == (modality.default_fps(genre), "default")
    assert brief(*CASES[7])["scene"]["fps_source"] == "user"


def test_axes_come_from_the_kernel_conventions():
    for case in CASES:
        ax = brief(*case)["scene"]["ax"]
        assert ax["rotation_convention"] == CONVENTIONS["rotation_convention"]
        assert (ax["up"], ax["forward"], ax["ground"]) == (CONVENTIONS["up"], CONVENTIONS["forward"], CONVENTIONS["ground"])


@pytest.mark.parametrize("query, genre", CASES)
def test_schema_gate(query, genre):
    result = brief(query, genre)
    validate_schema(result["scene"], SCENE_SCHEMA)
    nodes = json.loads((ROOT / "schemas" / "graphs" / "brief_nodes.schema.json").read_text())
    validate_schema({k: result[k] for k in ("entities", "props", "surfaces")}, nodes)


@pytest.mark.parametrize("query, genre", CASES)
def test_completeness_gate(query, genre):
    intent = parse_intent(query, genre=genre)
    result = expand(intent, CARDS)
    scene = result["scene"]
    for field in RESOLVABLE:
        assert (scene[field] is None) == (field in scene["missing"]) == (scene[field + "_source"] is None), field
    assert scene["genre_source"] and scene["fps_source"] and scene["missing"][-3:] == list(NEVER_RESOLVED)
    placed = [i["hint"] for i in result["entities"] + result["props"]] + [u["hint"] for u in scene["unresolved_hints"]]
    assert set(placed) == set(intent["parsed"]["entities_hinted"] + intent["parsed"]["props_hinted"])


@pytest.mark.parametrize("query, genre", CASES)
def test_non_invention_gate(query, genre):
    intent = parse_intent(query, genre=genre)
    result = expand(intent, CARDS)
    scene = result["scene"]
    for field in ("genre", "fps", "setting", "style_reference"):
        source = scene[field + "_source"]
        if source in ("user", "flag"):
            assert scene[field] == intent["parsed"][field]
        elif source == "default":
            assert scene[field] == modality.default_fps(scene["genre"])
    if scene["world"]:
        assert scene["ax"]["unit"] == CARDS[scene["world"]]["ax"]["unit"]
    for item in result["entities"] + result["props"]:
        card = CARDS[item["card_id"]]
        assert all(value == card[key] for key, value in item.items() if key in card)
        assert query[slice(*item["hint_evidence"]["span"])] == item["hint_evidence"]["text"] == item["hint"]
    for surface in result["surfaces"]:
        assert any(s["id"] == surface["id"] and s["description"] == surface["description"]
                   for s in CARDS[surface["world_card_id"]]["surfaces"])


@pytest.mark.integration
def test_determinism_gate_is_byte_identical_across_processes():
    outputs = set()
    for seed in ("0", "7", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outputs.add(subprocess.run([sys.executable, "-m", "planner.query_expander", CASES[5][0], "--genre", "anime"],
                                   cwd=ROOT, capture_output=True, text=True, env=env, check=True).stdout)
    assert outputs == {canonical_json(brief(*CASES[5]))}


@pytest.mark.integration
def test_s02_pass_writes_only_its_paths_and_needs_s01(order):
    after_s01 = pipeline.run(CASES[0][0], until="intent")
    snapshot = copy.deepcopy(after_s01)
    after_s02 = p02_brief.run(after_s01, cards=CARDS, order=order)
    assert after_s01 == snapshot
    assert check_pass_writes(order, "brief", after_s01, after_s02) == []
    assert "duration_s" not in after_s02["scene"] and "quadrant" not in after_s02["scene"]
    assert after_s02["nodes"]["surfaces"]["band"] == "L0.5" and after_s02["nodes"]["surfaces"]["step_id"] == "S02"
    with pytest.raises(ContractError) as error:
        p02_brief.run(pipeline.skeleton(), cards=CARDS, order=order)
    assert error.value.code == "MISSING_INPUT"


@pytest.mark.integration
def test_pipeline_runs_in_dag_order_and_requires_a_genre():
    envelope = pipeline.run(CASES[5][0], genre="anime")
    assert envelope["intent"]["step_id"] == "S01" and envelope["scene"]["genre"] == "anime"
    assert [row["pass"] for row in envelope["provenance"]["pass_history"]] == ["p01_intent", "p02_brief", "p03_constraint"]
    with pytest.raises(ContractError) as error:
        pipeline.run(CASES[5][0])
    assert error.value.code == "GENRE_REQUIRED"
    with pytest.raises(ContractError) as error:
        pipeline.run(CASES[0][0], until="hand_role")  # anime (read from the query): the UGC step does not exist
    assert error.value.code == "PIPELINE_TARGET"
