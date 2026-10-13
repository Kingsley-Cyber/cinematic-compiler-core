"""Owner O111 (2026-10-12) removed O97's length caps: a prompt's length never refuses its delivery."""

import pytest

from validators import checklist

pytestmark = pytest.mark.unit


def test_a_long_prompt_is_not_refused_for_its_length():
    assert checklist.deliverable([checklist.PASS], " ".join(["tenletters"] * 12000))
    assert not checklist.deliverable([checklist.PASS, checklist.FAIL], "a short prompt")
