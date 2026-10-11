"""M8.2 structured-prose prompts (owner O1-O3): Master Template sections, one staff line per slot, Euler blocks per mode,
root exact left out of the prose only, every other rule and negative carried."""

import json
import re

import pytest
from conftest import ROOT

from renderers import prose_renderer
from renderers.anime_renderer import constraint_rows

pytestmark = pytest.mark.unit
EXAMPLES = sorted(p for p in (ROOT / "examples").iterdir() if (p / "render.txt").exists())
SECTIONS = ("[SCENE]", "[MOVEMENT LANGUAGE]", "[LABAN STAFF – ", "[RULES]", "[NEGATIVES]")
LINE = re.compile(r"^\d+\.\d\d [A-Z]: SUPPORT ")


def load(folder):
    envelope = json.loads((folder / "envelope.json").read_text())
    return envelope, envelope["nodes"]["render"]["items"][0]


def staff(text):
    return [line for line in text.splitlines() if LINE.match(line)]


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_four_modes_with_sections_in_order_and_one_line_per_slot(folder):
    envelope, render = load(folder)
    assert set(render["prose"]) == set(prose_renderer.MODES)
    slots = len(envelope["nodes"]["motion"]["items"])
    for mode, row in render["prose"].items():
        text = row["text"]
        assert (folder / f"prose_{mode}.txt").read_text() == text
        positions = [text.index(s) for s in SECTIONS]
        assert positions == sorted(positions) and positions[0] == 0, mode
        assert len(staff(text)) == slots, mode


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_euler_blocks_sit_on_the_lines_each_mode_names(folder):
    _, render = load(folder)
    lines = {mode: staff(row["text"]) for mode, row in render["prose"].items()}
    assert not any("Root [" in line for line in lines["pure_staff"])
    assert all("Root [" in line and "Joints {" in line for line in lines["euler_heavy"])
    last = {}
    for i, line in enumerate(lines["pure_staff"]):
        last[line.split(":")[0].split(" ")[1]] = i
    first = {}
    for i, line in enumerate(lines["pure_staff"]):
        first.setdefault(line.split(":")[0].split(" ")[1], i)
    for i, line in enumerate(lines["pure_staff"]):
        strike = "[DOUBLE BOW + accent:" in line
        assert ("Root [" in lines["mixed"][i]) == (strike or i in first.values() or i in last.values())
        assert "Joints {" not in lines["mixed"][i]
        assert ("Joints {" in lines["upgraded_mixed"][i]) == (strike or i in last.values())
        assert lines["mixed"][i].startswith(line) and lines["euler_heavy"][i].startswith(line)


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_root_exact_only_in_lbn_and_every_other_rule_and_negative_in_the_prose(folder):
    envelope, render = load(folder)
    _, rows = constraint_rows(envelope, render["labels"])
    root_exact = {cid for _, _, cid, ref in rows if ref == prose_renderer.ROOT_EXACT}
    assert root_exact and "root exact" in render["text"]
    for mode, row in render["prose"].items():
        assert row["omitted_constraints"] == sorted(root_exact)
        assert "root exact" not in row["text"]
        body = row["text"]
        for section, text, _, ref in rows:
            if section in ("rules", "negative", "preface", "ax", "key") and ref != prose_renderer.ROOT_EXACT:
                if section == "key" and mode in ("pure_staff", "mixed"):
                    continue
                assert text in body, (mode, section, text)
        lead = ("Follow the SUPPORT column and the contact bows strictly" if mode == "pure_staff"
                else "Laban support and contacts are primary; Euler numbers are precision override only.")
        assert lead in body


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_every_entity_has_its_anchor_phrase_in_scene(folder):
    envelope, render = load(folder)
    scene = render["prose"]["mixed"]["text"].split("[MOVEMENT LANGUAGE]")[0]
    for entity in envelope["nodes"]["entities"]["items"]:
        assert f"{render['labels'][entity['id']]} = {entity['name']}: {entity['silhouette'].rstrip('.')}" in scene


def test_reference_strikes_are_the_impacts_on_other_bodies_and_free_props():
    _, render = load(ROOT / "examples" / "reference_fight")
    strikes = [line.split(" | ")[0].split(":")[0] for line in staff(render["prose"]["pure_staff"]["text"])
               if "[DOUBLE BOW + accent:" in line]
    assert {"2.50 A", "4.70 A", "6.60 B", "8.50 B"} <= set(strikes)
    text = render["prose"]["pure_staff"]["text"]
    assert "[DOUBLE BOW + accent: R foot > kunai blade at 3.00]" in text
    assert "chain " in next(line for line in staff(text) if line.startswith("2.50 A"))


def test_the_prose_is_a_pure_function_of_the_envelope():
    envelope, render = load(ROOT / "examples" / "ugc_glasses_demo")
    again = prose_renderer.render_all(envelope, render["frame_parts"], render["labels"])
    assert again == render["prose"]
    assert "FACE:" in render["prose"]["pure_staff"]["text"]
    assert not re.search(r"\bAU\s?\d", render["prose"]["pure_staff"]["text"])  # faces in words only (owner F4)
