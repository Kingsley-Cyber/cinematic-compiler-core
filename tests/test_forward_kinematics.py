"""Forward kinematics (owners O24, O72; backlog M9-06a): world points from the pelvis root, and the contact misses."""

import json

import pytest
from conftest import ROOT

from solver import contact_world, forward_kinematics

pytestmark = pytest.mark.unit
METRES = forward_kinematics.segments()
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
            assert -0.01 <= lowest <= 0.05 or key["id"] == "acrobat@b08", (name, key["id"], lowest)


def test_the_miss_list_names_the_kunai_pickup_and_its_cause():
    rows = {r["id"]: r for r in contact_world.measure(_envelope("reference_fight"))}
    pickup = rows["b19_c2"]                                                    # A takes the kunai at 8.0
    assert pickup["measurable"] and 1.2 < pickup["distance"] < 1.35 and pickup["target_point"] == [0.6, 0.0, 4.0]
    assert rows["b01_c1"]["distance"] <= contact_world.TOLERANCE_M          # A lands on the pillar's top (O21)
    assert not rows["b18_c1"]["measurable"]                                   # the pillar's face has no top to meet
