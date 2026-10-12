"""S06 replay: states of every entity, prop and surface at each beat start and at the scene end.

requires are read at t, before the beat's own effects; effects commit at t + dur (a beat starting when another ends
sees its effects), except a change of hands (F-061, RV-08): a prop's holder change commits at the instant of its
beat's possess (to the new holder) or release (to none) of that prop, and an entity's possession change at its own
possess or release, so a throw that lets go at its pose (`at: start`, O23) frees the prop at that instant.
A property's starting value is the value its first requirement asserts when that comes before any effect;
otherwise it is "unknown". A chained clip (M5.5) starts from the previous clip's end values instead, and a first
requirement must then agree with them. Conflicting effects committing at the same time are refused.
"""

UNKNOWN = "unknown"
EPSILON = 1e-9


def _finding(code, message, beat=None, detail=None):
    return {"code": code, "message": message, "beat": beat, "detail": detail}


def _key(fact):
    return fact["subject"]["kind"], fact["subject"]["id"], fact["property"]


def _contact_time(beat, contact):
    return beat["t"] + (0 if contact.get("at") == "start" else beat["dur"])


def commit_time(beat, fact):
    """When an effect commits: at the possess or release that hands its prop over (F-061), else at the beat's end."""
    kind, sid, prop = _key(fact)
    for contact in beat.get("contacts", []):
        if contact["contact_type"] not in ("possess", "release") or contact["b"]["kind"] != "prop":
            continue
        to = contact["a"]["id"] if contact["contact_type"] == "possess" else "none"
        if (kind, prop) == ("prop", "holder") and contact["b"]["id"] == sid and fact["value"] == to:
            return _contact_time(beat, contact)
        gives = contact["b"]["id"] if contact["contact_type"] == "possess" else "none"
        if (kind, prop) == ("entity", "possession") and contact["a"]["id"] == sid and fact["value"] == gives:
            return _contact_time(beat, contact)
    return beat["t"] + beat["dur"]


def replay(beats, subjects, tables, end_time, carried=None):
    """subjects: [(kind, id)]; tables: {(kind, id): [property, ...]}. Returns (snapshots, transitions, findings)."""
    findings = []
    ordered = sorted(beats, key=lambda b: (b["t"], b["id"]))
    commits = sorted(((commit_time(b, f), b["id"], _key(f), f["value"]) for b in ordered for f in b["effects"]),
                     key=lambda c: (c[0], c[1]))
    by_time = {}
    for time, beat_id, key, value in commits:
        previous = by_time.get((round(time, 9), key))
        if previous and previous[1] != value:
            findings.append(_finding("STATE_CONFLICT", "Two effects set one property at the same time", beat_id,
                                     [key, previous, value]))
        by_time[(round(time, 9), key)] = (beat_id, value)
    initial = dict(carried or {})
    for beat in ordered:
        for fact in beat["requires"]:
            key = _key(fact)
            if key in initial:
                continue
            earlier_commit = any(c[2] == key and c[0] <= beat["t"] + EPSILON and c[1] != beat["id"] for c in commits)
            initial[key] = UNKNOWN if earlier_commit else fact["value"]

    def value_at(key, time, inclusive=True, before=None):
        value = initial.get(key, UNKNOWN)
        for at, beat_id, commit_key, commit_value in commits:
            if commit_key == key and beat_id != before and (at <= time + EPSILON if inclusive else at < time - EPSILON):
                value = commit_value
        return value

    for beat in ordered:
        for fact in beat["requires"]:
            actual = value_at(_key(fact), beat["t"], before=beat["id"])  # before the beat's own effects
            if actual != fact["value"]:
                findings.append(_finding("REPLAY_REQUIRES", "A requirement does not hold at the beat start", beat["id"],
                                         [list(_key(fact)), fact["value"], actual]))
    anchors = {}
    points = [(b["t"], b["id"], b) for b in ordered] + [(end_time, "end", None)]
    snapshots, transitions, last = [], [], {}
    for time, beat_id, beat in points:
        for kind, sid in subjects:
            pos = facing = source = None
            if kind == "entity":
                if beat is not None and sid in beat["pos"]:
                    anchors[sid] = (beat["pos"][sid], beat["facing"][sid])
                    source = "beat"
                elif sid in anchors:
                    source = "carried"
                if sid in anchors:
                    pos, facing = (list(v) for v in anchors[sid])
            conditions = {prop: value_at((kind, sid, prop), time) for prop in tables[(kind, sid)]}
            node = {"id": f"{sid}@{beat_id}", "subject": {"kind": kind, "id": sid}, "beat": beat_id, "t": time,
                    "pos": pos, "facing": facing, "pos_source": source, "conditions": conditions}
            snapshots.append(node)
            prior = last.get((kind, sid))
            if prior is not None:
                changes = [{"property": p, "from": prior["conditions"][p], "to": conditions[p]}
                           for p in tables[(kind, sid)] if prior["conditions"][p] != conditions[p]]
                if changes:
                    landed = [c for c in commits if prior["t"] + EPSILON < c[0] <= time + EPSILON and c[2][:2] == (kind, sid)]
                    transitions.append({"id": f"{prior['id']}__{node['id']}", "from_state": prior["id"],
                                        "to_state": node["id"], "trigger_event": sorted({c[1] for c in landed}),
                                        "t": round(max((c[0] for c in landed), default=time), 6), "changes": changes})
            last[(kind, sid)] = node
    return snapshots, transitions, findings
