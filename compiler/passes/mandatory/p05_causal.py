"""S05 pass (band L1): causal edges from the beat plan, checked, plus scene.quadrant.

Checks: no cycles; while `linear` is true (owner: linear only) a beat has at most one outgoing cause;
a hard cause's target starts at or after the source ends and one source effect satisfies a target requirement (the
same subject, property and value; an effect's `at` says when it takes effect, not what it sets);
a soft cause's target starts at or after the source starts; every link's `why` states a cause (CAUSE_REASON,
validators/cause_reason.py: not a timeline template, an identifier or a sentence about nobody).
Quadrant (owner table): causal = branching + parallel effects + prerequisites (0–2 each); style 0–2;
0–2 → D, 3–4 → B (C when style is 2), 5–6 → A; strata 1 always, 2 if style, 3 if any causal score, 4 if 3 and
load-bearing.
"""

import copy
import json

from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from validators import cause_reason
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "causal"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "causal_graph.schema.json"
ENVELOPE_SCHEMA = ROOT / "schemas" / "cinematic_ir.schema.json"
EPSILON = 1e-9


def _finding(code, message, edge=None):
    return {"code": code, "message": message, "edge": edge}


def _band(value, edges):
    return next(score for limit, score in edges if value <= limit)


def _fact(effect):
    return {k: effect[k] for k in ("subject", "property", "value")}


def edges_and_findings(beats, *, linear=True):
    by_id = {b["id"]: b for b in beats}
    edges, findings = [], []
    for beat in beats:
        if linear and len(beat["causes"]) > 1:
            findings.append(_finding("CAUSE_BRANCHING", "Linear causality allows one outgoing cause per beat", beat["id"]))
        for cause in beat["causes"]:
            edge = {"id": f"{beat['id']}__causes__{cause['to']}", "from": beat["id"], "to": cause["to"],
                    "causal_strength": cause["causal_strength"], "why": cause["why"]}
            edges.append(edge)
            target = by_id.get(cause["to"])
            if target is None:
                findings.append(_finding("CAUSE_TARGET", "Cause target is not a beat", edge["id"]))
                continue
            if cause["causal_strength"] == "hard":
                if target["t"] + EPSILON < beat["t"] + beat["dur"]:
                    findings.append(_finding("CAUSE_TIMING", "A hard cause's target starts before the source ends", edge["id"]))
                if not any(_fact(e) == r for e in beat["effects"] for r in target["requires"]):
                    findings.append(_finding("CAUSE_EFFECT", "No source effect satisfies a target requirement", edge["id"]))
            elif target["t"] + EPSILON < beat["t"]:
                findings.append(_finding("CAUSE_TIMING", "A soft cause's target starts before the source", edge["id"]))
    graph = {}
    for edge in edges:
        graph.setdefault(edge["from"], []).append(edge["to"])
    state = {}

    def visit(node):
        state[node] = "open"
        for nxt in graph.get(node, []):
            if state.get(nxt) == "open" or (nxt not in state and visit(nxt)):
                return True
        state[node] = "done"
        return False
    if any(node not in state and visit(node) for node in sorted(graph)):
        findings.append(_finding("CAUSE_CYCLE", "Causes form a cycle"))
    return edges, findings


def reason_findings(edges, beats, envelope):
    """CAUSE_REASON: each link's reason states why the effect follows, in words that name its beats."""
    return [_finding("CAUSE_REASON", message, edge) for edge, message in cause_reason.problems(edges, beats, envelope)]


def quadrant(beats, edges, scene, *, linear=True, load_bearing=False):
    parallel = _band(max((len(b["effects"]) + len(b["causes"]) for b in beats), default=0), ((1, 0), (2, 1), (10**9, 2)))
    hard = sum(e["causal_strength"] == "hard" for e in edges)
    prerequisites = _band(hard, ((0, 0), (2, 1), (10**9, 2)))
    causal = {"branching": 0, "parallel_effects": parallel, "prerequisites": prerequisites}
    style = int(scene["style_reference"] is not None) + int(any(b["event_type"] == "hold" for b in beats))
    total = sum(causal.values())
    label = "D" if total <= 2 else "A" if total >= 5 else ("C" if style == 2 else "B")
    strata = [1] + ([2] if style else []) + ([3] if total else []) + ([4] if total and load_bearing else [])
    return {"linear": linear, "causal": causal, "style": style, "quadrant": label, "strata": strata,
            "load_bearing": load_bearing}


def run(envelope, *, order=None, load_bearing=False):
    order = order or load()
    if "beats" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S05 needs the S04 beats")
    beats = envelope["nodes"]["beats"]["items"]
    edges, findings = edges_and_findings(beats, linear=True)
    findings += reason_findings(edges, beats, envelope)
    if findings:
        raise StepFailed("S05", findings)
    validate_schema({"causal": edges}, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    scores = quadrant(beats, edges, envelope["scene"], linear=True, load_bearing=load_bearing)
    validate_schema(scores, json.loads(ENVELOPE_SCHEMA.read_text(encoding="utf-8"))["$defs"]["Scene"]["properties"]["quadrant"])
    node = node_index(order)[NODE]
    after = copy.deepcopy(envelope)
    after["edges"]["causal"] = {"band": node["band"], "step_id": node["step_id"], "items": edges}
    chained = envelope["scene"].get("chained_from")
    if chained:  # M5.5: the previous clip's unresolved causes, recorded for this clip to resolve
        scores = {**scores, "carried_causes": [b["id"] for b in chained["open_beats"]]}
    after["scene"]["quadrant"] = scores
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S05 changed paths it does not own", findings)
    return after
