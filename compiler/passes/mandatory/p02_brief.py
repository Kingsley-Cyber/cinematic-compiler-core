"""S02 pass (band L0.5): write /scene and the entities, props and surfaces node groups; nothing else."""

import copy
import json

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from planner.query_expander import expand
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "brief"
NODES_SCHEMA = ROOT / "schemas" / "graphs" / "brief_nodes.schema.json"
ENVELOPE_SCHEMA = ROOT / "schemas" / "cinematic_ir.schema.json"


def run(envelope, *, cards=None, order=None):
    """Return a new envelope with S02's paths set; the input envelope is never mutated."""
    order = order or load()
    if "intent" not in envelope or not isinstance(envelope.get("nodes"), dict):
        raise ContractError("MISSING_INPUT", "S02 needs /intent from S01 and the envelope's nodes container")
    result = expand(envelope["intent"], cards)
    envelope_schema = json.loads(ENVELOPE_SCHEMA.read_text(encoding="utf-8"))
    validate_schema(result["scene"], {"$ref": "#/$defs/SceneS02", "$defs": envelope_schema["$defs"]})
    groups = {key: result[key] for key in ("entities", "props", "surfaces")}
    validate_schema(groups, json.loads(NODES_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    after = copy.deepcopy(envelope)
    after["scene"] = result["scene"]
    for key, items in groups.items():
        after["nodes"][key] = {"band": node["band"], "step_id": node["step_id"], "items": items}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S02 changed paths it does not own", findings)
    return after
