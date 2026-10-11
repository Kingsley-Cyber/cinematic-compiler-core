"""Prop position and velocity rows (owner O8) shared by the LBN-2.4 and the structured-prose renderers.

Each S04 prop sample becomes one row: time, p[x,y,z], v[x,y,z] when moving, and words a model reads: held by <label>,
at rest, or moving up/down toward the performer it heads for (the entity whose direction from the prop best matches
the horizontal velocity, within about 45 degrees, at least 0.5 m away), else along the dominant scene axis.
Floats are marked.
"""

import math

from planner.dynamic_beat_validator import holds

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


def rows(envelope, labels, prop, compact):
    """[(t, text)] for one prop's samples, in time order."""
    beats = envelope["nodes"]["beats"]["items"]
    held, anchors, out = holds(beats), _anchors(beats), []
    for sample in sorted((s for b in beats for s in b.get("prop_samples", []) if s["prop"] == prop), key=lambda s: s["t"]):
        holder = next((h for start, end, h in held.get(prop, []) if start - EPSILON <= sample["t"] < end - EPSILON), None)
        moving = sample["v"] is not None and any(abs(x) > EPSILON for x in sample["v"]) and not holder
        t = (str(int(sample["t"])) if float(sample["t"]).is_integer() else str(sample["t"])) if compact else f"{sample['t']:.2f}"
        text = f"{t} p{_fmt(sample['p'], compact)}" + (f" v{_fmt(sample['v'], compact)}" if moving else "")
        out.append((sample["t"], f"{text} {motion_words(sample, holder, anchors, labels)}"))
    return out
