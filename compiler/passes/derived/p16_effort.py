"""S16 pass (band L5, authored): LMA Effort, Shape and Space per interval of one entity's consecutive slots.

Checks: an interval names slots its actor has, consecutive in time; every slot is covered exactly once; values come
from library/laban_vocabulary.yaml; the effort action matches weight x time x space (Laban's eight basic effort
actions, none unless all three are active); the effort mode card exists and the intensity lies in its range.
Derived: each interval's time span and `overlaps` edges between intervals of different entities.
"""

import json

import yaml

from compiler.authoring import run_authored, seal
from planner import library_vocab
from planner.dependency_graph import ROOT, load
from planner.scene_view import slots
from solver import shape_direction
from validators.schema_validator import validate_schema

NODE, STEP = "effort", "S16"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "effort_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "laban_synthesis.txt"
EPSILON = 1e-9
ACTIONS = {("light", "sustained", "indirect"): "float", ("strong", "sudden", "direct"): "punch",
           ("light", "sustained", "direct"): "glide", ("strong", "sudden", "indirect"): "slash",
           ("light", "sudden", "direct"): "dab", ("strong", "sustained", "indirect"): "wring",
           ("light", "sudden", "indirect"): "flick", ("strong", "sustained", "direct"): "press"}


def effort_modes():
    schema = json.loads((ROOT / "schemas" / "cards" / "effort_mode_card.schema.json").read_text(encoding="utf-8"))
    modes = {}
    for path in sorted((ROOT / "library" / "effort_modes").glob("*.yaml")):
        card = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_schema(card, schema)
        modes[card["card_id"]] = card
    return modes


def _body(node, drop=("id", "entity", "beat", "t")):
    return {k: v for k, v in node.items() if k not in drop}


def prepare(envelope):
    groups = {g: {n["id"]: n for n in envelope["nodes"][g]["items"]} for g in ("kinematic", "bartenieff", "motion")}
    beats = {b["id"]: b for b in envelope["nodes"]["beats"]["items"]}
    view = [{**{k: s[k] for k in ("slot", "entity", "beat", "t", "dur", "role", "label", "action")},
             "mode": beats[s["beat"]]["modes"].get(s["entity"]),
             "kinematic": _body(groups["kinematic"][s["slot"]]), "bartenieff": _body(groups["bartenieff"][s["slot"]]),
             "motion": _body(groups["motion"][s["slot"]], ("id", "entity", "beat", "t", "quat", "heading_basis"))}
            for s in slots(envelope)]
    modes = {k: {f: v[f] for f in ("description", "intensity", "tendencies")} for k, v in effort_modes().items()}
    return seal({"step_id": STEP, "band": "L5", "kind": "effort_plan", "schema": "urn:cinematic-compiler:schema:effort_plan:1.1",
                 "instructions": PROMPT.read_text(encoding="utf-8"), "slots": view,
                 "vocabulary": library_vocab.load("laban_vocabulary")["fields"], "effort_modes": modes})


def interval_id(interval):
    first, last = interval["beats"][0], interval["beats"][-1]
    return f"{interval['actor']}@{first}" + ("" if first == last else f"-{last}")


def _values(interval):
    return {**{f"effort.{k}": v for k, v in interval["effort"].items()}, "effort_action": interval["effort_action"],
            **{f"shape.{k}": v for k, v in interval["shape"].items()}, **{f"space.{k}": v for k, v in interval["space"].items()},
            "effort_mode": interval["effort_mode"]}


def check(document, packet):
    findings, covered = [], {}
    by_id = {s["slot"]: s for s in packet["slots"]}
    sequence = {}
    for s in packet["slots"]:
        sequence.setdefault(s["entity"], []).append(s["slot"])
    vocabulary = {"fields": packet["vocabulary"]}
    for interval in document["intervals"]:
        label = interval_id(interval)
        ids = [f"{interval['actor']}@{b}" for b in interval["beats"]]
        if any(i not in by_id for i in ids):
            findings.append({"code": "EFFORT_INTERVAL", "message": "Interval names a slot its actor does not have",
                             "slot": label})
            continue
        positions = [sequence[interval["actor"]].index(i) for i in ids]
        if positions != list(range(positions[0], positions[0] + len(positions))):
            findings.append({"code": "EFFORT_INTERVAL", "message": "An interval runs over consecutive slots in time order",
                             "slot": label})
        for i in ids:
            covered[i] = covered.get(i, 0) + 1
        for field, value in _values(interval).items():
            for problem in library_vocab.problems(vocabulary, field, value, []):
                findings.append({"code": "EFFORT_VOCABULARY", "message": problem, "slot": label})
        effort = interval["effort"]
        expected = ACTIONS.get((effort["weight"], effort["time"], effort["space"]), "none")
        if interval["effort_action"] != expected:
            findings.append({"code": "EFFORT_ACTION", "message": f"weight, time and space make {expected}", "slot": label})
        span = ids + sequence[interval["actor"]][positions[-1] + 1:positions[-1] + 2]
        quality = interval["shape"]["quality"]
        if len(span) > 1 and quality in shape_direction.OPPOSITE and shape_direction.judge(
                quality, [by_id[i]["motion"] for i in span], [by_id[i]["kinematic"]["support"] for i in span]) == "contradicted":
            findings.append({"code": "SHAPE_DIRECTION", "message": f"The body shows the opposite of shape {quality} "
                             "(owner O31, O73)", "slot": label})
        mode = packet["effort_modes"].get(interval["effort_mode"])
        if mode is not None and not mode["intensity"][0] <= interval["intensity"] <= mode["intensity"][1]:
            findings.append({"code": "EFFORT_MODE", "message": f"Intensity is outside the {interval['effort_mode']} range",
                             "slot": label})
    for slot_id in by_id:
        if covered.get(slot_id, 0) != 1:
            findings.append({"code": "EFFORT_COVERAGE", "message": "Every slot belongs to exactly one interval", "slot": slot_id})
    return findings


def build(envelope, document, packet):
    by_id = {s["slot"]: s for s in packet["slots"]}
    nodes = []
    for interval in document["intervals"]:
        spans = [by_id[f"{interval['actor']}@{b}"] for b in interval["beats"]]
        nodes.append({"id": interval_id(interval), **interval, "t": spans[0]["t"],
                      "end": round(max(s["t"] + s["dur"] for s in spans), 6) + 0.0})
    nodes.sort(key=lambda n: (n["t"], n["id"]))
    edges = []
    for i, left in enumerate(nodes):
        for right in nodes[i + 1:]:
            start, end = max(left["t"], right["t"]), min(left["end"], right["end"])
            if left["actor"] != right["actor"] and end - start > EPSILON:
                edges.append({"id": f"{left['id']}__{right['id']}", "from": left["id"], "to": right["id"], "relation": "overlaps",
                              "start": start, "end": end})
    return {"/nodes/efforts": nodes, "/edges/effort": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
