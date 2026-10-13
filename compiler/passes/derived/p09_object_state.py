"""S09 pass (band L2.6, derived, UGC): each object's internal states per beat, every change tied to a hand.

Internal states are the object card's own state properties (holder and location stay in S06); a state keeps S06's
`before_own_effects` for them (the values before its beat's own at-start effects) and each change its instant (F-161,
RV-61). Checks: every internal change has a hand contact on the object in its triggering beat at or before the
change's instant (a release only at that instant, F-173), or a hand holding it at that instant (the trigger contact);
and happens inside an S08 interaction on that object (the verb that changes it).
"""

import copy
import json

from compiler.authoring import StepFailed
from compiler.passes.mandatory.p07_contact import HANDS, events_for, lifecycle
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "object_state"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "object_state_graph.schema.json"
EPSILON = 1e-9


def _name(state):
    return "|".join(f"{p}:{v}" for p, v in sorted(state.items()))


def build(envelope):
    nodes = envelope["nodes"]
    beats = {b["id"]: b for b in nodes["beats"]["items"]}
    internal = {p["id"]: [s["property"] for s in p["states"]] for p in nodes["props"]["items"]}
    interactions = nodes["hand_role"]["items"]
    contacts = nodes["contacts"]["items"]
    _, _, intervals = lifecycle(events_for(envelope))

    def interaction_at(obj, beat):
        return next((i["id"] for i in interactions if i["object"] == obj and beat in i["beats"]), None)

    states, findings = [], []
    for s in nodes["states"]["items"]:
        obj = s["subject"]["id"]
        if s["subject"]["kind"] != "prop" or not internal[obj]:
            continue
        state = {p: s["conditions"][p] for p in internal[obj]}
        node = {"id": s["id"], "object": obj, "beat": s["beat"], "t": s["t"], "state": state, "state_name": _name(state),
                "interaction": interaction_at(obj, s["beat"]) if s["beat"] in beats else None}
        own = {p: v for p, v in s.get("before_own_effects", {}).items() if p in internal[obj]}
        if own:
            node["before_own_effects"] = own
        states.append(node)
    by_id = {s["id"]: s for s in states}
    edges = []
    for e in envelope["edges"]["state_transition"]["items"]:
        if e["to_state"] not in by_id:
            continue
        obj = by_id[e["to_state"]]["object"]
        changes = [{k: c[k] for k in ("property", "from", "to", "t")} for c in e["changes"] if c["property"] in internal[obj]]
        if not changes:
            continue
        for beat in e["trigger_event"]:
            start, end = beats[beat]["t"], beats[beat]["t"] + beats[beat]["dur"]
            instant = min((c["t"] for c in changes if start - EPSILON <= c["t"] <= end + EPSILON),
                          default=min(c["t"] for c in changes))  # F-161: the hand is on the object by then
            hand = [c["id"] for c in contacts if c["beat"] == beat and c["b"]["kind"] == "prop" and c["b"]["id"] == obj
                    and c["body_part"] in HANDS and c["t"] <= instant + EPSILON
                    and (c["contact_type"] != "release" or c["t"] >= instant - EPSILON)]  # F-173: let go before it
            held = [f"{pair[0]}.{pair[1]}" for pair, kind, t0, t1 in intervals if kind == "possess" and pair[1] in HANDS
                    and pair[2:4] == ("prop", obj) and t0 <= instant + EPSILON and (t1 is None or instant < t1 - EPSILON)]
            trigger = (hand or [f"held:{h}" for h in held] or [None])[0]
            if trigger is None:
                findings.append({"code": "OBJECT_STATE_TRIGGER", "message": f"{obj} changes in {beat} without a hand on it",
                                 "detail": e["id"]})
            interaction = interaction_at(obj, beat)
            if interaction is None:
                findings.append({"code": "OBJECT_STATE_INTERACTION", "message": f"{obj} changes in {beat} outside any "
                                 "S08 interaction on it", "detail": e["id"]})
            edges.append({"id": f"{e['id']}@{beat}", "from": e["from_state"], "to": e["to_state"],
                          "changes": changes, "trigger_beat": beat, "trigger_contact": trigger, "interaction": interaction})
    return {"object_state": states, "object_state_transition": edges}, findings


def run(envelope, *, order=None):
    order = order or load()
    if "hand_role" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S09 needs the S08 hand-role graph")
    graph, findings = build(envelope)
    if findings:
        raise StepFailed("S09", findings)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["object_state"] = {**tag, "items": graph["object_state"]}
    after["edges"]["object_state_transition"] = {**tag, "items": graph["object_state_transition"]}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S09 changed paths it does not own", findings)
    return after
