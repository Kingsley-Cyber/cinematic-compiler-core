"""PLAN-010 Phase 1 (S-133): every limb has one job at each instant, the declared roles are the contacts' twins, and a
strike lands from within reach, refused at S04 before any pose is written (ADR-O119: a valid and an invalid case per
check)."""

import pytest

from planner import dynamic_beat_validator as v

pytestmark = pytest.mark.unit
GROUND = {"kind": "surface", "id": "ground", "part": None}
KNIGHT = {"kind": "entity", "id": "knight", "part": "torso"}


def _contact(kind, part, target, at="end", verb=None):
    return {"contact_type": kind, "a": {"kind": "entity", "id": "ninja", "part": part}, "b": target, "at": at,
            **({"verb": verb} if verb else {})}


def _beat(bid, t, contacts, gap=1.0):
    beat = {"id": bid, "t": t, "dur": 0.5, "contacts": contacts,
            "pos": {"ninja": [0, 1, 0], "knight": [0, 1, gap]}}
    return {**beat, "roles": v.roles_from(beat)}


def _codes(beats):
    return [f["code"] for f in v._one_part_one_job(beats) + v._roles_agree(beats) + v._within_reach(beats)]


def test_a_foot_released_as_it_kicks_has_one_job():
    beats = [_beat("b01", 0.0, [_contact("support", "right_foot", GROUND)]),
             _beat("b02", 0.5, [_contact("release", "right_foot", GROUND), _contact("touch", "right_foot", KNIGHT)])]
    assert _codes(beats) == []


def test_a_foot_that_kicks_while_it_stands_is_refused():
    """The R20 idea's second run: the ninja's right foot kicked the knight while it stood on the floor."""
    beats = [_beat("b01", 0.0, [_contact("support", "right_foot", GROUND)]),
             _beat("b02", 0.5, [_contact("touch", "right_foot", KNIGHT)])]
    assert _codes(beats) == ["ONE_PART_ONE_JOB"]


def test_a_push_off_a_wall_is_a_moment_but_two_stands_at_once_are_refused():
    wall = {"kind": "surface", "id": "wall", "part": None}
    push = [_beat("b01", 0.0, [_contact("support", "left_foot", GROUND)]),
            _beat("b02", 0.5, [_contact("touch", "left_foot", wall, at="start")])]
    assert _codes(push) == []
    two = [_beat("b01", 0.0, [_contact("support", "left_foot", GROUND)]),
           _beat("b02", 0.5, [_contact("support", "left_foot", wall)])]
    assert _codes(two) == ["ONE_PART_ONE_JOB"]


def test_a_held_kunai_strikes_with_its_hand():
    kunai = {"kind": "prop", "id": "kunai", "part": None}
    beats = [_beat("b01", 0.0, [_contact("possess", "right_hand", kunai)]),
             _beat("b02", 0.5, [_contact("touch", "right_hand", KNIGHT)])]
    assert _codes(beats) == []


def test_roles_that_are_not_the_contacts_twins_are_refused():
    beat = _beat("b01", 0.0, [_contact("touch", "right_hand", KNIGHT, verb="block")])
    assert beat["roles"][0]["role"] == "block" and _codes([beat]) == []
    beat["roles"][0]["role"] = "strike"
    assert _codes([beat]) == ["CONSTRAINT_SATISFIABLE"]


def test_a_strike_from_out_of_reach_is_refused():
    assert _codes([_beat("b01", 0.0, [_contact("touch", "right_hand", KNIGHT)], gap=1.2)]) == []
    assert _codes([_beat("b01", 0.0, [_contact("touch", "right_hand", KNIGHT)], gap=3.0)]) == ["CONSTRAINT_SATISFIABLE"]
