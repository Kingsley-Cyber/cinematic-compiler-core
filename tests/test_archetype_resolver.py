"""Hint -> card matching: exact names first, then trailing words; ties stay ambiguous."""

import copy

import pytest

from planner.archetype_resolver import ENTITY_FIELDS, entity_from_card
from planner.card_loader import load_cards, match

pytestmark = pytest.mark.unit
CARDS = load_cards()
KINDS = {"archetype", "object"}


@pytest.mark.parametrize("hint, expected", [
    ("wizard", "wizard"), ("Mage", "wizard"), ("superman variant", "superman_variant"),
    ("superman-variant", "superman_variant"), ("dark knight", "knight"), ("armored knight", "knight"),
    ("glasses", "glasses"), ("ceramic coffee cup", "coffee_cup"), ("dragon", None)])
def test_match_rules(hint, expected):
    assert match(hint, CARDS, KINDS)[0] == expected


def test_ties_are_ambiguous_not_picked():
    cards = copy.deepcopy(CARDS)
    twin = copy.deepcopy(cards["ninja"])
    twin.update(card_id="shadow_ninja", names=["shadow fighter", "ninja"])
    cards["shadow_ninja"] = twin
    assert match("ninja", cards, KINDS) == (None, ["ninja", "shadow_ninja"])


def test_entity_copies_card_fields_only():
    evidence = {"source": "query", "span": [0, 6], "text": "wizard"}
    item = entity_from_card("wizard", CARDS["wizard"], "wizard", evidence)
    assert all(item[field] == CARDS["wizard"][field] for field in ENTITY_FIELDS)
    assert (item["card_status"], item["hint_evidence"]) == ("draft", evidence)
