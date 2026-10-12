"""The printed leg words that changed when the hips were read from the trunk (owner O84, rule R-35; backlog M9-06c,
S-029): recorded deviations under rule R-33. Each repo-authored key that leans through Sp had its hips re-expressed
(R_hip' = R_Sp^-1 R_hip) so no point of its body moved; a leg's word is read from its own rotation, now relative to the
trunk, so 47 of the 102 repo-authored legs read differently. The source's A rows (the reference fight) are unchanged.
"""

import json

import pytest
from conftest import ROOT

from solver import staff_geometry

pytestmark = pytest.mark.unit

# (example, key, side): (the word before S-029, the word now)
LEG_WORDS = {
    ("reference_fight", "ninja_broad@b01", "right"): ("right-forward-low", "forward-low"),
    ("reference_fight", "ninja_broad@b04", "left"): ("left-forward-low", "forward-low"),
    ("reference_fight", "ninja_broad@b05", "left"): ("forward-low", "left-forward-mid"),
    ("reference_fight", "ninja_broad@b05", "right"): ("right-back-low", "place-low"),
    ("reference_fight", "ninja_broad@b06", "left"): ("left-forward-low", "forward-low"),
    ("reference_fight", "ninja_broad@b08", "left"): ("forward-mid", "left-forward-mid"),
    ("reference_fight", "ninja_broad@b08", "right"): ("right-back-low", "right-forward-low"),
    ("reference_fight", "ninja_broad@b09", "left"): ("forward-mid", "left-forward-mid"),
    ("reference_fight", "ninja_broad@b09", "right"): ("right-back-low", "right-forward-low"),
    ("reference_fight", "ninja_broad@b10", "left"): ("forward-low", "forward-mid"),
    ("reference_fight", "ninja_broad@b10", "right"): ("right-back-low", "right-forward-low"),
    ("reference_fight", "ninja_broad@b11", "left"): ("forward-low", "forward-mid"),
    ("reference_fight", "ninja_broad@b11", "right"): ("right-back-low", "right-forward-low"),
    ("reference_fight", "ninja_broad@b12", "left"): ("left-forward-low", "left-back-low"),
    ("reference_fight", "ninja_broad@b12", "right"): ("right-back-low", "back-low"),
    ("reference_fight", "ninja_broad@b13", "left"): ("left-forward-low", "left-back-low"),
    ("reference_fight", "ninja_broad@b13", "right"): ("right-back-low", "back-low"),
    ("reference_fight", "ninja_broad@b14", "left"): ("forward-mid", "left-forward-mid"),
    ("reference_fight", "ninja_broad@b14", "right"): ("right-forward-low", "forward-low"),
    ("reference_fight", "ninja_broad@b17", "left"): ("forward-low", "forward-mid"),
    ("reference_fight", "ninja_broad@b17", "right"): ("right-back-low", "right-low"),
    ("reference_fight", "ninja_broad@b19", "left"): ("left-forward-low", "left-low"),
    ("reference_fight", "ninja_broad@b20", "left"): ("forward-low", "left-forward-low"),
    ("reference_fight", "ninja_broad@b20", "right"): ("right-forward-low", "right-back-low"),
    ("reference_fight", "ninja_broad@b21", "left"): ("forward-low", "forward-mid"),
    ("reference_fight", "ninja_broad@b21", "right"): ("right-forward-low", "forward-mid"),
    ("wizard_vs_acrobat", "acrobat@b01", "left"): ("back-low", "forward-low"),
    ("wizard_vs_acrobat", "acrobat@b02", "left"): ("forward-mid", "forward-high"),
    ("wizard_vs_acrobat", "acrobat@b02", "right"): ("forward-mid", "forward-high"),
    ("wizard_vs_acrobat", "acrobat@b03", "right"): ("forward-low", "place-low"),
    ("wizard_vs_acrobat", "acrobat@b05", "right"): ("forward-mid", "right-forward-mid"),
    ("wizard_vs_acrobat", "acrobat@b06", "left"): ("forward-low", "left-forward-low"),
    ("wizard_vs_acrobat", "acrobat@b06", "right"): ("forward-mid", "right-forward-low"),
    ("wizard_vs_acrobat", "acrobat@b11", "left"): ("forward-low", "forward-mid"),
    ("wizard_vs_acrobat", "acrobat@b13", "left"): ("forward-mid", "forward-high"),
    ("wizard_vs_acrobat", "acrobat@b13", "right"): ("forward-mid", "forward-high"),
    ("wizard_vs_acrobat", "wizard@b03", "left"): ("left-forward-low", "forward-low"),
    ("wizard_vs_acrobat", "wizard@b03", "right"): ("right-back-low", "place-low"),
    ("wizard_vs_acrobat", "wizard@b06", "right"): ("right-back-low", "back-low"),
    ("wizard_vs_acrobat", "wizard@b09", "right"): ("right-back-low", "right-low"),
    ("wizard_vs_acrobat", "wizard@b10", "right"): ("right-back-low", "right-low"),
    ("wizard_vs_acrobat", "wizard@b11", "left"): ("left-forward-low", "forward-low"),
    ("live_action_standoff", "knight@b01", "right"): ("right-back-low", "place-low"),
    ("ugc_glasses_demo", "ugc_creator@b01", "left"): ("place-low", "forward-low"),
    ("ugc_glasses_demo", "ugc_creator@b01", "right"): ("place-low", "forward-low"),
    ("ugc_glasses_demo", "ugc_creator@b02", "left"): ("place-low", "left-forward-low"),
    ("ugc_glasses_demo", "ugc_creator@b02", "right"): ("place-low", "right-forward-low"),
}


def test_each_rewritten_leg_prints_its_trunk_word():
    assert len(LEG_WORDS) == 47
    keys = {}
    for name in {n for n, _, _ in LEG_WORDS}:
        envelope = json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))
        keys |= {(name, k["id"]): k for k in envelope["nodes"]["motion"]["items"]}
    for (name, slot, side), (old, new) in LEG_WORDS.items():
        assert old != new and staff_geometry.pose_words(keys[(name, slot)])[side]["leg"] == new, (name, slot, side)
