"""M5.E: the UGC glasses demo compiles through S16; the ugc renderer carries every UGC graph item."""

import json

import pytest
from conftest import ROOT

from compiler.passes.derived import p16_render
from renderers import anime_renderer, ugc_renderer
from validators.envelope_validator import validate_envelope

pytestmark = pytest.mark.integration
FOLDER = ROOT / "examples" / "ugc_glasses_demo"
ENVELOPE = json.loads((FOLDER / "envelope.json").read_text(encoding="utf-8"))
RENDER = ENVELOPE["nodes"]["render"]["items"][0]
SPEC = json.loads(RENDER["text"][RENDER["text"].index("{"):])


def test_complete_valid_envelope_with_every_ugc_group():
    assert validate_envelope(ENVELOPE) == {"ok": True, "complete": True, "findings": []}
    for group in ("hand_role", "object_state", "affordance"):
        row = RENDER["coverage"]["groups"][group]
        assert row["items"] == row["rendered"] > 0, group
    assert RENDER["coverage"]["complete"]


def test_ugc_block_replaces_the_anime_block():
    assert p16_render.renderer(ENVELOPE) is ugc_renderer and "anime" not in SPEC and list(SPEC)[-2:] == ["ugc", "rules"]
    ugc = SPEC["ugc"]
    assert [row.split(" ")[2] for row in ugc["hand_roles"]] == ["unfold", "put_on"] and "no swap" in ugc["hand_roles"][0]
    assert ugc["affordances"][1].startswith("i02 put_on glasses: before temples:open|worn:no -> after temples:open|worn:yes")
    assert ugc["enables"] == ["i01 enables i02 via temples"] and ugc["frames"]["holds"] == [[5.5, 12]]


def test_product_shot_and_jump_cut_follow_the_ugc_card():
    shots = ENVELOPE["nodes"]["camera"]["items"]
    assert {s["intent"] for s in shots} >= {"product"} and shots[-1]["editing"]["transition_in"] == "jump_cut"
    assert all(s["position"]["side"] == "none" for s in shots)  # one entity: no action axis


def test_anime_scenes_keep_the_anime_renderer():
    courtyard = json.loads((ROOT / "examples" / "wizard_vs_acrobat" / "envelope.json").read_text(encoding="utf-8"))
    assert p16_render.renderer(courtyard) is anime_renderer
