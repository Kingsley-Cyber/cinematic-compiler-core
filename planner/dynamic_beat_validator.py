"""S04 checks on an authored beat plan, using only the plan and its packet (so anyone can re-run them).

Rules: unique ids; times inside the duration (or budget); actor/participants/parts resolve to the packet;
pos + facing for every entity in a beat; requires/effects use the closed vocabulary; contacts use declared
types and parts; causes point at real later-or-same-time beats; no filler beats; modes come from the archetype
card (mode_coherence) and a mode change needs a beat that causes it (mode_transition).
Teleport (owner O12): a body faster than 25 m/s between the anchors of two of its consecutive beats is refused
(TELEPORT), unless the earlier beat is a substitution with that body as actor and the substitution changes a prop's
state (the decoy revealed; the owner's rule also names the smoke pellet and the log, generalised here to any prop).
"""

import math

from planner.vocabulary import allowed

EPSILON = 1e-9
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
    return findings + _teleports(beats)


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
