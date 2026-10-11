"""M3.5 F.8b/F.9b: the live-action standoff compiles through S17 with faces and the live-action layout."""

import json
import re

import pytest
from conftest import ROOT

from compiler.passes.derived import p17_render
from renderers import live_renderer
from validators.envelope_validator import validate_envelope

pytestmark = pytest.mark.integration
FOLDER = ROOT / "examples" / "live_action_standoff"
ENVELOPE = json.loads((FOLDER / "envelope.json").read_text(encoding="utf-8"))
RENDER = ENVELOPE["nodes"]["render"]["items"][0]
SPEC = json.loads(RENDER["text"][RENDER["text"].index("{"):])


def test_complete_live_action_envelope_with_faces():
    assert validate_envelope(ENVELOPE) == {"ok": True, "complete": True, "findings": []}
    assert ENVELOPE["scene"]["genre"] == "live_action" and len(ENVELOPE["nodes"]["facial"]["items"]) == 8
    assert RENDER["coverage"]["groups"]["facial"] == {"items": 8, "rendered": 8, "missing": []}


def test_live_action_layout_puts_frame_parts_under_frames():
    assert p17_render.renderer(ENVELOPE) is live_renderer
    assert "frames" in SPEC and "anime" not in SPEC and list(SPEC)[-2:] == ["frames", "rules"]


def test_the_three_faces_that_carry_beats_reach_the_prompt_in_words():
    faces = {f["id"]: f for f in ENVELOPE["nodes"]["facial"]["items"]}
    carried = sorted(i for i, f in faces.items() if f["salience"] == "carries_beat")
    assert carried == ["knight@b01", "knight@b03", "wizard@b02"]
    assert faces["wizard@b02"]["aus"][0]["asymmetry"]["pattern"] == "contempt"
    assert (faces["knight@b03"]["onset"], faces["knight@b03"]["display_rule"]) == ("micro", "suppressed")
    text = RENDER["text"]
    assert "lip corners pulled up on their left side only (slight)" in text and "holding it back" in text
    assert not re.search(r"\bAU\s?\d", text)
