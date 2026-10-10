"""S12 pass (band L4b, authored): how each body coordinates the movement, per entity per beat.

Checks: one node per slot; values from library/bartenieff_vocabulary.yaml; initiation is a part or core;
follow-through parts are the entity's own; the body mode exists and allows the node's connectivity pattern.
`cpcs:` values are labelled extensions (listed per node), never presented as native Bartenieff/LMA.
"""

import json

import yaml

from compiler.authoring import run_authored, seal
from planner import library_vocab
from planner.dependency_graph import ROOT, load
from planner.scene_view import slots
from validators.schema_validator import validate_schema

NODE, STEP = "bartenieff", "S12"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "bartenieff_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "body_coordination.txt"
FIELDS = ("connectivity", "developmental_pattern", "intent", "initiation", "follow_through", "body_mode")


def body_modes():
    schema = json.loads((ROOT / "schemas" / "cards" / "body_mode_card.schema.json").read_text(encoding="utf-8"))
    modes = {}
    for path in sorted((ROOT / "library" / "body_modes").glob("*.yaml")):
        card = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_schema(card, schema)
        modes[card["card_id"]] = card
    return modes


def prepare(envelope):
    kinematic = {n["id"]: n for n in envelope["nodes"]["kinematic"]["items"]}
    parts = {e["id"]: e["parts"] for e in envelope["nodes"]["entities"]["items"]}
    view = [{**{k: s[k] for k in ("slot", "entity", "beat", "t", "dur", "role", "label", "action")},
             "kinematic": {k: v for k, v in kinematic[s["slot"]].items() if k not in ("id", "entity", "beat", "t")}}
            for s in slots(envelope)]
    modes = {k: {"description": v["description"], "connectivity": v["connectivity"]} for k, v in body_modes().items()}
    return seal({"step_id": STEP, "band": "L4b", "kind": "bartenieff_plan",
                 "schema": "urn:cinematic-compiler:schema:bartenieff_plan:1.0",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "slots": view, "parts": parts,
                 "vocabulary": library_vocab.load("bartenieff_vocabulary")["fields"], "body_modes": modes})


def check(document, packet):
    findings, seen = [], {}
    by_id = {s["slot"]: s for s in packet["slots"]}
    vocabulary = {"fields": packet["vocabulary"]}
    for node in document["nodes"]:
        seen[node["slot"]] = seen.get(node["slot"], 0) + 1
        slot = by_id.get(node["slot"])
        if slot is None:
            findings.append({"code": "BARTENIEFF_SLOT", "message": "Node names no packet slot", "slot": node["slot"]})
            continue
        parts = packet["parts"][slot["entity"]]
        for field in FIELDS:
            for problem in library_vocab.problems(vocabulary, field, node[field], parts):
                findings.append({"code": "BARTENIEFF_VOCABULARY", "message": problem, "slot": node["slot"]})
        mode = packet["body_modes"].get(node["body_mode"])
        if mode is not None and node["connectivity"] not in mode["connectivity"]:
            findings.append({"code": "BODY_MODE_COHERENCE", "message": "The body mode does not allow this connectivity pattern",
                             "slot": node["slot"]})
    for slot_id in by_id:
        if seen.get(slot_id, 0) != 1:
            findings.append({"code": "BARTENIEFF_SLOT", "message": "Every slot needs exactly one node", "slot": slot_id})
    return findings


def build(envelope, document, packet):
    by_id = {s["slot"]: s for s in packet["slots"]}
    nodes = []
    for node in sorted(document["nodes"], key=lambda n: (by_id[n["slot"]]["t"], n["slot"])):
        slot = by_id[node["slot"]]
        extensions = [f for f in FIELDS if isinstance(node[f], str) and node[f].startswith("cpcs:")]
        nodes.append({"id": node["slot"], "entity": slot["entity"], "beat": slot["beat"], "t": slot["t"],
                      **{f: node[f] for f in FIELDS}, "extensions": extensions})
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"],
                          "changes": [f for f in FIELDS if prior[f] != node[f]]})
        last[node["entity"]] = node
    return {"/nodes/bartenieff": nodes, "/edges/bartenieff_transition": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
