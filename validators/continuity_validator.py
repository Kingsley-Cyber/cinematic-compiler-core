"""S06 continuity: no subject disappears or is cloned, every change has a triggering beat, possession agrees."""

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
