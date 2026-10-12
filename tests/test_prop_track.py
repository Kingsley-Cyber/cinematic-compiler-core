"""Plan F2.1, F6.1 (as amended by W4) and F6.2: the derived track says where each prop is from 0 to the end."""

import copy
import json

import pytest
from conftest import ROOT

from renderers import prop_samples
from validators import prompt_validator

pytestmark = pytest.mark.unit


def _envelope(name):
    return json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))


def test_the_kunai_is_somewhere_every_moment():
    envelope = _envelope("reference_fight")
    spans = prop_samples.track(envelope, envelope["nodes"]["render"]["items"][0]["labels"], "kunai")
    assert [(start, stop, kind) for start, stop, kind, _ in spans] == [
        (0.0, 2.0, "held"), (2.0, 2.5, "flight"), (2.5, 2.72, "flight"), (2.72, 8.0, "rest"), (8.0, 10.0, "held")]
    assert spans[3][3] == "at rest on the ground at [1.4, 0, 3.77]"      # F6.2: one rest from 2.72 to the pickup (O77, O89)


def test_a_place_set_before_a_hold_does_not_outlive_it():
    envelope = _envelope("ugc_glasses_demo")
    spans = prop_samples.track(envelope, envelope["nodes"]["render"]["items"][0]["labels"], "glasses")
    assert spans[0][3] == "held by A R hand"            # taken on the tabletop at the first frame (RV-03, F-077, R-17)
    assert spans[-1][3] == "at rest at [0, 1.66, 0.06]"               # worn on the face (S-030), not 'on the tabletop'


def test_a_flight_without_its_physics_is_refused():
    envelope = _envelope("reference_fight")
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    broken = text.replace("2.50-2.72 ballistic under gravity from", "2.50-2.72 flies from")  # lands at 2.72 since O89
    assert "PROP_PHYSICS_UNSTATED" in {f["code"] for f in prompt_validator.check(broken, envelope, "mixed")}
    assert "PROP_PHYSICS_UNSTATED" not in {f["code"] for f in prompt_validator.check(text, envelope, "mixed")}


def test_a_prop_with_no_place_is_refused():
    envelope = copy.deepcopy(_envelope("ugc_glasses_demo"))
    for beat in envelope["nodes"]["beats"]["items"]:
        beat["prop_samples"], beat["contacts"] = [], []      # no hold either: held from 0.0 since RV-03 (F-077)
    for state in envelope["nodes"]["states"]["items"]:
        state["conditions"]["location"] = "unknown"
    labels = envelope["nodes"]["render"]["items"][0]["labels"]
    assert prop_samples.track(envelope, labels, "glasses")[0][2:] == ("unplaced", "place not given")
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    assert "PROP_VISIBILITY" in {f["code"] for f in prompt_validator.check(text, envelope, "mixed")}
