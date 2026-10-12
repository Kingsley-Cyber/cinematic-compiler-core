"""Each authoring step's instructions name every rule its plan must meet (F-162: the S04 instructions taught rules the
code had since changed; RV-48b). The codes are read from the checks' own sources, so a new rule fails here until its
step's instructions teach it. S04's plan must also meet the passes that read only it: S05, S06 and S07."""

import re

import pytest
from conftest import ROOT

pytestmark = pytest.mark.unit
EMITTED = re.compile(r'(?:_finding|add)\(\s*"([A-Z][A-Z_]+)"|"code":\s*"([A-Z][A-Z_]+)"')
PASS_CODES = {"MISSING_INPUT", "WRITE_SCOPE"}  # the pass's own contract with the envelope, not the plan's
STEPS = {
    "beat_planning.txt": ["planner/dynamic_beat_validator.py", "compiler/passes/mandatory/p05_causal.py",
                          "solver/prop_state_machine.py", "validators/continuity_validator.py",
                          "compiler/passes/mandatory/p07_contact.py"],
    "hand_roles.txt": ["compiler/passes/derived/p08_hand_role.py"],
}


def emitted(paths):
    codes = set()
    for path in paths:
        for match in EMITTED.finditer((ROOT / path).read_text(encoding="utf-8")):
            codes.add(match.group(1) or match.group(2))
    return codes - PASS_CODES


@pytest.mark.parametrize("prompt", sorted(STEPS))
def test_the_instructions_name_every_rule_the_plan_must_meet(prompt):
    text = (ROOT / "planner" / "prompts" / prompt).read_text(encoding="utf-8")
    codes = emitted(STEPS[prompt])
    assert codes and sorted(c for c in codes if not re.search(rf"\b{c}\b", text)) == []
