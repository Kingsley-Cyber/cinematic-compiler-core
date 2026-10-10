"""M5.5 clip chaining: damage, props, contacts and the camera axis carry across the cut; bad chains are refused."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler import pipeline
from compiler.passes.derived import p15_camera
from kernel.canonical import ContractError, content_hash
from planner.beat_planner import prepare

pytestmark = pytest.mark.integration
COURTYARD = json.loads((ROOT / "examples" / "wizard_vs_acrobat" / "envelope.json").read_text(encoding="utf-8"))
REFERENCE = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
COURTYARD_2 = "4 seconds anime fight scene: wizard versus acrobat in a moonlit bamboo courtyard"
REFERENCE_2 = json.loads((ROOT / "examples" / "reference_fight" / "request.json").read_text())["query"].replace("10s", "4s", 1)


def fact(kind, sid, prop, value):
    return {"subject": {"kind": kind, "id": sid}, "property": prop, "value": value}


def plan_for(query, previous, beats):
    envelope = pipeline.run(query, until="constraint", previous=previous)
    return {"step_id": "S04", "band": "L1", "packet_sha256": prepare(envelope)["packet_sha256"],
            "author": {"host": "test fixture", "model": "none"}, "attempt": 1, "beats": beats}


def beat(bid, t, dur, actor, others, action, *, requires=(), effects=(), contacts=(), causes=(), event_type="action"):
    bodies = [actor, *others]
    return {"id": bid, "t": t, "dur": dur, "event_type": event_type, "actor": actor, "label": bid + "_beat",
            "participants": [{"kind": "entity", "id": o} for o in others], "modes": {},
            "pos": {b: [0, 0, i * 2.0] for i, b in enumerate(bodies)}, "facing": {b: [0, 0, 1] for b in bodies},
            "action": action, "requires": list(requires), "effects": list(effects), "contacts": list(contacts),
            "causes": list(causes)}


def courtyard_clip(requires=()):
    beats = [beat("b01", 0, 2, "acrobat", ["wizard"], "Acrobat circles the scorched flagstones.", requires=requires,
                  causes=[{"to": "b02", "causal_strength": "soft", "why": "The circling sets up the stand-off."}]),
             beat("b02", 2, 2, "wizard", ["acrobat"], "They hold the stand-off.", event_type="hold")]
    plan = plan_for(COURTYARD_2, COURTYARD, beats)
    return pipeline.run(COURTYARD_2, until="contact", plans={"temporal": plan}, previous=COURTYARD)


def test_damage_carries_and_a_contradicting_requirement_is_refused():
    clip = courtyard_clip()
    start = {s["subject"]["id"]: s["conditions"] for s in clip["nodes"]["states"]["items"] if s["beat"] == "b01"}
    assert (start["ground"]["damage"], start["stone_pillar"]["damage"], start["bamboo_wall"]["damage"]) == \
        ("scorched", "cracked", "cut")
    assert clip["provenance"]["chained_from_envelope_hash"] == "sha256:" + content_hash(COURTYARD)
    causing = {e["from"] for e in COURTYARD["edges"]["causal"]["items"]}
    open_beats = [b["id"] for b in sorted(COURTYARD["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"]))
                  if b["event_type"] != "hold" and b["id"] not in causing]
    assert clip["scene"]["quadrant"]["carried_causes"] == open_beats
    with pytest.raises(ContractError) as error:
        courtyard_clip(requires=[fact("surface", "ground", "damage", "none")])
    assert error.value.code == "GATE_FAILED" and error.value.path[0]["code"] == "REPLAY_REQUIRES"


def reference_clip(requires):
    a, b = "ninja_lean", "ninja_broad"
    beats = [beat("b01", 0, 2, a, [b], "A lets the rope dart drop from the left hand.", requires=requires,
                  effects=[fact("prop", "rope_dart", "holder", "none")],
                  contacts=[{"contact_type": "release", "a": {"kind": "entity", "id": a, "part": "left_hand"},
                             "b": {"kind": "prop", "id": "rope_dart", "part": "rope"}}],
                  causes=[{"to": "b02", "causal_strength": "soft", "why": "Free hands, A rises over B."}]),
             beat("b02", 2, 2, a, [b], "A stays crouched over B.", event_type="hold")]
    beats[0]["participants"].append({"kind": "prop", "id": "rope_dart"})
    return beats


def test_props_and_contacts_carry_so_a_carried_hold_can_be_released():
    beats = reference_clip([fact("prop", "rope_dart", "holder", "ninja_lean")])
    plan = plan_for(REFERENCE_2, REFERENCE, beats)
    clip = pipeline.run(REFERENCE_2, until="contact", plans={"temporal": plan}, previous=REFERENCE)
    carried = [c for c in clip["nodes"]["contacts"]["items"] if c["beat"] == "chain"]
    assert {(c["body_part"], c["b"]["id"]) for c in carried} >= {("left_hand", "rope_dart"), ("right_hand", "kunai")}
    assert any(e["relation"] == "releases" and e["to"].startswith("chain_") for e in clip["edges"]["contact"]["items"])
    with pytest.raises(ContractError) as error:  # the same release with no previous clip has nothing to release
        unchained = plan_for(REFERENCE_2, None, beats)
        pipeline.run(REFERENCE_2, until="contact", plans={"temporal": unchained})
    assert error.value.code == "GATE_FAILED"
    contradicted = reference_clip([fact("prop", "rope_dart", "holder", "none")])
    with pytest.raises(ContractError) as error:
        pipeline.run(REFERENCE_2, until="contact", plans={"temporal": plan_for(REFERENCE_2, REFERENCE, contradicted)},
                     previous=REFERENCE)
    assert error.value.path[0]["code"] == "REPLAY_REQUIRES"


@pytest.mark.parametrize("last, code", [
    ({"id": "c11", "side": "right", "azimuth_deg": -90.0, "scale": "wide", "target": "midpoint"}, "CAMERA_AXIS"),
    ({"id": "c11", "side": "left", "azimuth_deg": 80.0, "scale": "wide", "target": "midpoint"}, "CAMERA_CONTINUITY"),
    ({"id": "c11", "side": "left", "azimuth_deg": 10.0, "scale": "wide", "target": "midpoint"}, None),
])
def test_the_first_shot_cuts_from_the_previous_clip(last, code):
    packet = {**p15_camera.prepare(courtyard("effort")), "chained_last_shot": last}
    plan = copy.deepcopy(courtyard_plans()["camera"])
    found = {f["code"] for f in p15_camera.check(plan, packet)}
    assert "CAMERA_TILING" in found  # a chained clip's first shot cannot open
    plan["shots"][0]["editing"]["transition_in"] = "cut"
    found = {f["code"] for f in p15_camera.check(plan, packet)}
    assert found == ({code} if code else set())


def test_bad_chains_are_refused():
    stale = copy.deepcopy(COURTYARD)
    stale["provenance"]["kernel_hash"] = "sha256:" + "0" * 64
    for previous, query, expected in ((stale, COURTYARD_2, "CHAIN_STALE"),
                                      (pipeline.run(COURTYARD_2, until="brief"), COURTYARD_2, "CHAIN_INCOMPLETE"),
                                      (COURTYARD, "4 seconds anime fight: wizard vs knight in a castle", "CHAIN_WORLD")):
        with pytest.raises(ContractError) as error:
            pipeline.run(query, until="brief", previous=previous)
        assert error.value.code == expected
