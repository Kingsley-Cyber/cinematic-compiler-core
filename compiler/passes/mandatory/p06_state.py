"""S06 pass (band L2): replay the beat plan into states and state transitions; nothing else is written."""

import copy
import json

from compiler.authoring import StepFailed
from kernel import kernel_files
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from planner.vocabulary import resolve
from solver.prop_state_machine import replay
from validators import continuity_validator
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "state"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "state_graph.schema.json"


def build(envelope):
    nodes = envelope["nodes"]
    entities, props, surfaces = (nodes[k]["items"] for k in ("entities", "props", "surfaces"))
    beats = nodes["beats"]["items"]
    vocabulary = resolve(entities, props, surfaces, kernel_files.load("state_vocabulary"))
    subjects = ([("entity", e["id"]) for e in entities] + [("prop", p["id"]) for p in props] +
                [("surface", s["id"]) for s in surfaces])
    tables = {}
    for kind, sid in subjects:
        table = vocabulary["prop"][sid] if kind == "prop" else vocabulary[kind]
        tables[(kind, sid)] = sorted(table)
    chained = envelope["scene"].get("chained_from") or {}
    carried = {(s["subject"]["kind"], s["subject"]["id"], prop): value for s in chained.get("end_states", [])
               for prop, value in s["conditions"].items()
               if value != "unknown" and prop in tables.get((s["subject"]["kind"], s["subject"]["id"]), [])}
    snapshots, transitions, findings = replay(beats, subjects, tables, envelope["scene"]["duration_s"], carried)
    beat_ids = [b["id"] for b in sorted(beats, key=lambda b: (b["t"], b["id"]))]
    findings += continuity_validator.check(snapshots, transitions, subjects, [b["id"] for b in beats])
    findings += continuity_validator.first_states(snapshots, beat_ids, {p["id"] for p in props if p.get("carried_by")})
    return {"states": snapshots, "state_transition": transitions}, findings


def run(envelope, *, order=None):
    order = order or load()
    if "beats" not in envelope.get("nodes", {}) or "quadrant" not in envelope.get("scene", {}):
        raise ContractError("MISSING_INPUT", "S06 needs the S04 beats and the S05 causal graph")
    graph, findings = build(envelope)
    if findings:
        raise StepFailed("S06", findings)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["states"] = {**tag, "items": graph["states"]}
    after["edges"]["state_transition"] = {**tag, "items": graph["state_transition"]}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S06 changed paths it does not own", findings)
    return after
