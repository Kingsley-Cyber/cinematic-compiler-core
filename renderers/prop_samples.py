"""Prop position and velocity rows (owner O8) shared by the LBN-2.4 and the structured-prose renderers.

Each S04 prop sample becomes one row: time, p[x,y,z], v[x,y,z] when moving, and words a model reads: held by <label>,
at rest, or moving up/down toward the performer it heads for (the entity whose direction from the prop best matches
the horizontal velocity, within about 45 degrees, at least 0.5 m away), else along the dominant scene axis.
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

from planner.dynamic_beat_validator import BEFORE, PHASE_ORDER, holds

EPSILON = 1e-9


def _fmt(values, compact):
    text = [str(int(v)) if float(v).is_integer() else str(v) for v in values]
    return "[" + ("," if compact else ", ").join(text) + "]"


def _anchors(beats):
    return sorted((b["t"], entity, pos) for b in beats for entity, pos in b["pos"].items() if pos is not None)


def motion_words(sample, holder, anchors, labels):
    if holder:
        return f"held by {labels.get(holder, holder)}"
    v = sample["v"]
    if v is None or all(abs(x) < EPSILON for x in v):
        return "at rest"
    parts = ["up"] if v[1] > 0.3 else ["down"] if v[1] < -0.3 else []
    flat = math.hypot(v[0], v[2])
    best = None
    latest = {}
    for at, entity, pos in anchors:
        if at <= sample["t"] + EPSILON:
            latest[entity] = pos
    for entity, pos in sorted(latest.items()):
        dx, dz = pos[0] - sample["p"][0], pos[2] - sample["p"][2]
        distance = math.hypot(dx, dz)
        if flat > 0.1 and distance > 0.5:
            cos = (dx * v[0] + dz * v[2]) / (distance * flat)
            if cos >= 0.7 and (best is None or cos > best[0]):
                best = (cos, entity)
    if best:
        parts.append(f"toward {labels.get(best[1], best[1])}")
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
    held, anchors, out = holds(beats), _anchors(beats), []
    for sample in sorted((s for b in beats for s in b.get("prop_samples", []) if s["prop"] == prop),
                         key=lambda s: (s["t"], PHASE_ORDER[s.get("phase")])):
        when = sample["t"] - (BEFORE if sample.get("phase") == "pre" else 0)
        holder = next((h for start, end, h in held.get(prop, []) if start - EPSILON <= when < end - EPSILON), None)
        moving = sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"]) and not holder
        t = (str(int(sample["t"])) if float(sample["t"]).is_integer() else str(sample["t"])) if compact else f"{sample['t']:.2f}"
        phase = f" {sample['phase']}-contact" if sample.get("phase") else ""
        text = f"{t}{phase} p{_fmt(sample['p'], compact)}" + (f" v{_fmt(sample['v'], compact)}" if moving else "")
        out.append((sample["t"], f"{text} {motion_words(sample, holder, anchors, labels)}"))
    return out
