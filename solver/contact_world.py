"""World contact points, their misses and CONTACT_WORLD (plan F5.1, F5.2; owners O24, O72, O81, O83).

For each touch, hold and support: the actor's point (the S13 key at the contact's instant, its world points by forward
kinematics) and the target's point (a prop's sample at that instant; another body's point from its own key; a
surface's top, vertically), and the distance between them. Flags mark the owner's measurement artefacts: the actor
airborne, the actor's key turning, the prop moving at the instant. A contact with no key at its instant, a prop with
no sample there, or a surface with no top (a wall, a pillar's face; a touch on any surface but a floor) is not
measurable. `measure` reads an envelope (the report, the prose); `measure_plan` reads S13's packet and its authored
keys (the check). CONTACT_WORLD (ADR-O83, O89) refuses a measurable miss over 0.15 m (O72) unless it is a genuine
artefact, or the motion plan lists it in `contact_world_exceptions` with its reason (the owner's source rows, ADR-O83
point 2, recorded in the golden test); an exception that names anything but such a miss is refused, so the list stays
true. A genuine artefact (ADR-O104) is a contact measured between keys or samples (an interpolated point) while its
actor is airborne or its prop moves; at an exact instant nothing is exempt, and a turn alone never is (O89). Every
contact measured today sits at an exact instant (`interpolated` is false).
"""

import math

from planner.dynamic_beat_validator import surface_tops
from solver.forward_kinematics import part_point, points

TOLERANCE_M = 0.15  # owner O72
KINDS = {"surface": "foot or body on a surface", "prop": "limb to prop", "entity": "limb to body"}
MEASURED = ("touch", "possess", "support")


def _words(text):
    return text.replace("_", " ")


def measure(envelope):
    """[{id, t, actor, part, target, kind, actor_point, target_point, distance, airborne, rotating, prop_moving,
    measurable, reason}] for every touch, possess and support contact, in time order."""
    keys = {(k["entity"], round(k["t"], 6)): k for k in envelope["nodes"]["motion"]["items"]}
    support = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
    surfaces = envelope["nodes"]["surfaces"]["items"]
    tops = surface_tops(surfaces, envelope["scene"]["ax"].get("ground"))
    samples = [sample for beat in envelope["nodes"]["beats"]["items"] for sample in beat.get("prop_samples", [])]
    return _rows(keys, support, tops, {s["id"] for s in surfaces if s["kind"] == "floor"}, samples,
                 envelope["nodes"]["contacts"]["items"])


def packet_view(envelope):
    """What S13's packet carries for CONTACT_WORLD: the contacts S07 wrote, the samples S04 wrote, the surfaces' tops."""
    surfaces = envelope["nodes"]["surfaces"]["items"]
    tops = surface_tops(surfaces, envelope["scene"]["ax"].get("ground"))
    return {"contacts": [{k: c[k] for k in ("id", "t", "contact_type", "body_part", "a", "b")}
                         for c in envelope["nodes"]["contacts"]["items"] if c["contact_type"] in MEASURED],
            "prop_samples": [{k: s[k] for k in ("prop", "t", "p", "v")} for beat in envelope["nodes"]["beats"]["items"]
                             for s in beat.get("prop_samples", [])],
            "surface_tops": dict(sorted(tops.items())), "floors": sorted(s["id"] for s in surfaces if s["kind"] == "floor")}


def measure_plan(keys, slots, packet):
    """The same rows from S13's packet and its authored keys ({slot: key}), the points by forward kinematics."""
    view = packet["contact_world"]
    named = {(slots[slot]["entity"], round(slots[slot]["t"], 6)):
             {"id": slot, "turn": key["turn"], "points": points(key, packet["segments"])} for slot, key in keys.items()}
    support = {slot: slots[slot]["kinematic"]["support"] for slot in keys}
    return _rows(named, support, view["surface_tops"], set(view["floors"]), view["prop_samples"], view["contacts"])


def _rows(keys, support, tops, floors, prop_samples, contacts):
    samples = {}
    for sample in prop_samples:
        samples.setdefault((sample["prop"], round(sample["t"], 6)), []).append(sample)
    rows = []
    for c in sorted(contacts, key=lambda c: (c["t"], c["id"])):
        if c["contact_type"] not in MEASURED:
            continue
        t, b = round(c["t"], 6), c["b"]
        key = keys.get((c["a"]["id"], t))
        row = {"id": c["id"], "t": c["t"], "actor": c["a"]["id"], "part": c["body_part"], "kind": KINDS[b["kind"]],
               "target": f"{_words(b['id'])}" + (f" {_words(b['part'])}" if b.get("part") else ""),
               "actor_point": None, "target_point": None, "distance": None, "measurable": False, "reason": "",
               "airborne": bool(key) and not support.get(key["id"]), "rotating": bool(key) and key["turn"] != "none",
               "prop_moving": False, "interpolated": False}
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


def artefact(row):
    """A genuine measurement artefact (O89, ADR-O104): a point interpolated between keys or samples while the actor is
    airborne or the prop moves. An exact-instant miss never is."""
    return row["interpolated"] and (row["airborne"] or row["prop_moving"])


def refusals(rows, exceptions):
    """CONTACT_WORLD findings (ADR-O83): a real miss that no exception lists, and an exception that lists no real miss."""
    real = {row["id"]: row for row in rows if row["measurable"] and row["distance"] > TOLERANCE_M and not artefact(row)}
    findings = [{"code": "CONTACT_WORLD", "contact": cid, "message": f"{row['actor']} {_words(row['part'])} misses "
                 f"{row['target']} by {row['distance']:g} m at {row['t']:g} (over {TOLERANCE_M:g} m, owner O72)"}
                for cid, row in real.items() if cid not in exceptions]
    findings += [{"code": "CONTACT_WORLD", "contact": cid, "message": "contact_world_exceptions lists a contact that is "
                  "not a real miss (it meets its target, is an artefact or is not measured)"}
                 for cid in sorted(exceptions) if cid not in real]
    return findings


def misses(envelope):
    return [row for row in measure(envelope) if row["measurable"] and row["distance"] > TOLERANCE_M]
