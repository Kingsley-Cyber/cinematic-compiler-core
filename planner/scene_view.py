"""Per-entity, per-beat slots that the body steps (S11–S13) are authored and checked against.

A slot exists for every entity that is a beat's actor or an entity participant. It carries the beat timing, the
S06 state at the beat start, the S04 pose anchor, and the S07 support contacts active at the beat start.
"""

from compiler.passes.mandatory.p07_contact import events_of, lifecycle

EPSILON = 1e-9


def active_supports(envelope, entity, time):
    _, _, intervals = lifecycle(events_of(envelope["nodes"]["beats"]["items"]))
    return sorted(pair[1] for pair, kind, start, end in intervals
                  if kind == "support" and pair[0] == entity and start <= time + EPSILON
                  and (end is None or time < end - EPSILON))


def slots(envelope):
    states = {s["id"]: s for s in envelope["nodes"]["states"]["items"]}
    result = []
    for beat in sorted(envelope["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"])):
        entities = [beat["actor"]] + [p["id"] for p in beat["participants"] if p["kind"] == "entity" and p["id"] != beat["actor"]]
        for entity in entities:
            state = states[f"{entity}@{beat['id']}"]
            result.append({"slot": f"{entity}@{beat['id']}", "entity": entity, "beat": beat["id"], "t": beat["t"],
                           "dur": beat["dur"], "role": "actor" if entity == beat["actor"] else "participant",
                           "label": beat["label"], "action": beat["action"], "event_type": beat["event_type"],
                           "pos": beat["pos"].get(entity), "facing": beat["facing"].get(entity),
                           "state": state["conditions"], "active_supports": active_supports(envelope, entity, beat["t"])})
    return result
