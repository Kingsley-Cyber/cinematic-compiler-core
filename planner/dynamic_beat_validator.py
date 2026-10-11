"""S04 checks on an authored beat plan, using only the plan and its packet (so anyone can re-run them).

Rules: unique ids; times inside the duration (or budget); actor/participants/parts resolve to the packet;
pos + facing for every entity in a beat; requires/effects use the closed vocabulary; contacts use declared
types and parts (a contact happens at its beat's end, or its start when marked `at: start`); causes point at real
later-or-same-time beats; no filler beats; modes come from the archetype card (mode_coherence) and a mode change needs
a beat that causes it (mode_transition).
Teleport (owner O12): a body faster than 25 m/s between the anchors of two of its consecutive beats is refused
(TELEPORT), unless the earlier beat is a substitution with that body as actor and the substitution changes a prop's
state (the decoy revealed; the owner's rule also names the smoke pellet and the log, generalised here to any prop).
Prop kinematics (owner O8, PROP_KINEMATICS): a beat's prop samples sit inside the beat and name declared props; a held
prop stays within 2 m of its holder's anchor; between two samples of a free prop with no contact on it in between, a
moving prop follows gravity from the first sample's velocity to the second position within 0.25 m, and a prop at rest
(v null or zero) does not move unless a contact on it at the second sample picks it up or knocks it down. A float
(stylised, no gravity) is allowed in anime only. The 2 m reach and the 0.25 m tolerance are Claude's interpretation.
"""

import math

from planner.vocabulary import allowed

EPSILON = 1e-9
GRAVITY = 9.81
REACH_M, KINEMATIC_TOLERANCE_M = 2.0, 0.25
TELEPORT_MPS = 25.0  # owner O12: anything faster between keys is a teleport (human sprint ~12, anime ~15, strikes ~20)


def _finding(code, message, beat=None, detail=None):
    return {"code": code, "message": message, "beat": beat, "detail": detail}


def validate(plan, packet):
    findings = []
    beats = plan["beats"]
    ids = [b["id"] for b in beats]
    by_id = {b["id"]: b for b in beats}
    for repeated in sorted({i for i in ids if ids.count(i) > 1}):
        findings.append(_finding("BEAT_ID", "Beat ids must be unique", repeated))
    entities = {e["id"]: e for e in packet["entities"]}
    props = {p["id"]: p for p in packet["props"]}
    surfaces = {s["id"]: s for s in packet["surfaces"]}
    known = {"entity": entities, "prop": props, "surface": surfaces}
    limit = packet["modality"]["duration_s"] or packet["modality"]["duration_budget_s"]
    incoming = {}
    for beat in beats:
        for cause in beat["causes"]:
            incoming.setdefault(cause["to"], []).append(beat["id"])
    last_mode = {}
    for beat in sorted(beats, key=lambda b: (b["t"], b["id"])):
        bid, end = beat["id"], beat["t"] + beat["dur"]
        if limit is not None and end > limit + EPSILON:
            findings.append(_finding("BEAT_TIME", "Beat ends after the scene duration or budget", bid, [end, limit]))
        if beat["event_type"] == "hold" and beat["dur"] <= 0:
            findings.append(_finding("BEAT_TIME", "A hold needs a positive duration", bid))
        if beat["actor"] not in entities:
            findings.append(_finding("BEAT_ACTOR", "Actor must be a declared entity", bid, beat["actor"]))
        for index, ref in enumerate(beat["participants"]):
            if ref["id"] not in known[ref["kind"]]:
                findings.append(_finding("BEAT_PARTICIPANT", "Participant is not declared", bid, ref))
            if ref in beat["participants"][:index] or (ref["kind"] == "entity" and ref["id"] == beat["actor"]):
                findings.append(_finding("BEAT_PARTICIPANT", "A participant is listed once and is not the actor", bid, ref))
        bodies = {beat["actor"]} | {r["id"] for r in beat["participants"] if r["kind"] == "entity"}
        for entity in sorted(bodies & set(entities)):
            for key in ("pos", "facing"):
                vector = beat[key].get(entity)
                if vector is None:
                    findings.append(_finding("BEAT_POSE_ANCHOR", f"Entity in the beat needs {key}", bid, entity))
                elif key == "facing" and all(abs(v) < EPSILON for v in vector):
                    findings.append(_finding("BEAT_POSE_ANCHOR", "facing must be a non-zero direction", bid, entity))
        for key in ("pos", "facing"):
            for entity in sorted(set(beat[key]) - set(entities)):
                findings.append(_finding("BEAT_POSE_ANCHOR", f"{key} names an undeclared entity", bid, entity))
        for kind in ("requires", "effects"):
            for fact in beat[kind]:
                subject = fact["subject"]
                if subject["id"] not in known[subject["kind"]]:
                    findings.append(_finding("BEAT_STATE", f"{kind} subject is not declared", bid, subject))
                    continue
                values = allowed(packet["vocabulary"], subject, fact["property"])
                if values is None:
                    findings.append(_finding("BEAT_STATE", f"{kind} property is not in the vocabulary", bid, fact["property"]))
                elif fact["value"] not in values:
                    findings.append(_finding("BEAT_STATE", f"{kind} value is not allowed", bid,
                                             [fact["property"], fact["value"]]))
        for contact in beat["contacts"]:
            a, b = contact["a"], contact["b"]
            if a["id"] not in entities or a["part"] not in entities[a["id"]]["parts"]:
                findings.append(_finding("BEAT_CONTACT", "Contact side a needs a declared entity part", bid, a))
            if b["id"] not in known[b["kind"]]:
                findings.append(_finding("BEAT_CONTACT", "Contact side b is not declared", bid, b))
            elif b["part"] is not None and b["part"] not in known[b["kind"]][b["id"]].get("parts", []):
                findings.append(_finding("BEAT_CONTACT", "Contact side b part is not declared", bid, b))
        for cause in beat["causes"]:
            target = by_id.get(cause["to"])
            if target is None or cause["to"] == bid:
                findings.append(_finding("BEAT_CAUSE", "Cause must point at another declared beat", bid, cause["to"]))
            elif target["t"] + EPSILON < beat["t"]:
                findings.append(_finding("BEAT_CAUSE", "A beat cannot cause an earlier beat", bid, cause["to"]))
        if (beat["event_type"] != "hold" and not beat["effects"] and not beat["contacts"] and not beat["causes"]
                and not incoming.get(bid)):
            findings.append(_finding("FILLER_BEAT", "Non-hold beat changes nothing and links to nothing", bid))
        for entity, mode in sorted(beat["modes"].items()):
            if entity not in entities or mode not in entities[entity]["modes"]:
                findings.append(_finding("MODE_COHERENCE", "Mode is not one of the entity's card modes", bid, [entity, mode]))
                continue
            if entity in last_mode and last_mode[entity] != mode and not incoming.get(bid):
                findings.append(_finding("MODE_TRANSITION", "A mode change needs a beat that causes it", bid, [entity, mode]))
            last_mode[entity] = mode
    return findings + _teleports(beats) + _prop_kinematics(beats, props, packet["scene"]["genre"])


def _teleports(beats):
    findings, last = [], {}
    for beat in sorted(beats, key=lambda b: (b["t"], b["id"])):
        for entity, pos in sorted(beat["pos"].items()):
            if entity in last and pos is not None:
                before, t0, p0 = last[entity]
                dt = beat["t"] - t0
                distance = math.dist(p0, pos)
                speed = math.inf if dt <= EPSILON and distance > EPSILON else (distance / dt if dt > EPSILON else 0.0)
                if speed > TELEPORT_MPS + EPSILON:
                    exempt = before["event_type"] == "substitution" and before["actor"] == entity
                    if exempt and not any(e["subject"]["kind"] == "prop" for e in before["effects"]):
                        findings.append(_finding("TELEPORT", "A substitution must reveal a decoy (change a prop's state)",
                                                 before["id"], entity))
                    elif not exempt:
                        findings.append(_finding("TELEPORT", f"{entity} moves {distance:.2f} m in {dt:.2f} s "
                                                 f"({speed:.1f} m/s > {TELEPORT_MPS:g}) without a declared substitution",
                                                 beat["id"], [before["id"], beat["id"]]))
            if pos is not None:
                last[entity] = (beat, beat["t"], pos)
    return findings


def _at(beat, contact):
    """A contact happens at its beat's end, or at its start when marked `at: start`."""
    return beat["t"] + (0 if contact.get("at") == "start" else beat["dur"])


def holds(beats):
    """prop -> [(start, end, holder)] from possess and release contacts, in contact time order."""
    held, open_ = {}, {}
    events = sorted(((_at(b, c), b["t"], b["id"], i, c) for b in beats for i, c in enumerate(b["contacts"])),
                    key=lambda e: e[:4])
    for at, _, _, _, c in events:
        if c["b"]["kind"] != "prop":
            continue
        if c["contact_type"] == "possess":
            open_[c["b"]["id"]] = (at, c["a"]["id"])
        elif c["contact_type"] == "release" and c["b"]["id"] in open_:
            start, holder = open_.pop(c["b"]["id"])
            held.setdefault(c["b"]["id"], []).append((start, at, holder))
    for prop, (start, holder) in open_.items():
        held.setdefault(prop, []).append((start, math.inf, holder))
    return held


def _prop_kinematics(beats, props, genre):
    findings, held, samples, touches = [], holds(beats), {}, {}
    anchors = sorted(((b["t"], entity, pos) for b in beats for entity, pos in b["pos"].items() if pos is not None))
    for beat in beats:
        for c in beat["contacts"]:
            if c["b"]["kind"] == "prop":
                touches.setdefault(c["b"]["id"], []).append(_at(beat, c))
        for sample in beat.get("prop_samples", []):
            if sample["prop"] not in props:
                findings.append(_finding("PROP_KINEMATICS", "Sample names an undeclared prop", beat["id"], sample["prop"]))
            elif not beat["t"] - EPSILON <= sample["t"] <= beat["t"] + beat["dur"] + EPSILON:
                findings.append(_finding("PROP_KINEMATICS", "Sample time is outside its beat", beat["id"], sample["t"]))
            else:
                samples.setdefault(sample["prop"], []).append((sample, beat["id"]))
            if sample["float"] and genre != "anime":
                findings.append(_finding("PROP_KINEMATICS", "Only anime may float a prop", beat["id"], sample["prop"]))

    def holder_at(prop, t):
        return next((h for start, end, h in held.get(prop, []) if start - EPSILON <= t < end - EPSILON), None)

    def anchor(entity, t):
        return next((pos for at, e, pos in reversed(anchors) if e == entity and at <= t + EPSILON), None)

    for prop, rows in samples.items():
        rows.sort(key=lambda r: r[0]["t"])
        for sample, beat_id in rows:
            holder = holder_at(prop, sample["t"])
            if holder and anchor(holder, sample["t"]) and math.dist(sample["p"], anchor(holder, sample["t"])) > REACH_M:
                findings.append(_finding("PROP_KINEMATICS", f"{prop} is held by {holder} but {REACH_M:g} m away", beat_id,
                                         sample["t"]))
        for (first, _), (second, beat_id) in zip(rows, rows[1:], strict=False):
            span = second["t"] - first["t"]
            if span <= EPSILON or holder_at(prop, first["t"]) or first["float"]:
                continue
            if any(first["t"] + EPSILON < t < second["t"] - EPSILON for t in touches.get(prop, [])):
                continue  # a contact changes the flight between the two samples
            moving = first["v"] is not None and any(abs(x) > EPSILON for x in first["v"])
            if moving:
                expected = [first["p"][i] + first["v"][i] * span - (0.5 * GRAVITY * span * span if i == 1 else 0)
                            for i in range(3)]
                if math.dist(expected, second["p"]) > KINEMATIC_TOLERANCE_M:
                    findings.append(_finding("PROP_KINEMATICS", f"{prop} from {first['t']} would be at "
                                             f"{[round(x, 2) for x in expected]} at {second['t']}, not {second['p']}",
                                             beat_id, [first["t"], second["t"]]))
            elif math.dist(first["p"], second["p"]) > KINEMATIC_TOLERANCE_M and not any(
                    abs(t - second["t"]) <= EPSILON for t in touches.get(prop, [])):
                findings.append(_finding("PROP_KINEMATICS", f"{prop} at rest moves between {first['t']} and {second['t']} "
                                         "with no contact", beat_id, [first["t"], second["t"]]))
    return findings
