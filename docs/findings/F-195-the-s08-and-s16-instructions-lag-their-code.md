# F-195 — The S08 and S16 instructions lag their code again

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
L2.5

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- planner/prompts/hand_roles.txt forbids undeclared hands to touch the object, not to hold it (RV-72)
- planner/prompts/camera_selection.txt lists four kinds of hit and says only "static" (RV-69's fifth kind and RV-71a's rig are missing)
- tests/test_instructions.py checks the codes' names, not what the instructions say (F-170)

## Description
Slices that changed a step's rule did not change its instructions in the same commit.

## Impact
Authors are taught yesterday's rules.

## Proposed Fix
Backlog RV-92: both instructions teach the current rules; from S-073 each slice's self-audit checks that its step's instructions teach the change.

## Owner Ruling
none needed

## Related
- RV-92
- F-162
- F-170
- RV-65

## Resolution
Open.
Noted in S-081 (the sixth review): beat_planning.txt does not teach FLOOR_PENETRATION, the every-key measure of
claimed supports, or that every weight-bearing part needs a support contact (RV-92).
