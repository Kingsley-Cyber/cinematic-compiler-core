"""S04: the beat validator rejects each rule's violation; the courtyard plan passes."""

import copy
import json

import pytest
from conftest import ROOT

from compiler import pipeline
from planner.beat_planner import prepare
from planner.dynamic_beat_validator import validate

pytestmark = pytest.mark.unit
EXAMPLE = ROOT / "examples" / "wizard_vs_acrobat"
QUERY = json.loads((EXAMPLE / "request.json").read_text())["query"]
PLAN = json.loads((EXAMPLE / "plans" / "temporal.json").read_text())
PACKET = prepare(pipeline.run(QUERY, until="constraint"))


def beat(plan, identity):
    return next(b for b in plan["beats"] if b["id"] == identity)


def codes_after(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {row["code"] for row in validate(plan, PACKET)}


def test_courtyard_plan_passes():
    assert validate(PLAN, PACKET) == []


@pytest.mark.parametrize("code, change", [
    ("BEAT_ID", lambda p: beat(p, "b02").update(id="b01")),
    ("BEAT_TIME", lambda p: beat(p, "b13").update(dur=2.0)),
    ("BEAT_TIME", lambda p: beat(p, "b13").update(dur=0)),
    ("BEAT_ACTOR", lambda p: beat(p, "b01").update(actor="dragon")),
    ("BEAT_PARTICIPANT", lambda p: beat(p, "b01")["participants"].append({"kind": "prop", "id": "staff"})),
    ("BEAT_PARTICIPANT", lambda p: beat(p, "b03")["participants"].append({"kind": "entity", "id": "acrobat"})),
    ("BEAT_PARTICIPANT", lambda p: beat(p, "b01")["participants"].append({"kind": "entity", "id": "acrobat"})),
    ("BEAT_POSE_ANCHOR", lambda p: beat(p, "b05")["pos"].pop("wizard")),
    ("BEAT_POSE_ANCHOR", lambda p: beat(p, "b01")["facing"].update(acrobat=[0, 0, 0])),
    ("BEAT_POSE_ANCHOR", lambda p: beat(p, "b01")["pos"].update(dragon=[0, 0, 0])),
    ("BEAT_STATE", lambda p: beat(p, "b01")["effects"].append(
        {"subject": {"kind": "entity", "id": "acrobat"}, "property": "mood", "value": "happy"})),
    ("BEAT_STATE", lambda p: beat(p, "b01")["effects"].append(
        {"subject": {"kind": "entity", "id": "acrobat"}, "property": "condition", "value": "exploded"})),
    ("BEAT_STATE", lambda p: beat(p, "b01")["requires"].append(
        {"subject": {"kind": "prop", "id": "staff"}, "property": "holder", "value": "wizard"})),
    ("BEAT_CONTACT", lambda p: beat(p, "b04")["contacts"][0]["a"].update(part="tail")),
    ("BEAT_CONTACT", lambda p: beat(p, "b05")["contacts"][1]["b"].update(part="wing")),
    ("BEAT_CAUSE", lambda p: beat(p, "b05")["causes"].append({"to": "b01", "causal_strength": "soft", "why": "x"})),
    ("BEAT_CAUSE", lambda p: beat(p, "b05")["causes"].append({"to": "b05", "causal_strength": "soft", "why": "x"})),
    ("FILLER_BEAT", lambda p: beat(p, "b03").update(effects=[], causes=[])),
    ("MODE_COHERENCE", lambda p: beat(p, "b01")["modes"].update(acrobat="calm_casting")),
    ("MODE_TRANSITION", lambda p: beat(p, "b03")["modes"].update(acrobat="focused")),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes_after(change)
