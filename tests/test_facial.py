"""S14 facial: FACS units, structured asymmetry, valence/arousal, face-body agreement, gaze, onsets; words only."""

import copy
import json
import re

import pytest
from conftest import ROOT
from ugc_scene import glasses, ugc_plans

from compiler.passes.derived import p14_facial
from kernel.canonical import canonical_json
from planner.card_loader import load_cards
from planner.dependency_graph import load
from planner.topological_sort import build_order
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = ugc_plans()["facial"]
BEFORE = glasses("motion")
PACKET = p14_facial.prepare(BEFORE)
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "facial_graph.schema.json").read_text())


def face(plan, beat):
    return next(f for f in plan["faces"] if f["slot"] == f"ugc_creator@{beat}")


def unit(plan, beat, au):
    return next(u for u in face(plan, beat)["aus"] if u["au"] == au)


def codes(change, packet=PACKET):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p14_facial.check(plan, packet)}


def test_glasses_faces_pass_and_libraries_are_complete():
    assert p14_facial.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]
    assert all("face_profile" in c for c in load_cards().values() if c["kind"] == "archetype")
    assert {"AU6", "AU12", "AU14", "AU46"} <= set(PACKET["units"]) and PACKET["units"]["AU46"]["laterality"] == "unilateral_only"


def test_the_face_runs_only_for_live_action_and_ugc():
    order = load()
    for genre, present in (("anime", False), ("live_action", True), ("ugc_ad", True)):
        sequence = build_order(order, genre)
        assert ("facial" in sequence) == present
        if present:
            assert sequence.index("motion") < sequence.index("facial") < sequence.index("effort") < sequence.index("camera")


@pytest.mark.parametrize("code, change", [
    ("FACIAL_COVERAGE", lambda p: p["faces"].pop()),
    ("FACS_AU", lambda p: face(p, "b01")["aus"].append({"au": "AU3", "intensity": "A", "bilateral": True})),
    ("FACS_AU", lambda p: face(p, "b01")["aus"].append({"au": "AU46", "intensity": "B", "bilateral": True})),
    ("FACS_AU", lambda p: unit(p, "b04", "AU12").update(right_intensity="C", asymmetry={"dominant_side": "left",
                                                                                         "magnitude": 1, "pattern": None})),
    ("FACS_ASYMMETRY", lambda p: unit(p, "b04", "AU12")["asymmetry"].update(dominant_side="right")),
    ("FACS_ASYMMETRY", lambda p: unit(p, "b04", "AU12").update(left_intensity="E", right_intensity="A",
                                                               asymmetry={"dominant_side": "left", "magnitude": 4,
                                                                          "pattern": None})),
    ("FACS_ASYMMETRY", lambda p: face(p, "b04")["aus"].__setitem__(2, {
        "au": "AU25", "left_intensity": "B", "right_intensity": "A", "bilateral": False,
        "asymmetry": {"dominant_side": "left", "magnitude": 1, "pattern": None}})),
    ("FACS_PATTERN", lambda p: unit(p, "b04", "AU12")["asymmetry"].update(pattern="contempt")),
    ("FACS_PATTERN", lambda p: unit(p, "b04", "AU12")["asymmetry"].update(pattern="sneer")),
    ("FACS_CONTRADICTION", lambda p: face(p, "b01")["inactive_aus"].append("AU12")),
    ("VALENCE_RANGE", lambda p: face(p, "b04").update(valence=-0.5)),
    ("VALENCE_RANGE", lambda p: face(p, "b02").update(emotion_label="contemptuous", valence=-0.3, arousal=0.0)),
    ("FACIAL_KINEMATIC", lambda p: face(p, "b04").update(arousal=0.7)),
    ("FACIAL_GAZE", lambda p: face(p, "b01").update(gaze_target="ugc_creator")),
    ("FACIAL_TRANSITION", lambda p: face(p, "b02").update(onset="slow")),
    ("FACIAL_TRANSITION", lambda p: face(p, "b03").update(onset="hold", onset_frames=0)),
    ("FACIAL_TRANSITION", lambda p: face(p, "b02").update(onset="micro", onset_frames=6)),
    ("FACIAL_WORDS", lambda p: face(p, "b04").update(description="AU12 on the left")),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_a_masked_face_may_leave_the_body_behind_and_leak_a_micro_expression():
    def masked(plan):
        face(plan, "b02").update(display_rule="suppressed", arousal=0.9, onset="micro", onset_frames=6)
    assert codes(masked) == set()


def test_costume_hides_lower_face_units():
    packet = copy.deepcopy(PACKET)
    packet["entities"]["ugc_creator"]["face_profile"]["visible_regions"] = ["brows", "eyes"]
    assert "FACS_OCCLUSION" in codes(lambda p: None, packet)
    packet["entities"]["ugc_creator"]["face_profile"] = None
    assert "FACE_PROFILE_MISSING" in codes(lambda p: None, packet)


def test_contempt_pattern_needs_one_sided_12_and_14_on_the_same_side():
    def contempt(plan):
        f = face(plan, "b02")
        f.update(emotion_label="contemptuous", valence=-0.4, arousal=0.0, inactive_aus=[], aus=[
            {"au": "AU12", "left_intensity": "B", "right_intensity": None, "bilateral": False,
             "asymmetry": {"dominant_side": "left", "magnitude": 2, "pattern": "contempt"}},
            {"au": "AU14", "left_intensity": None, "right_intensity": "B", "bilateral": False,
             "asymmetry": {"dominant_side": "right", "magnitude": 2, "pattern": "contempt"}}])
    packet = copy.deepcopy(PACKET)
    packet["entities"]["ugc_creator"]["face_profile"]["emotional_range"].append("contempt")
    found = codes(contempt, packet)
    assert found == {"FACS_PATTERN"}  # the two units sit on opposite sides


@pytest.mark.integration
def test_graph_words_scope_and_determinism(order):
    after, _ = p14_facial.run(copy.deepcopy(BEFORE), PLAN, order=order)
    assert check_pass_writes(order, "facial", BEFORE, after) == []
    nodes, edges = after["nodes"]["facial"]["items"], after["edges"]["facial_transition"]["items"]
    validate_schema({"facial": nodes, "facial_transition": edges}, GRAPH)
    reveal = nodes[-1]["words"]
    assert reveal["face"][1] == "lip corners pulled up (marked on their left, slight on their right)"
    assert reveal["feeling"] == "delighted, strongly pleasant and activated"
    assert [e["trigger"] for e in edges] == ["b01__causes__b02", "b02__causes__b03", "b03__causes__b04"]
    assert canonical_json(after) == canonical_json(p14_facial.run(copy.deepcopy(BEFORE), PLAN, order=order)[0])


def test_the_render_describes_faces_in_words_only():
    text = (ROOT / "examples" / "ugc_glasses_demo" / "render.txt").read_text()
    assert "FACE (carries the beat): cheeks raised" in text and "no smile" in text
    assert not re.search(r"\bAU\s?\d", text) and "valence" not in text


CAMERA_PLAN = ugc_plans()["camera"]


def camera_codes(change):
    from compiler.passes.derived import p16_camera
    packet = p16_camera.prepare(glasses("effort"))
    plan = copy.deepcopy(CAMERA_PLAN)
    change(next(s for s in plan["shots"] if s["id"] == "c04"))
    return {f["code"] for f in p16_camera.check(plan, packet)}


@pytest.mark.parametrize("code, change", [
    ("FACE_FRAMING", lambda s: s["angle"].update(azimuth_deg=180)),           # camera behind the creator
    ("FACE_ASYMMETRY_VISIBLE", lambda s: s["angle"].update(azimuth_deg=-60)),  # sees only the weaker (right) side
    (None, lambda s: s["angle"].update(azimuth_deg=15)),                      # frontal: both sides
    (None, lambda s: s["angle"].update(azimuth_deg=60)),                      # the stronger (left) side faces the lens
])
def test_the_camera_shows_the_face_that_carries_the_beat(code, change):
    found = camera_codes(change) & {"FACE_FRAMING", "FACE_ASYMMETRY_VISIBLE"}
    assert found == ({code} if code else set())


def test_anime_camera_packets_carry_no_faces():
    from scenes import courtyard

    from compiler.passes.derived import p16_camera
    assert "faces" not in p16_camera.prepare(courtyard("effort"))
