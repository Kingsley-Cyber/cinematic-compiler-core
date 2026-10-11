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


def test_every_kernel_and_reference_item_is_in_the_render():
    items = load_kernel("invariants")["items"]
    printed = [i for i in items if i["origin"] != "owner"]
    scopes = ("kernel", "kernel_actor", "kernel_prop", "scene_reference")
    counts = {scope: sum(i["scope"] == scope for i in printed) for scope in scopes}
    assert counts == {"kernel": 20, "kernel_actor": 6, "kernel_prop": 5, "scene_reference": 37}
    assert [i["id"] for i in printed if PREFACE_RECOUNTED.get(i["id"], i["text"]) not in TEXT] == []
    assert next(i["text"] for i in printed if i["id"] == "k_preface_03") not in TEXT  # the recount replaced it
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]


# Recorded deviations from the reference numbers, both owner decisions of 2026-10-11 (O7, O10 + O11):
# - knee flexion is +X under Q6, so the reference's negative knee angles (a hyperextended knee) read as +|x|;
# - the right hip at 1.1 and 3.0 (+90 = 90 degrees back) is clamped to the anime extension limit, +60.
HIP_CLAMPS = {1.1: 60, 3.0: 60}
# Owner O18 (2026-10-11, audit X9): A vanishes at 3.7 (the substitution) and reappears at 4.4, so the reference's A row
# at 4.0 (a full pose with both feet down while 'A already gone') is not drawn.
VANISHED = {4.0}
# Prop positions and velocities are authored on the beats and solved under gravity (owner O8, O10); the source's
# literal p/v (e.g. kunai thrown at 0.5 toward -Z, yet at +Z 5.0 at 2.0) are not copied, as they disagree with gravity.


def normalised(row):
    joints = {j: list(v) for j, v in row[4].items()}
    for knee in ("LL", "RL"):
        joints[knee][0] = abs(joints[knee][0])
    if row[0] in HIP_CLAMPS:
        joints["RUL"][0] = HIP_CLAMPS[row[0]]
    return [row[0], row[1].lower(), row[2], row[3], joints]


def test_a_roots_and_joints_are_the_reference_rows_with_the_recorded_deviations():
    assert RENDER["labels"] == {"ninja_lean": "A", "ninja_broad": "B"}
    reference = [row for row in REFERENCE["A"] if row[0] < 10 and row[0] not in VANISHED]  # 10.0 hold: no beat
    assert [[row["t"], row["label"], row["pos"], row["rot"], row["joints"]] for row in SPEC["A"]] == \
        [normalised(row) for row in reference]
    assert all(row["desc"].endswith(ref[5]) for row, ref in zip(SPEC["A"], reference, strict=True))


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


def test_render_txt_is_the_render_node():
    assert (FOLDER / "render.txt").read_text(encoding="utf-8") == TEXT + "\n"
