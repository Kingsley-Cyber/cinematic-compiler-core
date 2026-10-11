"""S16.6 golden: the LBN reference fight compiles from its preface + cards + in-session plans, and the render
contains every kernel and reference-fight item, carries A's reference roots exactly, and keeps its anime directives."""

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


def test_every_kernel_and_reference_item_is_in_the_render():
    items = load_kernel("invariants")["items"]
    printed = [i for i in items if i["origin"] != "owner"]
    scopes = ("kernel", "kernel_actor", "kernel_prop", "scene_reference")
    counts = {scope: sum(i["scope"] == scope for i in printed) for scope in scopes}
    assert counts == {"kernel": 20, "kernel_actor": 6, "kernel_prop": 5, "scene_reference": 37}
    assert [i["id"] for i in printed if i["text"] not in TEXT] == []
    assert RENDER["coverage"]["complete"] and RENDER["coverage"]["constraints"]["enforced_by_renderer"] == ["c_k_owner_00"]


def test_a_roots_and_joints_are_the_reference_rows_exactly():
    assert RENDER["labels"] == {"ninja_lean": "A", "ninja_broad": "B"}
    reference = [row for row in REFERENCE["A"] if row[0] < 10]  # the 10.0 hold row has no beat (beats end at 10)
    assert [[row["t"], row["label"], row["pos"], row["rot"], row["joints"]] for row in SPEC["A"]] == \
        [[row[0], row[1].lower(), row[2], row[3], row[4]] for row in reference]
    assert all(row["desc"].endswith(ref[5]) for row, ref in zip(SPEC["A"], reference, strict=True))


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
    assert anime["ink"] == REFERENCE["anime"]["ink"] and fx(anime["fx"]) == fx(REFERENCE["anime"]["fx"])
    assert len(SPEC["cam"]) == 21 and (SPEC["fps"], SPEC["dur"]) == (24, 10.0)


def test_render_txt_is_the_render_node():
    assert (FOLDER / "render.txt").read_text(encoding="utf-8") == TEXT + "\n"
