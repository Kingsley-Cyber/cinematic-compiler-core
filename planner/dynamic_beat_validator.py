"""S04 checks on an authored beat plan, using only the plan and its packet (so anyone can re-run them).

Rules: unique ids; times inside the duration (or budget); actor/participants/parts resolve to the packet;
pos + facing for every entity in a beat; requires/effects use the closed vocabulary; contacts use declared
types and parts (a contact happens at its beat's end, or its start when marked `at: start`); causes point at real
later-or-same-time beats; no filler beats; modes come from the archetype card (mode_coherence) and a mode change needs
a beat that causes it (mode_transition).
Teleport (owner O12): a body faster than 25 m/s between the anchors of two of its consecutive beats is refused
(TELEPORT), unless the earlier beat is a substitution with that body as actor and the substitution changes a prop's
state (the decoy revealed; the owner's rule also names the smoke pellet and the log, generalised here to any prop).
Vanished body (owner O18, audit X9, VANISHED_BODY): from a substitution's start until its actor's next beat as actor,
no other beat lists, anchors or touches with that actor.
Prop kinematics (owner O8, PROP_KINEMATICS): a beat's prop samples sit inside the beat and name declared props; a held
prop stays within 2 m of its holder's anchor; between two samples of a free prop with no contact on it in between, a
moving prop follows gravity from the first sample's velocity to the second position within 0.25 m, and a prop at rest
(v null or zero) does not move unless a contact on it at the second sample picks it up or knocks it down. A float
(stylised, no gravity) is allowed in anime only. The 2 m reach and the 0.25 m tolerance are Claude's interpretation.
Surface height (owner O21, audit X7, SURFACE_HEIGHT): when a foot starts bearing weight on a surface whose top is known
(its world card's geometry text, "from y=0 to y=8"; a floor without one sits at the convention's ground), the
performer's root (its anchor at that instant; a landing between two keys has none and is not judged) lies between
the top and the standing leg of the genre's body above it (the packet's `standing_leg_m`: thigh, shin and ankle of
library/body_segments.yaml, owner O85), within 0.05 m either way. Interpretation (Claude's, for owner review): the
range (1.2 m above the top before S-029); the root is the pelvis (ADR-O72).
Prop support (owner O78, PROP_SUPPORT): a free prop at rest lies on a surface's top (within 0.1 m of its height),
or a fact since its last hold places it (a location, or worn: yes on its wearer). Interpretation (Claude's, for owner
review): the height alone stands for "on the top" (surfaces have no extent), and a card's worn state is the wearer's
support.
Combat verbs (owner O22, plan F4.1, CONTACT_VERB): a contact's optional verb is one its contact type takes in the
packet's `combat_verbs` (library/combat_verbs.yaml); catch, throw and disarm name a prop, and a thrown prop has a sample
with velocity at the throw (interpretation: a throw sends the prop off moving, so a touch may throw).
Contact pairs (plan F2.2): two samples of a prop share a time only as a `pre` and a `post` on a contact on that prop at
that instant, at one position (the contact is instantaneous); gravity is checked into the pre sample, velocity too,
and out of the post sample. Interpretation (Claude's, for owner review): a free prop moving into a contact needs the
pair, and the velocity into a pre sample is held to 0.25 m/s.
"""

import math
import re

from planner.vocabulary import allowed

EPSILON = 1e-9
GRAVITY = 9.81
REACH_M, KINEMATIC_TOLERANCE_M = 2.0, 0.25
VELOCITY_TOLERANCE_MPS = 0.25  # interpretation (Claude's, for owner review): the pre sample's velocity under gravity
PHASE_ORDER = {"pre": 0, None: 1, "post": 2}
BEFORE = 1e-6  # a pre sample's holder is read this long before its contact
TOP = re.compile(r"to y=(-?\d+(?:\.\d+)?)")
GROUND = re.compile(r"y=(-?\d+(?:\.\d+)?)")
# interpretation (Claude's, for owner review): a root's height over its supporting top; a resting prop on a top
SURFACE_SLACK_M, SUPPORT_M = 0.05, 0.1
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
            verb = contact.get("verb")
            if verb is not None and verb not in packet["combat_verbs"].get(contact["contact_type"], []):
                findings.append(_finding("CONTACT_VERB", f"A {contact['contact_type']} contact does not take the verb "
                                         f"{verb}", bid, contact))
            elif verb in ("catch", "throw", "disarm") and b["kind"] != "prop":
                findings.append(_finding("CONTACT_VERB", f"A {verb} names a prop", bid, contact))
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
    return (findings + _teleports(beats) + _vanished(beats) + _prop_kinematics(beats, props, packet["scene"]["genre"])
            + _thrown(beats) + _surface_heights(beats, _tops(packet), packet["standing_leg_m"])
            + _prop_support(beats, _tops(packet)))


def _prop_support(beats, tops):
    """PROP_SUPPORT (owner O78, F-065): a free prop at rest has something under it."""
    findings, held = [], holds(beats)
    facts = sorted((b["t"] if kind == "requires" else b["t"] + b["dur"], f["subject"]["id"], f["property"], f["value"])
                   for b in beats for kind in ("requires", "effects") for f in b[kind] if f["subject"]["kind"] == "prop")
    for beat in beats:
        for sample in beat.get("prop_samples", []):
            prop, t = sample["prop"], sample["t"]
            moving = sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"])
            spans = held.get(prop, [])
            if moving or sample["float"] or any(start - EPSILON <= t < end - EPSILON for start, end, _ in spans):
                continue
            if any(abs(sample["p"][1] - top) <= SUPPORT_M + EPSILON for top in tops.values()):
                continue
            since = max((end for _, end, _ in spans if end <= t + EPSILON), default=-math.inf)
            if not any(what == prop and since - EPSILON <= at <= t + EPSILON and (
                    (name == "location" and value != "unknown") or (name == "worn" and value == "yes"))
                       for at, what, name, value in facts):
                findings.append(_finding("PROP_SUPPORT", f"{prop} rests at {sample['p']} at {t} with nothing under it "
                                         "(owner O78)", beat["id"], t))
    return findings


def _tops(packet):
    return surface_tops(packet["surfaces"], packet["scene"].get("ax", {}).get("ground", ""))


def surface_tops(surfaces, ground_text):
    """{surface: top y} from each surface's geometry text, a floor without one at the convention's ground (S04 and
    the prose's entrances share it)."""
    ground = GROUND.search(str(ground_text))
    tops = {}
    for surface in surfaces:
        found = TOP.search(surface.get("ax") or "")
        if found:
            tops[surface["id"]] = float(found.group(1))
        elif surface["kind"] == "floor" and ground:
            tops[surface["id"]] = float(ground.group(1))
    return tops


def _surface_heights(beats, tops, leg):
    """SURFACE_HEIGHT (owner O21): at a foot support's onset on a surface with a known top, the root stands on it,
    no higher than the body's standing leg (owner O85)."""
    findings = []
    anchors = sorted((b["t"], entity, pos) for b in beats for entity, pos in b["pos"].items() if pos is not None)
    for beat in beats:
        for contact in beat["contacts"]:
            surface, entity = contact["b"]["id"], contact["a"]["id"]
            if contact["contact_type"] != "support" or contact["b"]["kind"] != "surface" or surface not in tops \
                    or not contact["a"]["part"].endswith("_foot"):
                continue
            t = _at(beat, contact)  # judged on the pose at the onset; a landing between keys has none (S-027)
            root = next((pos for at, who, pos in reversed(anchors) if who == entity and abs(at - t) <= EPSILON), None)
            if root is not None and not tops[surface] - SURFACE_SLACK_M <= root[1] <= tops[surface] + leg + SURFACE_SLACK_M:
                findings.append(_finding("SURFACE_HEIGHT", f"{entity} stands on {surface} (top y={tops[surface]:g}) at "
                                         f"{t} with the root at y={root[1]:g}", beat["id"], contact))
    return findings


def _thrown(beats):
    """CONTACT_VERB: a throw leaves its prop moving, so the prop has a sample with velocity at the throw (the post one
    of a pair)."""
    findings = []
    samples = [s for b in beats for s in b.get("prop_samples", [])]
    for beat in beats:
        for contact in beat["contacts"]:
            if contact.get("verb") != "throw" or contact["b"]["kind"] != "prop":
                continue
            t = _at(beat, contact)
            at = [s for s in samples if s["prop"] == contact["b"]["id"] and abs(s["t"] - t) <= EPSILON
                  and s.get("phase") != "pre"]
            if not any(s["v"] is not None and any(abs(x) > EPSILON for x in s["v"]) for s in at):
                findings.append(_finding("CONTACT_VERB", f"A throw leaves {contact['b']['id']} moving: give it a sample "
                                         f"with velocity at {t}", beat["id"], contact))
    return findings


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


def vanish_windows(beats):
    """[(actor, substitution beat, start, reappearance t or None)]: a substitution's actor is gone from the
    substitution's start until its next beat as actor (owner O12, O18; audit X9)."""
    ordered = sorted(beats, key=lambda b: (b["t"], b["id"]))
    out = []
    for index, beat in enumerate(ordered):
        if beat["event_type"] == "substitution":
            back = next((b for b in ordered[index + 1:] if b["actor"] == beat["actor"]), None)
            out.append((beat["actor"], beat["id"], beat["t"], back["t"] if back else None))
    return out


def _vanished(beats):
    """VANISHED_BODY: no other beat lists, anchors or touches with a substituted body before it reappears, and none of
    its supports or holds stays open inside that window (owner O90, F-081): it lets go when it vanishes."""
    findings = []
    for actor, sub, start, back in vanish_windows(beats):
        for beat in beats:
            inside = beat["id"] != sub and start - EPSILON <= beat["t"] and (back is None or beat["t"] < back - EPSILON)
            if inside and beat["actor"] != actor and (actor in beat["pos"] or any(
                    p["id"] == actor for p in beat["participants"]) or any(c["a"]["id"] == actor for c in beat["contacts"])):
                findings.append(_finding("VANISHED_BODY", "A substituted body appears before it reappears", beat["id"], actor))
        for part, target, opened, closed in _open_contacts(beats, actor):
            if opened < (math.inf if back is None else back) - EPSILON and (closed is None or closed > start + EPSILON):
                findings.append(_finding("VANISHED_BODY", f"{actor}'s {part} stays on {target} while it is gone (owner O90)",
                                         sub, [opened, closed]))
    return findings


def _open_contacts(beats, actor):
    """[(part, target, opened, closed or None)]: the actor's supports and holds, each from its contact to its release."""
    out, open_ = [], {}
    events = sorted(((_at(b, c), c) for b in beats for c in b["contacts"] if c["a"]["id"] == actor),
                    key=lambda e: (e[0], e[1]["contact_type"] != "release"))
    for t, c in events:
        pair = (c["a"].get("part"), c["b"]["id"], c["b"].get("part"))
        if c["contact_type"] in ("support", "possess"):
            open_.setdefault(pair, t)  # a second opening of an open pair is S07's CONTACT_DUPLICATE
        elif c["contact_type"] == "release" and pair in open_:
            out.append((pair[0], pair[1], open_.pop(pair), t))
    return out + [(pair[0], pair[1], t, None) for pair, t in open_.items()]


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

    def holder_of(prop, sample):
        return holder_at(prop, sample["t"] - (BEFORE if sample.get("phase") == "pre" else 0))

    def anchor(entity, t):
        return next((pos for at, e, pos in reversed(anchors) if e == entity and at <= t + EPSILON), None)

    for prop, rows in samples.items():
        rows.sort(key=lambda r: (r[0]["t"], PHASE_ORDER[r[0].get("phase")]))
        findings += _contact_pairs(prop, rows, touches.get(prop, []), lambda t, p=prop: holder_at(p, t))
        for sample, beat_id in rows:
            holder = holder_of(prop, sample)
            if holder and anchor(holder, sample["t"]) and math.dist(sample["p"], anchor(holder, sample["t"])) > REACH_M:
                findings.append(_finding("PROP_KINEMATICS", f"{prop} is held by {holder} but {REACH_M:g} m away", beat_id,
                                         sample["t"]))
        for (first, _), (second, beat_id) in zip(rows, rows[1:], strict=False):
            span = second["t"] - first["t"]
            if span <= EPSILON or holder_of(prop, first) or first["float"]:
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
                velocity = [first["v"][0], first["v"][1] - GRAVITY * span, first["v"][2]]
                if second.get("phase") == "pre" and second["v"] is not None and \
                        math.dist(velocity, second["v"]) > VELOCITY_TOLERANCE_MPS:
                    findings.append(_finding("PROP_KINEMATICS", f"{prop} from {first['t']} would arrive at {second['t']} "
                                             f"with v {[round(x, 2) for x in velocity]}, not {second['v']}",
                                             beat_id, [first["t"], second["t"]]))
            elif math.dist(first["p"], second["p"]) > KINEMATIC_TOLERANCE_M:
                # F-077 (RV-03): a contact at the second sample takes or strikes the prop where it rests, so the prop
                # is still there at that instant; only a contact between the two samples moves it.
                findings.append(_finding("PROP_KINEMATICS", f"{prop} at rest moves between {first['t']} and {second['t']} "
                                         "with no contact before it", beat_id, [first["t"], second["t"]]))
    return findings


def _moving(sample):
    return sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"])


def _contact_pairs(prop, rows, touch_times, holder_at):
    """F2.2: same-time samples are one pre and one post on a contact at one position; a free prop moving into a
    contact has the pair there."""
    findings, at = [], {}
    for sample, beat_id in rows:
        at.setdefault(round(sample["t"], 6), []).append((sample, beat_id))
    for t, group in at.items():
        phases = sorted(sample.get("phase") or "none" for sample, _ in group)
        if len(group) == 1 and phases == ["none"]:
            continue
        beat_id = group[-1][1]
        if phases != ["post", "pre"]:
            findings.append(_finding("PROP_KINEMATICS", f"{prop} at {t} has samples {phases}: a time takes one sample, or "
                                     "one pre and one post on a contact", beat_id, t))
        elif not any(abs(x - t) <= EPSILON for x in touch_times):
            findings.append(_finding("PROP_KINEMATICS", f"{prop} has a pre and a post sample at {t} but no contact on it "
                                     "then", beat_id, t))
        elif math.dist(group[0][0]["p"], group[1][0]["p"]) > KINEMATIC_TOLERANCE_M:
            findings.append(_finding("PROP_KINEMATICS", f"{prop} moves between its pre and post samples at {t}; the "
                                     "contact is instantaneous", beat_id, t))
    for t in sorted(set(touch_times)):
        before = [sample for sample, _ in rows if sample["t"] < t - EPSILON]
        if holder_at(t - BEFORE) or not before or not _moving(before[-1]):
            continue
        phases = sorted(sample.get("phase") or "none" for sample, _ in at.get(round(t, 6), []))
        if phases != ["post", "pre"]:
            findings.append(_finding("PROP_KINEMATICS", f"{prop} is moving free into a contact at {t}: give it a pre and a "
                                     "post sample there (F2.2)", None, t))
    return findings
