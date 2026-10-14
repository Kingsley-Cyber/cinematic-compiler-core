"""S-130: a part meets a surface with its skin, not its bone's axis (as body to body, RV-49), and the re-block solver
repairs a claimed support off its surface and a contact at its beat's end on the key at that instant."""

import copy
import json

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.author import repair_motion
from compiler.passes.derived import p13_motion
from solver import contact_world, forward_kinematics

pytestmark = pytest.mark.unit
EXAMPLE = ROOT / "examples" / "wizard_vs_acrobat"


def test_a_back_on_the_floor_meets_it_with_its_skin_a_sole_with_its_underside():
    radii = forward_kinematics.radii("anime")
    lying = contact_world.surface_miss([0, 0.2, 0], "torso", radii, top=0.0)  # the spine 0.2 m up, the trunk 0.13 thick
    assert lying == (0.07, [0, 0.0, 0])
    assert contact_world.surface_miss([0, 0.02, 0], "left_foot", radii, top=0.0)[0] == 0.02
    pillar = [{"min": [1, 0, -1], "max": [2, 3, 1]}]
    assert contact_world.surface_miss([0.86, 1.2, 0], "left_arm", radii, boxes=pillar)[0] == 0.09  # the elbow 0.14 off
    assert contact_world.surface_miss([1.1, 1.2, 0], "left_arm", radii, boxes=pillar)[0] == 0.15  # pressed in 0.1


def _before():
    plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (EXAMPLE / "plans").glob("*.json")}
    request = json.loads((EXAMPLE / "request.json").read_text(encoding="utf-8"))
    before = pipeline.run(request["query"], genre=request.get("genre"), duration_s=request.get("duration_s"),
                          until="bartenieff", plans=plans)
    return plans["motion"], before


def test_a_support_foot_lifted_off_the_floor_is_put_back_by_the_solver():
    document, before = _before()
    support = {k["id"]: k["support"] for k in before["nodes"]["kinematic"]["items"]}
    lifted = copy.deepcopy(document)
    key = next(k for k in lifted["keys"] if support.get(k["slot"]) == ["left_foot", "right_foot"])
    key["bones"]["RUL"] = [key["bones"]["RUL"][0] - 25, *key["bones"]["RUL"][1:]]  # the right foot 0.2 m up
    packet = p13_motion.prepare(before)
    found = p13_motion.check(lifted, packet)
    assert [f["contact"] for f in found if f["code"] == "CONTACT_WORLD"] == [f"{key['slot']}:right_foot"]
    assert p13_motion.check(repair_motion(lifted, found, before), packet) == []


def test_a_contact_at_its_beat_s_end_is_repaired_on_the_key_at_that_instant():
    document, before = _before()
    packet = p13_motion.prepare(before)
    times = {s["slot"]: (s["entity"], s["t"]) for s in packet["slots"]}
    beats = {b["id"]: b for b in before["nodes"]["beats"]["items"]}
    contact = next(c for c in before["nodes"]["contacts"]["items"] if c["b"]["kind"] == "entity"
                   and abs(c["t"] - beats[c["beat"]]["t"]) > 1e-6
                   and any(v == (c["a"]["id"], c["t"]) for v in times.values()))
    slot = next(s for s, v in times.items() if v == (contact["a"]["id"], contact["t"]))
    moved = copy.deepcopy(document)
    key = next(k for k in moved["keys"] if k["slot"] == slot)
    for joint in ("LA", "RA", "LUL", "RUL"):  # the striking limb swung off its target
        key["bones"][joint] = [key["bones"][joint][0] + 40, *key["bones"][joint][1:]]
    found = p13_motion.check(moved, packet)
    assert contact["id"] in {f.get("contact") for f in found}
    repaired = p13_motion.check(repair_motion(moved, found, before), packet)
    assert contact["id"] not in {f.get("contact") for f in repaired}
