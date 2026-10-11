"""S05: causal edges are checked (linear, timing, effect, cycles) and the quadrant follows the owner table."""

import copy
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.authoring import StepFailed
from compiler.passes.mandatory import p05_causal
from kernel.canonical import ContractError, canonical_json
from validators.layer_dependency_validator import check_pass_writes

pytestmark = pytest.mark.unit
EXAMPLE = ROOT / "examples" / "wizard_vs_acrobat"
QUERY = json.loads((EXAMPLE / "request.json").read_text())["query"]
PLANS = {"temporal": json.loads((EXAMPLE / "plans" / "temporal.json").read_text())}
BEATS = pipeline.run(QUERY, until="temporal", plans=PLANS)["nodes"]["beats"]["items"]


def codes(beats):
    return {row["code"] for row in p05_causal.edges_and_findings(beats)[1]}


def find(beats, identity):
    return next(b for b in beats if b["id"] == identity)


def test_courtyard_causes_pass():
    edges, findings = p05_causal.edges_and_findings(BEATS)
    assert findings == [] and len(edges) == sum(len(b["causes"]) for b in BEATS)


@pytest.mark.parametrize("code, change", [
    ("CAUSE_BRANCHING", lambda b: find(b, "b05")["causes"].append({"to": "b09", "causal_strength": "soft", "why": "x"})),
    ("CAUSE_TIMING", lambda b: find(b, "b03")["causes"].__setitem__(0, {"to": "b04", "causal_strength": "hard", "why": "x"})),
    ("CAUSE_EFFECT", lambda b: find(b, "b10")["causes"].__setitem__(0, {"to": "b11", "causal_strength": "hard", "why": "x"})
     or find(b, "b09").update(causes=[])),
    ("CAUSE_TIMING", lambda b: find(b, "b11")["causes"].__setitem__(0, {"to": "b10", "causal_strength": "soft", "why": "x"})),
    ("CAUSE_TARGET", lambda b: find(b, "b13")["causes"].append({"to": "b99", "causal_strength": "soft", "why": "x"})),
])
def test_each_causal_rule_rejects_its_violation(code, change):
    beats = copy.deepcopy(BEATS)
    change(beats)
    assert code in codes(beats)


ENVELOPE = pipeline.run(QUERY, until="temporal", plans=PLANS)


def reason_codes(whys):
    """CAUSE_REASON findings after replacing the reasons of the named beats' causes."""
    beats = copy.deepcopy(BEATS)
    for beat in beats:
        for cause in beat["causes"]:
            cause["why"] = whys.get(beat["id"], cause["why"])
    edges, _ = p05_causal.edges_and_findings(beats)
    return sorted({f["edge"] for f in p05_causal.reason_findings(edges, beats, ENVELOPE)})


def test_a_reason_that_states_no_cause_is_refused():
    assert reason_codes({}) == []  # the wizard's authored reasons state causes
    assert reason_codes({"b01": "run_in leads straight into the next exchange."}) == ["b01__causes__b02"]  # identifier
    assert reason_codes({"b01": "It happens."}) == ["b01__causes__b02"]  # too short
    assert reason_codes({"b01": "A sudden gust makes everything go badly."}) == ["b01__causes__b02"]  # names nothing
    template = {b: f"The {who} keeps the fight going on." for b, who in (("b01", "acrobat"), ("b04", "acrobat"),
                                                                         ("b06", "wizard"))}
    assert reason_codes(template) == ["b01__causes__b02", "b04__causes__b05", "b06__causes__b07"]
    beats = copy.deepcopy(BEATS)
    find(beats, "b01")["causes"][0]["why"] = "x"
    envelope = copy.deepcopy(ENVELOPE)
    envelope["nodes"]["beats"]["items"] = beats
    with pytest.raises(StepFailed) as failed:
        p05_causal.run(envelope)
    assert "CAUSE_REASON" in {f["code"] for f in failed.value.findings}


def test_same_time_cycle_is_rejected():
    beats = [{"id": "b01", "t": 0, "dur": 0, "effects": [], "requires": [], "event_type": "action",
              "causes": [{"to": "b02", "causal_strength": "soft", "why": "x"}]},
             {"id": "b02", "t": 0, "dur": 0, "effects": [], "requires": [], "event_type": "action",
              "causes": [{"to": "b01", "causal_strength": "soft", "why": "x"}]}]
    assert "CAUSE_CYCLE" in codes(beats)


def synthetic(effects_per_beat, hard_edges, hold=False):
    beats = [{"id": f"b{i:02d}", "t": i, "dur": 1, "event_type": "action", "requires": [], "causes": [],
              "effects": [{"n": k} for k in range(effects_per_beat)]} for i in range(1, 6)]
    if hold:
        beats[-1]["event_type"] = "hold"
    edges = [{"causal_strength": "hard"}] * hard_edges
    return beats, edges


@pytest.mark.parametrize("effects, hard, style_ref, hold, expected", [
    (0, 0, None, False, "D"), (1, 2, None, False, "D"), (2, 3, None, False, "B"),
    (3, 3, None, True, "B"), (3, 3, "Ghibli", True, "C")])
def test_quadrant_follows_the_owner_table(effects, hard, style_ref, hold, expected):
    beats, edges = synthetic(effects, hard, hold)
    scores = p05_causal.quadrant(beats, edges, {"style_reference": style_ref})
    assert scores["quadrant"] == expected and scores["causal"]["branching"] == 0
    assert 1 in scores["strata"] and (3 in scores["strata"]) == (sum(scores["causal"].values()) > 0)


def test_linear_scenes_cannot_reach_quadrant_a_and_load_bearing_adds_stratum_4():
    beats, edges = synthetic(9, 9, True)
    scores = p05_causal.quadrant(beats, edges, {"style_reference": "x"}, load_bearing=True)
    assert scores["quadrant"] == "C" and scores["strata"] == [1, 2, 3, 4]


@pytest.mark.integration
def test_s05_writes_only_its_paths_and_is_deterministic(order):
    before = pipeline.run(QUERY, until="temporal", plans=PLANS)
    snapshot = copy.deepcopy(before)
    after = p05_causal.run(before, order=order)
    assert before == snapshot and check_pass_writes(order, "causal", before, after) == []
    assert after["scene"]["quadrant"]["quadrant"] == "B"
    with pytest.raises(ContractError):
        p05_causal.run(pipeline.run(QUERY, until="constraint"), order=order)
    outputs = {subprocess.run([sys.executable, "-m", "compiler.pipeline", QUERY, "--until", "causal", "--plans",
                               str(EXAMPLE / "plans")], cwd=ROOT, capture_output=True, text=True, check=True,
                              env={**os.environ, "PYTHONHASHSEED": seed}).stdout for seed in ("0", "9")}
    assert outputs == {canonical_json(pipeline.run(QUERY, until="causal", plans=PLANS))}
