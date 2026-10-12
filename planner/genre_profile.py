"""Genre profiles (owner O65; FR.7, O36, O37): one card per genre, library/genre_profiles/<genre>.yaml, validated against
schemas/genre_profile.schema.json. Today they carry the body forward kinematics uses (owner O85: body_type)."""

import json
from functools import cache

import yaml

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema


@cache
def load(genre):
    path = ROOT / "library" / "genre_profiles" / f"{genre}.yaml"
    if not path.exists():
        raise ContractError("GENRE_PROFILE_UNKNOWN", "No genre profile for this genre", genre)
    card = yaml.safe_load(path.read_text(encoding="utf-8"))
    validate_schema(card, json.loads((ROOT / "schemas" / "genre_profile.schema.json").read_text(encoding="utf-8")))
    if card["genre"] != genre or card["card_id"] != genre:
        raise ContractError("GENRE_PROFILE_ID", "A genre profile's card_id and genre must equal its file name", path.name)
    return card


def body_type(genre):
    """The genre's body (owner O85): the library/body_segments.yaml entry forward kinematics uses."""
    return load(genre)["body_type"]
