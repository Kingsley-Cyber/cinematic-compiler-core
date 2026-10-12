"""Forward kinematics (owners O24, O72, O84, O85; backlog M9-06a, M9-06c): world points from the pelvis root, the hips
read from the trunk, one body per genre group, and the contact misses."""

import json

import pytest
import yaml
from conftest import ROOT

from planner import genre_profile
from solver import contact_world, forward_kinematics
from validators import prompt_validator

pytestmark = pytest.mark.unit
METRES = forward_kinematics.segments("live_action")                          # the adult (O85)
ANIME = forward_kinematics.segments("anime")
REST = {j: [0, 0, 0] for j in ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")}


def _envelope(name):
    return json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))


def test_at_rest_the_soles_stand_under_the_pelvis():
    points = forward_kinematics.points({"pos": [0, 0.98, 0], "rot": [0, 0, 0], "bones": REST}, METRES)
    assert points["left_foot"] == [0.1, 0.0, 0.0] and points["right_foot"] == [-0.1, 0.0, 0.0]   # +X: the left
    assert points["head"][1] > points["torso"][1] > points["pelvis"][1]


def test_a_bent_hip_and_knee_carry_the_foot_forward_and_up():
    seated = {**REST, "LUL": [-90, 0, 0], "LL": [90, 0, 0]}                    # hip flexion -x, knee flexion +x (O7)
    foot = forward_kinematics.points({"pos": [0, 0.98, 0], "rot": [0, 0, 0], "bones": seated}, METRES)["left_foot"]
    assert foot == [0.1, 0.45, 0.45]


def test_each_genre_profile_names_its_body():
    """ADR-O85: the genre profile card's body_type (library/genre_profiles/<genre>.yaml, schema O65) picks the segment
    card's body, with no per-key or per-performer choice; anime bodies have the leg fitted to the source, live action
    and UGC keep the 0.98 m adult."""
    genres = sorted(p.stem for p in (ROOT / "schemas" / "modality").glob("*.schema.json"))
    profiles = {g.split(".")[0]: genre_profile.body_type(g.split(".")[0]) for g in genres}
    assert profiles == {"anime": "anime", "live_action": "adult", "ugc_ad": "adult"}
    bodies = set(yaml.safe_load((ROOT / "library" / "body_segments.yaml").read_text(encoding="utf-8"))["bodies"])
    cards = {path.stem for path in (ROOT / "library" / "genre_profiles").glob("*.yaml")}
    assert set(profiles.values()) <= bodies and cards == set(profiles)
    assert forward_kinematics.standing_leg(ANIME) == 1.22 and forward_kinematics.standing_leg(METRES) == 0.98
    assert forward_kinematics.segments("ugc_ad") == METRES and ANIME["spine"] == METRES["spine"]


def test_a_lean_in_the_spine_carries_the_legs():
    """ADR-O84 (rule R-35): the hips are read from the trunk, so a lean in Sp swings the legs with it unless the hips
    flex by the same angle."""
    lean = {**REST, "Sp": [30, 0, 0]}
    swung = forward_kinematics.points({"pos": [0, 0.98, 0], "rot": [0, 0, 0], "bones": lean}, METRES)["left_foot"]
    assert swung[2] < -0.4 and swung[1] > 0.1                                  # the foot swings back and up
    planted = {**lean, "LUL": [-30, 0, 0]}
    foot = forward_kinematics.points({"pos": [0, 0.98, 0], "rot": [0, 0, 0], "bones": planted}, METRES)["left_foot"]
    assert foot == [0.1, 0.0, 0.0]                                             # the hip at -30 keeps it under the body


# The source's own grounded A rows (kernel/sources/lbn-2.3-adv.txt, support=both feet on the ground, numbers as written)
# that miss the ground under the trunk reading and the anime body, and what the repo does with each (F-079): 3.0 right
# is flipped to the row's own words by O88 (S-038), so the repo's foot meets; 4.0 is not drawn (O18); the 5.9 slide is
# listed in the reference motion plan's contact_world_exceptions (b14_c2, b14_c3; ADR-O83 point 2, S-039).
SOURCE_EXCEPTIONS = {(3.0, "right"): "RUL +90 swings the thigh back, against the row's own 'R: leg fwd mid'",
                     (4.0, "right"): "the root at y 0.9 where the same pose stands at 1.1 (3.4, 4.4); not drawn (O18)",
                     (5.9, "left"): "the slide: the body tipped 80 degrees with the legs folded under",
                     (5.9, "right"): "the slide: the body tipped 80 degrees with the legs folded under"}


def test_the_source_grounded_rows_meet_the_ground_under_the_anime_body():
    """ADR-O82, O84, O85, as a regression pin (F-079): the anime body was fitted to these very rows (S-029), so the test
    fails only when the card or the trunk reading moves; it is not independent evidence that the fit is right."""
    text = (ROOT / "kernel" / "sources" / "lbn-2.3-adv.txt").read_text(encoding="utf-8")
    grounded = (r for r in json.loads(text[text.index("{"):])["A"] if r[0] >= 3)          # 0.6 and 1.1: the pillar
    rows = [r for r in grounded if r[5].split("support=")[1].startswith("both feet;")]
    soles = {}
    for t, _, pos, rot, bones, _ in rows:
        bones = {j: [abs(v[0]), *v[1:]] if j in ("LL", "RL") else v for j, v in bones.items()}
        points = forward_kinematics.points({"pos": pos, "rot": rot, "bones": bones}, ANIME)
        soles |= {(t, side): points[f"{side}_foot"][1] for side in ("left", "right")}
    assert len(soles) == 18
    assert {k for k, y in soles.items() if abs(y) > contact_world.TOLERANCE_M} == set(SOURCE_EXCEPTIONS)


def test_repo_authored_roots_stand_at_the_pelvis():
    """ADR-O72: a repo-authored key on its feet has its lowest supporting sole on the ground (the source's A rows are
    kept as written, ADR-O81)."""
    for name in ("wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo", "reference_fight"):
        envelope = _envelope(name)
        support = {k["id"]: k["support"] for k in envelope["nodes"]["kinematic"]["items"]}
        for key in envelope["nodes"]["motion"]["items"]:
            feet = [p for p in support[key["id"]] if p.endswith("_foot")]
            if name == "reference_fight" and key["entity"] == "ninja_lean" or not feet or set(support[key["id"]]) - set(feet):
                continue
            lowest = min(key["points"][p][1] for p in feet)
            assert -0.01 <= lowest <= 0.05, (name, key["id"], lowest)
    a_rows = {k["t"]: k for k in _envelope("reference_fight")["nodes"]["motion"]["items"] if k["entity"] == "ninja_lean"}
    for t, top in ((0.6, 8.0), (7.5, 0.0), (8.0, 0.0)):                    # A's repo-authored roots (O21, O18), S-029
        assert abs(min(a_rows[t]["points"][f"{side}_foot"][1] for side in ("left", "right")) - top) <= 0.01


def test_the_kunai_pickup_meets_since_its_re_block():
    """O89 (S-039): the deflect sits at A's right foot, so O77's v_post lands the kunai at [1.4, 0, 3.77], and A crouches
    there at 8.0 (S-030 had it at [0.6, 0, 4.0], 1.33 m from A's hand before that)."""
    rows = {r["id"]: r for r in contact_world.measure(_envelope("reference_fight"))}
    pickup = rows["b19_c2"]                                     # A takes the kunai at 8.0
    assert pickup["measurable"] and pickup["distance"] <= contact_world.TOLERANCE_M and pickup["target_point"] == [1.4, 0.0, 3.77]
    assert rows["b01_c1"]["distance"] <= contact_world.TOLERANCE_M          # A lands on the pillar's top (O21)
    assert not rows["b18_c1"]["measurable"]                                   # the pillar's face has no top to meet


def test_the_prompt_prints_both_points_of_each_contact():
    """CONTACT_WORLD (plan F5.2): A's kunai pickup at 8.0 prints the hand's point and the kunai's; without the second
    point the prompt is refused."""
    envelope = _envelope("reference_fight")
    text = (ROOT / "examples" / "reference_fight" / "prose_mixed.txt").read_text(encoding="utf-8")
    assert ", kunai handle at [1.4, 0, 3.77]" in text                       # the landing since O89 (S-039)
    broken = text.replace(", kunai handle at [1.4, 0, 3.77]", "", 1)
    assert "CONTACT_WORLD" in {f["code"] for f in prompt_validator.check(broken, envelope, "mixed")}


def test_every_example_passes_contact_world():
    """ADR-O83, O89: after the re-blocks no example holds a real miss; the reference fight lists the source's slide."""
    for name in ("wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo", "reference_fight"):
        plan = json.loads((ROOT / "examples" / name / "plans" / "motion.json").read_text(encoding="utf-8"))
        assert contact_world.refusals(contact_world.measure(_envelope(name)), plan.get("contact_world_exceptions", {})) == []


def test_a_release_leaves_the_prop_where_the_hand_is():
    """RV-02b (F-075, O105): CONTACT_WORLD measures a prop's release, the prop's sample against the releasing hand; a
    foot leaving the ground is a takeoff and is not measured."""
    import copy
    envelope = _envelope("reference_fight")
    rows = {r["id"]: r for r in contact_world.measure(envelope)}
    assert rows["b05_c1"]["measurable"] and rows["b05_c1"]["distance"] <= contact_world.TOLERANCE_M   # the 2.0 throw
    assert "b11_c3" not in rows                                                      # A's foot leaves the ground at 4.7
    moved = copy.deepcopy(envelope)
    sample = next(s for b in moved["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])
                  if s["prop"] == "kunai" and s["t"] == 2.0)
    sample["p"] = [1.2, 1.5, 4.3]                                                    # where S-039 left it
    assert [(f["code"], f["contact"]) for f in contact_world.refusals(contact_world.measure(moved), {})
            if f["contact"].startswith("b05")] == [("CONTACT_WORLD", "b05_c1")]
