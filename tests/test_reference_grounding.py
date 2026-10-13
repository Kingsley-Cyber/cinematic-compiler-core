"""S16.1: the LBN reference fight's preface grounds through S01-S03 with the reference cards."""

import pytest
from conftest import ROOT

from compiler import pipeline
from planner.intent_parser import parse_intent

pytestmark = pytest.mark.unit
SOURCE = (ROOT / "kernel" / "sources" / "lbn-2.3-adv.txt").read_text(encoding="utf-8")
QUERY = SOURCE[:SOURCE.index("{")].strip()


def test_cast_lines_and_prop_lists_are_literal_hints():
    parsed = parse_intent(QUERY)["parsed"]
    assert parsed["entities_hinted"] == ["lean ninja", "broad ninja"]
    assert parsed["props_hinted"] == ["kunai", "rope dart", "smoke pellet", "shuriken volley"]
    assert (parsed["duration_s"], parsed["fps"], parsed["genre"]) == (10, 24, "anime")
    assert parse_intent("6 seconds live action: wizard vs knight")["parsed"]["entities_hinted"] == ["wizard", "knight"]


def test_equipment_adds_the_substitution_log_after_the_query_props():
    envelope = pipeline.run(QUERY, until="brief")
    props = envelope["nodes"]["props"]["items"]
    assert [p["id"] for p in props] == ["kunai", "rope_dart", "smoke_pellet", "shuriken_volley", "substitution_log"]
    assert props[-1]["hint_evidence"] == {"source": "card", "card_id": "ninja_lean", "field": "equipment"}
    assert (props[3]["count"], props[3]["unit_name"], props[3]["group_name"]) == (3, "shuriken", "volley")
    assert [e["id"] for e in envelope["nodes"]["entities"]["items"]] == ["ninja_lean", "ninja_broad"]


def test_required_terms_pick_the_pillar_world_only_when_the_query_names_it():
    assert pipeline.run(QUERY, until="brief")["scene"]["world"] == "bamboo_courtyard_pillar"
    courtyard = pipeline.run("10 seconds anime fight scene: wizard versus acrobat in a moonlit bamboo courtyard", until="brief")
    assert courtyard["scene"]["world"] == "bamboo_courtyard"
    surfaces = {s["id"]: s for s in pipeline.run(QUERY, until="brief")["nodes"]["surfaces"]["items"]}
    assert surfaces["wooden_pillar"]["ax"] == "pillar at z=6 from y=0 to y=8"


def test_card_negatives_and_object_invariants_become_constraints():
    constraints = pipeline.run(QUERY, until="constraint")["nodes"]["constraints"]["items"]
    negatives = {c["rule"] for c in constraints if c["field"] == "negative" and c["source"]["kind"] != "kernel_invariant"}
    assert negatives == {"no scarf covering head", "no substitution log as a separate fighter",
                         "substitution log is a wooden block NOT a fighter",
                         # owner O54: FINAL's four negatives, through the fighters' cards
                         "no scarf covering head or face", "no scarf physics errors", "no floating limbs",
                         "no inverted gravity errors"}
    objects = {c["rule"] for c in constraints if c["id"].startswith("c_obj_")}  # S-123: an object card's rules
    assert "substitution log is a WOODEN BLOCK NOT a fighter" in objects


def test_each_prop_records_the_fighter_whose_card_carries_it():
    """Owner O63 (M9-03b): carried_by is the one entity whose archetype card lists the prop as equipment; shared gear
    (two cards list it) and gear nobody lists stay null (interpretation)."""
    import copy

    from planner.card_loader import load_cards
    from planner.query_expander import expand

    props = pipeline.run(QUERY, until="brief")["nodes"]["props"]["items"]
    assert {p["id"]: p["carried_by"] for p in props} == {
        "kunai": "ninja_broad", "rope_dart": "ninja_lean", "smoke_pellet": "ninja_lean", "shuriken_volley": "ninja_broad",
        "substitution_log": "ninja_lean"}
    cards = copy.deepcopy(load_cards())
    cards["ninja_broad"]["equipment"] = [*cards["ninja_broad"]["equipment"], "rope_dart"]
    shared = expand(parse_intent(QUERY), cards)["props"]
    assert {p["id"]: p["carried_by"] for p in shared}["rope_dart"] is None
