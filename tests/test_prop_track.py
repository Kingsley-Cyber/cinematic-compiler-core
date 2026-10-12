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
    """F-140 (RV-46): the kunai rests on the ground from 2.72 (its location set at 3.0) and A holds it from 8.0; the track
    says the hold from 8.0, not the ground S06 still names (F-106, RV-31)."""
    envelope = _envelope("reference_fight")
    spans = prop_samples.track(envelope, envelope["nodes"]["render"]["items"][0]["labels"], "kunai")
    assert spans[-2] == (2.72, 8.0, "rest", "at rest on the ground at [1.4, 0, 3.77]")
    assert spans[-1] == (8.0, 10, "held", "held by A R hand")
    states = {s["id"]: s["conditions"] for s in envelope["nodes"]["states"]["items"]}
    assert states["kunai@b21"]["location"] == "ground"


def test_the_glasses_are_held_from_the_first_frame_and_worn_at_the_end():
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


def test_a_track_names_a_goal_only_where_the_path_reaches_it():
    """F-122 (ADR-O108): the kunai thrown at 2.0 reaches A's foot, so it moves toward A; deflected at 2.5 it lands 0.85 m
    short of B, so it names no goal; aimed into B's body, it would."""
    envelope = _envelope("reference_fight")
    labels = envelope["nodes"]["render"]["items"][0]["labels"]
    texts = dict(prop_samples.rows(envelope, labels, "kunai", compact=False))
    assert texts[2.0].endswith("moving up toward A")
    rows = [text for t, text in prop_samples.rows(envelope, labels, "kunai", compact=False) if t == 2.5]
    assert rows[1].endswith("moving down along -Z")
    post = next(s for b in envelope["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])
                if s["prop"] == "kunai" and s.get("phase") == "post")
    body = prop_samples.bodies(envelope)
    torso = next(points["torso"] for t, points in body["ninja_broad"] if t == 2.5)
    tau = 0.2                                                      # into B's torso at 2.7, B's 2.5 key the nearest
    aimed = dict(post, v=[(torso[0] - post["p"][0]) / tau, (torso[1] - post["p"][1] + 0.5 * 9.81 * tau * tau) / tau,
                          (torso[2] - post["p"][2]) / tau])
    assert prop_samples.reaches(post, 2.72, body) is None and prop_samples.reaches(aimed, 2.72, body) == "ninja_broad"


def test_a_track_never_says_toward_what_the_prompt_says_not():
    """F-122 (PROMPT_CONTRADICTION): the deflected kunai's line said "toward B" beside "...NOT toward B"."""
    envelope = _envelope("reference_fight")
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    broken = text.replace("v[0.5, -4, -3] moving down along -Z", "v[0.5, -4, -3] moving down toward B", 1)
    assert broken != text
    assert "PROMPT_CONTRADICTION" in {f["code"] for f in prompt_validator.check(broken, envelope, "mixed")}
    assert "PROMPT_CONTRADICTION" not in {f["code"] for f in prompt_validator.check(text, envelope, "mixed")}
