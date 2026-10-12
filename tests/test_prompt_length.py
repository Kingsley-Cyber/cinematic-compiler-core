"""PROMPT_LENGTH (owner O97, RV-13, F-088): a prompt is delivered only within a documented target's cap; the cap
refuses delivery, not conformance (owner O10 keeps the golden's conformance with nothing set aside)."""

import json

import pytest
from conftest import ROOT

from validators import checklist, prompt_length

pytestmark = pytest.mark.unit


def test_the_caps_are_the_owner_s():
    assert prompt_length.CAPS == {"Runway": ("characters", 3500), "BytePlus": ("words", 1000)}
    short = " ".join(["word"] * 600)  # 2,999 characters, 600 words
    assert prompt_length.fits(short) == ["Runway", "BytePlus"] and prompt_length.problems(short) == []
    terse = " ".join(["tenletters"] * 900)  # 9,899 characters, 900 words
    assert prompt_length.fits(terse) == ["BytePlus"] and prompt_length.problems(terse) == []
    long = " ".join(["tenletters"] * 1200)
    assert prompt_length.fits(long) == []
    assert prompt_length.problems(long) == [("PROMPT_LENGTH", "13,199 characters over Runway's 3,500; 1,200 words over "
                                                              "BytePlus's 1,000 (owner O97)")]


def test_no_example_prompt_is_delivered_until_the_prompts_fit():
    """O97 with F-088: every prompt today is over both caps, so `cinematic compile` refuses each one and names its
    length (PROMPT_LENGTH); fitting them waits for the owner (RV-13b)."""
    envelope = json.loads((ROOT / "examples" / "ugc_glasses_demo" / "envelope.json").read_text(encoding="utf-8"))
    refused = checklist.refusals(envelope)
    assert len(refused) == 5 and all("PROMPT_LENGTH: " in line for line in refused)
    assert not checklist.deliverable([checklist.PASS], " ".join(["tenletters"] * 1200))
    assert checklist.deliverable([checklist.PASS], "a short prompt")
