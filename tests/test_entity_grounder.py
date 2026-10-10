"""Object cards become props with copied fields; the card kind decides entity vs prop."""

import pytest

from planner.card_loader import load_cards
from planner.entity_grounder import PROP_FIELDS, prop_from_card
from planner.intent_parser import parse_intent
from planner.query_expander import expand

pytestmark = pytest.mark.unit
CARDS = load_cards()


def test_prop_copies_card_fields_only():
    item = prop_from_card("jacket", CARDS["jacket"], "jacket", {"source": "query", "span": [0, 6], "text": "jacket"})
    assert all(item[field] == CARDS["jacket"][field] for field in PROP_FIELDS)


def test_product_hint_resolves_to_a_prop_not_an_entity():
    result = expand(parse_intent("ugc 15s, glasses product demo"), CARDS)
    assert [p["id"] for p in result["props"]] == ["glasses"] and result["entities"] == []
