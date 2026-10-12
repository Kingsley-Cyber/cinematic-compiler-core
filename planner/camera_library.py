"""Camera library (S16): grammar, tempo, per-genre conventions and per-archetype idioms, each schema-checked."""

import json
from functools import cache

import yaml

from kernel.canonical import ContractError
from planner import library_vocab
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


def rule_problems(rule, playback=("normal",)):
    """[message] for one card rule's structured asks (F-177, RV-71b): every scale, movement and playback is the
    grammar's, playback stays in the card's list, and a hit rule asks for a static hold on every body present at an
    impact scale (owner O92, R-21). Interpretation (Claude's, for owner review): the triggers and asks are read from
    each rule's words."""
    fields = library_vocab.load("camera_subdivisions")["fields"]
    words = {"scale": fields["framing.scale"]["values"], "movement": fields["movement.kind"]["values"],
             "playback": fields["playback.treatment"]["values"]}
    impact = next(r["in"] for r in grammar()["intents"]["impact"] if r["field"] == "framing.scale")
    asks, problems = rule["asks"], []
    for key, known in words.items():
        problems += [f"{rule['id']}: {value} is no {key} of the grammar" for value in asks.get(key, []) if value not in known]
    problems += [f"{rule['id']}: {value} playback is not the card's" for value in asks.get("playback", [])
                 if value not in playback]
    if rule["trigger"] == "hit" and (not set(asks.get("scale", impact)) <= set(impact) or asks.get("movement") != ["static"]
                                     or asks.get("subjects") != "all_present"):
        problems.append(f"{rule['id']}: a hit is a static hold on every body present at {', '.join(impact)} (owner O92)")
    return problems


def _checked(card, rules, playback):
    problems = [p for rule in card[rules] for p in rule_problems(rule, playback)]
    if problems:
        raise ContractError("CAMERA_CARD", "; ".join(problems), card["card_id"])
    return card


def convention(genre):
    card = _load(LIBRARY / "camera_conventions" / f"{genre}.yaml", "camera_convention_card")
    return _checked(card, "conventions", card["playback"])


def idioms(archetypes):
    """{archetype: idioms} from the idiom card each archetype names (its `camera_idioms`, else its own id; F-177)."""
    found = {}
    for archetype in archetypes:
        card = LIBRARY / "archetypes" / f"{archetype}.yaml"
        name = _load(card, "archetype_card").get("camera_idioms", archetype) if card.exists() else archetype
        path = LIBRARY / "camera_idioms" / f"{name}.yaml"
        if path.exists():
            found[archetype] = _checked(_load(path, "camera_idiom_card"), "idioms", ("normal",))["idioms"]
    return found
