"""S11 pass (band L4a, authored): visible bodily organization per entity per beat.

Checks: one node per slot; cue values from library/kinematic_cues.yaml; support parts are the entity's own;
support agrees with S07 (when supports are active they must match exactly) or else with S06 (airborne means no
support, grounded/braced/lying means some support; a support change in progress allows either side).
"""

from compiler.authoring import run_authored, seal
from planner import library_vocab
from planner.dependency_graph import ROOT, load
from planner.scene_view import slots

NODE, STEP = "kinematic", "S11"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "kinematic_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "kinematic_organization.txt"
CUES = ("balance", "loading", "bracing", "yielding", "weight_transfer", "tension", "release", "strain", "restraint", "breathing")
EPSILON = 1e-9


def _support_states(envelope, slot):
    states = {slot["state"]["support"]}
    for beat in envelope["nodes"]["beats"]["items"]:
        if beat["t"] + EPSILON < slot["t"] < beat["t"] + beat["dur"] - EPSILON:
            states |= {f["value"] for f in beat["effects"]
                       if f["subject"] == {"kind": "entity", "id": slot["entity"]} and f["property"] == "support"}
    return sorted(states)


def prepare(envelope):
    vocabulary = library_vocab.load("kinematic_cues")
    parts = {e["id"]: e["parts"] for e in envelope["nodes"]["entities"]["items"]}
    view = [{**s, "allowed_support_states": _support_states(envelope, s)} for s in slots(envelope)]
    return seal({"step_id": STEP, "band": "L4a", "kind": "kinematic_plan",
                 "schema": "urn:cinematic-compiler:schema:kinematic_plan:1.0",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "genre": envelope["scene"]["genre"],
                 "slots": view, "parts": parts, "vocabulary": vocabulary["fields"]})


def check(document, packet):
    findings, seen = [], {}
    slots_by_id = {s["slot"]: s for s in packet["slots"]}
    vocabulary = {"fields": packet["vocabulary"]}
    for node in document["nodes"]:
        seen[node["slot"]] = seen.get(node["slot"], 0) + 1
        slot = slots_by_id.get(node["slot"])
        if slot is None:
            findings.append({"code": "KINEMATIC_SLOT", "message": "Node names no packet slot", "slot": node["slot"]})
            continue
        parts = packet["parts"][slot["entity"]]
        for field in ("support", *CUES):
            for problem in library_vocab.problems(vocabulary, field, node[field], parts):
                findings.append({"code": "KINEMATIC_VOCABULARY", "message": problem, "slot": node["slot"]})
        support, active, allowed = set(node["support"]), set(slot["active_supports"]), set(slot["allowed_support_states"])
        if active and support != active:
            findings.append({"code": "KINEMATIC_SUPPORT", "message": "Support must match the active support contacts",
                             "slot": node["slot"]})
        elif not active and "unknown" not in allowed:
            if allowed == {"airborne"} and support:
                findings.append({"code": "KINEMATIC_SUPPORT", "message": "An airborne body has no support", "slot": node["slot"]})
            if "airborne" not in allowed and not support:
                findings.append({"code": "KINEMATIC_SUPPORT", "message": "A supported body needs support parts",
                                 "slot": node["slot"]})
    for slot_id in slots_by_id:
        if seen.get(slot_id, 0) != 1:
            findings.append({"code": "KINEMATIC_SLOT", "message": "Every slot needs exactly one node", "slot": slot_id})
    return findings


def build(envelope, document, packet):
    slots_by_id = {s["slot"]: s for s in packet["slots"]}
    nodes = []
    for node in sorted(document["nodes"], key=lambda n: (slots_by_id[n["slot"]]["t"], n["slot"])):
        slot = slots_by_id[node["slot"]]
        nodes.append({"id": node["slot"], "entity": slot["entity"], "beat": slot["beat"], "t": slot["t"],
                      **{k: v for k, v in node.items() if k != "slot"}})
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["entity"])
        if prior:
            changes = [f for f in ("support", *CUES) if prior[f] != node[f]]
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"], "changes": changes})
        last[node["entity"]] = node
    return {"/nodes/kinematic": nodes, "/edges/kinematic_transition": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
