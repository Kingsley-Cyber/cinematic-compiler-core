"""PLAN-010 Phase 2 (S-134): the model writes each pose in words, the compiler the joint angles; every word reads back
as itself (ADR-O119: one behavior per test, a valid and an invalid case per check)."""

import pytest

from solver import intent
from solver.staff_geometry import SECTORS, body_word, fold_word, head_word, pose_words

pytestmark = pytest.mark.unit
DIRECTIONS = [f"{s}-{lvl}" for s in SECTORS for lvl in ("high", "mid", "low")] + ["place-high", "place-low"]
POSE = {"body": "forward-high (30 lean)", "head": "forward-mid",
        "left": {"arm": "forward-high", "lower_arm": "folded 45", "leg": "back-low", "lower_leg": "folded 60"},
        "right": {"arm": "right-mid", "lower_arm": "straight", "leg": "forward-low", "lower_leg": "folded 15"}}
KEY = {"slot": "a@b01", "pos": [0, 1, 0], "rot": [0, 0, 0], "words": POSE}


def test_every_direction_word_reads_back_from_its_angles():
    sides = {"left": {"arm": None, "lower_arm": "straight", "leg": "place-low", "lower_leg": "straight"}}
    for word in DIRECTIONS:
        sides["left"]["arm"] = word
        bones = intent.bones_from_words({**sides, "right": sides["left"]})
        assert intent.reads_back(bones)["left"]["arm"] == word


def test_a_fold_reads_back_and_bends_each_limb_its_own_way():
    assert fold_word(intent.fold_angles("folded 45", "arm")) == "folded 45" == fold_word(intent.fold_angles("folded 45", "leg"))
    assert intent.fold_angles("folded 45", "arm")[0] < 0 < intent.fold_angles("folded 45", "leg")[0]


def test_a_body_lean_and_a_head_read_back():
    sp = intent.spine_angles("forward-high (30 lean)", [0, 0, 0])
    assert body_word({"rot": [0, 0, 0], "bones": {"Sp": sp}}) == "forward-high (30 lean)"
    assert head_word({"bones": {"NK": [0, 0, 0], "HD": intent.head_angles("left-mid")}}) == "left-mid"


def test_a_key_in_words_resolves_to_angles_that_read_as_its_words():
    resolved = intent.resolve_key(KEY)
    assert pose_words(resolved) == POSE


def test_the_joint_limits_bound_what_the_words_ask():
    resolved = intent.resolve_key(KEY, {"LA.x": (-30.0, 30.0)})
    assert -30.0 <= resolved["bones"]["LA"][0] <= 30.0 and pose_words(resolved)["left"]["arm"] != "forward-high"


def test_a_key_with_angles_keeps_them():
    key = {**KEY, "bones": {"Sp": [5, 0, 0]}}
    assert intent.resolve_key(key) is key


def test_the_model_writes_words_and_never_angles():
    from compiler.author import _schema
    item = _schema("motion")["properties"]["keys"]["items"]
    assert "bones" not in item["properties"] and "words" in item["required"]


def test_every_direction_word_stays_inside_the_schema_bound():
    """S-136: an arm straight out to the side reads the same at every pitch; the search keeps the one nearest rest."""
    assert all(abs(v) <= 180 for word in DIRECTIONS for v in intent.limb_angles(word))
