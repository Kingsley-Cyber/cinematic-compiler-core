"""S04 pass (band L1): accept an authored beat plan; write beats, temporal edges, beat-constraint edges, duration.

Temporal and beat-constraint edges are computed, never authored. Duration comes from the query/flag, else the
last beat end (duration_source: beat_plan_end).
"""

import copy
import json

from compiler.authoring import GateFailed, bind
from kernel.canonical import ContractError
from planner.beat_planner import given_duration, prepare
from planner.dependency_graph import ROOT, load, node_index
from planner.dynamic_beat_validator import validate
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "temporal"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "beat_plan.schema.json"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "temporal_graph.schema.json"
DIGITS = 6


def _temporal_edges(beats):
    edges = []
    for left, right in zip(beats, beats[1:], strict=False):
        end = left["t"] + left["dur"]
        relation = "starts_with" if right["t"] == left["t"] else "precedes" if right["t"] >= end else "overlaps"
        edges.append({"id": f"{left['id']}__{right['id']}", "from": left["id"], "to": right["id"], "relation": relation,
                      "duration": left["dur"], "gap": round(right["t"] - end, DIGITS)})
    return edges


def _beat_constraint_edges(beats, applications):
    applied = {}
    for row in applications:
        if row["target"]["kind"] in ("entity", "prop"):
            applied.setdefault((row["target"]["kind"], row["target"]["id"]), []).append(row["constraint_id"])
    edges = []
    for beat in beats:
        touched = {("entity", beat["actor"])} | {(r["kind"], r["id"]) for r in beat["participants"]}
        for constraint in sorted({c for key in touched for c in applied.get(key, [])}):
            edges.append({"id": f"{beat['id']}__{constraint}", "from": beat["id"], "to": constraint})
    return edges


def build(envelope, plan):
    packet = prepare(envelope)
    bind(packet, plan)
    validate_schema(plan, json.loads(PLAN_SCHEMA.read_text(encoding="utf-8")))
    findings = validate(plan, packet)
    if findings:
        raise GateFailed("S04", findings, packet)
    # the roles are S04's declaration, checked against the contacts (CONSTRAINT_SATISFIABLE); the contacts carry them on
    beats = sorted(({k: copy.deepcopy(v) for k, v in b.items() if k != "roles"} for b in plan["beats"]),
                   key=lambda b: (b["t"], b["id"]))
    graph = {"beats": beats, "temporal": _temporal_edges(beats),
             "beat_constraint": _beat_constraint_edges(beats, envelope["edges"]["constraint_application"]["items"])}
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    duration, source = given_duration(envelope["intent"])
    if duration is None:
        duration, source = round(max(b["t"] + b["dur"] for b in beats), DIGITS), "beat_plan_end"
    return packet, graph, duration, source


def run(envelope, plan, *, order=None):
    """Return (new envelope, packet); the input envelope is never mutated."""
    order = order or load()
    if "constraints" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S04 needs the S02 brief and the S03 constraint graph")
    packet, graph, duration, source = build(envelope, plan)
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["beats"] = {**tag, "items": graph["beats"]}
    after["edges"]["temporal"] = {**tag, "items": graph["temporal"]}
    after["edges"]["beat_constraint"] = {**tag, "items": graph["beat_constraint"]}
    after["scene"]["duration_s"], after["scene"]["duration_source"] = duration, source
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S04 changed paths it does not own", findings)
    return after, packet
