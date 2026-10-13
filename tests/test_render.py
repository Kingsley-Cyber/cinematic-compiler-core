"""S17: the LBN-2.x projection is complete, deterministic and generated from the graphs; frame-part checks."""

import copy
import json

import pytest
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p17_render
from compiler.passes.mandatory import p03_constraint
from validators.envelope_validator import validate_envelope
from validators.layer_dependency_validator import check_pass_writes

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["render"]
BEFORE = courtyard("camera")
PACKET = p17_render.prepare(BEFORE)
RENDER = courtyard("render")["nodes"]["render"]["items"][0]
SPEC = json.loads(RENDER["text"][RENDER["text"].index("{"):])


def test_render_is_complete_and_hash_bound():
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]
    assert all(row["items"] == row["rendered"] for row in RENDER["coverage"]["groups"].values())
    import hashlib
    assert RENDER["sha256"] == "sha256:" + hashlib.sha256(RENDER["text"].encode()).hexdigest()
    assert list(SPEC)[:8] == ["variant", "fps", "dur", "ax", "key", "lma_legend", "negative", "laban"]


def test_each_fighter_s_laban_chain_lists_its_own_moves():
    """F-091 (RV-16, owner O1): render.txt's laban chain for each fighter lists the beats it acts in, in time order, as
    the 2.4 source chains them: the acrobat's spinning kick is not the wizard's move."""
    labels = RENDER["labels"]
    beats = sorted(BEFORE["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"]))
    for entity, label in labels.items():
        if entity not in {e["id"] for e in BEFORE["nodes"]["entities"]["items"]}:
            continue
        own = [b["label"].replace("_", " ") for b in beats if b["actor"] == entity]
        assert SPEC["laban"][label].split("; ")[0] == ">".join(own)
    wizard, acrobat = SPEC["laban"][labels["wizard"]], SPEC["laban"][labels["acrobat"]]
    assert "spinning kick" in acrobat and "spinning kick" not in wizard


def test_layout_carries_every_graph():
    assert RENDER["text"].startswith(BEFORE["provenance"]["source_prompt"])
    assert RENDER["labels"] == {"wizard": "A", "acrobat": "B"}
    keys = BEFORE["nodes"]["motion"]["items"]
    between = [b for e in BEFORE["edges"]["motion"]["items"] for b in e.get("inbetweens", [])]  # ADR-O109 (RV-59e)
    assert len(SPEC["A"]) == sum(k["entity"] == "wizard" for k in keys) + sum(b["entity"] == "wizard" for b in between)
    assert len(SPEC["B"]) == sum(k["entity"] == "acrobat" for k in keys) + sum(b["entity"] == "acrobat" for b in between)
    assert sum(b["entity"] == "acrobat" for b in between) == 2
    assert {k: SPEC["A"][0][k] for k in ("t", "label", "pos", "rot")} == {
        "t": 1.6, "label": "bolt_cast_extend", "pos": [0, 1.19, 6], "rot": [0, 180, 0]}  # the anime pelvis (O72, O85, S-029)
    assert list(SPEC["A"][0]) == ["t", "label", "pos", "rot", "joints", "desc"]  # named fields (owner O9)
    assert len(SPEC["cam"]) == len(BEFORE["nodes"]["camera"]["items"])
    assert set(SPEC["set"]) == {"ground", "bamboo_wall", "stone_pillar"}
    assert "2.4 damage unknown->scorched" in SPEC["set"]["ground"]
    for beat in BEFORE["nodes"]["beats"]["items"]:
        assert beat["action"] in SPEC["rules"]


def test_kernel_controls_are_printed_or_regenerated_for_this_cast():
    scene_wide = {i["id"] for i in p03_constraint.load_kernel()["items"] if i["scope"] == "kernel"}  # S-123
    printed = [c["rule"] for c in BEFORE["nodes"]["constraints"]["items"]
               if c["source"]["ref"] in scene_wide and c["field"] != "owner"]
    assert all(rule in RENDER["text"] for rule in printed)
    for text in ("A faces -Z", "B faces +Z", "no cloned A", "no cloned B", "no extra fighters beyond A and B",
                 "slerp A joints", "B root exact", "TWO fighter identities A and B never merge or duplicate"):
        assert text in RENDER["text"]
    assert "A faces +Z" not in RENDER["text"]  # the reference cast's facing is never copied


def test_courtyard_frame_parts_pass():
    assert p17_render.check(PLAN, PACKET, BEFORE) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def codes(change, envelope=BEFORE):
    plan = copy.deepcopy(PLAN)
    change(plan["frame_parts"])
    return {f["code"] for f in p17_render.check(plan, PACKET, envelope)}


def test_a_hit_is_a_camera_hold_on_the_bodies():
    """Owner O92 (RV-09, F-083, R-21): a hold on an impact frame is a hit; the shot covering it holds still with every
    body present in frame and is no close-up, or S17 refuses it (HIT_HOLD)."""
    assert "HIT_HOLD" not in codes(lambda f: None)
    moving = copy.deepcopy(BEFORE)
    next(s for s in moving["nodes"]["camera"]["items"] if s["id"] == "c04")["movement"]["kind"] = "tracking"
    assert "HIT_HOLD" in codes(lambda f: None, moving)
    close = copy.deepcopy(BEFORE)
    next(s for s in close["nodes"]["camera"]["items"] if s["id"] == "c04")["framing"].update(scale="insert",
                                                                                         subjects=["acrobat"])
    assert "HIT_HOLD" in codes(lambda f: None, close)


def test_a_hit_from_the_contacts_is_held_whatever_s17_holds():
    """F-155 (RV-57, owner O92): the acrobat's kick lands on the wizard at 3.6, so the shot there owes a camera hold even
    when S17's frame parts drop the hold (HIT_HOLD)."""
    moving = copy.deepcopy(BEFORE)
    next(s for s in moving["nodes"]["camera"]["items"] if s["id"] == "c04")["movement"]["kind"] = "tracking"

    def unheld(frame):
        frame["holds"][:] = [h for h in frame["holds"] if abs(h["t"] - 3.6) > 1e-6]
    assert "HIT_HOLD" in codes(unheld, moving)


def test_a_hit_s_hold_is_on_a_still_rig_at_s17():
    """F-177 (RV-71a, owner O92): the shot holding the 3.6 kick is static on a locked tripod; on a shaky handheld rig it
    is no hold, and S17 refuses it (HIT_HOLD)."""
    shaky = copy.deepcopy(BEFORE)
    c04 = next(s for s in shaky["nodes"]["camera"]["items"] if s["id"] == "c04")
    c04["support"]["rig"], c04["movement_quality"]["stability"] = "handheld", "shaky"
    assert "HIT_HOLD" not in codes(lambda f: None) and "HIT_HOLD" in codes(lambda f: None, shaky)


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
    after, _ = p17_render.run(copy.deepcopy(BEFORE), PLAN, order=order)
    assert check_pass_writes(order, "render", BEFORE, after) == []
    assert after["nodes"]["render"]["projection"] is True and "render" not in after["edges"]
    assert validate_envelope(after) == {"ok": True, "complete": True, "findings": []}
    assert after["nodes"]["render"]["items"][0]["text"] == p17_render.run(copy.deepcopy(BEFORE), PLAN, order=order)[0][
        "nodes"]["render"]["items"][0]["text"]


def test_impact_contact_sync_wants_one_time_per_hit():
    """IMPACT_CONTACT_SYNC (O23, M9-02): the reference fight's hits sit on their impact frames; a strike moved off its
    frame, or an impact frame with no contact on it, is refused."""
    import json

    from conftest import ROOT

    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    impacts = envelope["nodes"]["render"]["items"][0]["frame_parts"]["impact"]
    assert p17_render.impact_sync(envelope, impacts) == []
    moved = copy.deepcopy(envelope)
    next(c for c in moved["nodes"]["contacts"]["items"] if c["id"] == "b06_c1")["t"] = 3.0  # the deflect lands late
    assert {f["message"] for f in p17_render.impact_sync(moved, impacts)} == {
        "Impact at 2.5 has no touch or support onset on that frame", "Strike b06_c1 at 3.0 lands on no impact frame"}
    assert [f["code"] for f in p17_render.impact_sync(envelope, impacts + [3.2])] == ["IMPACT_CONTACT_SYNC"]


def test_laban_actions_print_as_qualities_and_punch_as_thrust():
    """Owner O22, plan F4.2: the model reads 'punch' as a fist, so the prose prints Laban actions as qualities."""
    from conftest import ROOT
    text = (ROOT / "examples" / "reference_fight" / "prose_mixed.txt").read_text(encoding="utf-8")
    assert "(thrust quality)" in text and "(punch)" not in text and "(press quality)" in text


def test_an_entrance_from_above_says_when_the_feet_first_touch():
    """Probe V6 (owner O51, R19): A's feet touch the pillar top at 0.60, not earlier, and A does not stand on it at 0."""
    from conftest import ROOT

    from validators import prompt_validator
    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    assert "A's feet touch the wooden pillar top at 0.60, not earlier." in text
    broken = text.replace(", and A's feet touch the wooden pillar top at 0.60, not earlier.", ".")
    assert "ENTRANCE_UNSTATED" in {f["code"] for f in prompt_validator.check(broken, envelope, "mixed")}

