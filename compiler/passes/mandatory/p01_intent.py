"""S01 pass (band L0): write the Intent Document to /intent and nothing else."""

import copy
import json

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load
from planner.intent_parser import parse_intent
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "intent"
SCHEMA = ROOT / "schemas" / "intent_document.schema.json"


# what the parser reports for its own callers (the author's casting reads `ambiguous`); no layer reads them (S-123)
PARSE_DIAGNOSTICS = ("missing", "ambiguous", "confidence")


def run(envelope, query, *, genre=None, duration_s=None, order=None):
    """Return a new envelope with /intent set; the input envelope is never mutated."""
    order = order or load()
    after = copy.deepcopy(envelope)
    parsed = parse_intent(query, genre=genre, duration_s=duration_s)  # the parser's own diagnostics stay out (S-123)
    after["intent"] = {k: v for k, v in parsed.items() if k not in PARSE_DIAGNOSTICS}
    validate_schema(after["intent"], json.loads(SCHEMA.read_text(encoding="utf-8")))
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S01 changed paths it does not own", findings)
    return after
