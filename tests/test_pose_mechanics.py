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


def test_two_feet_share_the_weight_by_where_the_centre_of_mass_falls_and_outside_is_negative():
    feet = {"left_foot": [-0.2, 0, 0], "right_foot": [0.2, 0, 0]}
    middle = pose_mechanics.weight_distribution(feet, [0, 1, 0])
    assert middle["share"] == {"left_foot": 0.5, "right_foot": 0.5} and middle["margin_m"] == 0.1
    leaning = pose_mechanics.weight_distribution(feet, [0.1, 1, 0])
    assert leaning["share"] == {"left_foot": 0.25, "right_foot": 0.75}
    beyond = pose_mechanics.weight_distribution(feet, [0, 1, 0.5])
    assert beyond["margin_m"] == -0.4
    assert pose_mechanics.weight_distribution({}, [0, 1, 0]) is None
    tripod = pose_mechanics.weight_distribution({"a": [0, 0, 0], "b": [1, 0, 0], "c": [0, 0, 1]}, [0.2, 1, 0.2])
    assert tripod["margin_m"] > 0.1 and abs(sum(tripod["share"].values()) - 1) < 0.02


def test_the_clash_puts_naruto_s_weight_on_his_front_foot():
    """The clash frame (Claude's reading): Naruto drives off the rear foot onto the front one."""
    joints = JOINTED["clash/naruto"]["joints"]
    com = pose_mechanics.centre_of_mass(joints, forward_kinematics.masses())
    weight = pose_mechanics.weight_distribution({"left_foot": joints["left_sole"], "right_foot": joints["right_sole"]}, com)
    assert weight["share"]["right_foot"] > 0.5 and weight["margin_m"] > 0


def test_a_stable_pose_outside_its_support_is_refused_and_sent_to_s13():
    from compiler.author import ROUTES
    from compiler.passes.derived import p14_pose_mechanics

    envelope = _envelope("live_action_standoff")
    graph = {"pose_mechanics": copy.deepcopy(envelope["nodes"]["pose_mechanics"]["items"])}
    stable = next(k["id"] for k in envelope["nodes"]["kinematic"]["items"] if k["balance"] == "stable")
    node = next(n for n in graph["pose_mechanics"] if n["id"] == stable)
    node["weight"] = {**node["weight"], "margin_m": -0.06}  # past live action's 0.05 m (owner)
    assert [f["detail"] for f in p14_pose_mechanics.weight_findings(envelope, graph)] == [stable]
    node["weight"]["margin_m"] = -0.04
    assert p14_pose_mechanics.weight_findings(envelope, graph) == []
    assert ROUTES["WEIGHT_DISTRIBUTION"] == "motion"


def test_the_owner_s_exceptions_keep_the_four_source_poses_and_must_stay_true(monkeypatch, tmp_path):
    """The owner (2026-10-13): the reference fight's b07, b08, b11, b23 are recorded deviations; an exception that names a
    pose which is not a miss is refused."""
    from compiler.passes.derived import p14_pose_mechanics

    envelope = _envelope("reference_fight")
    graph = {"pose_mechanics": envelope["nodes"]["pose_mechanics"]["items"]}
    kept = p14_pose_mechanics.owner_exceptions(envelope["provenance"]["source_prompt"])
    assert sorted(kept) == ["ninja_lean@b07", "ninja_lean@b08", "ninja_lean@b11", "ninja_lean@b23"]
    assert p14_pose_mechanics.weight_findings(envelope, graph) == []
    extra = tmp_path / "weight_exceptions.yaml"
    extra.write_text(p14_pose_mechanics.EXCEPTIONS.read_text(encoding="utf-8").replace('key: "ninja_lean@b23"',
                                                                                         'key: "ninja_lean@b01"'))
    monkeypatch.setattr(p14_pose_mechanics, "EXCEPTIONS", extra)
    assert {f["detail"] for f in p14_pose_mechanics.weight_findings(envelope, graph)} == {"ninja_lean@b23", "ninja_lean@b01"}


def _eleven(joints):
    """The 11 points forward kinematics names, from a jointed figure."""
    return {"pelvis": joints["pelvis"], "torso": joints["torso"], "head": joints["head"],
            **{f"{s}_{n}": joints[f"{s}_{j}"] for s in ("left", "right")
               for n, j in (("arm", "elbow"), ("hand", "hand"), ("leg", "knee"), ("foot", "sole"))}}


SIDE_CAMERA = ([1.2, 1.1, -6.0], [1.2, 1.1, 0.0])  # the frames' own view: square on to the picture plane


def test_a_hand_held_against_the_chest_is_against_its_own_body_and_one_held_out_is_clear():
    body = {"pelvis": [0, 1.0, 0], "torso": [0, 1.3, 0], "head": [0, 1.7, 0], "left_hand": [0.05, 1.3, 0.2],
            "right_hand": [0.7, 1.4, 0], "left_foot": [-0.15, 0, 0], "right_foot": [0.15, 0, 0]}
    sil = pose_mechanics.silhouette([0, 1.2, 5], [0, 1.2, 0], {"a": body})
    assert {"subject": "a", "end": "left_hand", "body": "a"} in sil["against"] and "a:right_hand" in sil["clear"]


def test_the_flying_kick_lands_on_naruto_and_sasuke_s_hands_read_clear():
    """The flying_kick frame (Claude's reading): the kick meets Naruto's face, its own target; Sasuke's hands to the
    ground read clear of both trunks."""
    sasuke = _eleven(JOINTED["flying_kick/sasuke"]["joints"])
    naruto = {**FIGURES["flying_kick/naruto"]["points"], "left_hand": [2.35, 1.95, 0], "right_hand": [1.80, 2.30, 0]}
    sil = pose_mechanics.silhouette(*SIDE_CAMERA, {"sasuke": sasuke, "naruto": naruto})
    assert {"subject": "sasuke", "end": "right_foot", "body": "naruto"} in sil["against"]
    assert not any(x["subject"] == "sasuke" and x["body"] == "sasuke" and x["end"] == "right_foot" for x in sil["against"])
    assert {"sasuke:left_hand", "sasuke:right_hand"} <= set(sil["clear"])


def test_the_clash_reads_naruto_s_cocked_fist_clear_of_both_bodies():
    naruto = _eleven(JOINTED["clash/naruto"]["joints"])
    assert "naruto:left_hand" in pose_mechanics.silhouette(*SIDE_CAMERA, {"naruto": naruto})["clear"]


def test_a_strike_hidden_against_a_body_other_than_its_target_is_named():
    envelope = copy.deepcopy(_envelope("reference_fight"))
    strike = next(c for c in envelope["nodes"]["contacts"]["items"]
                  if c["contact_type"] == "touch" and c["b"]["kind"] == "entity")
    shot = next(s for s in envelope["nodes"]["camera"]["items"] if s["beats"] and s["beats"][0] == strike["beat"])
    side, _, part = strike["body_part"].partition("_")
    end = f"{side}_{pose_checks.END.get(part, part)}"
    shot["derived"]["silhouette"]["against"].append({"subject": strike["a"]["id"], "end": end, "body": strike["a"]["id"]})
    assert [n["code"] for n in pose_checks.silhouette_readable(envelope)
            if n["key"] == f"{shot['id']}:{strike['id']}"] == ["SILHOUETTE_READABLE"]
