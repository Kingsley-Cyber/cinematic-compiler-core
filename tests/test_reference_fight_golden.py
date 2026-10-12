"""S16.6 golden: the LBN reference fight compiles from its preface + cards + in-session plans, and the render
contains every kernel and reference-fight item, carries A's reference roots exactly and its joints with the recorded
deviations (owner O7/O10/O11), and keeps its anime directives."""

import json
import math
from pathlib import Path

import pytest
from conftest import ROOT

from kernel.kernel_files import load as load_kernel

pytestmark = pytest.mark.integration
FOLDER = ROOT / "examples" / "reference_fight"
ENVELOPE = json.loads((FOLDER / "envelope.json").read_text(encoding="utf-8"))
RENDER = ENVELOPE["nodes"]["render"]["items"][0]
TEXT = RENDER["text"]
SPEC = json.loads(TEXT[TEXT.index("{"):])
SOURCE = (ROOT / "kernel" / "sources" / "lbn-2.3-adv.txt").read_text(encoding="utf-8")
REFERENCE = json.loads(SOURCE[SOURCE.index("{"):])


# Owner O17 (2026-10-11): the query counts the substitution log, the fight's fifth prop (render finding F12; the
# prompt said FOUR props in SCENE and FIVE in RULES). The reference item k_preface_03 reads the corrected count.
PREFACE_RECOUNTED = {"k_preface_03": "TWO fighters, FIVE props (kunai, rope dart, smoke pellet, shuriken volley, "
                                     "substitution log)"}


# Owner O18 (2026-10-11, backlog M9-03, audit X2/X3): the golden's own tracks say A lands by the rope dart ("7.5 A lands
# near ground rope dart, A picks up rope dart") and takes the kunai from the ground at 8.0, while its rows and two of
# its rules put A in the air. The numbers and those two rules follow the words: A lands crouched by the rope dart at
# 7.5, runs to the kunai and takes it crouched at 8.0, then leaps at 8.5 for the drive.
GROUNDED_RULES = {"k_rules_18": "ROPE DART REGRAPPLE at 7.5 from a crouch,left hand throws rope dart,rope dart wraps B right "
                                "shoulder,A pulled toward B,this is a GRAPPLE NOT a strike",
                  "k_rules_27": "kunai picked up from ground at 8.0,A crouched by it"}
# Owner O79 (F-067, backlog M9-09f): O21 wins, A starts at y=10, so the query and its reference item say so.
START_HEIGHT = {"k_preface_04": "A starts ABOVE the frame, falling from y=10"}
# Owner O90 (F-081, RV-06, S-042): A lets go of everything at the substitution (3.7); the rope dart lies on the ground
# from then until A takes it at 7.5, so the slide no longer releases it.
VANISH_RULE = {"k_rules_26": "rope dart left on the ground at 3.7 when A vanishes,picked up again at 7.5 during wall-push "
                             "recovery"}
REWORDED = {**PREFACE_RECOUNTED, **GROUNDED_RULES, **START_HEIGHT, **VANISH_RULE}


def test_every_kernel_and_reference_item_is_in_the_render():
    items = load_kernel("invariants")["items"]
    printed = [i for i in items if i["origin"] != "owner"]
    scopes = ("kernel", "kernel_actor", "kernel_prop", "scene_reference")
    counts = {scope: sum(i["scope"] == scope for i in printed) for scope in scopes}
    assert counts == {"kernel": 20, "kernel_actor": 6, "kernel_prop": 5, "scene_reference": 37}
    assert [i["id"] for i in printed if REWORDED.get(i["id"], i["text"]) not in TEXT] == []
    assert [i["id"] for i in printed if i["id"] in REWORDED and i["text"] in TEXT] == []  # the rewording replaced them
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]


# Recorded deviations from the reference numbers, owner decisions of 2026-10-11 (O7; O10 + O11; O88):
# - knee flexion is +X under Q6, so the reference's negative knee angles (a hyperextended knee) read as +|x|;
# - O88 (S-038): where a joint's number points the other way to the row's own words, it flips so the printed word
#   follows the source: 19 limbs and 13 heads. A flip past the anime hip-extension limit is held at +60 (O11, as O10
#   clamped before); the right hips at 1.1 and 3.0 (+90, once clamped to +60) flip to -90 ("R: leg fwd mid"). The two
#   hips at 0.6 keep their crouch (ADR-O103: flipped, the soles would leave the pillar top).
WORD_FLIPS = {(1.1, "LA"): -60, (1.1, "LUL"): 60, (1.1, "RA"): 60, (1.1, "RUL"): -90, (1.6, "LUL"): 45, (1.6, "RUL"): -45,
              (2.0, "LA"): -90, (2.0, "RA"): -90, (2.5, "LA"): -60, (3.0, "RA"): -30, (3.0, "RUL"): -90,
              (3.7, "LA"): -60, (3.7, "RA"): -60, (4.7, "LA"): -60, (5.1, "LA"): -90, (5.1, "RA"): -90,
              (6.6, "LA"): -90, (7.0, "LUL"): 45, (7.0, "RUL"): -45}
HEAD_FLIPS = {0.0, 0.6, 1.1, 1.6, 2.0, 3.7, 5.1, 5.9, 7.0, 9.0, 9.5}  # HD's sign; 7.5 and 8.0 in GROUNDED_PICKUPS
# Owner O18 (2026-10-11, audit X9): A vanishes at 3.7 (the substitution) and reappears at 4.4, so the reference's A row
# at 4.0 (a full pose with both feet down while 'A already gone') is not drawn.
VANISHED = {4.0}
# Owner O18 (audit X5, X6): the backflip at 5.1 pitches A backward through 360 and the cartwheel at 6.3 rolls A to the
# left through 360; angles are continuous, so every later root carries the turn (X -360 after 5.1, Z -360 after 6.3).
ROOT_TURNS = ((5.1, 0, -360), (6.3, 2, -360))
# Prop positions and velocities are authored on the beats and solved under gravity (owner O8, O10); the source's
# literal p/v (e.g. kunai thrown at 0.5 toward -Z, yet at +Z 5.0 at 2.0) are not copied, as they disagree with gravity.


# The two pickup roots re-rooted in S-029 (O72, O82, O85): the soles on the ground under the anime body, hips read from
# the trunk (O84); 0.6 before. Re-blocked in S-030 (CONTACT_WORLD, ADR-O83, R-33): the left hand reaches the rope dart
# on the ground at 7.5 and A crouches at the kunai, the right hand on it at 8.0 (each within 0.15 m; the least change
# of root, crouch and arm, both soles on the ground). O89 (S-039): the kunai is deflected at A's right foot, so it lands
# at [1.4, 0, 3.77] (O77's v_post), and the 8.0 crouch moves with it, pose kept (+0.8 x, -0.23 z). O90 (S-042): the
# rope dart drops from A's left hand at the substitution and rests at [1.18, 0, 4.51], so the 7.5 crouch moves with
# it, pose and facing kept (+0.78 x, +0.71 z). RV-35a (F-110, S-080): that re-block made A crawl (trunk past flat, head at
# the pelvis, both hands down), so A crouches deeper (pelvis 0.40) on planted feet with one hand on the prop and the
# other off the floor, the trunk leaning 58 and 75 degrees with a twist; the values come from solver/reblock.py with
# the goals S-080 records, and S04 and S11 name the hand's support on the ground. RV-95 (F-206, S-083): that re-block
# put a knee in the floor and the hands on it through a throw and a leap, so A crouches at its own 0.57 m again, every
# knee 0.08 m over the floor, the hand on its prop only at the key (the feet bear the weight), from the commands S-083
# records (tests/test_reblock.py re-derives them); the words say the new numbers (bent N = 15 N degrees).
GROUNDED_PICKUPS = {  # O18: A's rows at the two pickups, crouched on the ground
    7.5: [7.5, "rope_dart_regrapple", [0.71, 0.57, 4.22], [-330, 30, -360],
          {"Sp": [28.625, -38.125, -29.0], "LUL": [-92.575, 0, 64.75], "RUL": [-94.25, 0, 60.0], "LL": [100.6, 0, 0],
           "RL": [108.0, 0, 0], "LA": [-61.1, 1.125, 30.125], "RA": [-103.375, 0, -0.5], "LFA": [-16.0, 0, 0],
           "RFA": [-45.375, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]}],
    8.0: [8.0, "pull_b_toward_pillar", [0.91, 0.57, 4.0], [-330, 90, -360],
          {"Sp": [40.0, 70.375, 27.125], "LUL": [-56.975, 0, -41.5], "RUL": [-57.6, 0, -37.5], "LL": [79.3, 0, 0],
           "RL": [91.0, 0, 0], "LA": [-60.0, 0, 0.0], "RA": [-39.325, -7.95, -58.875], "LFA": [-30.0, 0, 0],
           "RFA": [-4.75, 0, 0], "HD": [10, 0, 0], "NK": [0, 0, 0]}],
}
# ADR-O83 point 2 kept the source's one real miss (b06_c3, A's right foot 1.5 m over the ground at 3.0) as an
# exception; O88's flip of that hip to the row's own "R: leg fwd mid" puts the foot on the ground (S-038). O89 (S-039):
# a turn exempts nothing, so the source's slide at 5.9 (both soles 0.35-0.55 m over the ground, the source's root and
# legs) is listed with its reason, as the owner's M9-06b ruling keeps the source's misses.
CONTACT_EXCEPTIONS = {"b14_c2", "b14_c3"}


GROUNDED_DESCRIPTIONS = {
    7.5: "L:arm fwd mid bent1 taking the rope dart from the ground, leg fwd mid bent7, lLeg bent7; R:arm fwd mid "
         "bent3, leg fwd mid bent7, lLeg bent7; support=both feet; A LANDS CROUCHED BY THE ROPE DART and takes it with"
         " the left hand, then whips it forward to wrap B right shoulder, head facing B, this is a GRAPPLE NOT a "
         "strike",
    8.0: "L:arm fwd mid bent2 holding rope dart taut, leg fwd mid bent5, lLeg bent5; R:arm side mid straight taking "
         "the kunai from the ground, leg fwd mid bent6, lLeg bent6; support=both feet; A CROUCHES BY THE KUNAI, the "
         "right hand takes it from the ground while the left hand hauls the taut rope dart, B dragged toward the "
         "pillar at z=6, this is a PULL NOT a strike",
}


# Owner O21 (audit X7, backlog M9-08a): the pillar keeps its 8 m top, so A starts above the frame at root y=10 and lands
# with the feet on the top at y=8, root 8.5; the source's rows start A at 7.5 and land it at 7.2, under the top. S-029
# (O72, O82, O85): the landing root re-rooted to 8.71 so the soles meet the top under the anime body (O84).
OPENING = {0: [0, 10, 3.5], 0.6: [0, 8.71, 5.8]}
OPENING_WORDS = {0.6: ("both feet on pillar top y=7.2", "both feet on pillar top y=8")}
# Owner O90 (F-081, S-042): A holds no rope dart while it is gone or after, until 7.5, so A's own rows stop saying so.
ROPE_DART_WORDS = {
    4.4: [("L:arm fwd mid bent3 holding rope dart", "L:arm fwd mid bent3"),
          ("left hand holding rope dart", "left hand empty, rope dart on the ground")],
    4.7: [("L:arm fwd mid bent3 holding rope dart", "L:arm fwd mid bent3"),
          ("left hand still holding rope dart", "left hand empty, rope dart on the ground")],
    5.1: [("L:arm fwd mid bent3 holding rope dart", "L:arm fwd mid bent3"),
          ("left hand still holding rope dart", "left hand empty, rope dart on the ground")],
    5.5: [("L:arm fwd mid bent3 holding rope dart", "L:arm fwd mid bent3")],
    5.9: [("L:arm fwd low bent3 holding rope dart", "L:arm fwd low bent3"),
          ("left hand still holding rope dart", "left hand empty, rope dart on the ground")],
    6.3: [("left hand no longer holding rope dart, rope dart has been released during the slide",
           "left hand empty, rope dart on the ground since the substitution")]}
# Owner O96 (F-087, RV-12): the cartwheel at 6.3 is a full turn, as its keys roll it (O18), not the source's quarter turn.
CARTWHEEL_WORDS = {6.3: [("A body rotates sideways in screen plane one quarter turn",
                          "A body rotates sideways in screen plane one full turn")]}
WORDS = {t: [pair] for t, pair in OPENING_WORDS.items()} | {
    t: ROPE_DART_WORDS.get(t, []) + CARTWHEEL_WORDS.get(t, []) for t in ROPE_DART_WORDS | CARTWHEEL_WORDS}


def reworded(t, text):
    for old, new in WORDS.get(t, []):
        assert old in text, (t, old)
        text = text.replace(old, new)
    return text


def normalised(row):
    joints = {j: list(v) for j, v in row[4].items()}
    for knee in ("LL", "RL"):
        joints[knee][0] = abs(joints[knee][0])
    for (t, joint), x in WORD_FLIPS.items():
        if row[0] == t:
            joints[joint][0] = x
    if row[0] in HEAD_FLIPS:
        joints["HD"][0] = -joints["HD"][0]
    if row[0] in GROUNDED_PICKUPS:
        return GROUNDED_PICKUPS[row[0]]
    rot = list(row[3])
    for after, axis, degrees in ROOT_TURNS:
        if row[0] > after:
            rot[axis] += degrees
    return [row[0], row[1].lower(), OPENING.get(row[0], row[2]), rot, joints]


# S-030 (CONTACT_WORLD, ADR-O83, R-33): the repo-authored side of each real miss moved. The rope dart's sample at 3.0 sits
# in A's left hand (the source's pose); at 8.0 it is the dart, wrapped on B since 7.6, so it sits on B's torso while A
# keeps the rope's end; B steps in and straightens to catch A's elbow at 6.6 with both hands, re-blocked in S-038 when
# O88 turned A's left arm forward (B leans back 23 degrees to the elbow). Owner O89 (S-039, no exact-instant miss is
# an artefact): the kunai is deflected at A's right foot and lands where O77's v_post takes it; the pellet leaves A's
# right hand at 3.7; the volley leaves B's right hand at 5.5; B's palm reaches the log at 4.0 (a step to the side, the
# lean eased to 20 degrees, the arm extended); B rises on straighter legs to meet A's knee at 4.7.
REBLOCKED_SAMPLES = {("rope_dart", 3.0): [0.85, 0.74, 4.55], ("rope_dart", 8.0): [2.4, 1.53, 3.47],  # 8.0: with B, O86
                     ("kunai", 2.0): [1.19, 1.88, 3.45], ("kunai", 2.5): [1.29, 1.13, 4.44],
                     ("kunai", 2.72): [1.4, 0.0, 3.77], ("shuriken_volley", 5.5): [-1.12, 2.74, 4.83]}
CATCH_ROOT = [0.07, 1.03, 4.8]
# O105 (S-043): the kunai leaves B's right hand at 2.0 (CONTACT_WORLD measures releases), and B throws from A's -Z side.
# RV-49 (S-049, F-144, R-18: no body through another, a strike measured to the target's surface): B holds back at 3.7
# while A leans into the swap, then lunges to the log; B stands clear of A's legs at 4.4; A's knee meets the surface of
# B's back at 4.7, so B stands 0.24 m further along the launch; B bows less at 8.5; B lies 0.18 m aside at 9.0-9.5.
REBLOCKED_ROOTS = {"ninja_broad@b10": [1.0, 1.09, 5.0], "ninja_broad@b12": [-0.44, 1.2, 4.56],
                   "ninja_broad@b04": [1.4, 1.19, 3.3], "ninja_broad@b05": [1.77, 1.14, 2.97],
                   "ninja_broad@b06": [1.77, 1.19, 3.0], "ninja_broad@b09": [1.39, 1.07, 4.53],
                   "ninja_broad@b11": [-0.39, 1.07, 4.51], "ninja_broad@b21": [1.09, 1.08, 5.06],
                   "ninja_broad@b22": [0.96, 0.1, 5.48], "ninja_broad@b23": [0.96, 0.1, 5.48]}
# Owner O86 (F-071, S-032): at 8.0 B stands on A's far side from the pillar (z 6), pose and facing kept, so the rope from
# B to A's hand pulls toward the pillar and B is dragged that way to 8.5; with the kunai's landing since O89 (S-039).
PULL_ANCHOR = [2.2, 1.18, 3.47]


def test_the_pull_at_8_runs_toward_the_pillar():
    keys = {k["id"]: k for k in ENVELOPE["nodes"]["motion"]["items"]}
    a, b, later = (keys[slot]["pos"] for slot in ("ninja_lean@b20", "ninja_broad@b20", "ninja_broad@b21"))
    assert b == PULL_ANCHOR and a[2] > b[2] and later[2] > b[2]               # the rope and the drag both point to +z


def test_the_re_blocked_samples_and_the_catch_are_recorded():
    samples = {(s["prop"], s["t"]): s["p"] for b in ENVELOPE["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])}
    assert {k: samples[k] for k in REBLOCKED_SAMPLES} == REBLOCKED_SAMPLES
    keys = {k["id"]: k for k in ENVELOPE["nodes"]["motion"]["items"]}
    assert keys["ninja_broad@b17"]["pos"] == CATCH_ROOT
    assert {slot: keys[slot]["pos"] for slot in REBLOCKED_ROOTS} == REBLOCKED_ROOTS


def test_contact_world_excepts_only_the_source_miss():
    from solver import contact_world

    # the owner's list, not the authored plan (F-123, RV-43)
    plan = json.loads((ROOT / "examples" / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    kept = contact_world.owner_exceptions(ENVELOPE["provenance"]["source_prompt"])
    assert set(kept) == CONTACT_EXCEPTIONS and "contact_world_exceptions" not in plan
    assert all("O83" in reason for reason in kept.values())


def test_a_roots_and_joints_are_the_reference_rows_with_the_recorded_deviations():
    assert RENDER["labels"] == {"ninja_lean": "A", "ninja_broad": "B"}
    reference = [row for row in REFERENCE["A"] if row[0] < 10 and row[0] not in VANISHED]  # 10.0 hold: no beat
    assert [[row["t"], row["label"], row["pos"], row["rot"], row["joints"]] for row in SPEC["A"]] == \
        [normalised(row) for row in reference]
    assert all(row["desc"].endswith(reworded(row["t"], ref[5]))
               for row, ref in zip(SPEC["A"], reference, strict=True) if row["t"] not in GROUNDED_PICKUPS)
    pinned = {row["t"]: row["desc"] for row in SPEC["A"] if row["t"] in GROUNDED_PICKUPS}
    assert pinned.keys() == GROUNDED_DESCRIPTIONS.keys()
    assert all(pinned[t].endswith(text) for t, text in GROUNDED_DESCRIPTIONS.items())


# Owner O10 (2026-10-11): the golden passes conformance, so the two fx the source draws as a 'ring' read as a 'burst'
# (the kernel negative 'no ring' stays; audit X29).
FX_REWORDED = {"pillar-top landing dust ring": "pillar-top landing dust burst", "crash dust ring": "crash dust burst"}


def fx(text):
    rows = []
    for item in text.split(";"):
        when, what = item.split(" ", 1)
        rows.append(([float(x) for x in when.split("-")], what))
    return rows


def test_props_cast_and_anime_directives_survive():
    assert [k for k in SPEC if k in REFERENCE and isinstance(REFERENCE[k], list) and k not in ("A", "B", "cam")] == \
        ["kunai", "rope_dart", "smoke_pellet", "shuriken_volley", "substitution_log"]
    anime = SPEC["anime"]
    assert anime["impact"] == REFERENCE["anime"]["impact"] and [h[0] for h in anime["holds"]] == REFERENCE["anime"]["holds"]
    assert anime["ink"] == REFERENCE["anime"]["ink"] and fx(anime["fx"]) == [(when, FX_REWORDED.get(what, what))
                                                                             for when, what in fx(REFERENCE["anime"]["fx"])]
    assert len(SPEC["cam"]) == 22 and (SPEC["fps"], SPEC["dur"]) == (24, 10.0)  # the 9.5 push in is its own shot (RV-09)


# Owner O92 (RV-09, F-083, R-21): the hits at 2.5, 4.7 and 8.5 are camera holds with both bodies in frame, never a
# close-up or an insert, and no shot changes playback speed (the source's "slomo.25" at 4.7 and 8.5 goes with O92).
# R-17: the source's lenses are followed: fov45 at 0 (43.46 mm, not 35) and the slow push in on the crouch at fov35
# from 9.5 (57.09 mm), its own shot after the low hold on the crash at 9.0 (it was one 18 mm shot from 9.0).
def test_the_hits_are_held_and_the_source_lenses_kept():
    rows = {row.split(" ", 2)[1]: row for row in SPEC["cam"]}
    for shot in ("c05", "c11", "c20"):
        assert " on A,B: " in rows[shot] and "movement static: " in rows[shot] and "insert" not in rows[shot]
    assert all("playback normal x1;" in row for row in SPEC["cam"])
    assert REFERENCE["cam"][0].endswith("fov45") and "fov44.996126x" in rows["c01"]
    assert REFERENCE["cam"][-2] == "9.5 slow push in crouch fov35"
    assert rows["c22"].startswith("9.5-10 c22 ") and "fov34.999255x" in rows["c22"] and "dolly_in: slow push in" in rows["c22"]


# Owner O48 (2026-10-11, probes R12 and R17, as in R1-R5): the source keeps the log 'hidden in A coat' until 3.7, but the
# model draws a later object from the start whatever the prompt says. The log stands beside A as a post from 0.0 and is
# deployed into A's place in the smoke at the substitution (card state 'standing'). Owner O91 (RV-07): the deployment
# takes effect as the smoke bursts, at 3.7, as the source says ("3.7 A deploys substitution log at A former position"),
# no longer at the substitution's end (4.0).
SUBSTITUTION_POST = ["0 deployment=standing,holder=none,location=ground", "0 p[0.4,1,5.3] at rest"]


def test_the_substitution_log_stands_as_a_post_from_the_start():
    assert REFERENCE["substitution_log"][0].startswith("0.0 not present,hidden in A coat")
    assert REFERENCE["substitution_log"][1].startswith("3.7 A deploys substitution log")
    assert SPEC["substitution_log"][:2] == SUBSTITUTION_POST
    assert "3.7 deployment standing->deployed" in SPEC["substitution_log"]


# Owner O23 (2026-10-11, backlog M9-02): strike, throw and release contacts happen at their key pose, so bow, impact
# frame and pose share one time, as the golden's own words say ("B THROWS KUNAI at 2.0", "FOOT DEFLECT ... at 2.5",
# "RIGHT KNEE strikes B spine at 4.7"); the source's contacts sat at their beat's end, 0.4-0.5 s later.
CONTACTS_AT_POSE = {"b05_c1": 2.0, "b06_c1": 2.5, "b10_c1": 4.0, "b12_c1": 4.7, "b14_c1": 5.5, "b17_c1": 6.6,
                    "b17_c2": 6.6, "b21_c1": 8.5}


def test_strikes_throws_and_releases_happen_at_their_pose():
    times = {c["id"]: c["t"] for c in ENVELOPE["nodes"]["contacts"]["items"]}
    assert {i: times[i] for i in CONTACTS_AT_POSE} == CONTACTS_AT_POSE
    assert "FOOT DEFLECT KINDS: kunai REVERSES from +Z to -Z and downward at 2.5" in REFERENCE["rules"]


# Plan F2.2 (backlog M9-04a under owner O61's build order; ADR-O71 rule 1, covered): a deflect is instantaneous, so
# the kunai carries a pre-contact sample at 2.5 (the 2.0 throw under gravity for 0.5 s) beside the golden's own sample,
# now marked post-contact. Owner O77 (F-064): the golden is right, the kunai reverses from +Z to -Z: the post velocity
# is the source's own v_post [0.5,-4.0,-3.0]. Owner O89 (S-039): the pair sits at A's right foot, the throw arrives
# along +Z, and the kunai lands at 2.72 on [1.4,0,3.77], where A takes it at 8.0. O105 (S-043): B throws it from A's
# -Z side, so it leaves B's hand toward A. O108 (S-046): it goes back down to the ground on B's side, not at B (the
# source's "toward B and ground" with its "NOT toward B"), so the track names no goal after the deflect.
DEFLECT_PAIR = ["2.5 pre-contact p[1.29,1.13,4.44] v[0.2,-3.96,1.98] moving down along +Z",
                "2.5 post-contact p[1.29,1.13,4.44] v[0.5,-4,-3] moving down along -Z"]


def test_the_kunai_deflect_is_a_pre_and_post_pair():
    assert [row for row in SPEC["kunai"] if "-contact " in row] == DEFLECT_PAIR


# Owner O22 (plan F4.1, backlog M9-07a; ADR-O71 rule 1): the contacts the golden's own words name carry their combat
# verb ('B THROWS KUNAI', 'FOOT DEFLECT', 'palm hits log', 'knee strike', 'throw shuriken volley'). Owner O93 (RV-10):
# 'B CATCHES A LEFT ELBOW ... B throws A toward pillar' is a grasp with both hands at 6.6 and a throw that lets go at 6.8.
CONTACT_VERBS = {"b05_c1": "throw", "b06_c1": "deflect", "b10_c1": "strike", "b12_c1": "strike", "b14_c1": "throw",
                 "b17_c1": "catch", "b17_c2": "catch", "b17_c3": "throw", "b17_c4": "throw"}


def test_the_kunai_drive_holds_the_kunai_in_b_and_the_catch_grasps_then_throws():
    """Owner O93 (RV-10, F-084): from 8.5 the kunai is embedded in B's shoulder (the torso point) to the end while A is
    its holder; B's hands take A's left arm at 6.6 and throw A on that pose (O23, RV-48a)."""
    contacts = {c["id"]: c for c in ENVELOPE["nodes"]["contacts"]["items"]}
    # O23 (RV-48a, F-158): the throw lets go on the catch's pose, at 6.6, as the source flashes it
    assert [(contacts[i]["contact_type"], contacts[i]["t"]) for i in ("b17_c1", "b17_c2", "b17_c3", "b17_c4")] == [
        ("possess", 6.6), ("possess", 6.6), ("release", 6.6), ("release", 6.6)]
    keys = {k["id"]: k for k in ENVELOPE["nodes"]["motion"]["items"]}
    samples = {s["t"]: s["p"] for b in ENVELOPE["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])
               if s["prop"] == "kunai" and s["t"] >= 8.5}
    assert sorted(samples) == [8.5, 9.0, 9.5, 10.0]
    for t, slot in ((8.5, "ninja_broad@b21"), (9.0, "ninja_broad@b22"), (9.5, "ninja_broad@b23"), (10.0, "ninja_broad@b23")):
        assert samples[t] == [round(v, 2) for v in keys[slot]["points"]["torso"]]
    states = {s["id"]: s["conditions"] for s in ENVELOPE["nodes"]["states"]["items"] if s["subject"]["id"] == "kunai"}
    assert states["kunai@b22"]["embedded"] == "embedded" and states["kunai@end"]["holder"] == "ninja_lean"
    assert "kunai stays in B shoulder NOT released" in SOURCE and "B catches A left elbow with both hands" in SOURCE


def test_the_named_contacts_carry_their_combat_verbs():
    assert {c["id"]: c["verb"] for c in ENVELOPE["nodes"]["contacts"]["items"] if c.get("verb")} == CONTACT_VERBS


# Owner O73 (backlog M9-09a; rule R-33): the Shape quality of six intervals contradicted their bodies' path and form;
# each now names what the body does (the five airborne turns are not judged, O76).
SHAPE_REWRITES = {"ninja_broad@b06-b07": "rising", "ninja_broad@b15-b16": "rising", "ninja_lean@b15": "rising",
                  "ninja_broad@b17": "spreading", "ninja_lean@b18": "retreating", "ninja_broad@b19-b21": "advancing"}


def test_six_shape_qualities_follow_their_bodies():
    shapes = {e["id"]: e["shape"]["quality"] for e in ENVELOPE["nodes"]["efforts"]["items"]}
    assert {i: shapes[i] for i in SHAPE_REWRITES} == SHAPE_REWRITES


# Owner O74 (backlog M9-09b; rule R-33): the golden's aerial spans hang longer than gravity allows; each declares its
# stylised anime hang time on its airborne keys.
HANG_SPANS = {"ninja_lean": [(1.1, 3.0), (4.4, 5.9), (5.9, 7.5), (8.0, 9.0)], "ninja_broad": [(4.7, 6.3)]}


def test_the_aerial_spans_declare_their_hang_time():
    floats = sorted((n["entity"], n["t"]) for n in ENVELOPE["nodes"]["kinematic"]["items"] if n.get("float"))
    assert {entity for entity, _ in floats} == set(HANG_SPANS)
    assert all(any(t0 < t < t1 for t0, t1 in HANG_SPANS[entity]) for entity, t in floats)


# Owner O91 (RV-07, F-082): the smoke bursts at 3.7 at A's body ("3.7 A deploys smoke pellet at current position ...
# SMOKE BURST") and the spent pellet falls and rests: it leaves A's right hand at 3.7 (O89, S-039) and lies on the ground
# from 4.0, so it does not rest in the air (O78, F-065). S-024 had it burst on landing at 4.0, the reverse of O78's order.
PELLET = [(3.7, [1.18, 0.99, 4.85], [0, -1.83, 0]), (4.0, [1.18, 0.0, 4.85], [0, 0, 0])]
PELLET_STATES = ["3.7 smoke sealed->burst", "4 location unknown->ground"]


def test_the_smoke_bursts_at_a_s_body_and_the_spent_pellet_falls_and_rests():
    samples = sorted((s["t"], s["p"], s["v"]) for b in ENVELOPE["nodes"]["beats"]["items"]
                     for s in b.get("prop_samples", []) if s["prop"] == "smoke_pellet")
    assert samples == PELLET
    assert REFERENCE["smoke_pellet"][1].startswith("3.7 A deploys smoke pellet") and "SMOKE BURST" in REFERENCE[
        "smoke_pellet"][1]
    assert all(row in SPEC["smoke_pellet"] for row in PELLET_STATES)


def test_render_txt_is_the_render_node():
    assert (FOLDER / "render.txt").read_text(encoding="utf-8") == TEXT + "\n"


# RV-48a (F-138, F-165; owner O12, O48): the substitution swaps the log into A's former place at its start, 3.7, as the
# source deploys it "at A former position"; the swap needs no hand, so A's touch of the log at 3.7 went (it missed by
# 0.8 m once the log had a sample there).
LOG_SWAP = (3.7, [0.4, 1.0, 4.7])


def test_the_log_takes_a_s_place_at_the_swap():
    samples = {s["t"]: s["p"] for b in ENVELOPE["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])
               if s["prop"] == "substitution_log"}
    assert samples[LOG_SWAP[0]] == LOG_SWAP[1] and samples[0.0] == [0.4, 1.0, 5.3]
    assert REFERENCE["substitution_log"][1].startswith("3.7 A deploys substitution log at A former position")
    assert not any(c["a"]["id"] == "ninja_lean" and c["b"]["id"] == "substitution_log"
                   for c in ENVELOPE["nodes"]["contacts"]["items"])


# RV-62 (F-163, F-105; owners O23, O8, O83): the source holsters the volley "in B right thigh pouch" and throws it "from
# B right hand" at 5.5, with no draw between; B draws it at 5.1, its key in A's backflip beat, where the repo's own
# pose ("arms flung wide", no source row) now reaches the right hand to the thigh pouch, and lets it go with the throw.
# RV-68 (F-182): the volley waits in the pouch, on the thigh's outer side a quarter of the way from the hip, and the
# hand meets it there from outside the thigh, so the draw is measured, not placed on the hand.
VOLLEY_DRAW = (5.1, 5.5, [-1.18, 1.97, 4.2])
DRAW_POSE = {"RA": [30, -15, 0], "RFA": [-45, 0, 0]}


def test_b_draws_the_volley_before_throwing_it():
    held = {(c["contact_type"], c["t"]) for c in ENVELOPE["nodes"]["contacts"]["items"]
            if c["b"]["id"] == "shuriken_volley" and c["a"]["id"] == "ninja_broad" and c["body_part"] == "right_hand"}
    assert held == {("possess", VOLLEY_DRAW[0]), ("touch", VOLLEY_DRAW[1]), ("release", VOLLEY_DRAW[1])}
    key = next(k for k in ENVELOPE["nodes"]["motion"]["items"] if k["id"] == "ninja_broad@b13")
    assert {joint: key["bones"][joint] for joint in DRAW_POSE} == DRAW_POSE
    samples = {s["t"]: s["p"] for b in ENVELOPE["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])
               if s["prop"] == "shuriken_volley"}
    assert samples[VOLLEY_DRAW[0]] == VOLLEY_DRAW[2] and "holstered in B right thigh pouch" in SOURCE
    from solver import forward_kinematics as fk
    metres, radii = fk.segments("anime"), fk.radii("anime")
    joints = fk.joints(key, metres)
    hip, knee, hand = joints["right_hip"], joints["right_knee"], joints["right_hand"]
    pouch = math.dist(VOLLEY_DRAW[2], fk.closest(VOLLEY_DRAW[2], hip, knee)) - radii["thigh"]
    assert abs(pouch) <= 0.02  # the volley rests on the thigh's surface
    assert math.dist(hand, fk.closest(hand, hip, knee)) - radii["thigh"] >= radii["forearm"]  # the hand stays outside it
    assert math.dist(hand, VOLLEY_DRAW[2]) <= 0.15  # and meets the pouch (owner O72)
    text = RENDER["prose"]["mixed"]["text"]
    assert "B's right hand is empty from 2.00 until 5.10" in text and "B's right hand is empty from 5.50 until 6.60" in text
    assert "5.10 flight holstered -> drawn, holder none -> B" in text and "5.50 flight drawn -> flying" in text


# RV-15a (F-090, S-076; owners O72, O92): the shots VERTICAL_FRAMING or the moved aim refused, re-authored with the
# least printed change; each changed field as S-076 left it (typed as DEV-32, RV-100).
REAUTHORED_SHOTS = {"c02": {"framing.scale": "extreme_wide", "position.distance_m": 7.5},
                    "c05": {"position.distance_m": 3.5}, "c07": {"composition.placement.ninja_broad": "right_third"},
                    "c08": {"composition.placement.ninja_lean": "left_third"}, "c11": {"position.distance_m": 2.3},
                    "c12": {"position.distance_m": 2.1}, "c16": {"composition.placement.ninja_broad": "center"},
                    "c18": {"composition.placement.ninja_broad": "center"},
                    "c19": {"framing.scale": "medium_wide", "position.distance_m": 3.0},
                    "c20": {"position.distance_m": 1.95}, "c22": {"composition.placement.ninja_broad": "center"}}
# RV-14a (F-089, S-078; owner O72): B's lunge at 3.4 and 3.7 plants its front sole by the hip alone, a hand choice
# (typed as DEV-33, RV-100).
B_LUNGE = {"ninja_broad@b08": {"LUL": [-70.17, 1.29, 22.95]}, "ninja_broad@b09": {"LUL": [-65.7, 2.7, 23.3]}}


def test_the_re_authored_shots_and_the_lunge_are_what_the_records_say():
    """F-212 (RV-100): the shots S-076 re-authored and the lunge S-078 re-posed are held to their records, so a change
    to either is a change to a typed deviation."""
    shots = {s["id"]: s for s in json.loads((FOLDER / "plans" / "camera.json").read_text(encoding="utf-8"))["shots"]}
    for shot, fields in REAUTHORED_SHOTS.items():
        for path, value in fields.items():
            node = shots[shot]
            for step in path.split("."):
                node = node[step]
            assert node == value, (shot, path)
    keys = {k["slot"]: k for k in json.loads((FOLDER / "plans" / "motion.json").read_text(encoding="utf-8"))["keys"]}
    assert {slot: {joint: keys[slot]["bones"][joint] for joint in bones} for slot, bones in B_LUNGE.items()} == B_LUNGE


def test_every_recorded_deviation_is_typed_and_ruled():
    """RV-45 (F-128, R-17, R-33; docs/prompts/no_shortcuts.md): each of this test's records is a typed deviation in
    examples/reference_fight/deviations.yaml, and each names rulings that exist as ADR files."""
    import re

    import yaml
    registry = yaml.safe_load((FOLDER / "deviations.yaml").read_text(encoding="utf-8"))
    own = Path(__file__).read_text(encoding="utf-8")
    records = set(re.findall(r"(?m)^([A-Z][A-Z_]+) = ", own)) - {"FOLDER", "ENVELOPE", "RENDER", "TEXT", "SPEC", "SOURCE",
                                                                    "REFERENCE"}
    entries = {d["record"]: d for d in registry["deviations"]}
    assert records == set(entries) | set(registry["aggregates"])
    assert len({d["id"] for d in registry["deviations"]}) == len(registry["deviations"])
    decisions = {p.name.split("-", 2)[0] + "-" + p.name.split("-", 2)[1] for p in (ROOT / "docs" / "decisions").glob("ADR-*.md")}
    for entry in registry["deviations"]:
        assert entry["type"] in registry["types"] and entry["rulings"], entry["id"]
        assert set(entry["rulings"]) <= decisions, (entry["id"], set(entry["rulings"]) - decisions)
    known = {d["id"] for d in registry["deviations"]}
    assert all(set(ids) <= known for ids in registry["aggregates"].values())

