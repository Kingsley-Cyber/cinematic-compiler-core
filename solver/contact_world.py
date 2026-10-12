"""World contact points and their misses (plan F5.1, owners O24, O72, O81).

For each touch, hold and support in the envelope: the actor's point (the S13 key at the contact's instant, its world
points by forward kinematics) and the target's point (a prop's sample at that instant; another body's point from its
own key; a surface's top, vertically), and the distance between them. CONTACT_WORLD will refuse a distance over
0.15 m (ADR-O72) once the owner has reviewed the misses (ADR-O81, backlog M9-06b); until then this only measures.
Flags mark what the owner asked to separate from real misses: the actor airborne, the actor's key turning, the prop
moving at the instant. A contact with no key at its instant, a prop with no sample there, or a surface with no top (a
wall, a pillar's face; a touch on any surface but a floor) is not measurable.
"""

import math

from planner.dynamic_beat_validator import surface_tops
from solver.forward_kinematics import part_point

TOLERANCE_M = 0.15  # owner O72
KINDS = {"surface": "foot or body on a surface", "prop": "limb to prop", "entity": "limb to body"}


def _words(text):
    return text.replace("_", " ")


def measure(envelope):
    """[{id, t, actor, part, target, kind, actor_point, target_point, distance, airborne, rotating, prop_moving,
    measurable, reason}] for every touch, possess and support contact, in time order."""
    keys = {(k["entity"], round(k["t"], 6)): k for k in envelope["nodes"]["motion"]["items"]}
    support = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
    tops = surface_tops(envelope["nodes"]["surfaces"]["items"], envelope["scene"]["ax"].get("ground"))
    floors = {s["id"] for s in envelope["nodes"]["surfaces"]["items"] if s["kind"] == "floor"}
    samples = {}
    for beat in envelope["nodes"]["beats"]["items"]:
        for sample in beat.get("prop_samples", []):
            samples.setdefault((sample["prop"], round(sample["t"], 6)), []).append(sample)
    rows = []
    for c in sorted(envelope["nodes"]["contacts"]["items"], key=lambda c: (c["t"], c["id"])):
        if c["contact_type"] not in ("touch", "possess", "support"):
            continue
        t, b = round(c["t"], 6), c["b"]
        key = keys.get((c["a"]["id"], t))
        row = {"id": c["id"], "t": c["t"], "actor": c["a"]["id"], "part": c["body_part"], "kind": KINDS[b["kind"]],
               "target": f"{_words(b['id'])}" + (f" {_words(b['part'])}" if b.get("part") else ""),
               "actor_point": None, "target_point": None, "distance": None, "measurable": False, "reason": "",
               "airborne": bool(key) and not support.get(key["id"]), "rotating": bool(key) and key["turn"] != "none",
               "prop_moving": False}
        rows.append(row)
        if key is None:
            row["reason"] = "no key at the contact's instant"
            continue
        point = part_point(key["points"], c["body_part"])
        if point is None:
            row["reason"] = f"no point for {c['body_part']}"
            continue
        row["actor_point"] = point
        if b["kind"] == "surface":
            if b["id"] not in tops or (c["contact_type"] == "touch" and b["id"] not in floors):
                row["reason"] = "a surface's face (no top to meet)"  # a touch on a wall or a pillar; a floor has only a top
                continue
            row["target_point"] = [point[0], tops[b["id"]], point[2]]
            row["distance"] = round(abs(point[1] - tops[b["id"]]), 3)
        elif b["kind"] == "prop":
            here = samples.get((b["id"], t), [])
            if not here:
                row["reason"] = f"no {_words(b['id'])} sample at {c['t']}"
                continue
            row["prop_moving"] = any(s["v"] is not None and any(abs(x) > 1e-9 for x in s["v"]) for s in here)
            row["target_point"] = list(here[0]["p"])
            row["distance"] = round(math.dist(point, here[0]["p"]), 3)
        else:
            other = keys.get((b["id"], t))
            target = part_point(other["points"], b.get("part") or "torso") if other else None
            if target is None:
                row["reason"] = f"no key or point for {_words(b['id'])} at {c['t']}"
                continue
            row["target_point"] = target
            row["distance"] = round(math.dist(point, target), 3)
        row["measurable"] = True
    return rows


def misses(envelope):
    return [row for row in measure(envelope) if row["measurable"] and row["distance"] > TOLERANCE_M]
