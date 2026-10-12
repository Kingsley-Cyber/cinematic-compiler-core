"""Hits (owner O92, R-21, F-155, RV-57): the contacts that are hits, found from the contacts themselves, so each owes a
camera hold on every body present whatever S17 holds (HIT_HOLD at S16, S17 and in the prompt). A hit is
- a touch on another performer's body (A's knee on B at 4.7);
- a strike, deflect or parry on a prop another performer holds, or threw and no one holds (A's foot on the kunai B
  threw, 2.5);
- a catch of another performer's body (B catches A's arm at 6.6, O93);
- a body touched by a prop another performer holds that affords stab (the kunai A drives into B at 8.5, O93).
Interpretation (Claude's, for owner review): the four kinds, read from F-155's list; a touch on a body counts whatever its
verb, a touch on a prop only with a striking verb or a stabbing blade.
"""

from compiler.passes.mandatory.p07_contact import events_for, lifecycle
from planner.dynamic_beat_validator import vanish_windows

EPSILON = 1e-9
STRIKING = ("strike", "deflect", "parry")


def hits(envelope):
    """[{t, contact, kind, bodies}] in time order; bodies are the performers present then (a vanished one is not, O18)."""
    nodes = envelope["nodes"]
    stab = {p["id"] for p in nodes["props"]["items"] if "stab" in p.get("affordances", [])}
    contacts = sorted((c for c in nodes["contacts"]["items"] if c["beat"] != "chain"), key=lambda c: (c["t"], c["id"]))
    _, _, intervals = lifecycle(events_for(envelope))
    gone = vanish_windows(nodes["beats"]["items"])
    entities = sorted(e["id"] for e in nodes["entities"]["items"])

    def holder(prop, t):  # the performer holding the prop as the contact lands
        return next((pair[0] for pair, kind, t0, t1 in intervals if kind == "possess" and pair[2:4] == ("prop", prop)
                     and t0 < t - EPSILON and (t1 is None or t1 > t - EPSILON)), None)

    def thrower(prop, t):  # who last threw it
        thrown = [c for c in contacts if c["b"]["id"] == prop and c["t"] < t - EPSILON and c.get("verb") == "throw"]
        return thrown[-1]["a"]["id"] if thrown else None

    out = []
    for c in contacts:
        who, target, verb = c["a"]["id"], c["b"], c.get("verb")
        held = holder(target["id"], c["t"]) if target["kind"] == "prop" else None
        kind = None
        if c["contact_type"] == "touch" and target["kind"] == "entity" and target["id"] != who:
            kind = "a touch on another performer's body"
        elif c["contact_type"] == "touch" and target["kind"] == "prop" and verb in STRIKING and (
                held not in (None, who) or (held is None and thrower(target["id"], c["t"]) not in (None, who))):
            kind = f"a {verb} on a prop another performer holds or threw"
        elif c["contact_type"] == "possess" and verb == "catch" and target["kind"] == "entity" and target["id"] != who:
            kind = "a catch of another performer's body"
        elif c["contact_type"] == "touch" and target["id"] in stab and held not in (None, who):
            kind = "a body touched by a blade another performer holds"
        if kind:
            present = [e for e in entities if not any(actor == e and start < c["t"] - EPSILON
                                                      and (back is None or c["t"] < back - EPSILON)
                                                      for actor, _, start, back in gone)]
            out.append({"t": c["t"], "contact": c["id"], "kind": kind, "bodies": present})
    return out


def hold_times(envelope, frame_parts):
    """The instants a camera hold is owed (owner O92): every hit from the contacts and every S17 hold on an impact frame,
    one per frame."""
    tolerance = 0.5 / envelope["scene"]["fps"] + EPSILON
    held = {round(h["t"], 6) for h in frame_parts["holds"] if any(abs(h["t"] - i) <= tolerance for i in frame_parts["impact"])}
    out = []
    for t in sorted({round(h["t"], 6) for h in hits(envelope)} | held):
        if not out or t - out[-1] > tolerance:
            out.append(t)
    return out
