"""S14 pass (band L4e, computed; PLAN-009): the pose mechanics of every S13 key, computed, never authored.

S-125 added the step empty; S-126 writes each key's line of action. Each mechanic (line of action, counterbalance,
weight distribution) adds its fields in its own slice; the camera-dependent ones (silhouette) are computed in S17's
`derived` block.
"""

import copy
import hashlib
import json

import yaml

from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner import genre_profile
from planner.dependency_graph import ROOT, load, node_index
from solver import forward_kinematics, pose_mechanics
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "pose_mechanics"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "pose_mechanics_graph.schema.json"


def build(envelope):
    """{pose_mechanics: [...], pose_mechanics_transition: [...]} for the envelope's motion keys: one node per key,
    its line of action (PM-3, S-126), its centre of mass and counterbalance (S-127), its weight over S11's supports
    (S-128)."""
    nodes = []
    metres, masses = forward_kinematics.segments(envelope["scene"]["genre"]), forward_kinematics.masses()
    supports = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
    for key in sorted(envelope["nodes"]["motion"]["items"], key=lambda k: (k["t"], k["id"])):
        line = pose_mechanics.line_of_action(key["points"])
        if line is None:
            continue
        joints = forward_kinematics.joints(key, metres)
        com = pose_mechanics.centre_of_mass(joints, masses)
        nodes.append({"id": key["id"], "line_of_action": line, "centre_of_mass": com,
                      "counterbalance": pose_mechanics.counterbalance(joints, com),
                      "weight": pose_mechanics.weight_distribution(_carried(key, joints, supports), com)})
    return {"pose_mechanics": nodes, "pose_mechanics_transition": []}


EXCEPTIONS = ROOT / "kernel" / "weight_exceptions.yaml"
TRUNK = ("torso", "back", "chest", "spine")  # a body on its back or front lies along its trunk, pelvis to chest


def _carried(key, joints, supports):
    """{support point: world point} for the parts S11 says carry this key: a trunk part along its whole length (the
    pelvis and the chest), any other part at its contact point."""
    out = {}
    for part in supports.get(key["id"], []):
        if part in TRUNK:
            out |= {f"{part}:pelvis": joints["pelvis"], f"{part}:chest": joints["chest"]}
        elif (point := forward_kinematics.part_point(key["points"], part)) is not None:
            out[part] = point
    return out


def owner_exceptions(query):
    """{key: reason} the owner keeps for the scene whose query this is (kernel/weight_exceptions.yaml)."""
    digest = hashlib.sha256(query.encode("utf-8")).hexdigest()
    entries = yaml.safe_load(EXCEPTIONS.read_text(encoding="utf-8"))["exceptions"]
    return {e["key"]: f"{e['reason']} [{e['ruling']}]" for e in entries if e["query_sha256"] == digest}


def weight_findings(envelope, graph):
    """WEIGHT_DISTRIBUTION (PLAN-009 PM-2, S-128; refuses from the start, owner 2026-10-13): a pose S11 calls stable
    keeps its centre of mass inside its support base, or outside it by no more than the genre's allowance (owner:
    anime 0.15 m, live action 0.05 m, UGC 0.10 m). Fixed at S13: the pose follows S11's intent (owner)."""
    allowance = genre_profile.com_allowance(envelope["scene"]["genre"])
    balance = {k["id"]: k["balance"] for k in envelope["nodes"]["kinematic"]["items"]}
    kept = owner_exceptions(envelope["provenance"]["source_prompt"])
    out, missed = [], set()
    for node in graph["pose_mechanics"]:
        weight = node["weight"]
        if weight is not None and balance.get(node["id"]) == "stable" and weight["margin_m"] < -allowance:
            missed.add(node["id"])
            if node["id"] in kept:
                continue
            out.append({"code": "WEIGHT_DISTRIBUTION", "detail": node["id"],
                        "message": f"{node['id']} is stable (S11) but its centre of mass stands "
                                   f"{-weight['margin_m']:g} m outside its support base ({', '.join(weight['supports'])}; "
                                   f"the genre allows {allowance:g} m): pose it over its supports"})
    out += [{"code": "WEIGHT_DISTRIBUTION", "detail": key, "message": f"the owner's exceptions name {key}, which is not a "
             "stable pose past its support base: the list must stay true"} for key in sorted(set(kept) - missed)]
    return out


def run(envelope, *, order=None):
    """Return a new envelope with S14's groups set; the input envelope is never mutated."""
    order = order or load()
    if not {"motion", "kinematic"} <= set(envelope.get("nodes", {})):
        raise ContractError("MISSING_INPUT", "S14 needs the S13 motion graph and the S11 kinematic graph")
    graph = build(envelope)
    findings = weight_findings(envelope, graph)
    if findings:
        raise StepFailed("S14", findings)
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
