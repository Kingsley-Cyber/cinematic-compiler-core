# F-043 — Words do not cap the rotation count

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L6

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
P3

## Evidence
R13, R18

## Description
Words do not cap the rotation count:** quarter-turn angles and "exactly ONE" still gave two flips (R13; R8 and R6 also over-rotated).

## Impact
The printed wording decides what the model draws.

## Proposed Fix
ROTATION_ANGLES_PRINTED (W3)

## Owner Ruling
ADR-O47

## Related
- PLAN-003
- backlog M9-01
- docs/render_tests/2026-10-11-m9-probes/README.md

## Resolution
ROTATION_ANGLES_PRINTED (W3); built in backlog M9-01 (commit 7cc69f8).
