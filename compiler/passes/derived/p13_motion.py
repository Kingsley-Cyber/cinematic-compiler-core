"""S13 pass (band L4c, authored + derived): one Euler key pose per entity per beat, checked against S04.

Authored: root pos/rot, the kernel joints, turn and axis declarations. Checked by solver/euler_solver.py, by
CONTACT_WORLD (solver/contact_world.py) and by BODY_OVERLAP (solver/body_overlap.py: no body through another, RV-49).
Derived: root quaternion per key (solver/quaternion.py) and per-entity follows edges with the Euler delta,
interpolation and root trajectory (solver/trajectory.py).
"""

import json

import yaml

from compiler.authoring import run_authored, seal
from kernel.kernel_files import load as load_kernel
from planner.dependency_graph import ROOT, load
from planner.scene_view import slots, values_in_progress
from solver import body_overlap, contact_world, euler_solver, forward_kinematics, quaternion, trajectory
from validators.schema_validator import validate_schema

NODE, STEP = "motion", "S13"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "motion_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "euler_solving.txt"
SLOT_FIELDS = ("slot", "entity", "beat", "t", "dur", "role", "label", "action", "event_type", "pos", "facing", "state",
               "active_supports")


def joint_limits(genre):
    """library/joint_limits.yaml validated, then widened for the genre (owner O11)."""
    card = yaml.safe_load((ROOT / "library" / "joint_limits.yaml").read_text(encoding="utf-8"))
    validate_schema(card, json.loads((ROOT / "schemas" / "cards" / "joint_limits.schema.json").read_text(encoding="utf-8")))
    return euler_solver.effective_limits(card, genre)


def _body(node):
    return {k: v for k, v in node.items() if k not in ("id", "entity", "beat", "t")}


def prepare(envelope):
    convention = envelope["scene"]["ax"]["rotation_convention"]
    quaternion.require(convention)
    kinematic = {n["id"]: n for n in envelope["nodes"]["kinematic"]["items"]}
    bartenieff = {n["id"]: n for n in envelope["nodes"]["bartenieff"]["items"]}
    view = [{**{k: s[k] for k in SLOT_FIELDS}, "allowed_postures": values_in_progress(envelope, s, "posture"),
             "kinematic": _body(kinematic[s["slot"]]),
             "bartenieff": _body(bartenieff[s["slot"]])} for s in slots(envelope)]
    return seal({"step_id": STEP, "band": "L4c", "kind": "motion_plan", "schema": "urn:cinematic-compiler:schema:motion_plan:2.0",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "rotation_convention": convention,
                 "joints": euler_solver.kernel_joints(load_kernel("invariants")),
                 "joint_limits": joint_limits(envelope["scene"]["genre"]),
                 "segments": forward_kinematics.segments(envelope["scene"]["genre"]), "slots": view,  # owner O85
                 "radii": forward_kinematics.radii(envelope["scene"]["genre"]),  # RV-49 (draft)
                 "contact_world": contact_world.packet_view(envelope)})  # plan F5.2, ADR-O83


def _keys(document, packet):
    by_id = {s["slot"]: s for s in packet["slots"]}
    findings, seen = [], {}
    for key in document["keys"]:
        seen[key["slot"]] = seen.get(key["slot"], 0) + 1
        if key["slot"] not in by_id:
            findings.append({"code": "MOTION_SLOT", "message": "Key names no packet slot", "slot": key["slot"]})
    for slot_id in by_id:
        if seen.get(slot_id, 0) != 1:
            findings.append({"code": "MOTION_SLOT", "message": "Every slot needs exactly one key", "slot": slot_id})
    return findings, {k["slot"]: k for k in document["keys"] if k["slot"] in by_id}, by_id


def check(document, packet):
    findings, keys, by_id = _keys(document, packet)
    if findings:
        return findings
    findings = euler_solver.check(keys, by_id, packet["joints"], packet["rotation_convention"]["turns"],
                                  packet["joint_limits"])[0]
    if any(f["code"] == "MOTION_JOINTS" for f in findings):
        return findings  # forward kinematics needs every joint
    rows = contact_world.measure_plan(keys, by_id, packet)  # CONTACT_WORLD (plan F5.2, owners O72, O83)
    return (findings + contact_world.refusals(rows, packet["contact_world"]["exceptions"])  # the owner's list (F-123)
            + body_overlap.refusals(contact_world.plan_bodies(keys, by_id, packet)))  # RV-49 (F-144, R-18)


def build(envelope, document, packet):
    _, keys, by_id = _keys(document, packet)
    bases = euler_solver.check(keys, by_id, packet["joints"], packet["rotation_convention"]["turns"],
                               packet["joint_limits"])[1]
    nodes = []
    for slot_id in sorted(keys, key=lambda s: (by_id[s]["t"], s)):
        key, slot = keys[slot_id], by_id[slot_id]
        nodes.append({"id": slot_id, "entity": slot["entity"], "beat": slot["beat"], "t": slot["t"], "name": key["name"],
                      "pos": key["pos"], "rot": key["rot"], "quat": quaternion.quaternion(key["rot"]),
                      "bones": {j: key["bones"][j] for j in packet["joints"]}, "turn": key["turn"],
                      "axis_declaration": key["axis_declaration"], "heading_basis": bases[slot_id],
                      "description": key["description"],
                      "points": forward_kinematics.points(key, packet["segments"])})  # owner O24, O72 (M9-06a)
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"], "relation": "follows",
                          "turn": prior["turn"], "axis_declaration": prior["axis_declaration"],
                          "euler_delta": [round(b - a, 6) + 0.0 for a, b in zip(prior["rot"], node["rot"], strict=True)],
                          "interpolation": "slerp" if prior["turn"] == "none" else "euler_axis",
                          "slerp_angle": quaternion.arc_degrees(prior["rot"], node["rot"]),
                          "trajectory": trajectory.segment(prior, node)})
        last[node["entity"]] = node
    return {"/nodes/motion": nodes, "/edges/motion": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
