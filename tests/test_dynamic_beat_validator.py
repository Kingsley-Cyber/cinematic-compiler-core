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
    ("BEAT_TIME", lambda p: beat(p, "b14").update(dur=0)),  # the wizard's hold (b14 since O38, S-011)
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


def _two_beats(distance, dt, event_type="action", prop_effect=True):
    first = {"id": "b01", "t": 0.0, "dur": dt, "actor": "a", "event_type": event_type, "pos": {"a": [0, 0, 0]},
             "effects": [{"subject": {"kind": "prop", "id": "log"}, "property": "x", "value": "y"}] if prop_effect else []}
    second = {"id": "b02", "t": dt, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [distance, 0, 0]},
              "effects": []}
    return [first, second]


@pytest.mark.parametrize("distance, dt, event_type, prop_effect, fires", [
    (12.0, 0.5, "action", True, False),          # 24 m/s: fast, not a teleport
    (13.0, 0.5, "action", True, True),           # 26 m/s without a substitution: TELEPORT
    (13.0, 0.5, "substitution", True, False),    # a declared substitution that reveals a decoy may jump
    (13.0, 0.5, "substitution", False, True),    # a substitution that reveals nothing is refused
    (1.0, 0.0, "action", True, True),            # any jump in zero time
])
def test_teleport_threshold_and_the_substitution_exemption(distance, dt, event_type, prop_effect, fires):
    from planner.dynamic_beat_validator import _teleports
    assert any(f["code"] == "TELEPORT" for f in _teleports(_two_beats(distance, dt, event_type, prop_effect))) == fires


def _flight(p1, v0=(0.0, 2.0, 1.0), held=False, contact_inside=False, flt=False, genre="anime"):
    first = {"id": "b01", "t": 0.0, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]}, "effects": [],
             "contacts": ([{"contact_type": "possess", "a": {"kind": "entity", "id": "a", "part": "right_hand"},
                            "b": {"kind": "prop", "id": "k", "part": None}}] if held else []),
             "prop_samples": [{"prop": "k", "t": 0.5, "p": [0.0, 1.0, 0.0], "v": list(v0), "float": flt}]}
    second = {"id": "b02", "t": 0.5, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]}, "effects": [],
              "contacts": ([{"contact_type": "touch", "a": {"kind": "entity", "id": "a", "part": "right_foot"},
                             "b": {"kind": "prop", "id": "k", "part": None}}] if contact_inside else []),
              "prop_samples": [{"prop": "k", "t": 1.0, "p": list(p1), "v": None, "float": False}]}
    from planner.dynamic_beat_validator import _prop_kinematics
    return [f["code"] for f in _prop_kinematics([first, second], {"k": {}}, genre)]


def test_prop_kinematics_holds_free_flight_to_gravity():
    landing = [0.0, 1.0 + 2.0 * 0.5 - 0.5 * 9.81 * 0.25, 0.5]           # where gravity puts it after 0.5 s
    assert _flight(landing) == []
    assert _flight([0.0, 2.0, 0.5]) == ["PROP_KINEMATICS"]                # it would have to float up
    assert _flight([0.0, 2.0, 0.5], flt=True) == []                      # a declared anime float skips gravity
    assert _flight([0.0, 2.0, 0.5], flt=True, genre="live_action") == ["PROP_KINEMATICS"]  # floats are anime-only
    assert _flight([5.0, 1.0, 0.0], v0=(0.0, 0.0, 0.0)) == ["PROP_KINEMATICS"]   # a resting prop moved with no contact
    # the contact is at the end: still checked, and a free prop moving into a contact needs a pre/post pair (F2.2)
    assert _flight([0.0, 2.0, 0.5], contact_inside=True) == ["PROP_KINEMATICS", "PROP_KINEMATICS"]


GRAVITY_AT = [0.0, 1.0 + 2.0 * 0.5 - 0.5 * 9.81 * 0.25, 0.5]  # where a prop thrown at 0.0 from [0, 1, 0] is at 0.5
VELOCITY_AT = [0.0, 2.0 - 9.81 * 0.5, 1.0]


def _deflect(phases=("pre", "post"), contact=True, pre_v=None, post_p=None):
    """A free prop thrown at 0.0 meets a foot at 0.5: the pre sample ends the first beat, the post starts the second."""
    pre = {"prop": "k", "t": 0.5, "p": GRAVITY_AT, "v": pre_v or VELOCITY_AT, "float": False}
    post = {"prop": "k", "t": 0.5, "p": post_p or GRAVITY_AT, "v": [0.0, -1.0, -2.0], "float": False}
    for sample, phase in zip((pre, post), phases, strict=True):
        if phase:
            sample["phase"] = phase
    first = {"id": "b01", "t": 0.0, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]}, "effects": [],
             "contacts": [], "prop_samples": [{"prop": "k", "t": 0.0, "p": [0.0, 1.0, 0.0], "v": [0.0, 2.0, 1.0],
                                               "float": False}, pre]}
    second = {"id": "b02", "t": 0.5, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]},
              "effects": [], "prop_samples": [post],
              "contacts": ([{"contact_type": "touch", "a": {"kind": "entity", "id": "a", "part": "right_foot"},
                             "b": {"kind": "prop", "id": "k", "part": None}, "at": "start"}] if contact else [])}
    from planner.dynamic_beat_validator import _prop_kinematics
    return [f["message"] for f in _prop_kinematics([first, second], {"k": {}}, "anime")]


def test_a_contact_on_a_flying_prop_is_a_pre_and_post_pair():
    assert _deflect() == []                                                     # F2.2: the deflect is instantaneous
    assert _deflect(contact=False) == ["k has a pre and a post sample at 0.5 but no contact on it then"]
    assert _deflect(phases=(None, None)) == [
        "k at 0.5 has samples ['none', 'none']: a time takes one sample, or one pre and one post on a contact",
        "k is moving free into a contact at 0.5: give it a pre and a post sample there (F2.2)"]
    assert _deflect(phases=("post", "post"))[0].startswith("k at 0.5 has samples ['post', 'post']")
    assert _deflect(post_p=[1.0, 1.0, 0.5]) == [
        "k moves between its pre and post samples at 0.5; the contact is instantaneous"]


def test_gravity_reaches_the_pre_sample_in_velocity_too():
    assert _deflect(pre_v=[0.0, 2.0, 1.0]) == [                                 # the throw's velocity, no gravity
        "k from 0.0 would arrive at 0.5 with v [0.0, -2.91, 1.0], not [0.0, 2.0, 1.0]"]
    assert _deflect(pre_v=[0.0, VELOCITY_AT[1] + 0.2, 1.0]) == []                # within 0.25 m/s (interpretation)


def test_one_sample_at_a_contact_on_a_flying_prop_is_refused():
    """Without the pair the sample's velocity is ambiguous: before or after the foot?"""
    from planner.dynamic_beat_validator import _prop_kinematics
    first = {"id": "b01", "t": 0.0, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]}, "effects": [],
             "contacts": [], "prop_samples": [{"prop": "k", "t": 0.0, "p": [0.0, 1.0, 0.0], "v": [0.0, 2.0, 1.0],
                                               "float": False}]}
    second = {"id": "b02", "t": 0.5, "dur": 0.5, "actor": "a", "event_type": "action", "pos": {"a": [0, 0, 0]},
              "effects": [], "prop_samples": [{"prop": "k", "t": 0.5, "p": GRAVITY_AT, "v": [0.0, -1.0, -2.0],
                                               "float": False}],
              "contacts": [{"contact_type": "touch", "a": {"kind": "entity", "id": "a", "part": "right_foot"},
                            "b": {"kind": "prop", "id": "k", "part": None}, "at": "start"}]}
    findings = _prop_kinematics([first, second], {"k": {}}, "anime")
    assert [f["code"] for f in findings] == ["PROP_KINEMATICS"]
    assert [f["message"] for f in findings] == [
        "k is moving free into a contact at 0.5: give it a pre and a post sample there (F2.2)"]


def test_the_rows_print_the_pair_pre_before_post():
    from renderers import prop_samples
    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    rows = [text for _, text in prop_samples.rows(envelope, {"ninja_lean": "A", "ninja_broad": "B"}, "kunai", False)]
    at = [text for text in rows if text.startswith("2.50")]
    assert at == ["2.50 pre-contact p[0.5, 1, 4.6] v[-1.4, -3.46, 0.2] moving down along -X",
                  "2.50 post-contact p[0.5, 1, 4.6] v[-0.5, -0.54, 1.75] moving down along +Z"]
