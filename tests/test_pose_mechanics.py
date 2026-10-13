"""PLAN-009 S14, the pose mechanics: each computed from a key's world points, printed on its staff line, and read back
from the owner's reference frames (tests/pose_references.py, Claude's interpretation of the images)."""

import copy
import json

import pytest
from conftest import ROOT
from pose_references import FIGURES, JOINTED

from solver import forward_kinematics, pose_mechanics
from solver.pose_mechanics import line_of_action
from validators import pose_checks

pytestmark = pytest.mark.unit
EXAMPLES = ("reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo")


def _envelope(name):
    return json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))


def _body(head, torso, pelvis, left, right):
    return {"head": head, "torso": torso, "pelvis": pelvis, "left_foot": left, "right_foot": right}


def test_a_standing_body_is_a_straight_line_a_bowed_one_a_c_and_a_twist_an_s():
    stand = line_of_action(_body([0, 1.7, 0], [0, 1.3, 0], [0, 0.95, 0], [-0.1, 0, 0], [0.1, 0, 0]))
    assert stand["shape"] == "straight" and stand["tension"] < 0.08 and not stand["inverted"]
    bowed = line_of_action(_body([0, 1.7, 0], [0.3, 1.2, 0], [0.25, 0.8, 0], [-0.1, 0, 0], [0.1, 0, 0]))
    assert bowed["shape"] == "c" and bowed["apex"] == "torso" and bowed["bulge"][0] > 0.9
    twist = line_of_action(_body([0, 1.7, 0], [0.25, 1.3, 0], [-0.25, 0.9, 0], [0, 0, 0], [0, 0, 0.1]))
    assert twist["shape"] == "s"
    assert line_of_action({"head": [0, 1, 0]}) is None


@pytest.mark.parametrize("name", sorted(FIGURES))
def test_the_owner_reference_frames_read_back(name):
    """Each frame's figure gives back what the frame shows (shape, base foot, upside down, how hard it bends)."""
    shows, got = FIGURES[name]["shows"], line_of_action(FIGURES[name]["points"])
    assert got["shape"] == shows["shape"]
    for key in ("base", "inverted"):
        if key in shows:
            assert got[key] == shows[key], key
    if "tension" in shows:
        low, high = shows["tension"]
        assert low <= got["tension"] <= high
    if shows.get("horizontal"):
        assert abs(got["chord"][1]) < 0.2


def test_the_clash_bends_sasuke_harder_than_naruto():
    assert line_of_action(FIGURES["clash/sasuke"]["points"])["tension"] > \
        line_of_action(FIGURES["clash/naruto"]["points"])["tension"]


@pytest.mark.parametrize("name", EXAMPLES)
def test_every_key_has_its_line_of_action_and_its_staff_line_prints_it(name):
    envelope = _envelope(name)
    keys = {k["id"] for k in envelope["nodes"]["motion"]["items"]}
    mechanics = envelope["nodes"]["pose_mechanics"]["items"]
    assert {m["id"] for m in mechanics} == keys
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    assert text.count("line of action: ") >= len(keys) - len(envelope["edges"]["motion"]["items"]) and "LINE:" in \
        envelope["nodes"]["render"]["items"][0]["text"]


def test_a_strike_along_a_straight_line_is_named():
    envelope = copy.deepcopy(_envelope("reference_fight"))
    strike = next(c for c in envelope["nodes"]["contacts"]["items"]
                  if c["contact_type"] == "touch" and c["b"]["kind"] == "entity")
    key = next(k["id"] for k in envelope["nodes"]["motion"]["items"]
               if k["entity"] == strike["a"]["id"] and abs(k["t"] - strike["t"]) < 1e-6)
    node = next(m for m in envelope["nodes"]["pose_mechanics"]["items"] if m["id"] == key)
    node["line_of_action"] = {**node["line_of_action"], "shape": "straight", "tension": 0.02}
    assert [n["key"] for n in pose_checks.line_of_action(envelope)] == [key]


def test_a_body_standing_straight_has_its_centre_of_mass_over_its_hips_and_no_reach():
    joints = {"pelvis": [0, 1.0, 0], "chest": [0, 1.5, 0], "neck": [0, 1.6, 0], "head": [0, 1.7, 0],
              **{f"{s}_{j}": [x, y, 0] for s, x in (("left", 0.15), ("right", -0.15))
                 for j, y in (("shoulder", 1.5), ("elbow", 1.2), ("hand", 0.85), ("hip", 1.0), ("knee", 0.55),
                              ("ankle", 0.1), ("sole", 0.0))}}
    com = pose_mechanics.centre_of_mass(joints, forward_kinematics.masses())
    assert com[0] == 0 and 0.9 < com[1] < 1.15
    assert pose_mechanics.counterbalance(joints, com) == {"extended": [], "lead": None, "reach_m": 0.0, "counter": []}


@pytest.mark.parametrize("name", sorted(JOINTED))
def test_the_owner_reference_frames_balance_as_drawn(name):
    """The reach that leads and the limb that counters it, as the frame shows (Claude's reading of the image)."""
    figure = JOINTED[name]
    com = pose_mechanics.centre_of_mass(figure["joints"], forward_kinematics.masses())
    cb = pose_mechanics.counterbalance(figure["joints"], com)
    assert cb["lead"] == figure["shows"]["lead"] and figure["shows"]["counter_has"] in cb["counter"]


def test_a_reach_with_nothing_on_the_other_side_is_named():
    envelope = copy.deepcopy(_envelope("wizard_vs_acrobat"))
    node = envelope["nodes"]["pose_mechanics"]["items"][0]
    node["counterbalance"] = {"extended": ["right_arm"], "lead": "right_arm", "reach_m": 0.7, "counter": []}
    assert node["id"] in [n["key"] for n in pose_checks.counterbalance(envelope)]
