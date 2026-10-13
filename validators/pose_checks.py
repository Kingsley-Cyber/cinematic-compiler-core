"""The pose-mechanics checks (PLAN-009): measured and printed first, refusing later per genre (owner, 2026-10-13),
except WEIGHT_DISTRIBUTION, which refuses from the start. Each returns [{code, key, message}]; a check that does not
refuse yet is a report (`python -m validators.pose_checks [envelope.json]`), not a gate.

LINE_OF_ACTION (PM-3, S-126): a body that strikes reads along one bent line; the key at a strike's instant whose line
of action is straight (under solver/pose_mechanics.py STRAIGHT) is named. A strike: a touch from a body part to
another body (S07's contacts).

COUNTERBALANCE (S-127): a pose whose leading limb reaches out from the centre of mass with no limb on the other side
to oppose it is named: animation's opposition, not a fall (the trunk already balances it; WEIGHT_DISTRIBUTION is the
physics).
"""

import json
import sys
from pathlib import Path


def _items(envelope, kind, group):
    return envelope.get(kind, {}).get(group, {}).get("items", [])


def line_of_action(envelope):
    keys = {(k["entity"], round(k["t"], 6)): k["id"] for k in _items(envelope, "nodes", "motion")}
    lines = {m["id"]: m["line_of_action"] for m in _items(envelope, "nodes", "pose_mechanics")}
    out = []
    for c in _items(envelope, "nodes", "contacts"):
        if c["contact_type"] != "touch" or c["b"]["kind"] != "entity":
            continue
        key = keys.get((c["a"]["id"], round(c["t"], 6)))
        line = lines.get(key)
        if line is not None and line["shape"] == "straight":
            out.append({"code": "LINE_OF_ACTION", "key": key,
                        "message": f"{key} strikes at {c['t']:g} along a straight line (tension {line['tension']:g})"})
    return out


def counterbalance(envelope):
    """COUNTERBALANCE (S-127): a key whose leading limb reaches out with no limb on the other side to counter it."""
    out = []
    for m in _items(envelope, "nodes", "pose_mechanics"):
        cb = m["counterbalance"]
        if cb["lead"] is not None and not cb["counter"]:
            out.append({"code": "COUNTERBALANCE", "key": m["id"],
                        "message": f"{m['id']}: {cb['lead']} reaches {cb['reach_m']:g} m and nothing counters it"})
    return out


CHECKS = {"LINE_OF_ACTION": line_of_action, "COUNTERBALANCE": counterbalance}


def report(envelope):
    return [note for check in CHECKS.values() for note in check(envelope)]


if __name__ == "__main__":
    from validators.graph_map import load_examples

    envelopes = ({Path(p).parent.name: json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]}
                 or load_examples())
    for name, envelope in envelopes.items():
        notes = report(envelope)
        print(f"{name}: {len(notes)} note(s)")
        for note in notes:
            print(f"  {note['code']}: {note['message']}")
