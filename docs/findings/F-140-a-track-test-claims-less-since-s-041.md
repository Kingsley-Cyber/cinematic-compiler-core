# F-140 — A track test claims less since S-041

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
low

## Layer
all

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
- tests/test_prop_track.py::test_a_place_set_before_a_hold_does_not_outlive_it pins "held by A R hand" since S-041; the UGC glasses have no place before their hold any more

## Description
The test keeps its name but no longer shows a place giving way to a hold.

## Impact
A claim the suite makes is not tested.

## Proposed Fix
Backlog RV-46: the test keeps its claim on a fixture with a place before a hold (the reference kunai at rest 2.72-8.0, then held).

## Owner Ruling
none needed (ADR-O102)

## Related
- PLAN-007
- F-077

## Resolution
RV-46 (S-056): tests/test_prop_track.py::test_a_place_set_before_a_hold_does_not_outlive_it shows its claim again
on the reference kunai (at rest on the ground 2.72-8.0, then held by A, while S06 still names the ground); the glasses'
pins moved to their own test.
