"""S08 pass (band L2.5, authored, UGC): lock which hand does what for each interaction with an object.

Checks: the verb is an affordance of the object card; beats are consecutive and contain the actor and the object;
hands are the actor's own, distinct, and match the role template; grips come from library/grip_types.yaml and the
object card; roles hold across the interaction (only the declared hands touch the object, the agent hand acts on it,
and a support hand holds or touches it, F-137; no other hand of the actor touches or holds it, F-173); no hand serves
two overlapping interactions. Derived: span, duration, role invariant, next_interaction edges.
"""

import json

import yaml

from compiler.authoring import run_authored, seal
from compiler.passes.mandatory.p07_contact import HANDS, events_for, lifecycle
from planner import library_vocab
from planner.dependency_graph import ROOT, load
from validators.schema_validator import validate_schema

NODE, STEP = "hand_role", "S08"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "hand_role_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "hand_roles.txt"
EPSILON = 1e-9


def role_templates():
    document = yaml.safe_load((ROOT / "library" / "role_templates.yaml").read_text(encoding="utf-8"))
    validate_schema(document, json.loads((ROOT / "schemas" / "cards" / "role_templates.schema.json").read_text(encoding="utf-8")))
    return {t["id"]: t for t in document["templates"]}


def prepare(envelope):
    beats = sorted(envelope["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"]))
    _, _, intervals = lifecycle(events_for(envelope))
    held = {b["id"]: sorted([pair[0], pair[1], pair[3]] for pair, kind, start, end in intervals
                            if kind == "possess" and pair[2] == "prop" and start <= b["t"] + EPSILON
                            and (end is None or b["t"] < end - EPSILON)) for b in beats}
    return seal({
        "step_id": STEP, "band": "L2.5", "kind": "hand_role_plan", "schema": "urn:cinematic-compiler:schema:hand_role_plan:1.0",
        "instructions": PROMPT.read_text(encoding="utf-8"),
        "beats": [{"id": b["id"], "t": b["t"], "dur": b["dur"], "actor": b["actor"], "label": b["label"], "action": b["action"],
                   "bodies": [b["actor"]] + [p["id"] for p in b["participants"] if p["kind"] == "entity"],
                   "objects": [p["id"] for p in b["participants"] if p["kind"] == "prop"], "held_at_start": held[b["id"]]}
                  for b in beats],
        "contacts": [{"id": c["id"], "beat": c["beat"], "t": c["t"], "contact_type": c["contact_type"], "entity": c["a"]["id"],
                      "part": c["body_part"], "object": c["b"]["id"]} for c in envelope["nodes"]["contacts"]["items"]
                     if c["b"]["kind"] == "prop"],
        "entities": {e["id"]: e["parts"] for e in envelope["nodes"]["entities"]["items"]},
        "objects": {p["id"]: {"affordances": p["affordances"], "grips": p["grips"]} for p in envelope["nodes"]["props"]["items"]},
        "grips": library_vocab.load("grip_types")["fields"]["grip"]["values"], "templates": role_templates()})


def _on(hand, interaction, beats, inside):
    """The hand holds the object at the start of one of the interaction's beats, or makes a contact on it in one."""
    held = [interaction["actor"], hand, interaction["object"]]
    return any(held in beats[b]["held_at_start"] for b in interaction["beats"]) or any(c["part"] == hand for c in inside)


def _span(interaction, packet):
    beats = {b["id"]: b for b in packet["beats"]}
    rows = [beats[b] for b in interaction["beats"]]
    return min(r["t"] for r in rows), round(max(r["t"] + r["dur"] for r in rows), 6) + 0.0


def check(document, packet):
    findings, spans = [], {}
    order = [b["id"] for b in packet["beats"]]
    beats = {b["id"]: b for b in packet["beats"]}

    def add(code, message, interaction):
        findings.append({"code": code, "message": message, "slot": interaction["id"]})

    for i in document["interactions"]:
        obj, actor = packet["objects"].get(i["object"]), i["actor"]
        if obj is None or actor not in packet["entities"]:
            add("HAND_ROLE_OBJECT", "The object must be a declared prop and the actor a declared entity", i)
            continue
        if i["verb"] not in obj["affordances"]:
            add("HAND_ROLE_OBJECT", f"{i['verb']} is not an affordance of {i['object']}", i)
        if any(b not in beats for b in i["beats"]):
            add("HAND_ROLE_BEATS", "An interaction beat does not exist", i)
            continue
        positions = [order.index(b) for b in i["beats"]]
        if positions != list(range(positions[0], positions[0] + len(positions))):
            add("HAND_ROLE_BEATS", "Interaction beats are consecutive and in time order", i)
        for b in i["beats"]:
            if actor not in beats[b]["bodies"] or i["object"] not in beats[b]["objects"]:
                add("HAND_ROLE_BEATS", f"{b} must include the actor and the object", i)
        parts = packet["entities"][actor]
        template = packet["templates"].get(i["role_template"])
        if i["agent_hand"] not in parts or i["agent_hand"] == i["support_hand"] or (
                i["support_hand"] != "none" and i["support_hand"] not in parts):
            add("HAND_ROLE_HANDS", "Agent and support hands are two different hands of the actor", i)
        if template is None or (template["support"] == "none") != (i["support_hand"] == "none"):
            add("HAND_ROLE_HANDS", "The role template and the support hand disagree", i)
        for hand, grip in ((i["agent_hand"], i["agent_grip"]), (i["support_hand"], i["support_grip"])):
            if hand == "none":
                if grip != "none":
                    add("HAND_ROLE_GRIP", "No support hand means support_grip none", i)
            elif grip not in packet["grips"] or grip not in obj["grips"]:
                add("HAND_ROLE_GRIP", f"Grip {grip} is not a grip type of {i['object']}", i)
        inside = [c for c in packet["contacts"]
                  if c["beat"] in i["beats"] and c["entity"] == actor and c["object"] == i["object"]]
        allowed = {i["agent_hand"], i["support_hand"]}
        for c in inside:
            if c["part"] in HANDS and c["part"] not in allowed:
                add("HAND_ROLE_SWAP", f"{c['part']} touches {i['object']} in {c['beat']} but holds no role", i)
        for b in i["beats"]:  # F-173 (RV-72): a hand holding the object is on it too
            for who, hand, obj in beats[b]["held_at_start"]:
                if who == actor and obj == i["object"] and hand in HANDS and hand not in allowed:
                    add("HAND_ROLE_SWAP", f"{hand} holds {i['object']} at {b}'s start but holds no role", i)
        if not _on(i["agent_hand"], i, beats, inside):
            add("HAND_ROLE_SWAP", "The agent hand never acts on the object during the interaction", i)
        if i["support_hand"] != "none" and not _on(i["support_hand"], i, beats, inside):
            add("HAND_ROLE_SWAP", "The support hand never holds or touches the object during the interaction", i)
        spans[i["id"]] = _span(i, packet)
    ids = [i["id"] for i in document["interactions"]]
    for repeated in sorted({x for x in ids if ids.count(x) > 1}):
        findings.append({"code": "HAND_ROLE_OBJECT", "message": "Interaction ids are unique", "slot": repeated})
    for a in document["interactions"]:
        for b in document["interactions"]:
            if a["id"] < b["id"] and a["actor"] == b["actor"] and a["id"] in spans and b["id"] in spans:
                (s1, e1), (s2, e2) = spans[a["id"]], spans[b["id"]]
                shared = ({a["agent_hand"], a["support_hand"]} & {b["agent_hand"], b["support_hand"]}) - {"none"}
                if min(e1, e2) - max(s1, s2) > EPSILON and shared:
                    add("HAND_ROLE_OVERLAP", f"{sorted(shared)} serve {a['id']} and {b['id']} at once", b)
    return findings


def build(envelope, document, packet):
    nodes = []
    for i in document["interactions"]:
        t, end = _span(i, packet)
        support = "no support hand" if i["support_hand"] == "none" else f"{i['support_hand']} supports ({i['support_grip']})"
        nodes.append({**i, "t": t, "end": end, "duration": round(end - t, 6) + 0.0,
                      "role_invariant": f"{i['agent_hand']} does {i['verb']} ({i['agent_grip']}) and {support} on {i['object']} "
                                        f"from {t} to {end}; no swap"})
    nodes.sort(key=lambda n: (n["t"], n["id"]))
    edges, last = [], {}
    for node in nodes:
        prior = last.get(node["actor"])
        if prior:
            edges.append({"id": f"{prior['id']}__{node['id']}", "from": prior["id"], "to": node["id"],
                          "agent_hand_changed": prior["agent_hand"] != node["agent_hand"],
                          "support_hand_changed": prior["support_hand"] != node["support_hand"]})
        last[node["actor"]] = node
    return {"/nodes/hand_role": nodes, "/edges/hand_role_transition": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
