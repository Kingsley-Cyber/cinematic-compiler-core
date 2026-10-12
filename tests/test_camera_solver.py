"""S16: camera geometry, the shot-list checks (one violation per rule family), derived edges, scope."""

import copy
import json

import pytest
import yaml
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p16_camera
from kernel.canonical import canonical_json
from solver import camera_geometry as geometry
from validators import camera_validator
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["camera"]
PACKET = p16_camera.prepare(courtyard("effort"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "camera_graph.schema.json").read_text())


def test_geometry_follows_the_kernel_frame():
    aim = [0.0, 1.0, 3.0]
    camera = geometry.camera_position(aim, 2, 0, 90)          # azimuth 90 = +X (performer's left facing +Z)
    assert geometry.rounded(camera) == [2.0, 1.0, 3.0]
    assert geometry.side(camera, [0, 0, 0], [0, 0, 6], 0.3) == "left"
    assert geometry.side([-2, 1, 3], [0, 0, 0], [0, 0, 6], 0.3) == "right"
    assert geometry.side([0.1, 1, -4], [0, 0, 0], [0, 0, 6], 0.3) == "on_axis"
    assert geometry.screen_x(camera, aim, [0, 1, 2], 50, [36, 24]) > 0   # toward -Z is screen right from +X
    assert geometry.frame_height(2, 48, [36, 24]) == 1.0 and geometry.azimuth_change(350, 10) == 20
    # F-090 (RV-15a): up as well as across; 0.25 m above the aim at 2 m is half way to the top of a 1 m frame
    assert geometry.screen_xy(camera, aim, [0, 1.25, 3], 48, [36, 24]) == (0.0, 0.5)
    assert geometry.screen_xy(camera, aim, [3, 1, 3], 48, [36, 24]) is None   # behind the camera


def test_plan_schema_embeds_the_camera_node_schema():
    plan = json.loads((ROOT / "schemas" / "graphs" / "camera_plan.schema.json").read_text())
    node = json.loads((ROOT / "schemas" / "camera.schema.json").read_text())
    assert plan["$defs"]["shot"] == {k: v for k, v in node.items() if k not in ("$schema", "$id")}
    assert len([k for k in node["required"] if k not in ("id", "t", "dur", "beats", "intent", "motivation")]) == 13


def test_courtyard_shot_list_passes():
    assert p16_camera.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def shot(plan, sid):
    return next(s for s in plan["shots"] if s["id"] == sid)


def codes(change, packet=PACKET):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p16_camera.check(plan, packet)}


def unframe_acrobat(plan):
    s = shot(plan, "c05")
    s["framing"]["subjects"], s["composition"]["placement"] = ["wizard"], {"wizard": "left_third"}
    s["focus"]["target"], s["relation_to_action"]["subject"], s["blur"]["affected"] = "wizard", "wizard", ["wizard"]


@pytest.mark.parametrize("code, change", [
    ("CAMERA_TILING", lambda p: shot(p, "c02").update(t=1.3)),
    ("CAMERA_TILING", lambda p: shot(p, "c01")["editing"].update(transition_in="cut")),
    ("CAMERA_COVERAGE", lambda p: shot(p, "c03").update(beats=["b04"])),
    ("CAMERA_VOCABULARY", lambda p: shot(p, "c01")["framing"].update(scale="cowboy")),
    ("CAMERA_MOTIVATION", lambda p: shot(p, "c04")["motivation"].update(ref="b02_c1")),
    ("CAMERA_MOTIVATION", lambda p: shot(p, "c01")["motivation"].update(ref="anime_lens_flare")),
    ("CAMERA_AXIS", lambda p: shot(p, "c05")["position"].update(side="right")),
    ("CAMERA_AXIS", lambda p: shot(p, "c08")["angle"].update(azimuth_deg=242.3)
     or shot(p, "c08")["position"].update(side="right")),
    ("CAMERA_COUPLING", lambda p: shot(p, "c03")["framing"].update(scale="medium")),
    ("CAMERA_COUPLING", unframe_acrobat),
    ("CAMERA_COUPLING", lambda p: shot(p, "c02")["lens"].update(focal_length_mm=50)),
    ("CAMERA_COMPOSITION", lambda p: shot(p, "c01")["composition"].update(placement={"wizard": "right_third",
                                                                                      "acrobat": "left_third"})),
    ("CAMERA_CONTINUITY", lambda p: shot(p, "c02").update(beats=["b02"]) or shot(p, "c02")["framing"].update(scale="wide")
     or shot(p, "c02")["angle"].update(azimuth_deg=100)),
    ("CAMERA_GENRE", lambda p: shot(p, "c05")["angle"].update(roll_deg=45)),
    ("CAMERA_COHERENCE", lambda p: shot(p, "c01")["movement"].update(kind="dolly_in")),
    ("CAMERA_COHERENCE", lambda p: shot(p, "c04")["playback"].update(treatment="slow", speed=1)),
    # owner O92 (RV-09): an impact shot frames the bodies (medium to full), no close-up, no slowed playback
    ("CAMERA_INTENT", lambda p: shot(p, "c04")["blur"].update(motion_blur="none", affected=[])),
    ("PLAYBACK_RAMP", lambda p: shot(p, "c06")["playback"].update(treatment="ramp", speed=0.3)),
    ("CAMERA_INTENT", lambda p: shot(p, "c07")["focus"].update(depth_of_field="deep")),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_no_camera_card_slows_playback_or_puts_a_close_up_on_a_hit():
    """F-160, F-177 (RV-60, RV-71b; owner O92): every camera convention card plays at normal speed only, and each rule's
    structured asks stay in the grammar and hold a hit still on every body present at an impact scale; the struck rules,
    written as fields, and a card carrying one are refused (CAMERA_CARD). The test moved from the rules' words to
    their fields with the check it pins (ADR-O102)."""
    from kernel.canonical import ContractError
    from planner import camera_library
    for path in sorted((ROOT / "library" / "camera_conventions").glob("*.yaml")):
        card = yaml.safe_load(path.read_text())
        assert card["playback"] == ["normal"], path.name
        assert [p for c in card["conventions"] for p in camera_library.rule_problems(c, card["playback"])] == [], path.name
    for path in sorted((ROOT / "library" / "camera_idioms").glob("*.yaml")):
        assert [p for i in yaml.safe_load(path.read_text())["idioms"] for p in camera_library.rule_problems(i)] == [], path.name
    struck = [{"id": "reaction_close", "trigger": "hit", "asks": {"scale": ["close"], "subjects": "actor"}},
              {"id": "blade_insert", "trigger": "hit", "asks": {"scale": ["insert"], "subjects": "detail"}},
              {"id": "shield_arm", "trigger": "hit", "asks": {"scale": ["medium"], "movement": ["static"], "subjects": "detail"}},
              {"id": "slow_peak", "trigger": "fast_move", "asks": {"playback": ["slow"]}}]
    assert all(camera_library.rule_problems(rule) for rule in struck)
    card = {"card_id": "probe", "conventions": struck}
    with pytest.raises(ContractError) as refused:
        camera_library._checked(card, "conventions", ["normal"])
    assert refused.value.code == "CAMERA_CARD"


def test_a_card_rule_s_words_ask_only_what_its_fields_ask():
    """F-187 (RV-85, owner O92): the words a rule prints are read in the grammar's camera terms and their common
    synonyms, and each must be one its fields allow, so a struck rule cannot pass under a compliant or empty label."""
    from planner import camera_library
    said = {"Go tight on the face.": "close", "An ECU of the eyes.": "extreme_close", "A detail shot of the blade.": "insert",
            "Crash zoom in.": "zoom", "Play it slow-mo.": "slow", "Run it at half speed.": "slow", "Bullet time.": "slow",
            "Overcrank the fall.": "slow", "Speed up the run.": "fast", "Fast motion through the crowd.": "fast",
            "A slow push in.": "dolly_in", "Hold on both.": "static", "A whip pan.": "whip_pan"}
    assert {words: sorted(v for _, v in camera_library.terms(words)) for words in said} == {
        words: [value] for words, value in said.items()}
    struck = [{"id": "a", "statement": "Cut close on the receiver after a blow lands.", "trigger": "hit",
               "asks": {"scale": ["medium"], "movement": ["static"], "subjects": "all_present"}},
              {"id": "b", "statement": "Slow motion around the peak of every move.", "trigger": "fast_move", "asks": {}},
              {"id": "c", "statement": "Crash zoom to an ECU of the face.", "trigger": "fast_move", "asks": {}}]
    assert [any("its words ask for" in p for p in camera_library.rule_problems(rule)) for rule in struck] == [True] * 3


def test_a_rule_that_speaks_of_a_hit_is_a_hit_rule():
    """F-187 (RV-85, owner O92): a rule whose words name a blow, hit, impact or strike carries the hit trigger, so O92's
    hold applies to it whatever its label; "between hits" does not name one."""
    from planner import camera_library
    heavy = {"id": "knight_weight_low", "when": "a heavy blow or charge", "prefer": "Low, steady frame.",
             "trigger": "heavy_move", "asks": {}}
    assert camera_library.rule_problems(heavy) == ["knight_weight_low: its words speak of a hit, so its trigger is hit"]
    between = {"id": "follow", "statement": "A fast body move between hits is followed by a tracking or whip move.",
               "trigger": "fast_move", "asks": {"movement": ["tracking", "whip_pan"]}}
    assert camera_library.rule_problems(between) == []


def test_a_hit_from_the_contacts_is_a_camera_hold_at_s16():
    """F-155 (RV-57, owner O92): S16 sees the contacts, so the shot covering each hit holds still on every body present:
    the acrobat's kick lands on the wizard at 3.6 (HIT_HOLD)."""
    assert [(h["t"], h["bodies"]) for h in PACKET["hits"]] == [(3.6, ["acrobat", "wizard"])]
    assert "HIT_HOLD" not in codes(lambda p: None)
    assert "HIT_HOLD" in codes(lambda p: shot(p, "c04")["movement"].update(kind="tracking"))
    assert "HIT_HOLD" in codes(lambda p: shot(p, "c04")["framing"].update(subjects=["acrobat"]))


def test_a_hit_s_hold_is_on_a_still_rig_and_idioms_reach_their_archetypes():
    """F-177 (RV-71a, owner O92): a static shot on a shaky or floating rig is no hold (HIT_HOLD at S16); the ninja
    idioms reach the fight's ninja_lean and ninja_broad through their cards' camera_idioms."""
    assert "HIT_HOLD" not in codes(lambda p: None)
    assert "HIT_HOLD" in codes(lambda p: (shot(p, "c04")["support"].update(rig="handheld"),
                                          shot(p, "c04")["movement_quality"].update(stability="shaky")))
    assert "HIT_HOLD" in codes(lambda p: (shot(p, "c04")["support"].update(rig="gimbal"),
                                          shot(p, "c04")["movement_quality"].update(stability="floating")))
    from planner import camera_library
    found = camera_library.idioms(["ninja_broad", "ninja_lean"])
    assert sorted(found) == ["ninja_broad", "ninja_lean"] and found["ninja_lean"] == found["ninja_broad"] != []


def test_the_camera_aims_at_the_middle_of_the_body_it_frames():
    """F-090 (RV-15a, owner O72): a shot aims at the middle of the extent of the parts its scale shows of its target, at
    its first beat's keys (both axis performers for `midpoint`), never aim_height_m above the pelvis; a close-up aims
    at the head."""
    points, grammar = PACKET["points"], PACKET["grammar"]
    assert camera_validator.derive(shot(PLAN, "c07"), PACKET)["aim"] == points["b09"]["wizard"]["head"]  # the close-up
    body = [points["b06"][e][part] for e in ("acrobat", "wizard") for part in grammar["visible_parts"]["full"]]
    middle = [(min(p[i] for p in body) + max(p[i] for p in body)) / 2 for i in range(3)]
    assert camera_validator.derive(shot(PLAN, "c04"), PACKET)["aim"] == geometry.rounded(middle)
    pelvis = PACKET["positions"]["b06"]["wizard"]
    assert middle[1] < pelvis[1] + grammar["aim_height_m"] - 0.5  # the old aim sat over the heads


def test_every_part_a_shot_shows_is_in_frame_up_and_down():
    """F-090 (RV-15a): every part a shot's scale shows of each subject projects inside the frame, up and down as well
    as across (VERTICAL_FRAMING), at every beat a static shot lists. c06 as authored before S-076 (eye level at 4.4 m)
    loses the airborne acrobat's head above the frame; a head raised at c11's last beat is out of the static wide."""
    assert "VERTICAL_FRAMING" not in codes(lambda p: None)
    assert "VERTICAL_FRAMING" in codes(lambda p: (shot(p, "c06")["angle"].update(elevation_deg=0),
                                                  shot(p, "c06")["position"].update(distance_m=4.4)))
    packet = copy.deepcopy(PACKET)
    body = packet["points"]["b14"]["acrobat"]
    packet["points"]["b14"]["acrobat"] = {**body, "head": [body["head"][0], body["head"][1] + 6, body["head"][2]]}
    found = [f for f in p16_camera.check(PLAN, packet) if f["code"] == "VERTICAL_FRAMING"]
    assert [(f["slot"], f["message"].split(" is ")[0]) for f in found] == [("c11", "At b14, acrobat's head")]


def test_an_insert_aims_at_its_detail():
    """F-090 (RV-15b): an insert aims at its detail, a part of its target (forward kinematics' contact points) or a prop,
    no longer aim_height_m above the target's pelvis; a detail that names neither is refused (CAMERA_VOCABULARY)."""
    plan = copy.deepcopy(PLAN)
    insert = shot(plan, "c07")  # the wizard's close-up at b09, made an insert on the right hand
    insert["framing"].update(scale="insert", detail="right_hand")
    insert["position"]["distance_m"] = 0.9  # 85 mm: a 0.25 m frame
    assert camera_validator.derive(insert, PACKET)["aim"] == PACKET["points"]["b09"]["wizard"]["right_hand"]
    assert "CAMERA_VOCABULARY" not in codes(lambda p: (shot(p, "c07")["framing"].update(scale="insert",
                                                                                        detail="right_hand"),
                                                      shot(p, "c07")["position"].update(distance_m=0.9)))
    assert "CAMERA_VOCABULARY" in codes(lambda p: (shot(p, "c07")["framing"].update(scale="insert", detail="aura"),
                                                   shot(p, "c07")["position"].update(distance_m=0.9)))


def test_a_framed_prop_is_in_frame():
    """F-090 (RV-15b): a prop a shot frames is held in frame where the packet places it (its sample, the hand that
    holds it, its flight or its rest), as a body's parts are (VERTICAL_FRAMING)."""
    packet = copy.deepcopy(PACKET)
    packet["props"] = sorted(packet["props"] + ["orb"])
    near = packet["points"]["b06"]["wizard"]["right_hand"]
    packet["prop_points"]["b06"]["orb"] = near

    def framed(plan):
        shot(plan, "c04")["framing"]["subjects"].append("orb")

    assert "VERTICAL_FRAMING" not in codes(framed, packet)
    packet["prop_points"]["b06"]["orb"] = [near[0], near[1] + 4, near[2]]
    assert "VERTICAL_FRAMING" in codes(framed, packet)


def test_genre_card_rules_apply_scene_wide():
    packet = copy.deepcopy(PACKET)
    packet["convention"]["required_intents"] = ["product"]
    assert "CAMERA_GENRE" in codes(lambda p: None, packet)
    packet = copy.deepcopy(PACKET)
    packet["convention"]["cross_line"] = "forbidden"
    crossing = codes(lambda p: shot(p, "c08")["angle"].update(azimuth_deg=242.3)
                     or shot(p, "c08")["position"].update(side="right") or shot(p, "c08")["editing"].update(axis="cross")
                     or shot(p, "c09")["editing"].update(axis="cross"), packet)
    assert "CAMERA_GENRE" in crossing


@pytest.mark.integration
def test_derived_geometry_edges_scope_and_determinism(order):
    before = courtyard("effort")
    snapshot = copy.deepcopy(before)
    after, _ = p16_camera.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "camera", before, after) == []
    nodes, edges = after["nodes"]["camera"]["items"], after["edges"]["camera"]["items"]
    validate_schema({"camera": nodes, "camera_edges": edges}, GRAPH)
    assert [n["id"] for n in nodes] == [f"c{i:02d}" for i in range(1, 12)] and len(edges) == len(nodes) - 1
    assert all(n["derived"]["side"] == n["position"]["side"] for n in nodes)
    assert {e["side_to"] for e in edges} == {"left"}  # the kick's on-axis insert became a hold on both bodies (O92)
    assert camera_validator.derive(nodes[0], p16_camera.prepare(before)) == nodes[0]["derived"]
    assert courtyard("camera")["validation"]["camera_kinematic_coupling"] == "pass"
    assert canonical_json(after) == canonical_json(p16_camera.run(courtyard("effort"), PLAN, order=order)[0])
