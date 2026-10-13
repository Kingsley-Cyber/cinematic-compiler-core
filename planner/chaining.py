"""M5.5 clip chaining: S02 reads the previous clip's envelope once and keeps what continuity needs.

`summary(previous)` is written to scene.chained_from; every later step reads only that:
- end_states: each subject's conditions at the previous end (S06 starts from them);
- active_contacts: possess/support contacts still open at the previous end (S07 starts with them);
- open_beats: the previous clip's unresolved causes, non-hold beats that cause nothing (S05 records them);
- last_shot: the previous clip's last camera shot, side and axis (S17 checks its first cut against it).
The previous envelope must be built with the current kernel and carry states and contacts.
"""

from kernel.canonical import ContractError, content_hash
from kernel.kernel_files import kernel_hash


def summary(previous):
    nodes, edges = previous.get("nodes", {}), previous.get("edges", {})
    if previous.get("provenance", {}).get("kernel_hash") != kernel_hash():
        raise ContractError("CHAIN_STALE", "The previous clip was built with another kernel; recompile it first")
    if "states" not in nodes or "contacts" not in nodes:
        raise ContractError("CHAIN_INCOMPLETE", "The previous clip must be compiled through S07 (states and contacts)")
    from compiler.passes.mandatory.p07_contact import events_for, lifecycle

    beats = sorted(nodes["beats"]["items"], key=lambda b: (b["t"], b["id"]))
    _, _, intervals = lifecycle(events_for(previous))
    causing = {e["from"] for e in edges.get("causal", {}).get("items", [])}
    shots = nodes.get("camera", {}).get("items", [])
    last = shots[-1] if shots else None
    return {
        "envelope_sha256": "sha256:" + content_hash(previous),
        "source_prompt": previous["provenance"]["source_prompt"],
        "world": previous["scene"]["world"], "duration_s": previous["scene"]["duration_s"],
        "end_states": [{"subject": s["subject"], "conditions": s["conditions"], "pos": s["pos"], "facing": s["facing"]}
                       for s in nodes["states"]["items"] if s["beat"] == "end"],
        "active_contacts": [{"a": pair[0], "body_part": pair[1], "b": {"kind": pair[2], "id": pair[3], "part": pair[4]},
                             "contact_type": kind, "since": start}
                            for pair, kind, start, end in intervals if end is None],
        "open_beats": [{"id": b["id"], "label": b["label"], "action": b["action"]} for b in beats
                       if b["event_type"] != "hold" and b["id"] not in causing],
        "last_shot": None if last is None else {
            "id": last["id"], "side": last["derived"]["side"], "azimuth_deg": last["angle"]["azimuth_deg"],
            "scale": last["framing"]["scale"], "target": last["position"]["target"]},
    }
