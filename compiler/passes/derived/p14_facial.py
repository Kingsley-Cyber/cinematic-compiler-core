"""S14 pass (band L4d, authored; live_action and ugc_ad): one face per entity per beat.

The packet carries what the face answers to (the slot's beat, its kinematic tension/breathing/strain, the head pose
from S13, the causal edges the beat reacts to, the archetype face profile) and the three face libraries. Checks:
validators/facial_validator.py. Derived: the words the render prints for each face and `transitions_to` edges
between an entity's consecutive faces, triggered by the beat's incoming causal edge.
"""

import json
from functools import cache

import yaml

from compiler.authoring import run_authored, seal
from planner.dependency_graph import ROOT, load
from planner.scene_view import slots
from solver.quaternion import head_heading
from validators import facial_validator
from validators.schema_validator import validate_schema

NODE, STEP = "facial", "S14"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "facial_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "facial_acting.txt"
LIBRARIES = ("facs_action_units", "facs_asymmetry_bounds", "emotion_families")


@cache
def library(name):
    document = yaml.safe_load((ROOT / "library" / f"{name}.yaml").read_text(encoding="utf-8"))
    validate_schema(document, json.loads((ROOT / "schemas" / "cards" / f"{name}.schema.json").read_text(encoding="utf-8")))
    return document


def prepare(envelope):
    kinematic = {n["id"]: n for n in envelope["nodes"]["kinematic"]["items"]}
    motion = {n["id"]: n for n in envelope["nodes"]["motion"]["items"]}
    causes = envelope["edges"]["causal"]["items"]
    units, bounds, emotions = (library(name) for name in LIBRARIES)
    view = []
    for s in slots(envelope):
        key = motion[s["slot"]]
        view.append({**{k: s[k] for k in ("slot", "entity", "beat", "t", "dur", "role", "label", "action", "event_type")},
                     "kinematic": {k: kinematic[s["slot"]][k]
                                   for k in ("tension", "breathing", "strain", "release", "restraint")},
                     "head": {"root_rot": key["rot"], "NK": key["bones"]["NK"], "HD": key["bones"]["HD"],
                              "heading_deg": head_heading(key)},
                     "reacts_to": [{k: e[k] for k in ("id", "from", "causal_strength", "why")}
                                   for e in causes if e["to"] == s["beat"]]})
    return seal({
        "step_id": STEP, "band": "L4d", "kind": "facial_plan", "schema": "urn:cinematic-compiler:schema:facial_plan:1.0",
        "instructions": PROMPT.read_text(encoding="utf-8"), "fps": envelope["scene"]["fps"], "slots": view,
        "entities": {e["id"]: {"name": e["name"], "face_profile": e.get("face_profile")}
                     for e in envelope["nodes"]["entities"]["items"]},
        "props": sorted(p["id"] for p in envelope["nodes"]["props"]["items"]),
        "units": {u["au"]: {k: u[k] for k in ("name", "region", "laterality", "words", "absent")} for u in units["units"]},
        "intensity_scale": units["intensity_scale"], "max_step_difference": bounds["max_step_difference"],
        "patterns": bounds["patterns"], "emotions": {k: emotions[k] for k in ("labels", "bands", "display_rules")}})


def check(document, packet):
    return facial_validator.check(document["faces"], packet)


def build(envelope, document, packet):
    by_slot = {s["slot"]: s for s in packet["slots"]}
    families = {label["id"]: label["family"] for label in packet["emotions"]["labels"]}
    nodes = []
    for face in sorted(document["faces"], key=lambda f: (by_slot[f["slot"]]["t"], f["slot"])):
        slot = by_slot[face["slot"]]
        nodes.append({"id": face["slot"], "entity": slot["entity"], "beat": slot["beat"], "t": slot["t"],
                      **{k: v for k, v in face.items() if k != "slot"}, "family": families[face["emotion_label"]],
                      "words": facial_validator.words(face, packet)})
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            trigger = next((e["id"] for e in by_slot[node["id"]]["reacts_to"]), None)
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"],
                          "relation": "transitions_to",
                          "onset": node["onset"], "onset_frames": node["onset_frames"], "trigger": trigger})
        last[node["entity"]] = node
    return {"/nodes/facial": nodes, "/edges/facial_transition": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
