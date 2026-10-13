"""Cross-graph consistency (owner, 2026-10-13: the graphs must agree): every reference one graph makes into another
names something that exists there. A beat's performer is an entity; a contact's body part is a part its performer
declares and the beat declares that contact; a rule binds a beat that exists; every edge joins two nodes of its own
groups; every per-performer node sits on a performer and a beat that exist.

`problems(envelope)` gives [{code: GRAPH_REFERENCE, group, message}]; the gate runs it on every example
(tests/test_data_flow.py), and `python -m validators.cross_graph [envelope.json]` on any envelope.
"""

import json
import sys
from pathlib import Path

from validators.graph_map import load_examples

KINDS = {"entity": "entities", "prop": "props", "surface": "surfaces"}
# edge group: (node group of `from`, node group of `to`)
EDGES = {"temporal": ("beats", "beats"), "causal": ("beats", "beats"), "beat_constraint": ("beats", "constraints"),
         "state_transition": ("states", "states"), "contact": ("contacts", "contacts"),
         "hand_role_transition": ("hand_role", "hand_role"),
         "object_state_transition": ("object_state", "object_state"),
         "affordance_dependency": ("affordance", "affordance"),
         "kinematic_transition": ("kinematic", "kinematic"), "bartenieff_transition": ("bartenieff", "bartenieff"),
         "motion": ("motion", "motion"), "facial_transition": ("facial", "facial"), "effort": ("efforts", "efforts"),
         "camera": ("camera", "camera"), "pose_mechanics_transition": ("pose_mechanics", "pose_mechanics")}
PER_PERFORMER = ("kinematic", "bartenieff", "motion", "facial")
END = "end"  # S06's closing snapshot: one state per subject per beat, plus the end (state_graph schema)
MIDPOINT = "midpoint"  # a shot's target between the two axis entities (camera_graph schema)


def _items(envelope, kind, group):
    return envelope.get(kind, {}).get(group, {}).get("items", [])


def problems(envelope):
    out = []

    def add(group, message):
        out.append({"code": "GRAPH_REFERENCE", "group": group, "message": message})

    ids = {group: {i["id"] for i in _items(envelope, "nodes", group)} for group in
           ("entities", "props", "surfaces", "constraints", "beats", "states", "contacts", "hand_role", "object_state",
            "affordance", "kinematic", "bartenieff", "motion", "pose_mechanics", "facial", "efforts", "camera")}
    parts = {i["id"]: set(i.get("parts", [])) for g in ("entities", "props") for i in _items(envelope, "nodes", g)}
    beats = {b["id"]: b for b in _items(envelope, "nodes", "beats")}

    def ref(group, where, target):
        """`target` is {id, kind} (a scene thing) or a bare entity id."""
        if isinstance(target, dict):
            kind, ident = target.get("kind"), target.get("id")
            if kind == "scene":
                return
            if ident not in ids.get(KINDS.get(kind, ""), set()):
                add(group, f"{where}: {kind} '{ident}' does not exist")
        elif target not in ids["entities"]:
            add(group, f"{where}: performer '{target}' does not exist")

    def part(group, where, owner, name):
        if name is not None and owner in parts and name not in parts[owner]:
            add(group, f"{where}: '{name}' is not a part {owner} declares")

    for b in beats.values():
        where = f"beat {b['id']}"
        ref("beats", f"{where} actor", b["actor"])
        for key in ("pos", "facing", "modes"):
            for performer in b.get(key) or {}:
                ref("beats", f"{where} {key}", performer)
        for p in b.get("participants", []):
            ref("beats", f"{where} participant", p)
        for key in ("effects", "requires"):
            for fact in b.get(key, []):
                ref("beats", f"{where} {key}", fact["subject"])
        for cause in b.get("causes", []):
            if cause["to"] not in beats:
                add("beats", f"{where} causes '{cause['to']}', which is not a beat")
        for c in b.get("contacts", []):
            for end in ("a", "b"):
                ref("beats", f"{where} contact {end}", c[end])
                part("beats", f"{where} contact {end}", c[end]["id"], c[end].get("part"))
    for c in _items(envelope, "nodes", "contacts"):
        where = f"contact {c['id']}"
        beat = beats.get(c["beat"])
        if beat is None:
            add("contacts", f"{where}: beat '{c['beat']}' does not exist")
            continue
        ref("contacts", f"{where} a", c["a"])
        ref("contacts", f"{where} b", c["b"])
        part("contacts", f"{where} body part", c["a"]["id"], c["body_part"])
        declared = any(d["a"]["id"] == c["a"]["id"] and d["a"].get("part") == c["body_part"]
                       and d["b"]["id"] == c["b"]["id"] and d["contact_type"] == c["contact_type"]
                       for d in beat.get("contacts", []))
        if not declared:
            add("contacts", f"{where}: {c['a']['id']} {c['body_part']} to {c['b']['id']} ({c['contact_type']}) is not "
                            f"a contact beat {c['beat']} declares")
    for s in _items(envelope, "nodes", "states"):
        ref("states", f"state {s['id']} subject", s["subject"])
        if s.get("beat") not in beats and s.get("beat") not in (None, END):
            add("states", f"state {s['id']}: beat '{s['beat']}' does not exist")
    for group in PER_PERFORMER:
        for n in _items(envelope, "nodes", group):
            ref(group, f"{group} {n['id']} entity", n["entity"])
            if n.get("beat") is not None and n["beat"] not in beats:
                add(group, f"{group} {n['id']}: beat '{n['beat']}' does not exist")
    for k in _items(envelope, "nodes", "kinematic"):
        for name in k.get("support", []):
            part("kinematic", f"kinematic {k['id']} support", k["entity"], name)
    for e in _items(envelope, "nodes", "efforts"):
        ref("efforts", f"effort {e['id']} actor", e["actor"])
        for beat in e.get("beats", []):
            if beat not in beats:
                add("efforts", f"effort {e['id']}: beat '{beat}' does not exist")
    things = ids["entities"] | ids["props"] | ids["surfaces"]
    for cam in _items(envelope, "nodes", "camera"):
        where = f"shot {cam['id']}"
        for beat in cam.get("beats", []):
            if beat not in beats:
                add("camera", f"{where}: beat '{beat}' does not exist")
        targets = [cam.get("position", {}).get("target"), cam.get("focus", {}).get("target"),
                   *cam.get("framing", {}).get("subjects", [])]
        for target in (t for t in targets if t not in (None, MIDPOINT)):
            if target not in things:
                add("camera", f"{where}: '{target}' is not a performer, prop or surface")
    for p in _items(envelope, "nodes", "props"):
        if p.get("carried_by") is not None:
            ref("props", f"prop {p['id']} carried_by", p["carried_by"])
    for a in _items(envelope, "edges", "constraint_application"):
        if a["constraint_id"] not in ids["constraints"]:
            add("constraint_application", f"{a['id']}: rule '{a['constraint_id']}' does not exist")
        ref("constraint_application", a["id"], a["target"])
    for invariant in envelope.get("invariants", []):
        if invariant["id"] not in ids["constraints"]:
            add("invariants", f"invariant '{invariant['id']}' is not a rule of the constraint graph")
    for group, (source, target) in EDGES.items():
        for e in _items(envelope, "edges", group):
            start, end = e.get("from", e.get("from_state")), e.get("to", e.get("to_state"))
            if start not in ids[source]:
                add(group, f"{e['id']}: from '{start}' is not in {source}")
            if end not in ids[target]:
                add(group, f"{e['id']}: to '{end}' is not in {target}")
    for t in _items(envelope, "edges", "state_transition"):
        for beat in t.get("trigger_event", []):
            if beat not in beats:
                add("state_transition", f"{t['id']}: trigger '{beat}' is not a beat")
    render = _items(envelope, "nodes", "render")
    for performer in (render[0].get("labels", {}) if render else {}):
        ref("render", "render label", performer)
    return out


if __name__ == "__main__":
    envelopes = ({Path(p).parent.name: json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]}
                 or load_examples())
    for name, envelope in envelopes.items():
        found = problems(envelope)
        print(f"{name}: {len(found)} problem(s)")
        for p in found:
            print(f"  {p['group']}: {p['message']}")
    sys.exit(1 if any(problems(e) for e in envelopes.values()) else 0)
