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
    # owner O22, plan F4.1: a verb its contact type does not take; a throw that names no prop
    ("CONTACT_VERB", lambda p: beat(p, "b13")["contacts"][0].update(verb="strike")),    # a support takes no verb
    # owner O21 (audit X7): the acrobat lands on the ground at 9.80 with the root 2 m up
    ("SURFACE_HEIGHT", lambda p: beat(p, "b14")["pos"].update(acrobat=[-1.1, 2.0, 5.3])),
    ("CONTACT_VERB", lambda p: beat(p, "b12")["contacts"][0].update(verb="catch")),     # a release takes only throw
    ("CONTACT_VERB", lambda p: beat(p, "b12")["contacts"][0].update(verb="throw")),     # the ground is no prop
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
    ("FILLER_BEAT", lambda p: beat(p, "b03").update(effects=[], causes=[], contacts=[])),  # b03 lifts the vault hand (O89)
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
    assert at == ["2.50 pre-contact p[1.29, 1.13, 4.44] v[0.18, -3.2, 0.28] moving down along +Z",
                  "2.50 post-contact p[1.29, 1.13, 4.44] v[0.5, -4, -3] moving down along -Z"]  # owners O77, O89


def test_a_throw_leaves_its_prop_moving():
    """CONTACT_VERB (owner O22; interpretation: a throw sends the prop off moving, so a touch may throw)."""
    from planner.dynamic_beat_validator import _thrown
    throw = {"contact_type": "release", "verb": "throw", "a": {"kind": "entity", "id": "a", "part": "right_hand"},
             "b": {"kind": "prop", "id": "k", "part": None}, "at": "start"}
    beat = {"id": "b01", "t": 0.0, "dur": 0.5, "contacts": [throw],
            "prop_samples": [{"prop": "k", "t": 0.0, "p": [0.0, 1.0, 0.0], "v": [0.0, 2.0, 1.0], "float": False}]}
    assert _thrown([beat]) == []
    beat["prop_samples"][0]["v"] = None                                            # still in the hand: no throw
    assert [f["code"] for f in _thrown([beat])] == ["CONTACT_VERB"]


def test_a_landing_stands_on_the_top_it_lands_on():
    """SURFACE_HEIGHT (owner O21, audit X7): the root lies between the top and the body's standing leg above it (owner O85;
    the range is an interpretation)."""
    from planner.dynamic_beat_validator import _surface_heights
    feet = [{"contact_type": "support", "a": {"kind": "entity", "id": "a", "part": part},
             "b": {"kind": "surface", "id": "pillar", "part": None}, "at": "start"} for part in ("left_foot", "right_foot")]

    def codes(root_y, leg=1.22):                                              # the anime body (O85)
        beat = {"id": "b02", "t": 0.6, "dur": 0.5, "pos": {"a": [0, root_y, 5.8]}, "contacts": feet}
        return [f["code"] for f in _surface_heights([beat], {"pillar": 8.0}, leg)]

    assert codes(8.5) == []                                                   # O21: feet on the 8 m top, root 8.5
    assert codes(7.2) == ["SURFACE_HEIGHT", "SURFACE_HEIGHT"]                  # the source's 7.2: under the top
    assert codes(9.5) == ["SURFACE_HEIGHT", "SURFACE_HEIGHT"]                  # floating over it
    assert codes(9.2) == [] and codes(9.2, leg=0.98) == ["SURFACE_HEIGHT", "SURFACE_HEIGHT"]  # the bound is the body's leg


def test_a_resting_prop_has_something_under_it():
    """PROP_SUPPORT (owner O78, F-065): on a top, or placed by a fact since its last hold (a location, or worn)."""
    from planner.dynamic_beat_validator import _prop_support

    def codes(y, facts=()):
        beat = {"id": "b01", "t": 0.0, "dur": 1.0, "contacts": [], "requires": [], "effects": list(facts),
                "prop_samples": [{"prop": "k", "t": 1.0, "p": [0.0, y, 0.0], "v": [0, 0, 0], "float": False}]}
        return [f["code"] for f in _prop_support([beat], {"ground": 0.0})]

    fact = lambda name, value: {"subject": {"kind": "prop", "id": "k"}, "property": name, "value": value}  # noqa: E731
    assert codes(0.0) == []                                                   # on the ground
    assert codes(1.1) == ["PROP_SUPPORT"]                                     # the pellet before O78: mid-air
    assert codes(1.1, [fact("location", "wooden_pillar")]) == []              # stuck in the pillar
    assert codes(1.6, [fact("worn", "yes")]) == []                            # worn: the wearer holds it up



def test_a_resting_prop_is_where_it_rests_when_a_contact_takes_it():
    """F-077 (RV-03): a prop at rest is still where it rested at the instant a contact takes it, so it may not jump
    there (the UGC glasses left the table before the hand reached them); a contact between two samples still moves it."""
    from planner.dynamic_beat_validator import _prop_kinematics

    def taken_at(contact_t, p_after):
        take = {"contact_type": "possess", "a": {"kind": "entity", "id": "a", "part": "right_hand"},
                "b": {"kind": "prop", "id": "k", "part": None}}
        first = {"id": "b01", "t": 0.0, "dur": contact_t, "pos": {"a": [0, 1, 0]}, "contacts": [take],
                 "prop_samples": [{"prop": "k", "t": 0.0, "p": [0.3, 0.75, 0.3], "v": [0, 0, 0], "float": False}]}
        second = {"id": "b02", "t": contact_t, "dur": 1.0 - contact_t, "pos": {"a": [0, 1, 0]}, "contacts": [],
                  "prop_samples": [{"prop": "k", "t": 1.0, "p": p_after, "v": None, "float": False}]}
        return [(f["code"], f["message"]) for f in _prop_kinematics([first, second], {"k": {}}, "anime")]
    assert taken_at(1.0, [0.2, 1.1, 0.3]) == [("PROP_KINEMATICS",
                                               "k at rest moves between 0.0 and 1.0 with no contact before it")]
    assert taken_at(1.0, [0.3, 0.75, 0.3]) == []                       # taken where it rests
    assert taken_at(0.5, [0.2, 1.1, 0.3]) == []                        # taken at 0.5, then lifted


def test_a_vanished_body_lets_go_of_its_supports_and_holds():
    """VANISHED_BODY (owner O90, F-081): from a substitution until its actor's next beat the actor has no open support
    or hold; letting go at the substitution's start, and standing again when it reappears, pass."""
    from planner.dynamic_beat_validator import _vanished

    def plan(release_at):
        foot = {"contact_type": "support", "a": {"kind": "entity", "id": "x", "part": "left_foot"},
                "b": {"kind": "surface", "id": "ground", "part": None}, "at": "start"}
        let_go = {**foot, "contact_type": "release"}
        base = {"pos": {}, "participants": [], "event_type": "action", "actor": "x"}
        beats = [{**base, "id": "b01", "t": 0.0, "dur": 1.0, "contacts": [foot]},
                 {**base, "id": "b02", "t": 1.0, "dur": 1.0, "event_type": "substitution", "contacts": []},
                 {**base, "id": "b03", "t": 2.0, "dur": 1.0, "contacts": []},
                 {**base, "id": "b04", "t": 3.0, "dur": 1.0, "contacts": []}]
        if release_at == 1.0:                                    # lets go as it vanishes, stands again at 2.0
            beats[1]["contacts"], beats[2]["contacts"] = [let_go], [foot]
        else:
            beats[3]["contacts"] = [let_go]
        return [(f["code"], f["beat"]) for f in _vanished(beats)]
    assert plan(1.0) == []                                       # lets go as it vanishes, stands again at 2.0
    assert ("VANISHED_BODY", "b02") in plan(3.0)                  # the foot stays on the ground while x is gone
