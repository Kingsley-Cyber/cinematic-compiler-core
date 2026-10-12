"""Camera library (S16): grammar, tempo, per-genre conventions and per-archetype idioms, each schema-checked."""

import json
from functools import cache

import yaml

from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema

LIBRARY = ROOT / "library"


def _load(path, schema_name):
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    validate_schema(document, json.loads((ROOT / "schemas" / "cards" / f"{schema_name}.schema.json").read_text(encoding="utf-8")))
    return document


@cache
def grammar():
    return _load(LIBRARY / "camera_grammar.yaml", "camera_grammar")


@cache
def tempo():
    return _load(LIBRARY / "camera_tempo.yaml", "camera_tempo")


def convention(genre):
    return _load(LIBRARY / "camera_conventions" / f"{genre}.yaml", "camera_convention_card")


def idioms(archetypes):
    """{archetype: idioms} from the idiom card each archetype names (its `camera_idioms`, else its own id; F-177)."""
    found = {}
    for archetype in archetypes:
        card = LIBRARY / "archetypes" / f"{archetype}.yaml"
        name = _load(card, "archetype_card").get("camera_idioms", archetype) if card.exists() else archetype
        path = LIBRARY / "camera_idioms" / f"{name}.yaml"
        if path.exists():
            found[archetype] = _load(path, "camera_idiom_card")["idioms"]
    return found
