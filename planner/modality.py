"""Genre (modality) schemas: per-genre envelope requirements plus the fps default and duration budget."""

import json
from functools import cache

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT
from validators.schema_validator import check_schema


@cache
def load(genre):
    path = ROOT / "schemas" / "modality" / f"{genre}.schema.json"
    if not path.exists():
        raise ContractError("MODALITY_UNKNOWN", "No modality schema for this genre", genre)
    schema = json.loads(path.read_text(encoding="utf-8"))
    check_schema(schema)
    return schema


def default_fps(genre):
    return load(genre)["properties"]["scene"]["properties"]["fps"]["default"]


def duration_budget(genre):
    return load(genre)["properties"]["scene"]["properties"]["duration_s"]["default"]


def guidance(genre):
    return load(genre)["description"]
