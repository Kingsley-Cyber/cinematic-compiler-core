"""S15: camera geometry, the shot-list checks (one violation per rule family), derived edges, scope."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p15_camera
from kernel.canonical import canonical_json
from solver import camera_geometry as geometry
from validators import camera_validator
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["camera"]
PACKET = p15_camera.prepare(courtyard("effort"))
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


def test_plan_schema_embeds_the_camera_node_schema():
    plan = json.loads((ROOT / "schemas" / "graphs" / "camera_plan.schema.json").read_text())
    node = json.loads((ROOT / "schemas" / "camera.schema.json").read_text())
    assert plan["$defs"]["shot"] == {k: v for k, v in node.items() if k not in ("$schema", "$id")}
    assert len([k for k in node["required"] if k not in ("id", "t", "dur", "beats", "intent", "motivation")]) == 13


def test_courtyard_shot_list_passes():
    assert p15_camera.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def shot(plan, sid):
    return next(s for s in plan["shots"] if s["id"] == sid)


def codes(change, packet=PACKET):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p15_camera.check(plan, packet)}


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
    ("CAMERA_COHERENCE", lambda p: shot(p, "c04")["playback"].update(speed=1)),
    ("CAMERA_INTENT", lambda p: shot(p, "c04")["playback"].update(treatment="normal", speed=1)),
    ("CAMERA_INTENT", lambda p: shot(p, "c07")["focus"].update(depth_of_field="deep")),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


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
    after, _ = p15_camera.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "camera", before, after) == []
    nodes, edges = after["nodes"]["camera"]["items"], after["edges"]["camera"]["items"]
    validate_schema({"camera": nodes, "camera_edges": edges}, GRAPH)
    assert [n["id"] for n in nodes] == [f"c{i:02d}" for i in range(1, 12)] and len(edges) == len(nodes) - 1
    assert all(n["derived"]["side"] == n["position"]["side"] for n in nodes)
    assert {e["side_to"] for e in edges} == {"left", "on_axis"}
    assert camera_validator.derive(nodes[0], p15_camera.prepare(before)) == nodes[0]["derived"]
    assert courtyard("camera")["validation"]["camera_kinematic_coupling"] == "pass"
    assert canonical_json(after) == canonical_json(p15_camera.run(courtyard("effort"), PLAN, order=order)[0])
