"""Setting -> world card by shared match terms; ties and zero matches stay unresolved."""

import copy

import pytest

from planner.card_loader import load_cards
from planner.world_grounder import ground_world, surfaces_from_card

pytestmark = pytest.mark.unit
CARDS = load_cards()


@pytest.mark.parametrize("setting, expected", [
    ("moonlit bamboo courtyard", "bamboo_courtyard"), ("castle", "medieval_fantasy"),
    ("kitchen counter", "modern_ugc"), ("deep space station", None), (None, None)])
def test_world_matching(setting, expected):
    assert ground_world(setting, CARDS)[0] == expected


def test_world_tie_is_ambiguous():
    cards = copy.deepcopy(CARDS)
    twin = copy.deepcopy(cards["bamboo_courtyard"])
    twin.update(card_id="stone_courtyard", names=["stone courtyard"], match_terms=["stone", "courtyard"])
    cards["stone_courtyard"] = twin
    assert ground_world("courtyard", cards) == (None, ["bamboo_courtyard", "stone_courtyard"])
    assert ground_world("stone courtyard", cards)[0] == "stone_courtyard"


def test_surfaces_are_the_card_surfaces():
    surfaces = surfaces_from_card(CARDS["bamboo_courtyard"])
    assert [s["id"] for s in surfaces] == [s["id"] for s in CARDS["bamboo_courtyard"]["surfaces"]]
