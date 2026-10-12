"""World contact points, their misses and CONTACT_WORLD (plan F5.1, F5.2; owners O24, O72, O81, O83).

For each touch, hold and support: the actor's point (the S13 key at the contact's instant, its world points by forward
kinematics) and the target's point (a prop's sample at that instant; a surface's top, vertically; another body's
surface, from its own key: the nearest point of the named part's capsules, the torso when none is named), and the
distance between them; between two bodies it runs from surface to surface, the actor's part carrying its segment's
radius (RV-49, F-144: a strike is measured to the target's surface, and BODY_OVERLAP refuses one inside it; F-152 asks
the owner whether O72's point measure or this one holds). Flags mark the conditions ADR-O83 named for a measurement
artefact: the actor airborne, the actor's key turning, the prop moving at the instant. A
contact with no key at its instant, a prop with no sample there, or a surface with no top (a wall, a pillar's face; a
touch on any surface but a floor) is not measurable. `measure` reads an envelope (the report, the prose);
`measure_plan` reads S13's packet and its authored keys (the check). CONTACT_WORLD (ADR-O83, O89) refuses a
measurable miss over 0.15 m (O72) unless it is a genuine
artefact, or the owner's list keeps it with its reason (kernel/contact_world_exceptions.yaml, read through S13's packet,
never from an authored plan: the owner's source rows, ADR-O83 point 2, F-123); an exception that names anything but
such a miss is refused, so the list stays true. A genuine artefact (ADR-O104) is a contact measured between keys or
samples (an interpolated point) while its actor is airborne or its prop moves; at an exact instant nothing is exempt,
and a turn alone never is (O89). Every contact measured today sits at an exact instant (`interpolated` is false).
Every key's claimed supports (its S11 kinematic node) are measured too, not only a support contact's onset (RV-14a,
F-089; row id `<slot>:<part>`): each part to the top of the surface its open support contact names, or to the floor
when no contact names one (the lowest floor top, else the convention's ground). A part on any other surface than a
floor waits for that surface's faces (RV-22); a held or embedded prop at every sample waits for F-148 (RV-14b); a
contact between keys for RV-59. The owner's exceptions name contacts, so they keep covering only an onset.
"""

import hashlib
import math
from pathlib import Path

import yaml

from planner.dynamic_beat_validator import surface_tops
from solver import forward_kinematics
from solver.floor_penetration import floor_level
from solver.forward_kinematics import capsules, part_capsules, part_point, part_radius, points, surface_gap

TOLERANCE_M = 0.15  # owner O72
EXCEPTIONS = Path(__file__).resolve().parents[1] / "kernel" / "contact_world_exceptions.yaml"


def owner_exceptions(query):
    """{contact id: reason} the owner keeps for the scene whose query this is (ADR-O83 point 2, F-123): read from
    kernel/contact_world_exceptions.yaml, never from an authored plan."""
    key = hashlib.sha256(query.encode("utf-8")).hexdigest()
    entries = yaml.safe_load(EXCEPTIONS.read_text(encoding="utf-8"))["exceptions"]
    return {e["contact"]: f"{e['reason']} [{e['ruling']}]" for e in entries if e["query_sha256"] == key}
KINDS = {"surface": "foot or body on a surface", "prop": "limb to prop", "entity": "limb to body"}
MEASURED = ("touch", "possess", "support", "release")  # a release only of a prop: it leaves the hand where the hand is


def _words(text):
    return text.replace("_", " ")


def measure(envelope):
    """[{id, t, actor, part, target, kind, actor_point, target_point, distance, airborne, rotating, prop_moving,
    measurable, reason}] for every touch, possess and support contact and every release of a prop, in time order."""
    genre = envelope["scene"]["genre"]
    metres, radii = forward_kinematics.segments(genre), forward_kinematics.radii(genre)
    keys = {(k["entity"], round(k["t"], 6)): {**k, "capsules": capsules(k, metres, radii)}
            for k in envelope["nodes"]["motion"]["items"]}
    support = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
    surfaces = envelope["nodes"]["surfaces"]["items"]
    tops = surface_tops(surfaces, envelope["scene"]["ax"].get("ground"))
    samples = [sample for beat in envelope["nodes"]["beats"]["items"] for sample in beat.get("prop_samples", [])]
    return _rows(keys, support, tops, {s["id"] for s in surfaces if s["kind"] == "floor"}, samples,
                 envelope["nodes"]["contacts"]["items"], radii, floor_level(surfaces, envelope["scene"]["ax"].get("ground")))


def packet_view(envelope):
    """What S13's packet carries for CONTACT_WORLD: the contacts S07 wrote, the samples S04 wrote, the surfaces' tops."""
    surfaces = envelope["nodes"]["surfaces"]["items"]
    tops = surface_tops(surfaces, envelope["scene"]["ax"].get("ground"))
    return {"contacts": [{k: c[k] for k in ("id", "t", "contact_type", "body_part", "a", "b")}
                         for c in envelope["nodes"]["contacts"]["items"] if c["contact_type"] in MEASURED],
            "prop_samples": [{k: s[k] for k in ("prop", "t", "p", "v")} for beat in envelope["nodes"]["beats"]["items"]
                             for s in beat.get("prop_samples", [])],
            "surface_tops": dict(sorted(tops.items())), "floors": sorted(s["id"] for s in surfaces if s["kind"] == "floor"),
            "exceptions": owner_exceptions(envelope["provenance"]["source_prompt"])}


def plan_bodies(keys, slots, packet):
    """{(entity, t): {id, turn, points, capsules}} from S13's packet and its authored keys ({slot: key})."""
    return {(slots[slot]["entity"], round(slots[slot]["t"], 6)):
            {"id": slot, "turn": key["turn"], "points": points(key, packet["segments"]),
             "capsules": capsules(key, packet["segments"], packet["radii"])} for slot, key in keys.items()}


def measure_plan(keys, slots, packet):
    """The same rows from S13's packet and its authored keys ({slot: key}), the points by forward kinematics."""
    view = packet["contact_world"]
    support = {slot: slots[slot]["kinematic"]["support"] for slot in keys}
    return _rows(plan_bodies(keys, slots, packet), support, view["surface_tops"], set(view["floors"]),
                 view["prop_samples"], view["contacts"], packet["radii"], packet.get("floor_y"))


def _rows(keys, support, tops, floors, prop_samples, contacts, radii, floor=None):
    samples = {}
    for sample in prop_samples:
        samples.setdefault((sample["prop"], round(sample["t"], 6)), []).append(sample)
    rows = []
    for c in sorted(contacts, key=lambda c: (c["t"], c["id"])):
        if c["contact_type"] not in MEASURED or (c["contact_type"] == "release" and c["b"]["kind"] != "prop"):
            continue  # RV-02b (F-075): a release lets a prop go from the hand; a foot leaving a surface is a takeoff
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
            if other is None:
                row["reason"] = f"no key for {_words(b['id'])} at {c['t']}"
                continue
            target = [other["capsules"][name] for name in part_capsules(b.get("part") or "torso")]
            row["distance"], row["target_point"] = surface_gap(point, part_radius(c["body_part"], radii), target)
        row["measurable"] = True
    rows += _claims(keys, support, tops, floors, contacts, floor)
    return sorted(rows, key=lambda row: (row["t"], row["id"]))


def _claims(keys, support, tops, floors, contacts, floor):
    """RV-14a (F-089): every key's claimed supports, each part to its open support contact's surface or to the floor;
    a support contact's own onset is measured with the contacts."""
    ordered = sorted(contacts, key=lambda c: (c["t"], c["id"]))
    onsets = {(c["a"]["id"], c["body_part"], round(c["t"], 6)) for c in ordered if c["contact_type"] == "support"}
    rows = []
    for (entity, t), key in sorted(keys.items(), key=lambda item: (item[0][1], item[0][0])):
        for part in support.get(key["id"]) or []:
            surface = None
            for c in ordered:
                if c["t"] > t + 1e-9:
                    break
                if (c["a"]["id"], c["body_part"], c["b"]["kind"]) == (entity, part, "surface"):
                    surface = c["b"]["id"] if c["contact_type"] == "support" else (None if c["contact_type"] == "release"
                                                                                   else surface)
            top = (tops.get(surface) if surface in floors else None) if surface else floor
            point = part_point(key["points"], part)
            if (entity, part, t) in onsets or top is None or point is None:
                continue  # an onset is measured with its contact; a face (RV-22) or a part with no point is not
            rows.append({"id": f"{key['id']}:{part}", "t": t, "actor": entity, "part": part, "kind": KINDS["surface"],
                         "target": _words(surface) if surface else "the floor", "actor_point": point,
                         "target_point": [point[0], top, point[2]], "distance": round(abs(point[1] - top), 3),
                         "measurable": True, "reason": "", "airborne": False, "rotating": key["turn"] != "none",
                         "prop_moving": False, "interpolated": False})
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
    findings += [{"code": "CONTACT_WORLD", "contact": cid, "message": "the owner's exception list names a contact that is "
                  "not a real miss (it meets its target, is an artefact or is not measured)"}
                 for cid in sorted(exceptions) if cid not in real]
    return findings


def misses(envelope):
    return [row for row in measure(envelope) if row["measurable"] and row["distance"] > TOLERANCE_M]
