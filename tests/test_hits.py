"""Hits from the contacts (owner O92, F-155, RV-57): what counts as a hit in the examples, and what does not."""

import json

import pytest
from conftest import ROOT

from planner import hits

pytestmark = pytest.mark.unit


def envelope(name):
    return json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))


def test_hits_come_from_the_contacts():
    fight = envelope("reference_fight")
    found = hits.hits(fight)
    assert [(h["t"], h["contact"], h["kind"]) for h in found] == [
        (2.5, "b06_c1", "a deflect on a prop another performer holds or threw"),
        (4.7, "b12_c1", "a touch on another performer's body"),
        (6.6, "b17_c1", "a catch of another performer's body"), (6.6, "b17_c2", "a catch of another performer's body"),
        (8.5, "b21_c1", "a body touched by a blade another performer holds")]
    # B's palm on the log no one holds (4.0), B's flick of its own volley (5.5), A's rope dart on B (no blade, 8.0)
    assert not {"b10_c1", "b14_c1", "b19_c1"} & {h["contact"] for h in found}
    assert all(h["bodies"] == ["ninja_broad", "ninja_lean"] for h in found)
    assert [h["t"] for h in hits.hits(envelope("wizard_vs_acrobat"))] == [3.6]
    assert hits.hits(envelope("live_action_standoff")) == [] == hits.hits(envelope("ugc_glasses_demo"))
    assert hits.hold_times(fight, fight["nodes"]["render"]["items"][0]["frame_parts"]) == [2.5, 4.7, 6.6, 8.5]


def test_a_prop_another_performer_threw_is_a_hit_whatever_the_verb():
    """F-175 (RV-69, owner O92): the kunai B threw, landing in A's torso and written with A as side a and no verb (as
    the golden writes the 8.5 drive), is a hit; it owes the same camera hold as the deflect."""
    import copy
    fight = envelope("reference_fight")
    probe = copy.deepcopy(fight)
    contact = next(c for c in probe["nodes"]["contacts"]["items"] if c["id"] == "b06_c1")
    contact.update(a={"kind": "entity", "id": "ninja_lean", "part": "torso"}, body_part="torso", verb=None)
    found = {h["contact"]: h["kind"] for h in hits.hits(probe)}
    assert found["b06_c1"] == "a body touched by a prop another performer threw"
    assert [h["t"] for h in hits.hits(probe)] == [h["t"] for h in hits.hits(fight)]

