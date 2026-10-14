"""S01 reads a place the library has a world card for (owner, 2026-10-13: the cards name the places)."""

from planner.intent_parser import parse_intent


def test_world_card_names_a_place():
    assert parse_intent("10s anime fight on a desolate wasteland")["parsed"]["setting"] == "desolate wasteland"


def test_place_without_card_is_not_read():
    assert parse_intent("10s anime fight on a lunar crater")["parsed"]["setting"] is None
