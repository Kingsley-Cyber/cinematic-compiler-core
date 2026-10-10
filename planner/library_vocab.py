"""Load a library vocabulary (closed value sets for an authored step) and check one value against it."""

import json
from functools import cache

import yaml

from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema


@cache
def load(vocabulary_id):
    document = yaml.safe_load((ROOT / "library" / f"{vocabulary_id}.yaml").read_text(encoding="utf-8"))
    validate_schema(document, json.loads((ROOT / "schemas" / "cards" / "vocabulary.schema.json").read_text(encoding="utf-8")))
    return document


def problems(vocabulary, field, value, parts):
    """Why `value` is not allowed for `field` (empty list when it is)."""
    rule = vocabulary["fields"][field]
    if rule["kind"] == "values":
        return [] if value in rule["values"] else [f"{field}={value} is not in the vocabulary"]
    if rule["kind"] == "parts":
        return [f"{field} part {p} is not one of the entity's parts" for p in value if p not in parts]
    if rule["kind"] == "part_or_core":
        return [] if value == "core" or value in parts else [f"{field}={value} is not a part or core"]
    return []
