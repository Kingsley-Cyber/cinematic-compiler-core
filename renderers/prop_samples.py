"""Prop position and velocity rows (owner O8) shared by the LBN-2.4 and the structured-prose renderers.

Each S04 prop sample becomes one row: time, p[x,y,z], v[x,y,z] when moving, and words a model reads: held by <label>,
at rest, or moving up/down toward the performer its path reaches, else along the dominant scene axis. A path reaches a
performer when the prop's free flight from the sample (ballistic, or straight when it floats) to its next sample or
the ground passes within REACH_M of one of that performer's body points (the key nearest in time) and comes nearer than
it starts (F-122: "toward B" printed where the kunai lands short of B, beside "NOT toward B"). A pre-contact sample
describes its arrival and names no goal. Interpretation (Claude's, for owner review): REACH_M 0.3 m, APPROACH_M 0.1 m.
Floats are marked. A contact pair (plan F2.2) prints as two rows at one time, "pre-contact" before "post-contact"; a
pre sample's holder is read just before its contact.

`track` says where a prop is from 0 to the scene's end (plan F2.1, F6.1 as amended by W4, F6.2): the spans between its
holds and samples, each held by a hand, carried by its owner (O63), ballistic under gravity (or a declared float) from
the last sample's p and v, or at rest at a place. Interpretation (Claude's, for owner review): a resting span names the
S06 location in force at its start or first set inside it, since S06 commits a location at the end of the beat that
changes it; a location set before the prop's last hold does not count after it (S06 keeps a held prop's last surface:
the UGC glasses stay 'tabletop' on the face).
"""

import math

from planner.dynamic_beat_validator import BEFORE, GRAVITY, PHASE_ORDER, holds

EPSILON = 1e-9
REACH_M, APPROACH_M, STEP_S, FLIGHT_S = 0.3, 0.1, 0.02, 2.0  # interpretation (Claude's, for owner review)


def _fmt(values, compact):
    text = [str(int(v)) if float(v).is_integer() else str(v) for v in values]
    return "[" + ("," if compact else ", ").join(text) + "]"


def bodies(envelope):
    """{entity: [(t, body points)]} from S13's keys (forward kinematics, F5.1)."""
    out = {}
    for key in envelope["nodes"].get("motion", {}).get("items", []):
        if key.get("points"):
            out.setdefault(key["entity"], []).append((key["t"], key["points"]))
    return out


def reaches(sample, until, body_keys):
    """The performer the prop's free flight reaches before `until` (its next sample) or the ground, or None."""
    p, v, best = sample["p"], sample["v"], None
    span = min((until if until is not None else sample["t"] + FLIGHT_S) - sample["t"], FLIGHT_S)
    if span <= EPSILON:
        return None
    steps = max(1, round(span / STEP_S))
    for entity, keys in sorted(body_keys.items()):
        start = nearest = None
        for i in range(steps + 1):
            tau = span * i / steps
            drop = 0.0 if sample["float"] else 0.5 * GRAVITY * tau * tau
            point = (p[0] + v[0] * tau, p[1] + v[1] * tau - drop, p[2] + v[2] * tau)
            if point[1] < -EPSILON:
                break  # on the ground
            points = min(keys, key=lambda k: abs(k[0] - (sample["t"] + tau)))[1]
            d = min(math.dist(point, q) for q in points.values())
            start = d if start is None else start
            nearest = d if nearest is None else min(nearest, d)
        if nearest is not None and nearest <= REACH_M and nearest < start - APPROACH_M and (best is None or nearest < best[0]):
            best = (nearest, entity)
    return best[1] if best else None


def motion_words(sample, holder, labels, goal=None):
    if holder:
        return f"held by {labels.get(holder, holder)}"
    v = sample["v"]
    if v is None or all(abs(x) < EPSILON for x in v):
        return "at rest"
    parts = ["up"] if v[1] > 0.3 else ["down"] if v[1] < -0.3 else []
    flat = math.hypot(v[0], v[2])
    if goal and flat > 0.1:
        parts.append(f"toward {labels.get(goal, goal)}")
    elif flat > 0.1:
        axis = 0 if abs(v[0]) >= abs(v[2]) else 2
        parts.append(f"along {'+' if v[axis] > 0 else '-'}{'XZ'[axis // 2]}")
    words = "moving " + " ".join(parts) if parts else "moving"
    return words + (" (stylised float, no gravity)" if sample["float"] else "")


def _hand(part):
    side, _, name = part.partition("_")
    return f"{side[0].upper()} {name}" if side in ("left", "right") and name else part.replace("_", " ")


def _moving(sample):
    return sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"])


def _place(places, start, stop, labels, since):
    """'on the ground' from the S06 location set at or before the span's start or first inside it, and not before
    `since` (the end of the prop's last hold); '' when unknown."""
    usable = [(t, where) for t, where in places if t >= since - EPSILON]
    before = [where for t, where in usable if t <= start + EPSILON]
    inside = [where for t, where in usable if start + EPSILON < t < stop - EPSILON]
    known = [where for where in before[-1:] + inside if where and where != "unknown"]
    if not known:
        return ""
    return f"on {labels[known[0]]}" if known[0] in labels else f"on the {known[0].replace('_', ' ')}"


def track(envelope, labels, prop_id):
    """[(start, end, kind, text)] tiling 0 to the scene's end; kind is held, carried, flight, rest or unplaced."""
    beats, end_t = envelope["nodes"]["beats"]["items"], envelope["scene"]["duration_s"]
    prop = next(p for p in envelope["nodes"]["props"]["items"] if p["id"] == prop_id)
    held = [(start, min(end, end_t), holder) for start, end, holder in holds(beats).get(prop_id, [])]
    grips = {round(c["t"], 6): c["body_part"] for c in envelope["nodes"]["contacts"]["items"]
             if c["contact_type"] == "possess" and c["b"] == {"kind": "prop", "id": prop_id, "part": c["b"].get("part")}}
    samples = sorted((s for b in beats for s in b.get("prop_samples", []) if s["prop"] == prop_id),
                     key=lambda s: (s["t"], PHASE_ORDER[s.get("phase")]))
    snapshots = sorted((s["t"], s["conditions"].get("location")) for s in envelope["nodes"]["states"]["items"]
                       if s["subject"] == {"kind": "prop", "id": prop_id})
    places = [(t, where) for i, (t, where) in enumerate(snapshots) if i == 0 or snapshots[i - 1][1] != where]
    cuts = sorted({0.0, end_t, *(t for start, end, _ in held for t in (start, end)), *(s["t"] for s in samples)})
    spans = []
    for start, stop in zip(cuts, cuts[1:], strict=False):
        if stop - start <= EPSILON or start < -EPSILON or stop > end_t + EPSILON:
            continue
        hold = next(((first, holder) for first, end, holder in held if first - EPSILON <= start < end - EPSILON), None)
        last = [s for s in samples if s["t"] <= start + EPSILON]
        since = max((end for _, end, _ in held if end <= start + EPSILON), default=-math.inf)
        if hold:
            part = grips.get(round(hold[0], 6))
            kind, text = "held", f"held by {labels.get(hold[1], hold[1])}" + (f" {_hand(part)}" if part else "")
        elif last and _moving(last[-1]):
            sample = last[-1]
            physics = "stylised float, no gravity," if sample["float"] else "ballistic under gravity"
            kind, text = "flight", f"{physics} from p{_fmt(sample['p'], False)} v{_fmt(sample['v'], False)}"
        elif last:
            place = _place(places, start, stop, labels, since)
            kind, text = "rest", f"at rest {place + ' ' if place else ''}at {_fmt(last[-1]['p'], False)}"
        elif prop.get("carried_by"):
            kind, text = "carried", f"carried by {labels.get(prop['carried_by'], prop['carried_by'])}"
        else:
            place = _place(places, start, stop, labels, since)
            kind, text = ("rest", f"at rest {place}") if place else ("unplaced", "place not given")
        if spans and spans[-1][2:] == (kind, text):
            spans[-1] = (spans[-1][0], stop, kind, text)
        else:
            spans.append((start, stop, kind, text))
    return spans


def where_line(spans):
    return "WHERE: " + " · ".join(f"{start:.2f}-{stop:.2f} {text}" for start, stop, _, text in spans)


def rows(envelope, labels, prop, compact):
    """[(t, text)] for one prop's samples, in time order."""
    beats = envelope["nodes"]["beats"]["items"]
    held, body_keys, out = holds(beats), bodies(envelope), []
    samples = sorted((s for b in beats for s in b.get("prop_samples", []) if s["prop"] == prop),
                     key=lambda s: (s["t"], PHASE_ORDER[s.get("phase")]))
    for index, sample in enumerate(samples):
        when = sample["t"] - (BEFORE if sample.get("phase") == "pre" else 0)
        holder = next((h for start, end, h in held.get(prop, []) if start - EPSILON <= when < end - EPSILON), None)
        moving = sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"]) and not holder
        t = (str(int(sample["t"])) if float(sample["t"]).is_integer() else str(sample["t"])) if compact else f"{sample['t']:.2f}"
        phase = f" {sample['phase']}-contact" if sample.get("phase") else ""
        text = f"{t}{phase} p{_fmt(sample['p'], compact)}" + (f" v{_fmt(sample['v'], compact)}" if moving else "")
        after = next((s["t"] for s in samples[index + 1:] if s["t"] > sample["t"] + EPSILON), None)
        goal = None if sample.get("phase") == "pre" or not moving else reaches(sample, after, body_keys)
        out.append((sample["t"], f"{text} {motion_words(sample, holder, labels, goal)}"))
    return out
