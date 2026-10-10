"""Load library concept cards, validate each against its kind's schema, and match hints to cards.

Matching is deterministic: a hint matches a card when its normalised text equals one of the card's
names, or (failing any exact match) when the hint's trailing words equal a card name; the longest
such name wins. Several different cards at the best level is an ambiguity, never a pick.
"""

import json
import re

import yaml

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema

FOLDERS = {"archetype": "archetypes", "world": "worlds", "object": "ontology/objects"}


def normalize(text):
    return re.sub(r"\s+", " ", re.sub(r"[-_]", " ", text.lower())).strip()


def load_cards(root=ROOT):
    """card_id -> card, validated, in sorted path order."""
    cards = {}
    for kind, folder in FOLDERS.items():
        schema = json.loads((root / "schemas" / "cards" / f"{kind}_card.schema.json").read_text(encoding="utf-8"))
        for path in sorted((root / "library" / folder).glob("*.yaml")):
            card = yaml.safe_load(path.read_text(encoding="utf-8"))
            validate_schema(card, schema)
            if card["card_id"] != path.stem:
                raise ContractError("CARD_ID", "card_id must equal the file name", path.name)
            if card["card_id"] in cards:
                raise ContractError("CARD_ID", "card_id is used by two cards", card["card_id"])
            cards[card["card_id"]] = card
    names = {}
    for card in cards.values():
        for name in card["names"]:
            key = (card["kind"], normalize(name))
            if key in names and names[key] != card["card_id"]:
                raise ContractError("CARD_NAME", "Two cards of one kind share a name",
                                    [key[1], names[key], card["card_id"]])
            names[key] = card["card_id"]
    return cards


def match(text, cards, kinds):
    """(card_id or None, sorted candidate ids) for one hint against cards of the given kinds."""
    words = normalize(text).split()
    exact, trailing = set(), {}
    for card in cards.values():
        if card["kind"] not in kinds:
            continue
        for name in card["names"]:
            name_words = normalize(name).split()
            if name_words == words:
                exact.add(card["card_id"])
            elif len(name_words) < len(words) and words[-len(name_words):] == name_words:
                trailing[card["card_id"]] = max(trailing.get(card["card_id"], 0), len(name_words))
    if exact:
        found = sorted(exact)
    elif trailing:
        best = max(trailing.values())
        found = sorted(card_id for card_id, size in trailing.items() if size == best)
    else:
        found = []
    return (found[0] if len(found) == 1 else None), found
