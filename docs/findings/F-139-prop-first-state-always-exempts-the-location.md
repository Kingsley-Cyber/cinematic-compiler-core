# F-139 — PROP_FIRST_STATE always exempts the location

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

## Layer
L2.1

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- validators/continuity_validator.py exempts `location` for every prop; its docstring limits that to a prop held or hidden
- the rope dart, the smoke pellet and the shuriken start with holder none and location unknown

## Description
A free prop can start nowhere.

## Impact
The prompt cannot say where it is at the start.

## Proposed Fix
Backlog RV-48a: exempt the location only while the prop is held or carried.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
RV-48a (S-057): PROP_FIRST_STATE exempts a prop's unknown first location only while it is held or carried
(validators/continuity_validator.py; tests/test_state_pass.py::test_a_free_prop_starts_somewhere); the test scene's
cup starts on the ground.
