# F-098 — SHAPE_DIRECTION is wider than O76's words and narrower than the plan

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L5

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- solver/shape_direction.py: an airborne turn skips the whole judgement (ADR-O76: skip the lean); it reads local bones, not world points
- tests/test_effort_solver.py has no grounded-lean case; three printed shapes contradict the root's path (the acrobat b12-b13 "retreating" while advancing 1.28 m; A b03-b04 "advancing" while retreating 0.9 m; A b13-b14)
- plan F9.1's Space-plane and Effort-time checks were not built though M9-09a is done; O73's "leave the 24 as-is until M9-10" is not in M9-10's text

## Description
The Shape check skips more than the owner said and misses what the plan asked.

## Impact
Printed qualities contradict the motion.

## Proposed Fix
Backlog RV-23: skip only the lean in an airborne turn; read the world points; a grounded-lean test; the two F9.1 checks; M9-10 carries the 24 intervals.

## Owner Ruling
ADR-O76, ADR-O73 as worded

## Related
- PLAN-007
- ADR-O76
- ADR-O73

## Resolution
Open.
