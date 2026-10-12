"""S13: convention math, key-pose checks against S04/S06, turn axes, derived quaternions/edges, write scope."""

import copy
import json
import math

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p13_motion
from kernel.canonical import ContractError, canonical_json
from solver import quaternion
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["motion"]
PACKET = p13_motion.prepare(courtyard("bartenieff"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "motion_graph.schema.json").read_text())


def rounded(vector):
    return [round(v, 6) + 0.0 for v in vector]


@pytest.mark.parametrize("rot, vector, expected", [
    ([90, 0, 0], (0, 0, 1), [0, -1, 0]),   # +X pitches the nose down
    ([0, 90, 0], (0, 0, 1), [1, 0, 0]),    # +Y yaws the nose to the performer's left (+X)
    ([0, 0, 90], (1, 0, 0), [0, 1, 0]),    # +Z rolls clockwise: left side up, right shoulder down
])
def test_convention_directions(rot, vector, expected):
    assert rounded(quaternion.apply(quaternion.matrix(rot), vector)) == expected


@pytest.mark.parametrize("rot", [[0, 0, 0], [90, 0, 0], [0, 90, 0], [0, 0, 90], [30, -45, 60], [180, -389.055, 0],
                                 [-120, 75, 200]])
def test_quaternion_round_trips_to_the_same_rotation(rot):
    w, x, y, z = quaternion.quaternion(rot)
    assert w >= 0 and math.isclose(w * w + x * x + y * y + z * z, 1, abs_tol=1e-8)
    from_quat = ((1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)),
                 (2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)),
                 (2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)))
    for row_a, row_b in zip(from_quat, quaternion.matrix(rot), strict=True):
        assert all(math.isclose(a, b, abs_tol=1e-7) for a, b in zip(row_a, row_b, strict=True))


def test_other_conventions_are_refused():
    with pytest.raises(ContractError) as error:
        quaternion.require({"euler_order": "YXZ", "kind": "intrinsic", "handedness": "right", "units": "degrees"})
    assert error.value.code == "ROTATION_CONVENTION"


def key(plan, slot):
    return next(k for k in plan["keys"] if k["slot"] == slot)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p13_motion.check(plan, PACKET)}


def test_a_tipped_root_without_a_turn_reads_its_more_horizontal_axis():
    from solver.euler_solver import basis_for
    turns = PACKET["rotation_convention"]["turns"]
    slide = {"rot": [80, 0, 0], "turn": "none"}          # pitched 80 degrees: the lateral axis stays level
    on_side = {"rot": [0, 0, 80], "turn": "none"}        # rolled 80 degrees: the forward axis stays level
    assert basis_for(slide, None, turns) == "lateral" and basis_for(on_side, None, turns) == "forward"
    assert basis_for({"rot": [0, 30, 0], "turn": "none"}, None, turns) == "forward"


def test_courtyard_keys_pass_and_the_joints_come_from_the_kernel():
    assert p13_motion.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]
    assert PACKET["joints"] == ["Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK"]


@pytest.mark.parametrize("code, change", [
    ("MOTION_SLOT", lambda p: p["keys"].pop(0)),
    ("MOTION_JOINTS", lambda p: key(p, "wizard@b03")["bones"].pop("NK")),
    ("MOTION_JOINTS", lambda p: key(p, "wizard@b03")["bones"].update(TAIL=[0, 0, 0])),
    ("MOTION_POS", lambda p: key(p, "acrobat@b05").update(pos=[1.0, 0, 4.3])),
    ("MOTION_FACING", lambda p: key(p, "wizard@b11").update(rot=[0, 175, 0])),
    ("MOTION_FACING", lambda p: key(p, "acrobat@b13").update(rot=[180, -330, 0])),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b02").update(axis_declaration="Y")),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b02").update(turn="none", axis_declaration="none")),
    ("MOTION_AXIS", lambda p: key(p, "acrobat@b05").update(turn="cartwheel", axis_declaration="Z")),
    ("MOTION_AXIS", lambda p: key(p, "wizard@b11").update(turn="spin", axis_declaration="Y")),
    ("MOTION_POSTURE", lambda p: key(p, "acrobat@b12").update(rot=[460, -389.055, 0])),
    ("TURN_LABEL", lambda p: key(p, "acrobat@b12").update(turn="spin", axis_declaration="Y")),  # dodge_flip as a spin
    # FR.3: the dodge_flip stopped at its 180-degree apex (the plan before O38), turning back, upright at the apex
    ("ROTATION_INCOMPLETE", lambda p: key(p, "acrobat@b13").update(turn="none", axis_declaration="none")),
    ("ROTATION_NOT_MONOTONIC", lambda p: key(p, "acrobat@b13").update(rot=[420, -389.055, 0])),
    ("INVERSION_MISSING", lambda p: key(p, "acrobat@b13").update(rot=[180, -389.055, 180])),
    # FR.4, owner O80: the dodge flip declared from the grounded 7.60 key turns before its 8.60 launch (F-058)
    ("AIRBORNE_WITHOUT_LAUNCH", lambda p: key(p, "acrobat@b11").update(turn="flip", axis_declaration="X")),
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(LL=[-30, 0, 0])),   # knee hyperextension (O7)
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(LFA=[-170, 0, 0])),  # elbow past 150, no anime allowance
    ("JOINT_LIMIT", lambda p: key(p, "wizard@b03")["bones"].update(NK=[40, 0, 0], HD=[40, 0, 0])),  # neck 80 > 45 + 30
    # F5.2, owners O72, O83: the kick's pose before S-030 leaves the foot 1.2 m under the wizard's torso
    ("CONTACT_WORLD", lambda p: key(p, "acrobat@b06")["bones"].update(RUL=[-40, 0, -15], RL=[15, 0, 0])),
    # RV-49 (F-144, R-18): the kick's pose before S-049 drives the acrobat's foot through the wizard's trunk
    ("BODY_OVERLAP", lambda p: key(p, "acrobat@b06")["bones"].update(Sp=[-20, 0, 0], RUL=[-87, 2.2, -2.7])),
    # RV-14a (F-089): the backflip takeoff before S-078 sank both soles 0.185 m under the ground
    ("FLOOR_PENETRATION", lambda p: key(p, "acrobat@b12")["bones"].update(LUL=[-20, 0, 5], LL=[45, 0, 0],
                                                                          RUL=[-20, 0, -5], RL=[45, 0, 0])),
    # RV-14a (F-089): a foot the kinematic node claims as a support, lifted off the floor at its key
    ("CONTACT_WORLD", lambda p: key(p, "wizard@b05")["bones"].update(LUL=[-60, 0, 0], LL=[90, 0, 0])),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


def test_contact_world_spares_a_listed_exception_and_an_artefact():
    """ADR-O83: a miss the owner's list keeps with its reason (read through S13's packet since RV-43, F-123) is not
    refused. Owner O89 (ADR-O104), re-pinned in S-039: a miss at an exact instant is never an artefact, airborne,
    turning or not; only a point interpolated between keys or samples while the actor is airborne or the prop moves is.
    The acrobat's hand plant (b02_c1), this test's artefact since S-030 (1.8 m off the ground at 2.0), is a support at the
    vault's first key and meets the ground (F-076)."""
    plan, packet = copy.deepcopy(PLAN), copy.deepcopy(PACKET)
    key(plan, "acrobat@b06")["bones"].update(RUL=[-40, 0, -15], RL=[15, 0, 0])
    packet["contact_world"]["exceptions"] = {"b05_c2": "kept for the test"}
    assert "CONTACT_WORLD" not in {f["code"] for f in p13_motion.check(plan, packet)}
    from solver import contact_world
    rows = {r["id"]: r for r in contact_world.measure_plan({k["slot"]: k for k in PLAN["keys"]},
                                                           {s["slot"]: s for s in PACKET["slots"]}, PACKET)}
    assert rows["b02_c1"]["distance"] <= contact_world.TOLERANCE_M and codes(lambda p: None) == set()
    miss = dict(rows["b02_c1"], distance=1.0, airborne=True, rotating=True, prop_moving=True)
    assert not contact_world.artefact(miss) and contact_world.refusals([miss], {})       # an exact instant: refused
    assert contact_world.refusals([dict(miss, interpolated=True)], {}) == []             # between keys: an artefact
    assert contact_world.refusals([dict(miss, interpolated=True, airborne=False, prop_moving=False)], {})  # a turn alone


def test_a_contact_between_keys_is_measured_on_the_interpolated_pose():
    """F-089 (RV-59d, ADR-O104): a contact with no key at its instant but keys on both sides is measured on the pose the
    declared interpolation gives there. The wizard example's landing, back at 6.4 (between the pillar brace at 5.2 and
    the lunge at 6.6, S-088), misses the ground and is refused: the torso is still on the pillar. Emptying the 5.2
    key's claim no longer excuses it: a landing is never airborne (RV-59h, F-222; S-088 had excused it)."""
    from solver import contact_world
    packet = copy.deepcopy(PACKET)
    for contact in packet["contact_world"]["contacts"]:
        if contact["id"] in ("b08_c2", "b08_c3"):
            contact["t"] = 6.4
    slots = {s["slot"]: s for s in packet["slots"]}
    rows = {r["id"]: r for r in contact_world.measure_plan({k["slot"]: k for k in PLAN["keys"]}, slots, packet)}
    landing = [rows["b08_c2"], rows["b08_c3"]]
    assert all(r["measurable"] and r["interpolated"] and not r["airborne"] for r in landing)
    assert [r["distance"] for r in landing] == [0.275, 0.181]
    assert {f["contact"] for f in p13_motion.check(PLAN, packet) if f["code"] == "CONTACT_WORLD"} == {"b08_c2", "b08_c3"}
    slots["acrobat@b08"]["kinematic"]["support"] = []
    rows = contact_world.measure_plan({k["slot"]: k for k in PLAN["keys"]}, slots, packet)
    assert {f["contact"] for f in contact_world.refusals([r for r in rows if r["id"] in ("b08_c2", "b08_c3")], {})} == \
        {"b08_c2", "b08_c3"}


def test_a_touch_in_the_air_between_keys_is_excused_and_a_landing_never_is():
    """F-222 (RV-59h, ADR-O104, O89): between keys the actor is airborne only when no support of its own is open just
    before the contact, and a support's onset (a landing) never is. Planted on the wizard example with the pillar let
    go at 5.2: a touch of the ground at 5.3, 1.16 m off it, is excused as airborne; the landings there are refused."""
    from solver import contact_world
    packet = copy.deepcopy(PACKET)
    contacts = packet["contact_world"]["contacts"]
    for contact in contacts:
        if contact["id"] == "b08_c1":  # the torso's release from the pillar
            contact["t"] = 5.2
        if contact["id"] in ("b08_c2", "b08_c3"):
            contact["t"] = 5.3
    contacts.append({**next(c for c in contacts if c["id"] == "b08_c2"), "id": "b08_c9", "contact_type": "touch"})
    slots = {s["slot"]: s for s in packet["slots"]}
    rows = {r["id"]: r for r in contact_world.measure_plan({k["slot"]: k for k in PLAN["keys"]}, slots, packet)}
    assert rows["b08_c9"]["airborne"] and rows["b08_c9"]["distance"] > 1.0 and contact_world.artefact(rows["b08_c9"])
    assert not rows["b08_c2"]["airborne"] and not rows["b08_c3"]["airborne"]
    assert {f["contact"] for f in contact_world.refusals(list(rows.values()), {})} == {"b08_c2", "b08_c3"}


def test_a_prop_between_its_samples_runs_straight_and_moves_when_its_samples_differ():
    """RV-59d (ADR-O104): a prop with no sample at a contact's instant but samples on both sides is read straight between
    them, moving when the samples differ or carry a velocity; outside its samples it is not measured."""
    from solver.contact_world import _prop_at
    samples = {("kunai", 1.0): [{"t": 1.0, "p": [0.0, 1.0, 0.0], "v": [0, 0, 0]}],
               ("kunai", 2.0): [{"t": 2.0, "p": [1.0, 1.0, 0.0], "v": None}],
               ("log", 1.0): [{"t": 1.0, "p": [2.0, 0.0, 0.0], "v": [0, 0, 0]}],
               ("log", 3.0): [{"t": 3.0, "p": [2.0, 0.0, 0.0], "v": [0, 0, 0]}]}
    assert _prop_at(samples, "kunai", 1.25) == ([{"p": [0.25, 1.0, 0.0], "v": None}], True, True)
    assert _prop_at(samples, "log", 2.0) == ([{"p": [2.0, 0.0, 0.0], "v": None}], False, True)
    assert _prop_at(samples, "kunai", 2.5) == ([], False, False)


def test_no_body_sinks_into_the_floor_at_any_key():
    """F-089 (RV-14a, owner O72): at every key no body point lies more than 0.15 m under the floor, the lowest floor's
    top or, where a scene names no floor, the convention's ground."""
    from solver import floor_penetration
    assert PACKET["floor_y"] == 0.0 and "FLOOR_PENETRATION" not in codes(lambda p: None)
    body = {("acrobat", 1.0): {"id": "acrobat@b99", "points": {"left_foot": [0, -0.12, 0], "head": [0, 1.5, 0]}}}
    assert floor_penetration.refusals(body, 0.0) == []                                 # 0.12 m: within O72's 0.15 m
    assert [f["slot"] for f in floor_penetration.refusals(body, 0.1)] == ["acrobat@b99"]  # 0.22 m under a floor at 0.1
    assert floor_penetration.floor_level([{"id": "tabletop", "kind": "tabletop"}], "y=0") == 0.0


def test_every_claimed_support_meets_its_surface_at_every_key():
    """F-089 (RV-14a): CONTACT_WORLD measures each key's claimed supports (its S11 kinematic node), not only a support
    contact's onset: each part to the top its open support contact names, or to the floor when none does."""
    from solver import contact_world
    plan = copy.deepcopy(PLAN)
    key(plan, "wizard@b05")["bones"].update(LUL=[-60, 0, 0], LL=[90, 0, 0])
    rows = {r["id"]: r for r in contact_world.measure_plan({k["slot"]: k for k in plan["keys"]},
                                                           {s["slot"]: s for s in PACKET["slots"]}, PACKET)}
    lifted = rows["wizard@b05:left_foot"]
    assert lifted["target"] == "the floor" and lifted["distance"] > contact_world.TOLERANCE_M
    assert rows["wizard@b05:right_foot"]["distance"] <= contact_world.TOLERANCE_M
    assert [(f["code"], f["contact"]) for f in contact_world.refusals(list(rows.values()), {})] == [
        ("CONTACT_WORLD", "wizard@b05:left_foot")]


def test_contact_world_exceptions_are_the_owners_alone():
    """F-123 (RV-43): a motion plan that lists its own CONTACT_WORLD exception fails S13's schema (motion_plan 2.0); an
    owner's exception that names a contact that meets is refused, so the owner's list stays true."""
    plan = copy.deepcopy(PLAN)
    plan["contact_world_exceptions"] = {"b05_c2": "the author's own"}
    with pytest.raises(ContractError):
        p13_motion.run(courtyard("bartenieff"), plan)
    packet = copy.deepcopy(PACKET)
    packet["contact_world"]["exceptions"] = {"b04_c1": "a landing that meets the ground"}
    assert "CONTACT_WORLD" in {f["code"] for f in p13_motion.check(PLAN, packet)}


def test_a_vault_launches_from_its_planted_hand():
    """Owner O80 with O89's vault hand (F-076, S-039): the vault's flip starts on the planted right hand alone and leaves
    the ground after it; a first key that also stands on a foot turns on the ground before its launch (F-058)."""
    slots = {s["slot"]: s for s in PACKET["slots"]}
    assert slots["acrobat@b02"]["kinematic"]["support"] == ["right_hand"] and codes(lambda p: None) == set()
    for support in (["right_hand", "left_foot"], ["left_foot", "right_foot"]):
        packet = copy.deepcopy(PACKET)
        next(s for s in packet["slots"] if s["slot"] == "acrobat@b02")["kinematic"]["support"] = support
        assert "AIRBORNE_WITHOUT_LAUNCH" in {f["code"] for f in p13_motion.check(PLAN, packet)}, support


@pytest.mark.integration
def test_derived_graph_scope_and_determinism(order):
    before = courtyard("bartenieff")
    snapshot = copy.deepcopy(before)
    after, _ = p13_motion.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "motion", before, after) == []
    nodes, edges = after["nodes"]["motion"]["items"], after["edges"]["motion"]["items"]
    validate_schema({"motion": nodes, "motion_edges": edges}, GRAPH)
    bases = {n["id"]: n["heading_basis"] for n in nodes}
    assert {s for s, b in bases.items() if b == "lateral"} == {"acrobat@b03", "acrobat@b04", "acrobat@b13"}
    assert len(edges) == len(nodes) - len({n["entity"] for n in nodes})
    by_id = {n["id"]: n for n in nodes}
    for edge in edges:
        start, end = by_id[edge["from"]], by_id[edge["to"]]
        axis = {"flip": 0, "spin": 1, "cartwheel": 2}.get(start["turn"])  # RV-108 (F-225): a half turn or more runs straight
        assert edge["interpolation"] == ("euler_axis" if axis is not None and abs(edge["euler_delta"][axis]) >= 180 else "slerp")
        assert edge["euler_delta"] == rounded([b - a for a, b in zip(start["rot"], end["rot"], strict=True)])
        assert math.isclose(edge["trajectory"]["distance"], math.dist(start["pos"], end["pos"]), abs_tol=1e-6)
    spin = next(e for e in edges if e["turn"] == "spin")
    assert spin["euler_delta"][1] == -367.26 and spin["slerp_angle"] == 7.26  # slerp alone would lose the full turn
    assert canonical_json(after) == canonical_json(p13_motion.run(courtyard("bartenieff"), PLAN, order=order)[0])


def test_joint_limits_follow_the_owner_table_and_widen_for_anime():
    from compiler.passes.derived.p13_motion import joint_limits
    from solver.euler_solver import limit_findings
    human, anime = joint_limits("live_action"), joint_limits("anime")
    assert human["LL"]["x"] == [0, 135] and anime["LL"]["x"] == [0, 165]       # a hinge stop stays at 0
    assert human["LA"]["x"] == [-180, 60] and anime["LA"]["x"] == [-210, 90]
    assert human["LFA"]["x"] == anime["LFA"]["x"] == [-150, 0]                 # the elbow gets no anime allowance
    pose = {"bones": {j: [0, 0, 0] for j in ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")}}
    pose["bones"]["LL"] = [150, 0, 0]
    assert [f["code"] for f in limit_findings(pose, "s", human)] == ["JOINT_LIMIT"]
    assert limit_findings(pose, "s", anime) == []


def test_a_spin_is_written_once_like_a_named_flip():
    """FR.1 as amended by W3: ROTATION_PATH_UNSTATED reads every turn run, a spin that no beat names as much as a flip."""
    from validators import prompt_validator
    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    words = "turns to the left 90 degrees about the vertical axis (transverse plane), 1.60–2.00"
    assert words in text
    found = {f["code"] for f in prompt_validator.check(text.replace(words, "turns left, 1.60–2.00"), envelope, "mixed")}
    assert "ROTATION_PATH_UNSTATED" in found and "TURN_LABEL" not in found       # no beat names this spin



def test_the_face_heading_reads_the_whole_chain():
    """Owner O76, rule R-34 (S-026 audit): the spine's twist turns the face; a face pointing up keeps the old reading."""
    bones = {j: [0, 0, 0] for j in ("Sp", "LUL", "RUL", "LL", "RL", "LA", "RA", "LFA", "RFA", "HD", "NK")}
    twisted = {"rot": [0, 0, 0], "bones": {**bones, "Sp": [0, 30, 0]}}
    assert quaternion.head_heading(twisted) == 30.0                       # the old sum of root, NK and HD said 0
    supine = {"rot": [-90, 0, 0], "bones": {**bones, "NK": [0, 10, 0]}}    # on the back, the face up
    assert quaternion.head_heading(supine) == 10.0                         # no horizontal heading: the old reading
