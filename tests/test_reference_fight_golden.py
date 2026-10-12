"""S16.6 golden: the LBN reference fight compiles from its preface + cards + in-session plans, and the render
contains every kernel and reference-fight item, carries A's reference roots exactly and its joints with the recorded
deviations (owner O7/O10/O11), and keeps its anime directives."""

import json

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
REWORDED = {**PREFACE_RECOUNTED, **GROUNDED_RULES, **START_HEIGHT}


def test_every_kernel_and_reference_item_is_in_the_render():
    items = load_kernel("invariants")["items"]
    printed = [i for i in items if i["origin"] != "owner"]
    scopes = ("kernel", "kernel_actor", "kernel_prop", "scene_reference")
    counts = {scope: sum(i["scope"] == scope for i in printed) for scope in scopes}
    assert counts == {"kernel": 20, "kernel_actor": 6, "kernel_prop": 5, "scene_reference": 37}
    assert [i["id"] for i in printed if REWORDED.get(i["id"], i["text"]) not in TEXT] == []
    assert [i["id"] for i in printed if i["id"] in REWORDED and i["text"] in TEXT] == []  # the rewording replaced them
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]


# Recorded deviations from the reference numbers, both owner decisions of 2026-10-11 (O7, O10 + O11):
# - knee flexion is +X under Q6, so the reference's negative knee angles (a hyperextended knee) read as +|x|;
# - the right hip at 1.1 and 3.0 (+90 = 90 degrees back) is clamped to the anime extension limit, +60.
HIP_CLAMPS = {1.1: 60, 3.0: 60}
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
# on the ground at 7.5 and A crouches at the kunai, which lands at [0.6, 0, 4.0] since O77, the right hand on it at 8.0
# (each within 0.15 m; the least change of root, crouch and arm, both soles on the ground).
GROUNDED_PICKUPS = {  # O18: A's rows at the two pickups, crouched on the ground (from A's own crouches at 5.9 and 9.5)
    7.5: [7.5, "rope_dart_regrapple", [-0.07, 0.57, 3.51], [-330, 30, -360],
          {"Sp": [59.6, 0, 0], "LUL": [-110.2, 0, 0], "RUL": [-108.5, 0, 0], "LL": [104.6, 0, 0], "RL": [108, 0, 0],
           "LA": [-65.1, -4, 0], "RA": [-45, 0, 0], "LFA": [-27, 0, 0], "RFA": [-45, 0, 0], "HD": [-10, 0, 0], "NK": [0, 0, 0]}],
    8.0: [8.0, "pull_b_toward_pillar", [0.11, 0.59, 4.23], [-330, 90, -360],
          {"Sp": [85.6, 0, 0], "LUL": [-104.1, 0, 0], "RUL": [-100.6, 0, 0], "LL": [89.8, 0, 0], "RL": [97.5, 0, 0],
           "LA": [-60, 0, 0], "RA": [-68.2, 14.8, 0], "LFA": [-30, 0, 0], "RFA": [-27.9, 0, 0], "HD": [-10, 0, 0],
           "NK": [0, 0, 0]}],
}
# ADR-O83 point 2: the source's one real miss, kept as the owner wrote it and listed in the motion plan with its reason.
CONTACT_EXCEPTIONS = {"b06_c3"}  # 3.0, A's right foot 1.5 m over the ground (RUL +90 against 'R: leg fwd mid')


GROUNDED_DESCRIPTIONS = {
    7.5: "L:arm fwd low bent1 taking the rope dart from the ground, leg fwd mid bent7, lLeg bent7; R:arm fwd mid bent3, leg "
         "fwd mid bent7, lLeg bent7; support=both feet; A LANDS CROUCHED BY THE ROPE DART and takes it with the left hand, "
         "then whips it forward to wrap B right shoulder, head facing B, this is a GRAPPLE NOT a strike",
    8.0: "L:arm fwd mid bent3 holding rope dart taut, leg fwd mid bent7, lLeg bent7; R:arm fwd low bent1 taking the kunai "
         "from the ground, leg fwd mid bent7, lLeg bent7; support=both feet; A CROUCHES BY THE KUNAI, the right hand takes "
         "it from the ground while the left hand hauls the taut rope dart, B dragged toward the pillar at z=6, this is a "
         "PULL NOT a strike",
}


# Owner O21 (audit X7, backlog M9-08a): the pillar keeps its 8 m top, so A starts above the frame at root y=10 and lands
# with the feet on the top at y=8, root 8.5; the source's rows start A at 7.5 and land it at 7.2, under the top. S-029
# (O72, O82, O85): the landing root re-rooted to 8.71 so the soles meet the top under the anime body (O84).
OPENING = {0: [0, 10, 3.5], 0.6: [0, 8.71, 5.8]}
OPENING_WORDS = {0.6: ("both feet on pillar top y=7.2", "both feet on pillar top y=8")}


def normalised(row):
    joints = {j: list(v) for j, v in row[4].items()}
    for knee in ("LL", "RL"):
        joints[knee][0] = abs(joints[knee][0])
    if row[0] in HIP_CLAMPS:
        joints["RUL"][0] = HIP_CLAMPS[row[0]]
    if row[0] in GROUNDED_PICKUPS:
        return GROUNDED_PICKUPS[row[0]]
    rot = list(row[3])
    for after, axis, degrees in ROOT_TURNS:
        if row[0] > after:
            rot[axis] += degrees
    return [row[0], row[1].lower(), OPENING.get(row[0], row[2]), rot, joints]


# S-030 (CONTACT_WORLD, ADR-O83, R-33): the repo-authored side of each real miss moved. The rope dart's sample at 3.0 sits
# in A's left hand (the source's pose); at 8.0 it is the dart, wrapped on B since 7.6, so it sits on B's torso while A
# keeps the rope's end; B steps in and straightens to catch A's elbow at 6.6 with both hands.
REBLOCKED_SAMPLES = {("rope_dart", 3.0): [0.85, 0.74, 4.55], ("rope_dart", 8.0): [1.6, 1.53, 3.7]}  # 8.0: with B, O86
CATCH_ROOT = [0.13, 1.2, 4.87]
# Owner O86 (F-071, S-032): at 8.0 B stands on A's far side from the pillar (z 6), pose and facing kept, so the rope from
# B to A's hand pulls toward the pillar and B is dragged that way to 8.5.
PULL_ANCHOR = [1.4, 1.18, 3.7]


def test_the_pull_at_8_runs_toward_the_pillar():
    keys = {k["id"]: k for k in ENVELOPE["nodes"]["motion"]["items"]}
    a, b, later = (keys[slot]["pos"] for slot in ("ninja_lean@b20", "ninja_broad@b20", "ninja_broad@b21"))
    assert b == PULL_ANCHOR and a[2] > b[2] and later[2] > b[2]               # the rope and the drag both point to +z


def test_the_re_blocked_samples_and_the_catch_are_recorded():
    samples = {(s["prop"], s["t"]): s["p"] for b in ENVELOPE["nodes"]["beats"]["items"] for s in b.get("prop_samples", [])}
    assert {k: samples[k] for k in REBLOCKED_SAMPLES} == REBLOCKED_SAMPLES
    keys = {k["id"]: k for k in ENVELOPE["nodes"]["motion"]["items"]}
    assert keys["ninja_broad@b17"]["pos"] == CATCH_ROOT


def test_contact_world_excepts_only_the_source_miss():
    plan = json.loads((ROOT / "examples" / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    assert set(plan["contact_world_exceptions"]) == CONTACT_EXCEPTIONS
    assert all("O83" in reason for reason in plan["contact_world_exceptions"].values())


def test_a_roots_and_joints_are_the_reference_rows_with_the_recorded_deviations():
    assert RENDER["labels"] == {"ninja_lean": "A", "ninja_broad": "B"}
    reference = [row for row in REFERENCE["A"] if row[0] < 10 and row[0] not in VANISHED]  # 10.0 hold: no beat
    assert [[row["t"], row["label"], row["pos"], row["rot"], row["joints"]] for row in SPEC["A"]] == \
        [normalised(row) for row in reference]
    assert all(row["desc"].endswith(ref[5].replace(*OPENING_WORDS.get(row["t"], ("", ""))))
               for row, ref in zip(SPEC["A"], reference, strict=True) if row["t"] not in GROUNDED_PICKUPS)
    assert all(old in ref[5] for t, (old, _) in OPENING_WORDS.items() for ref in reference if ref[0] == t)
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
    assert len(SPEC["cam"]) == 21 and (SPEC["fps"], SPEC["dur"]) == (24, 10.0)


# Owner O48 (2026-10-11, probes R12 and R17, as in R1-R5): the source keeps the log 'hidden in A coat' until 3.7, but the
# model draws a later object from the start whatever the prompt says. The log stands beside A as a post from 0.0 and is
# deployed into A's place in the smoke at the substitution (card state 'standing').
SUBSTITUTION_POST = ["0 deployment=standing,holder=none,location=ground", "0 p[0.4,1,5.3] at rest"]


def test_the_substitution_log_stands_as_a_post_from_the_start():
    assert REFERENCE["substitution_log"][0].startswith("0.0 not present,hidden in A coat")
    assert SPEC["substitution_log"][:2] == SUBSTITUTION_POST
    assert "4 deployment standing->deployed" in SPEC["substitution_log"]


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
# is the source's own v_post [0.5,-4.0,-3.0], so the kunai lands at 2.7 on [0.6,0,4.0] and A takes it there at 8.0.
DEFLECT_PAIR = ["2.5 pre-contact p[0.5,1,4.6] v[-1.4,-3.46,0.2] moving down along -X",
                "2.5 post-contact p[0.5,1,4.6] v[0.5,-4,-3] moving down along -Z"]


def test_the_kunai_deflect_is_a_pre_and_post_pair():
    assert [row for row in SPEC["kunai"] if "-contact " in row] == DEFLECT_PAIR


# Owner O22 (plan F4.1, backlog M9-07a; ADR-O71 rule 1): the contacts the golden's own words name carry their combat
# verb ('B THROWS KUNAI', 'FOOT DEFLECT', 'palm hits log', 'knee strike', 'throw shuriken volley').
CONTACT_VERBS = {"b05_c1": "throw", "b06_c1": "deflect", "b10_c1": "strike", "b12_c1": "strike", "b14_c1": "throw"}


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


# Owner O78 (F-065, backlog M9-09e): the smoke pellet does not rest in the air; A's hand throws it down at 3.7 and it
# bursts on the ground at 4.0 (the source's burst time) and stays there.
PELLET = [(3.7, [0.4, 1.1, 4.7], [0, -2.2, 0]), (4.0, [0.4, 0.0, 4.7], [0, 0, 0])]


def test_the_smoke_pellet_falls_and_bursts_on_the_ground():
    samples = sorted((s["t"], s["p"], s["v"]) for b in ENVELOPE["nodes"]["beats"]["items"]
                     for s in b.get("prop_samples", []) if s["prop"] == "smoke_pellet")
    assert samples == PELLET


def test_render_txt_is_the_render_node():
    assert (FOLDER / "render.txt").read_text(encoding="utf-8") == TEXT + "\n"
