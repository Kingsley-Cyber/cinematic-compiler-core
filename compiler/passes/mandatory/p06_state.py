"""S06 pass (band L2): replay the beat plan into states and state transitions; nothing else is written."""

import copy
import json

from compiler.authoring import StepFailed
from kernel import kernel_files
from kernel.canonical import ContractError
from planner.dependency_graph import ROOT, load, node_index
from planner.vocabulary import resolve
from solver.prop_state_machine import replay
from validators import continuity_validator
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

NODE = "state"
GRAPH_SCHEMA = ROOT / "schemas" / "graphs" / "state_graph.schema.json"


HANDS = ("left_hand", "right_hand")
EMPTY = "empty"


def hands(snapshots, beats, entities):
    """Each performer's hands at each of its states (R20 next action 1: nothing in a hand unless declared): a prop is
    in a hand when the prop's holder at the same state is the performer, and in the hand of the performer's last
    possess contact on it up to that state; a held prop no contact places goes to `unplaced`."""
    order = {b["id"]: (b["t"], b["id"]) for b in beats}
    holders = {}
    for s in snapshots:
        if s["subject"]["kind"] == "prop" and s["conditions"].get("holder") not in (None, "none", "unknown"):
            holders.setdefault((s["conditions"]["holder"], s["beat"]), []).append(s["subject"]["id"])
    grips = sorted((order[b["id"]], c["a"]["id"], c["b"]["id"], c["a"].get("part"))
                    for b in beats for c in b.get("contacts", [])
                    if c["contact_type"] == "possess" and c["b"]["kind"] == "prop" and c["a"].get("part") in HANDS)
    handed = {e["id"] for e in entities if set(HANDS) <= set(e.get("parts", []))}
    last = max(order.values(), default=(0, ""))
    for s in snapshots:
        who = s["subject"]["id"]
        if s["subject"]["kind"] != "entity" or who not in handed:
            continue
        now = order.get(s["beat"], (last[0], "~"))
        held = {h: EMPTY for h in HANDS}
        unplaced = []
        for prop in sorted(holders.get((who, s["beat"]), [])):
            hand = next((part for at, actor, target, part in reversed(grips)
                         if at <= now and actor == who and target == prop), None)
            if hand is None:
                unplaced.append(prop)
            else:
                held[hand] = prop
        s["hands"] = {**held, **({"unplaced": unplaced} if unplaced else {})}
    return snapshots


def build(envelope):
    nodes = envelope["nodes"]
    entities, props, surfaces = (nodes[k]["items"] for k in ("entities", "props", "surfaces"))
    beats = nodes["beats"]["items"]
    vocabulary = resolve(entities, props, surfaces, kernel_files.load("state_vocabulary"))
    subjects = ([("entity", e["id"]) for e in entities] + [("prop", p["id"]) for p in props] +
                [("surface", s["id"]) for s in surfaces])
    tables = {}
    for kind, sid in subjects:
        table = vocabulary["prop"][sid] if kind == "prop" else vocabulary[kind]
        tables[(kind, sid)] = sorted(table)
    chained = envelope["scene"].get("chained_from") or {}
    carried = {(s["subject"]["kind"], s["subject"]["id"], prop): value for s in chained.get("end_states", [])
               for prop, value in s["conditions"].items()
               if value != "unknown" and prop in tables.get((s["subject"]["kind"], s["subject"]["id"]), [])}
    snapshots, transitions, findings = replay(beats, subjects, tables, envelope["scene"]["duration_s"], carried)
    snapshots = hands(snapshots, beats, entities)
    beat_ids = [b["id"] for b in sorted(beats, key=lambda b: (b["t"], b["id"]))]
    findings += continuity_validator.check(snapshots, transitions, subjects, [b["id"] for b in beats])
    findings += continuity_validator.first_states(snapshots, beat_ids, {p["id"] for p in props if p.get("carried_by")})
    return {"states": snapshots, "state_transition": transitions}, findings


def run(envelope, *, order=None):
    order = order or load()
    if "beats" not in envelope.get("nodes", {}) or "quadrant" not in envelope.get("scene", {}):
        raise ContractError("MISSING_INPUT", "S06 needs the S04 beats and the S05 causal graph")
    graph, findings = build(envelope)
    if findings:
        raise StepFailed("S06", findings)
    validate_schema(graph, json.loads(GRAPH_SCHEMA.read_text(encoding="utf-8")))
    node = node_index(order)[NODE]
    tag = {"band": node["band"], "step_id": node["step_id"]}
    after = copy.deepcopy(envelope)
    after["nodes"]["states"] = {**tag, "items": graph["states"]}
    after["edges"]["state_transition"] = {**tag, "items": graph["state_transition"]}
    findings = check_pass_writes(order, NODE, envelope, after)
    if findings:
        raise ContractError("WRITE_SCOPE", "S06 changed paths it does not own", findings)
    return after
