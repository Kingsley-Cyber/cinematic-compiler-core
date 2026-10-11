"""S07 pass (band L2): contact events from the beat plan, their lifecycle, and cross-checks with S06.

Lifecycle: touch is instant; possess/support become active at their beat end and stay active until a release
of the same pair (entity part ↔ target part); a release needs an active contact; a pair is not acquired twice;
a hand possesses one thing at a time. Cross-checks: a prop's holder matches an active possess contact, and every
prop state change has a contact event in its triggering beat or an active contact on the prop.
"""

import copy
import json

from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "contact"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "contact_graph.schema.json"
HANDS = {"left_hand", "right_hand"}
EPSILON = 1e-9


def _finding(code, message, detail=None):
    return {"code": code, "message": message, "detail": detail}


def _pair(event):
    return event["a"]["id"], event["body_part"], event["b"]["kind"], event["b"]["id"], event["b"]["part"]


def events_of(beats):
    events = []
    for beat in sorted(beats, key=lambda b: (b["t"] + b["dur"], b["t"], b["id"])):
        for index, contact in enumerate(beat["contacts"], 1):
            events.append({"id": f"{beat['id']}_c{index}", "t": contact_time(beat, contact), "beat": beat["id"],
                           "contact_type": contact["contact_type"], "body_part": contact["a"]["part"],
                           "a": {"kind": "entity", "id": contact["a"]["id"]}, "b": dict(contact["b"]),
                           **({"verb": contact["verb"]} if contact.get("verb") else {})})  # owner O22
    return events


def contact_time(beat, contact):
    """A contact happens at its beat's end, or at its start when marked `at: start` (M8.12: a prop in hand at t=0)."""
    return round(beat["t"] + (0 if contact.get("at") == "start" else beat["dur"]), 6)


def chain_events(scene):
    """M5.5: contacts still open at the previous clip's end, re-opened here at t=0 (beat "chain")."""
    chained = scene.get("chained_from") or {}
    return [{"id": f"chain_c{index}", "t": 0.0, "beat": "chain", "contact_type": c["contact_type"],
             "body_part": c["body_part"], "a": {"kind": "entity", "id": c["a"]}, "b": dict(c["b"])}
            for index, c in enumerate(chained.get("active_contacts", []), 1)]


def events_for(envelope):
    """Every contact event of a clip: carried ones first, then the beat plan's."""
    return chain_events(envelope.get("scene", {})) + events_of(envelope["nodes"]["beats"]["items"])


def lifecycle(events):
    """Returns (edges, findings, intervals) — intervals: [(pair, contact_type, start_t, end_t or None)]."""
    active, last, edges, findings, intervals = {}, {}, [], [], []
    for event in events:
        pair = _pair(event)
        if pair in last:
            edges.append({"id": f"{last[pair]}__precedes__{event['id']}", "from": last[pair], "to": event["id"],
                          "relation": "precedes"})
        last[pair] = event["id"]
        kind = event["contact_type"]
        if kind == "release":
            opened = active.pop(pair, None)
            if opened is None:
                findings.append(_finding("CONTACT_RELEASE", "A release needs an active possess or support of the same pair",
                                         event["id"]))
            else:
                edges.append({"id": f"{event['id']}__releases__{opened['id']}", "from": event["id"], "to": opened["id"],
                              "relation": "releases"})
                intervals.append((pair, opened["contact_type"], opened["t"], event["t"]))
        elif kind in ("possess", "support"):
            if pair in active:
                findings.append(_finding("CONTACT_DUPLICATE", "The pair is already in contact", event["id"]))
                continue
            if kind == "possess" and event["body_part"] in HANDS and any(
                    p[0] == pair[0] and p[1] == pair[1] and c["contact_type"] == "possess" for p, c in active.items()):
                findings.append(_finding("CONTACT_HAND", "A hand possesses one thing at a time", event["id"]))
            active[pair] = event
    intervals.extend((pair, event["contact_type"], event["t"], None) for pair, event in active.items())
    return edges, findings, intervals


def _active_possessors(intervals, prop_id, time):
    return {pair[0] for pair, kind, start, end in intervals
            if kind == "possess" and pair[2:4] == ("prop", prop_id) and start <= time + EPSILON
            and (end is None or time < end - EPSILON)}


def cross_check(events, intervals, states, transitions, beats):
    findings = []
    for node in states:
        if node["subject"]["kind"] != "prop":
            continue
        holder = node["conditions"].get("holder", "unknown")
        holders = _active_possessors(intervals, node["subject"]["id"], node["t"])
        # A release at its own beat's start (O23: a throw lets go at its pose) ends the possess at the instant the beat
        # begins; at that instant the prop is still in the hand (S06 commits the holder change at the beat's end).
        holders |= {e["a"]["id"] for e in events if e["contact_type"] == "release" and e["beat"] == node.get("beat")
                    and e["b"]["kind"] == "prop" and e["b"]["id"] == node["subject"]["id"] and abs(e["t"] - node["t"]) <= EPSILON}
        if holder not in ("unknown", "none") and holder not in holders:
            findings.append(_finding("HOLDER_CONTACT", "The prop's holder has no active possess contact", node["id"]))
        if holder == "none" and holders:
            findings.append(_finding("HOLDER_CONTACT", "The prop is possessed but its holder is none", node["id"]))
    by_state = {s["id"]: s for s in states}
    beat_start = {b["id"]: b["t"] for b in beats}
    for edge in transitions:
        subject = by_state[edge["to_state"]]["subject"]
        if subject["kind"] != "prop":
            continue
        for beat_id in edge["trigger_event"]:
            touched = any(e["beat"] == beat_id and e["b"]["kind"] == "prop" and e["b"]["id"] == subject["id"] for e in events)
            held = any(pair[2:4] == ("prop", subject["id"]) and start <= beat_start[beat_id] + EPSILON
                       and (end is None or beat_start[beat_id] < end - EPSILON) for pair, _, start, end in intervals)
            if not (touched or held):
                findings.append(_finding("PROP_CHANGE_CONTACT", "A prop changed without a contact", [edge["id"], beat_id]))
    return findings


def run(envelope, *, order=None):
    order = order or load()
    if "states" not in envelope.get("nodes", {}):
        raise ContractError("MISSING_INPUT", "S07 needs the S06 state graph")
    beats = envelope["nodes"]["beats"]["items"]
    events = events_for(envelope)
    edges, findings, intervals = lifecycle(events)
    findings += cross_check(events, intervals, envelope["nodes"]["states"]["items"],
                            envelope["edges"]["state_transition"]["items"], beats)
    if findings:
        raise StepFailed("S07", findings)
    graph = {"contacts": events, "contact": edges}
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["contacts"] = {**tag, "items": events}
    after["edges"]["contact"] = {**tag, "items": edges}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S07 changed paths it does not own", findings)
    return after
