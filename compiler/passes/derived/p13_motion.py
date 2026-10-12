"""S13 pass (band L4c, authored + derived): one Euler key pose per entity per beat, checked against S04.

Authored: root pos/rot, the kernel joints, turn and axis declarations. Checked by solver/euler_solver.py, by
CONTACT_WORLD (solver/contact_world.py; a support on a floor at every key it spans, RV-14a), by BODY_OVERLAP
(solver/body_overlap.py: no body through another, RV-49) and by FLOOR_PENETRATION (solver/floor_penetration.py: no
body under the floor at any key, RV-14a). An in-between key (ADR-O109, RV-59f) is checked like a key: its span
(INBETWEEN_SPAN), the kernel joints and their limits, its root's speed to its neighbours (TELEPORT, owner O12), the
floor and the other bodies at its instant, posed as the declared interpolation has them.
Derived: root quaternion per key (solver/quaternion.py) and per-entity follows edges with the Euler delta,
interpolation and root trajectory (solver/trajectory.py).
"""

import json
import math

import yaml

from compiler.authoring import run_authored, seal
from kernel.kernel_files import load as load_kernel
from planner.dependency_graph import ROOT, load
from planner.dynamic_beat_validator import TELEPORT_MPS, vanish_windows
from planner.scene_view import slots, values_in_progress
from solver import (
    body_overlap,
    contact_world,
    euler_solver,
    floor_penetration,
    forward_kinematics,
    interpolation,
    quaternion,
    trajectory,
)
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
    return seal({"step_id": STEP, "band": "L4c", "kind": "motion_plan", "schema": "urn:cinematic-compiler:schema:motion_plan:2.1",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "rotation_convention": convention,
                 "joints": euler_solver.kernel_joints(load_kernel("invariants")),
                 "joint_limits": joint_limits(envelope["scene"]["genre"]),
                 "segments": forward_kinematics.segments(envelope["scene"]["genre"]), "slots": view,  # owner O85
                 "radii": forward_kinematics.radii(envelope["scene"]["genre"]),  # RV-49 (draft)
                 "contact_world": contact_world.packet_view(envelope),  # plan F5.2, ADR-O83
                 "floor_y": floor_penetration.floor_level(envelope["nodes"]["surfaces"]["items"],  # RV-14a (F-089)
                                                          envelope["scene"]["ax"].get("ground")),
                 "fps": envelope["scene"]["fps"],  # ADR-O109 (RV-59f): an in-between sits on a frame of its own
                 "vanished": [[entity, start, back] for entity, _, start, back in
                              vanish_windows(envelope["nodes"]["beats"]["items"])]})


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


def _timeline(keys, by_id):
    """{entity: [key with t and id, in time order]} of the authored keys."""
    timeline = {}
    for slot_id, key in keys.items():
        timeline.setdefault(by_id[slot_id]["entity"], []).append({**key, "t": by_id[slot_id]["t"], "id": slot_id})
    return {entity: sorted(own, key=lambda k: k["t"]) for entity, own in timeline.items()}


def _inbetweens(document, keys, by_id, packet):
    """(findings, the in-betweens that stand in their spans) for ADR-O109's in-between keys (RV-59f)."""
    fps, timeline, findings, standing = packet["fps"], _timeline(keys, by_id), [], []
    taken = {(entity, round(k["t"] * fps)) for entity, own in timeline.items() for k in own}
    for between in sorted(document.get("inbetweens", []), key=lambda b: (b["entity"], b["t"])):
        ident, own = f"{between['entity']}@{between['t']:g}", timeline.get(between["entity"], [])
        frame = (between["entity"], round(between["t"] * fps))
        if not any(k["t"] < between["t"] for k in own) or not any(k["t"] > between["t"] for k in own) or frame in taken:
            findings.append({"code": "INBETWEEN_SPAN", "slot": ident, "message": "An in-between key stands strictly between "
                             "two keys of its entity, on a frame no key or other in-between holds (ADR-O109)"})
            continue
        taken.add(frame)
        if set(between["bones"]) != set(packet["joints"]):
            findings.append({"code": "MOTION_JOINTS", "slot": ident, "message": "An in-between key carries the kernel joints"})
            continue
        findings += euler_solver.limit_findings(between, ident, packet["joint_limits"])
        standing.append(between)
    return findings, standing


def _inbetween_world(standing, keys, by_id, packet):
    """TELEPORT, FLOOR_PENETRATION and BODY_OVERLAP at each standing in-between key (ADR-O109, RV-59f), every refusal
    naming the in-between."""
    findings, own = [], interpolation.sequences(_timeline(keys, by_id), standing)
    for entity, sequence in own.items():
        for a, b in zip(sequence, sequence[1:], strict=False):
            if "id" in a and "id" in b:
                continue  # two keys: S04's TELEPORT judges their anchors
            speed = math.dist(a["pos"], b["pos"]) / (b["t"] - a["t"])
            if speed > TELEPORT_MPS + 1e-9:
                between = b if "id" in a else a
                findings.append({"code": "TELEPORT", "slot": f"{entity}@{between['t']:g}", "message": f"{_words(entity)} "
                                 f"moves {speed:.1f} m/s to or from an in-between key (over {TELEPORT_MPS:g} m/s, owner O12)"})
    for between in standing:
        entity, t = between["entity"], between["t"]
        ident = f"{entity}@{t:g}"
        findings += floor_penetration.refusals({(entity, t): {"id": ident, "points": forward_kinematics.points(
            between, packet["segments"])}}, packet["floor_y"])
        bodies = {(entity, t): {"id": ident, "capsules": forward_kinematics.capsules(between, packet["segments"],
                                                                                     packet["radii"])}}
        for other, sequence in own.items():
            gone = any(e == other and start - 1e-9 <= t and (back is None or t < back - 1e-9)
                       for e, start, back in packet["vanished"])
            pose = None if other == entity or gone else _posed(sequence, t)
            if pose is not None:
                bodies[(other, t)] = {"id": other, "capsules": forward_kinematics.capsules(pose, packet["segments"],
                                                                                         packet["radii"])}
        for _, first, second, depth, one, two in body_overlap.overlaps(bodies):
            if entity in (first[0], second[0]):
                mine, theirs = (one, (second[0], two)) if first[0] == entity else (two, (first[0], one))
                findings.append({"code": "BODY_OVERLAP", "slot": ident, "message": f"{_words(entity)} {_words(mine)} and "
                                 f"{_words(theirs[0])} {_words(theirs[1])} overlap by {depth:g} m at the in-between key "
                                 f"{t:g} (R-18: no body through another)"})
    return findings


def _words(text):
    return text.replace("_", " ")


def _posed(sequence, t):
    """An entity's key or in-between at instant t, else its pose between them there, else None outside them."""
    for key in sequence:
        if abs(key["t"] - t) < 1e-9:
            return key
    before, after = [k for k in sequence if k["t"] < t], [k for k in sequence if k["t"] > t]
    return interpolation.pose(before[-1], after[0], t) if before and after else None


def check(document, packet):
    findings, keys, by_id = _keys(document, packet)
    if findings:
        return findings
    findings = euler_solver.check(keys, by_id, packet["joints"], packet["rotation_convention"]["turns"],
                                  packet["joint_limits"])[0]
    if any(f["code"] == "MOTION_JOINTS" for f in findings):
        return findings  # forward kinematics needs every joint
    between_findings, standing = _inbetweens(document, keys, by_id, packet)
    rows = contact_world.measure_plan(keys, by_id, packet, standing)  # CONTACT_WORLD (plan F5.2, owners O72, O83)
    bodies = contact_world.plan_bodies(keys, by_id, packet)
    return (findings + contact_world.refusals(rows, packet["contact_world"]["exceptions"])  # the owner's list (F-123)
            + body_overlap.refusals(bodies)  # RV-49 (F-144, R-18)
            + floor_penetration.refusals(bodies, packet["floor_y"])  # RV-14a (F-089, owner O72)
            + between_findings + _inbetween_world(standing, keys, by_id, packet))  # ADR-O109 (RV-59f)


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
    inbetweens = sorted(document.get("inbetweens", []), key=lambda b: (b["entity"], b["t"]))
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            edge = {"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"], "relation": "follows",
                    "turn": prior["turn"], "axis_declaration": prior["axis_declaration"],
                    "euler_delta": [round(b - a, 6) + 0.0 for a, b in zip(prior["rot"], node["rot"], strict=True)],
                    "interpolation": "slerp" if prior["turn"] == "none" else "euler_axis",
                    "slerp_angle": quaternion.arc_degrees(prior["rot"], node["rot"]),
                    "trajectory": trajectory.segment(prior, node)}
            inside = [b for b in inbetweens if b["entity"] == node["entity"] and prior["t"] < b["t"] < node["t"]]
            if inside:  # ADR-O109 (RV-59f): the declared interpolation runs through them
                edge["inbetweens"] = [{"id": f"{b['entity']}@{b['t']:g}", "entity": b["entity"], "t": b["t"],
                                       "name": b["name"], "pos": b["pos"], "rot": b["rot"],
                                       "quat": quaternion.quaternion(b["rot"]),
                                       "bones": {j: b["bones"][j] for j in packet["joints"]}, "turn": prior["turn"],
                                       "description": b["description"],
                                       "points": forward_kinematics.points(b, packet["segments"])} for b in inside]
            edges.append(edge)
        last[node["entity"]] = node
    return {"/nodes/motion": nodes, "/edges/motion": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
