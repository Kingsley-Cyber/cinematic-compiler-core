"""S10 pass (band L2.7, derived, UGC): prove every functional verb succeeds.

For each S08 interaction the library/affordances entry for (object card, verb) must exist; its preconditions hold
in the S09 object state when the interaction starts, its postconditions hold once it ends (each read before the
own effects of the beat starting there, as S06's requirements are: F-161, RV-61), the agent hand uses the required
grip, and the interaction lasts within the entry's duration range. Edges: an earlier verb's postconditions
that satisfy a later verb's preconditions on the same object (`enables`).
"""

import copy
import json
from functools import cache

import yaml

from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "affordance"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "affordance_graph.schema.json"
LIBRARY_SCHEMA = ROOT / "schemas" / "cards" / "affordance_library.schema.json"
EPSILON = 1e-9


@cache
def library():
    schema = json.loads(LIBRARY_SCHEMA.read_text(encoding="utf-8"))
    entries = {}
    for path in sorted((ROOT / "library" / "affordances").glob("*.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_schema(document, schema)
        for entry in document["entries"]:
            key = (entry["object"], entry["action"])
            if key in entries:
                raise ContractError("AFFORDANCE_LIBRARY", "One entry per (object, action)", list(key))
            entries[key] = {**entry, "library": document["library_id"]}
    return entries


def _before(node):
    """An object state as it stands before its beat's own effects (S06's `before_own_effects`, carried by S09)."""
    return {**node["state"], **node.get("before_own_effects", {})}


def _holds(conditions, state):
    return all(state.get(c["property"]) in c["values"] for c in conditions)


def build(envelope):
    nodes = envelope["nodes"]
    cards = {p["id"]: p["card_id"] for p in nodes["props"]["items"]}
    states = nodes["object_state"]["items"]
    entries = library()
    affordances, findings = [], []
    for i in sorted(nodes["hand_role"]["items"], key=lambda n: (n["t"], n["id"])):
        own = sorted((s for s in states if s["object"] == i["object"]), key=lambda s: s["t"])
        before = _before(next(s for s in own if s["beat"] == i["beats"][0]))
        after = _before(next((s for s in own if s["t"] >= i["end"] - EPSILON and s["beat"] not in i["beats"]), own[-1]))
        entry = entries.get((cards[i["object"]], i["verb"]))
        if entry is None:
            findings.append({"code": "AFFORDANCE_MISSING", "message": f"No affordance entry for {i['object']} {i['verb']}",
                             "detail": i["id"]})
            continue
        problems = []
        if not _holds(entry["preconditions"], before):
            problems.append(("AFFORDANCE_PRECONDITION", f"{i['verb']} needs {entry['preconditions']} before, found {before}"))
        if not _holds(entry["postconditions"], after):
            problems.append(("AFFORDANCE_POSTCONDITION", f"{i['verb']} must leave {entry['postconditions']}, found {after}"))
        if i["agent_grip"] != entry["required_grip"]:
            problems.append(("AFFORDANCE_GRIP", f"{i['verb']} needs the agent hand in a {entry['required_grip']} grip"))
        low, high = entry["duration_s"]
        if not low - EPSILON <= i["duration"] <= high + EPSILON:
            problems.append(("AFFORDANCE_DURATION", f"{i['verb']} takes {low}-{high} s, not {i['duration']}"))
        findings += [{"code": code, "message": message, "detail": i["id"]} for code, message in problems]
        affordances.append({"id": i["id"], "object": i["object"], "action": i["verb"],
                            "preconditions": entry["preconditions"], "postconditions": entry["postconditions"],
                            "required_grip": entry["required_grip"], "agent_grip": i["agent_grip"], "duration": i["duration"],
                            "duration_range": entry["duration_s"], "before": before, "after": after})
    edges = []
    for x in affordances:
        for y in affordances:
            if x["object"] != y["object"] or x is y or affordances.index(x) > affordances.index(y):
                continue
            produced = {c["property"]: set(c["values"]) for c in x["postconditions"]}
            via = [c["property"] for c in y["preconditions"] if produced.get(c["property"], set()) & set(c["values"])]
            if via:
                edges.append({"id": f"{x['id']}__enables__{y['id']}", "from": x["id"], "to": y["id"],
                              "via": via})
    return {"affordance": affordances, "affordance_dependency": edges}, findings


def run(envelope, *, order=None):
    order = order or load()
    if "object_state" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S10 needs the S09 object-state graph")
    graph, findings = build(envelope)
    if findings:
        raise StepFailed("S10", findings)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["affordance"] = {**tag, "items": graph["affordance"]}
    after["edges"]["affordance_dependency"] = {**tag, "items": graph["affordance_dependency"]}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S10 changed paths it does not own", findings)
    return after
