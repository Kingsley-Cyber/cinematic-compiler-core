# F-119 — The anti-reward-hacking clause and R-33: does a recorded deviation count as the owner's ask?

<!-- docs-version: 1.0 -->

## Type
question

## Severity
high

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- AGENTS.md section 18 (ADR-O100), rule 1: tests, fixtures and expected outputs are immutable "unless the user explicitly
  asks to change them"; rule 5: if the specification and tests conflict, stop and report
- R-33 (ADR-O75): "A slice may rewrite the examples so they pass its own new check, as recorded deviations (the golden
  test and the session file), without a ruling per change"
- past slices moved test pins along with data a ruling moved (S-029: tests/test_render.py, tests/test_state_pass.py,
  tests/test_dynamic_beat_validator.py; S-030: tests/test_leg_frame_rewrites.py, tests/test_reference_fight_golden.py)

## Description
The clause makes tests immutable without the owner's explicit ask, while R-33 lets a slice record deviations in the
golden test without a ruling per change, and slices have also moved other test pins when a ruling moved the data they
pin. Questions: (1) does a ruling that says "record each as an R-33 deviation" (as O88 does) count as the explicit ask?
(2) may a slice change a pin that holds data its ruling moves (a root height the ruling raised), or must it stop and
report each one? (3) does R-33 itself still stand?

## Impact
Step 3 changes data the golden test and other tests pin; the answer decides whether each such pin stops the slice.

## Proposed Fix
Until the owner answers: a test changes only where a ruling explicitly asks for the record; any other test a change
would break stops the slice and is reported.

## Owner Ruling
none yet

## Related
- ADR-O100
- ADR-O75
- PLAN-007

## Resolution
Open.
