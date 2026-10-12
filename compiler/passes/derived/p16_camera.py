"""S16 pass (band L5.5, authored): the shot list — 13 subdivisions + motivation per shot, checked and placed.

The packet carries the scene facts a camera answers to (beats, positions, contact onsets, effort intervals, causal
edges, surfaces) and the camera library (subdivision vocabulary, grammar, tempo, the genre's conventions, the
archetypes' idioms), and each performer's body points at every beat (F-090, RV-15a). Checks:
validators/camera_validator.py. Derived: the aim (the middle of the parts the scale shows), camera position, side,
field of view, frame height and screen x per subject (solver/camera_geometry.py), and `cuts_to` edges between
consecutive shots.
"""

from compiler.authoring import run_authored, seal
from planner import camera_library, hits, library_vocab
from planner.dependency_graph import ROOT, load
from solver import forward_kinematics
from solver.camera_geometry import azimuth_change
from solver.quaternion import head_heading
from validators import camera_validator

NODE, STEP = "camera", "S16"
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "camera_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "camera_selection.txt"
ONSETS = ("touch", "possess", "support")


def _positions(envelope, beats, entities):
    states = {s["id"]: s for s in envelope["nodes"]["states"]["items"]}
    anchors = {e: next((states[f"{e}@{b['id']}"]["pos"] for b in beats if states[f"{e}@{b['id']}"]["pos"] is not None), None)
               for e in entities}
    return {b["id"]: {e: states[f"{e}@{b['id']}"]["pos"] or anchors[e] for e in entities if anchors[e] is not None}
            for b in beats}


def _points(envelope, beats, entities):
    """{beat: {entity: {part: [x, y, z]}}}: each entity's body points at its key in each beat (forward kinematics of the
    S13 keys), carried from its last key, and from its first before it has one, as `_positions` carries the anchors
    (F-090, RV-15a: the camera aims at the body it frames)."""
    metres = forward_kinematics.segments(envelope["scene"]["genre"])
    keys = {k["id"]: k for k in envelope["nodes"]["motion"]["items"]}
    bodies = {(e, b["id"]): {part: [round(v, 4) + 0.0 for v in point]
                             for part, point in forward_kinematics.points(keys[f"{e}@{b['id']}"], metres).items()}
              for b in beats for e in entities if f"{e}@{b['id']}" in keys}
    last = {e: next((bodies[e, b["id"]] for b in beats if (e, b["id"]) in bodies), None) for e in entities}
    out = {}
    for b in beats:
        last |= {e: bodies[e, b["id"]] for e in entities if (e, b["id"]) in bodies}
        out[b["id"]] = {e: last[e] for e in sorted(entities) if last[e] is not None}
    return out


def prepare(envelope):
    scene = envelope["scene"]
    beats = sorted(envelope["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"]))
    entities = {e["id"]: {"archetype": e["card_id"], "parts": e["parts"]} for e in envelope["nodes"]["entities"]["items"]}
    ids = sorted(entities)
    motion = {n["id"]: {k: n[k] for k in ("name", "turn", "description")} for n in envelope["nodes"]["motion"]["items"]}
    return seal({
        "step_id": STEP, "band": "L5.5", "kind": "camera_plan", "schema": "urn:cinematic-compiler:schema:camera_plan:1.0",
        "instructions": PROMPT.read_text(encoding="utf-8"),
        "scene": {k: scene[k] for k in ("genre", "duration_s", "fps", "setting", "style_reference")},
        "beats": [{"id": b["id"], "t": b["t"], "dur": b["dur"], "event_type": b["event_type"], "actor": b["actor"],
                   "participants": [p["id"] for p in b["participants"] if p["kind"] == "entity"], "label": b["label"],
                   "action": b["action"]} for b in beats],
        "beat_index": {b["id"]: i for i, b in enumerate(beats)},
        "entities": entities, "props": sorted(p["id"] for p in envelope["nodes"]["props"]["items"]),
        "surfaces": sorted(s["id"] for s in envelope["nodes"]["surfaces"]["items"]),
        "axis": ids[:2] if len(ids) >= 2 else [], "positions": _positions(envelope, beats, ids),
        "points": _points(envelope, beats, ids),
        "contacts": [{"id": c["id"], "t": c["t"], "beat": c["beat"], "contact_type": c["contact_type"], "entity": c["a"]["id"],
                      "part": c["body_part"], "other": c["b"]["id"]}
                     for c in envelope["nodes"]["contacts"]["items"]
                     # a contact carried from the previous clip or open at t=0 is the starting state, not an event
                     if c["contact_type"] in ONSETS and c["a"]["kind"] == "entity" and c["beat"] != "chain"
                     and c["t"] > 1e-9],
        "efforts": [{k: e[k] for k in ("id", "actor", "t", "end", "effort_action", "intensity")}
                    for e in envelope["nodes"]["efforts"]["items"]],
        "causal": [{k: e[k] for k in ("id", "from", "to")} for e in envelope["edges"]["causal"]["items"]],
        "hits": hits.hits(envelope),  # owner O92 (F-155, RV-57): each owes a camera hold on its bodies
        "motion": motion, "vocabulary": library_vocab.load("camera_subdivisions")["fields"],
        "grammar": camera_library.grammar(), "tempo": camera_library.tempo(),
        "convention": camera_library.convention(scene["genre"]),
        "idioms": camera_library.idioms(sorted({e["archetype"] for e in entities.values()})),
        **({"chained_last_shot": scene["chained_from"]["last_shot"]} if scene.get("chained_from") else {}),
        **({"faces": _faces(envelope)} if "facial" in envelope["nodes"] else {})})


def _faces(envelope):
    """S14 faces the camera must answer to: salience, head heading and the dominant side of one-sided units."""
    motion = {n["id"]: n for n in envelope["nodes"]["motion"]["items"]}
    return [{"slot": f["id"], "entity": f["entity"], "beat": f["beat"], "salience": f["salience"],
             "head_heading_deg": head_heading(motion[f["id"]]),
             "dominant_sides": sorted({u["asymmetry"]["dominant_side"] for u in f["aus"] if not u["bilateral"]})}
            for f in envelope["nodes"]["facial"]["items"]]


def check(document, packet):
    return camera_validator.check(document["shots"], packet)[0]


def build(envelope, document, packet):
    derived = camera_validator.check(document["shots"], packet)[1]
    nodes = [{**shot, "derived": derived[shot["id"]]} for shot in sorted(document["shots"], key=lambda s: (s["t"], s["id"]))]
    edges = [{"id": f"{a['id']}__{b['id']}", "from": a["id"], "to": b["id"], "relation": "cuts_to",
              "transition": b["editing"]["transition_in"], "axis": b["editing"]["axis"],
              "side_from": a["derived"]["side"], "side_to": b["derived"]["side"],
              "azimuth_change_deg": azimuth_change(a["angle"]["azimuth_deg"], b["angle"]["azimuth_deg"]),
              "scale_from": a["framing"]["scale"], "scale_to": b["framing"]["scale"]}
             for a, b in zip(nodes, nodes[1:], strict=False)]
    return {"/nodes/camera": nodes, "/edges/camera": edges}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=check, build=build, order=order or load())
