"""S16: the LBN-2.x projection is complete, deterministic and generated from the graphs; frame-part checks."""

import copy
import json

import pytest
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p16_render
from validators.envelope_validator import validate_envelope
from validators.layer_dependency_validator import check_pass_writes

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["render"]
BEFORE = courtyard("camera")
PACKET = p16_render.prepare(BEFORE)
RENDER = courtyard("render")["nodes"]["render"]["items"][0]
SPEC = json.loads(RENDER["text"][RENDER["text"].index("{"):])


def test_render_is_complete_and_hash_bound():
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]
    assert all(row["items"] == row["rendered"] for row in RENDER["coverage"]["groups"].values())
    import hashlib
    assert RENDER["sha256"] == "sha256:" + hashlib.sha256(RENDER["text"].encode()).hexdigest()
    assert list(SPEC)[:8] == ["variant", "fps", "dur", "ax", "key", "lma_legend", "negative", "laban"]


def test_layout_carries_every_graph():
    assert RENDER["text"].startswith(BEFORE["provenance"]["source_prompt"])
    assert RENDER["labels"] == {"wizard": "A", "acrobat": "B"}
    keys = BEFORE["nodes"]["motion"]["items"]
    assert len(SPEC["A"]) == sum(k["entity"] == "wizard" for k in keys)
    assert len(SPEC["B"]) == sum(k["entity"] == "acrobat" for k in keys)
    assert SPEC["A"][0][:4] == [1.6, "bolt_cast_extend", [0, 0, 6], [0, 180, 0]]
    assert len(SPEC["cam"]) == len(BEFORE["nodes"]["camera"]["items"])
    assert set(SPEC["set"]) == {"ground", "bamboo_wall", "stone_pillar"}
    assert "2.4 damage unknown->scorched" in SPEC["set"]["ground"]
    for beat in BEFORE["nodes"]["beats"]["items"]:
        assert beat["action"] in SPEC["rules"]


def test_kernel_controls_are_printed_or_regenerated_for_this_cast():
    printed = [c["rule"] for c in BEFORE["nodes"]["constraints"]["items"] if c["scope"] == "kernel" and c["field"] != "owner"]
    assert all(rule in RENDER["text"] for rule in printed)
    for text in ("A faces -Z", "B faces +Z", "no cloned A", "no cloned B", "no extra fighters beyond A and B",
                 "slerp A joints", "B root exact", "TWO fighter identities A and B never merge or duplicate"):
        assert text in RENDER["text"]
    assert "A faces +Z" not in RENDER["text"]  # the reference cast's facing is never copied


def test_courtyard_frame_parts_pass():
    assert p16_render.check(PLAN, PACKET, BEFORE) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def codes(change, envelope=BEFORE):
    plan = copy.deepcopy(PLAN)
    change(plan["frame_parts"])
    return {f["code"] for f in p16_render.check(plan, PACKET, envelope)}


@pytest.mark.parametrize("code, change", [
    ("FRAME_IMPACT", lambda f: f["impact"].append(1.0)),
    ("FRAME_SMEAR", lambda f: f["smear"][0].update(part=None)),
    ("FRAME_SMEAR", lambda f: f["smear"].append({"t0": 5.2, "t1": 6.4, "subject": "wizard", "part": "left_arm", "note": "x"})),
    ("FRAME_SPEEDLINES", lambda f: f["speedlines"].append({"t0": 1, "t1": 2, "subject": "dragon"})),
    ("FRAME_HOLD", lambda f: f["holds"].append({"t": 1.0, "frames": 2})),
    ("FRAME_FX", lambda f: f["fx"].append({"t": 11, "t_end": None, "text": "x"})),
])
def test_each_frame_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_a_dropped_item_fails_coverage():
    envelope = copy.deepcopy(BEFORE)
    ghost = copy.deepcopy(envelope["nodes"]["efforts"]["items"][0])
    envelope["nodes"]["efforts"]["items"].append({**ghost, "id": "ghost@b01", "actor": "ghost"})
    assert "RENDER_COVERAGE" in codes(lambda f: None, envelope)


@pytest.mark.integration
def test_render_scope_and_complete_envelope(order):
    after, _ = p16_render.run(copy.deepcopy(BEFORE), PLAN, order=order)
    assert check_pass_writes(order, "render", BEFORE, after) == []
    assert after["nodes"]["render"]["projection"] is True and "render" not in after["edges"]
    assert validate_envelope(after) == {"ok": True, "complete": True, "findings": []}
    assert after["nodes"]["render"]["items"][0]["text"] == p16_render.run(copy.deepcopy(BEFORE), PLAN, order=order)[0][
        "nodes"]["render"]["items"][0]["text"]
