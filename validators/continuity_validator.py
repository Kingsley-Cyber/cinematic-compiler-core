"""S06 continuity: no subject disappears or is cloned, every change has a triggering beat, possession agrees, and every
prop's state is known from the first beat (PROP_FIRST_STATE, M8.12: owner render R4 put B's kunai in A's hand at 0.0,
R1-R5 drew the substitution log before it was used; both prompts said 'state unknown' at 0.00)."""

from solver.prop_state_machine import UNKNOWN


def _finding(code, message, detail=None):
    return {"code": code, "message": message, "detail": detail}


def check(snapshots, transitions, subjects, beat_ids):
    findings = []
    per_point = {}
    for node in snapshots:
        per_point.setdefault(node["beat"], []).append((node["subject"]["kind"], node["subject"]["id"]))
    for point in [*beat_ids, "end"]:
        present = per_point.get(point, [])
        if sorted(present) != sorted(subjects):
            findings.append(_finding("CONTINUITY_PRESENCE", "Every subject appears exactly once at every beat", point))
    for edge in transitions:
        if not edge["trigger_event"]:
            findings.append(_finding("CONTINUITY_TRIGGER", "A state change has no triggering beat", edge["id"]))
    by_point = {}
    for node in snapshots:
        by_point.setdefault(node["beat"], {})[(node["subject"]["kind"], node["subject"]["id"])] = node["conditions"]
    for point, table in by_point.items():
        for (kind, sid), conditions in table.items():
            if kind == "entity" and conditions.get("possession", UNKNOWN) not in (UNKNOWN, "none"):
                holder = table.get(("prop", conditions["possession"]), {}).get("holder", UNKNOWN)
                if holder not in (UNKNOWN, sid):
                    findings.append(_finding("POSSESSION_MISMATCH", "Actor possession and prop holder disagree", [point, sid]))
            if kind == "prop" and conditions.get("holder", UNKNOWN) not in (UNKNOWN, "none"):
                held = table.get(("entity", conditions["holder"]), {}).get("possession", UNKNOWN)
                if held not in (UNKNOWN, sid):
                    findings.append(_finding("POSSESSION_MISMATCH", "Prop holder and actor possession disagree", [point, sid]))
    return findings


def first_states(snapshots, beat_ids):
    """PROP_FIRST_STATE: at the first beat each prop's holder and card states are known (its location may be unknown
    while it is held or hidden). They come from first requirements, a chained clip's end states and contacts at start."""
    first = beat_ids[0] if beat_ids else None
    findings = []
    for node in snapshots:
        if node["beat"] == first and node["subject"]["kind"] == "prop":
            gaps = sorted(k for k, v in node["conditions"].items() if v == UNKNOWN and k != "location")
            if gaps:
                findings.append(_finding("PROP_FIRST_STATE", f"{node['subject']['id']}: {', '.join(gaps)} unknown at the "
                                         "first beat", [first, node["subject"]["id"]]))
    return findings
