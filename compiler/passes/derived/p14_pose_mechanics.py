"""S14 pass (band L4e, computed; PLAN-009): the pose mechanics of every S13 key, computed, never authored.

S-125 adds the step empty: it writes its two groups with no items, so the renumber lands on a green gate before any
mechanic does. Each mechanic (line of action, counterbalance, weight distribution) adds its fields in its own slice;
the camera-dependent ones (silhouette) are computed in S17's `derived` block.
"""

import copy
import json

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "pose_mechanics"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "pose_mechanics_graph.schema.json"


def build(envelope):
    """{pose_mechanics: [...], pose_mechanics_transition: [...]} for the envelope's motion keys."""
    return {"pose_mechanics": [], "pose_mechanics_transition": []}


def run(envelope, *, order=None):
    """Return a new envelope with S14's groups set; the input envelope is never mutated."""
    order = order or load()
    if "motion" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S14 needs the S13 motion graph")
    graph = build(envelope)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["pose_mechanics"] = {**tag, "items": graph["pose_mechanics"]}
    after["edges"]["pose_mechanics_transition"] = {**tag, "items": graph["pose_mechanics_transition"]}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S14 changed paths it does not own", findings)
    return after
