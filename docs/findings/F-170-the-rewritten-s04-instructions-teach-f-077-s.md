# F-170 — The rewritten S04 instructions teach F-077's jump and a stale first state

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L1.1

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- planner/prompts/beat_planning.txt (prop samples) and planner/dynamic_beat_validator.py's docstring: "a prop at rest does not move unless a contact on it at the second sample picks it up or knocks it down"; the code refuses that move (the F-077 comment in `_prop_kinematics`), and tests/test_dynamic_beat_validator.py pins the refusal
- beat_planning.txt's first-state example "deployment hidden", against O48's standing log (R-24)
- tests/test_instructions.py checks only that each code's name appears in the instructions

## Description
RV-48b (S-058) copied the validator's stale sentence into the instructions, and the test that closed F-162 checks names, not what the instructions say.

## Impact
An S04 author is taught a move the code refuses and a first state the owner replaced.

## Proposed Fix
Backlog RV-67: both sentences and the docstring follow the code; F-162 reopened in part.

## Owner Ruling
none needed

## Related
- RV-67
- F-162
- F-077
- ADR-O48

## Resolution
RV-67 (S-065): planner/prompts/beat_planning.txt and planner/dynamic_beat_validator.py's docstring say a resting prop
stays where it rests (a contact at the second sample takes or strikes it there, F-077), a contact between two samples
moves it only by taking hold of it, and any other move needs a sample at the contact's instant; the first-state
example reads "deployment standing" (O48). tests/test_instructions.py still checks names only; the wording is checked
by review.
