"""S03 pass (band constraint): build the constraint graph from kernel + world + archetype rules.

- kernel items with scope `kernel` apply to the scene; `kernel_actor` to every declared entity;
  `kernel_prop` to every declared prop; `scene_reference` items are not applied (reference fight only).
- the matched world card's invariants apply to the scene; each archetype card's invariants apply to
  the entities built from it.
Rules are copied verbatim; a constraint with nothing to apply to is not emitted.
Writes /nodes/constraints, /edges/constraint_application and /invariants; nothing else.
"""

import copy
import json

import yaml

from kernel.canonical import ContractError
from planner.card_loader import load_cards
from planner.dependency_graph import ROOT, load, node_index
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "constraint"
KERNEL = ROOT / "kernel" / "invariants.yaml"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "constraint_graph.schema.json"
KERNEL_SCHEMA = ROOT / "schemas" / "kernel_invariants.schema.json"


def load_kernel():
    document = yaml.safe_load(KERNEL.read_text(encoding="utf-8"))
    validate_schema(document, json.loads(KERNEL_SCHEMA.read_text(encoding="utf-8")))
    return document


def build(scene, entities, props, *, cards, kernel):
    constraints, applications = [], []

    def add(constraint, targets):
        if not targets:
            return
        constraints.append(constraint)
        for kind, identity in targets:
            applications.append({"id": f"{constraint['id']}__{kind}_{identity}", "constraint_id": constraint["id"],
                                 "target": {"kind": kind, "id": identity}})

    entity_targets = [("entity", item["id"]) for item in entities]
    prop_targets = [("prop", item["id"]) for item in props]
    for item in kernel["items"]:
        targets = {"kernel": [("scene", "scene")], "kernel_actor": entity_targets,
                   "kernel_prop": prop_targets, "scene_reference": []}[item["scope"]]
        add({"id": "c_" + item["id"].lower(), "origin": "kernel", "scope": item["scope"], "field": item["field"],
             "rule": item["text"], "source": {"kind": "kernel_invariant", "ref": item["id"],
                                              "version": f"{kernel['version']}:{kernel['status']}"},
             "reference_labels": list(item["reference_labels"]), "status": kernel["status"],
             "enforcement": "required"}, targets)
    if scene["world"]:
        world = cards[scene["world"]]
        for row in world["invariants"]:
            add({"id": f"c_world_{world['card_id']}_{row['id']}", "origin": "world", "scope": "world",
                 "field": "invariant", "rule": row["rule"],
                 "source": {"kind": "card", "ref": world["card_id"],
                            "version": f"{world['card_version']}:{world['status']}"},
                 "reference_labels": [], "status": world["status"], "enforcement": "required"}, [("scene", "scene")])
    by_card = {}
    for item in entities:
        by_card.setdefault(item["card_id"], []).append(("entity", item["id"]))
    for card_id, targets in by_card.items():
        card = cards[card_id]
        for row in card["invariants"]:
            add({"id": f"c_arch_{card_id}_{row['id']}", "origin": "archetype", "scope": "archetype",
                 "field": "invariant", "rule": row["rule"],
                 "source": {"kind": "card", "ref": card_id, "version": f"{card['card_version']}:{card['status']}"},
                 "reference_labels": [], "status": card["status"], "enforcement": "required"}, targets)
    invariants = [{"id": row["id"], "band": "constraint", "rule": row["rule"]} for row in constraints]
    return {"constraints": constraints, "applications": applications, "invariants": invariants}


def run(envelope, *, cards=None, kernel=None, order=None):
    """Return a new envelope with S03's paths set; the input envelope is never mutated."""
    order = order or load()
    nodes = envelope.get("nodes", {})
    if "scene" not in envelope or not {"entities", "props"} <= set(nodes) or "edges" not in envelope:
        raise ContractError("MISSING_INPUT", "S03 needs /scene and the entities and props groups from S02")
    graph = build(envelope["scene"], nodes["entities"]["items"], nodes["props"]["items"],
                  cards=load_cards() if cards is None else cards, kernel=load_kernel() if kernel is None else kernel)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["constraints"] = {**tag, "items": graph["constraints"]}
    after["edges"]["constraint_application"] = {**tag, "items": graph["applications"]}
    after["invariants"] = graph["invariants"]
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S03 changed paths it does not own", findings)
    return after
