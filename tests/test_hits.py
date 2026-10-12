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
