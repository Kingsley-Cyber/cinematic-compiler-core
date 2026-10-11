"""M8.1 staff geometry: limb, body and head words from key poses, support words and turn signs."""

import json
import re

import pytest
from conftest import ROOT

from solver import staff_geometry as g

pytestmark = pytest.mark.unit
JOINTS = ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")
WORD = re.compile(r"^(place-(high|low)|(forward|back|left|right|left-forward|left-back|right-forward|right-back)"
                  r"-(high|mid|low))$")


def key(rot=(0, 0, 0), **bones):
    return {"rot": list(rot), "bones": {j: list(bones.get(j, (0, 0, 0))) for j in JOINTS}}


def test_rest_pose_hangs_every_limb_and_stands_upright():
    words = g.pose_words(key())
    assert words["body"] is None and words["head"] is None
    for side in ("left", "right"):
        assert words[side] == {"arm": "place-low", "leg": "place-low", "lower_arm": "straight", "lower_leg": "straight"}


@pytest.mark.parametrize("bones, side, limb, word", [
    ({"LA": (-90, 0, 0)}, "left", "arm", "forward-mid"),
    ({"LA": (-180, 0, 0)}, "left", "arm", "place-high"),
    ({"LA": (-170, 0, 0)}, "left", "arm", "forward-high"),     # lookup: overhead 170 -> forward / high
    ({"LA": (-135, 0, 0)}, "left", "arm", "forward-high"),     # lookup: forward 135 -> forward / high
    ({"LA": (-120, 0, 0)}, "left", "arm", "forward-mid"),      # lookup: forward 120 -> forward / middle
    ({"LUL": (-60, 0, 0)}, "left", "leg", "forward-mid"),      # lookup: forward 60 -> forward / middle
    ({"LUL": (-45, 0, 0)}, "left", "leg", "forward-low"),      # lookup: forward 45 -> forward / low
    ({"RUL": (60, 0, 0)}, "right", "leg", "back-mid"),         # lookup: back 60 -> back / middle
    ({"LA": (0, 0, 90)}, "left", "arm", "left-mid"),           # +Z swings a hanging limb toward +X, the performer's left
    ({"RA": (0, 0, -90)}, "right", "arm", "right-mid"),
    ({"LA": (-90, 0, 45)}, "left", "arm", "left-forward-mid"),
])
def test_limb_direction_and_level(bones, side, limb, word):
    assert g.pose_words(key(**bones))[side][limb] == word


def test_limbs_read_relative_to_the_body_and_the_body_against_gravity():
    turned = g.pose_words(key((0, 90, 0), LA=(-90, 0, 0), Sp=(30, 0, 0)))
    assert turned["left"]["arm"] == "forward-mid" and turned["body"] == "forward-high (30 lean)"
    assert g.pose_words(key((30, 0, 0)))["body"] == "forward-high (30 lean)"
    assert g.pose_words(key(Sp=(5, 0, 0)))["body"] is None
    assert g.pose_words(key(Sp=(90, 0, 0)))["body"] == "forward-mid (90 lean)"
    assert g.pose_words(key((0, 0, 180)))["body"] == "inverted"
    assert g.pose_words(key(HD=(-30, 0, 0)))["head"] == "back-high"


@pytest.mark.parametrize("rot, word", [((-90, 0, 0), "folded 90"), ((-7, 0, 0), "straight"),
                                       ((-100, 0, 0), "folded 105"), ((-97.5, 0, 0), "folded 105")])
def test_fold_steps_round_half_up(rot, word):
    assert g.fold_word(list(rot)) == word


def test_azimuth_ties_round_up():
    assert g.elevation_azimuth((1.0, 0.0, 1.0 / 0.41421356237))[1] == 22.5
    assert g.direction_word((1.0, 0.0, 1.0 / 0.41421356237)) == "left-forward-mid"
    assert g.direction_word((1.0, 0.0, 1.0)) == "left-forward-mid"


@pytest.mark.parametrize("parts, kwargs, words, tags", [
    ([], {}, "NO SUPPORT", ""),
    (["left_foot", "right_foot"], {}, "both feet place-mid", "[f:both]"),
    (["left_foot", "right_foot"], {"knee_folds": {"left": 90}}, "both feet place-low", "[f:both]"),
    (["right_foot"], {"posture": "crouching"}, "RIGHT foot place-low", "[f:R]"),
    (["left_hand"], {}, "LEFT hand place-low", "[h:L]"),
    (["left_hand", "right_hand"], {"posture": "inverted"}, "both hands place-low (inverted)", "[h:both]"),
    (["torso"], {}, "torso place-low", "[torso]"),
    (["left_foot", "right_foot"], {"surfaces": {"left_foot": "stone_wall", "right_foot": "stone_wall"}},
     "both feet place-mid ON THE stone wall", "[f:both_on_stone_wall]"),
    (["left_hand", "right_foot"], {}, "RIGHT foot place-mid + LEFT hand place-low", "[f:R] [h:L]"),
])
def test_support_words_and_tags(parts, kwargs, words, tags):
    assert g.support_words(parts, **kwargs) == {"words": words, "tags": tags}


def test_turn_signs_name_the_axis_and_the_side():
    assert g.turn_words({"turn": "none", "rot": [0, 0, 0]}) is None
    assert g.turn_words({"turn": "cartwheel", "rot": [0, 0, 0]}) == "cartwheel sign (sagittal axis)"
    assert g.turn_words({"turn": "cartwheel", "rot": [0, 0, 0]}, {"rot": [0, 0, 180]}) == \
        "cartwheel sign (sagittal axis, toward the performer's right, 180)"
    assert g.turn_words({"turn": "flip", "rot": [0, 0, 0]}, {"rot": [-360, 0, 0]}) == \
        "flip sign (lateral axis, backward, 360)"
    assert g.turn_words({"turn": "spin", "rot": [0, 10, 0]}, {"rot": [0, 100, 0]}) == \
        "turn sign (vertical axis, to the left, 90)"


def test_every_example_key_reads_in_the_closed_vocabulary():
    for path in sorted((ROOT / "examples").glob("*/envelope.json")):
        for node in json.loads(path.read_text())["nodes"]["motion"]["items"]:
            words = g.pose_words(node)
            for side in ("left", "right"):
                assert WORD.match(words[side]["arm"]) and WORD.match(words[side]["leg"]), (path.parent.name, node["id"])


def test_derived_directions_mostly_agree_with_the_23_sources_own_words():
    """The 2.3 source writes each key twice, as numbers and as words ('L:arm fwd mid'). Under the Q6 convention the
    derived direction matches its words for most limbs; a flipped sign convention would read most forward limbs as
    back. The source is not consistent (audit X5/X21: the same word with opposite signs), so this is a floor."""
    source = (ROOT / "kernel" / "sources" / "lbn-2.3-adv.txt").read_text()
    rows = json.loads(source[source.index("{"):])["A"]
    hits = total = 0
    for _, _, _, rot, joints, description in (row[:6] for row in rows):
        sides = re.match(r"L:(.*?); R:(.*?);", description)
        words = g.pose_words({"rot": rot, "bones": {j: joints.get(j, [0, 0, 0]) for j in JOINTS}})
        for side, text in (("left", sides.group(1)), ("right", sides.group(2))):
            text = sides.group(1) if text == "same" else text
            for limb in ("arm", "leg"):
                found = re.search(rf"\b{limb} (fwd|back) ", text)
                if found:
                    total += 1
                    hits += words[side][limb].startswith({"fwd": "forward", "back": "back"}[found.group(1)])
    assert total >= 80 and hits / total >= 0.7, (hits, total)
