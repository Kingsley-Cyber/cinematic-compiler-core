# F-099 — The launch check is looser than O80's words

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L4c

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
- solver/euler_solver.py `_launch_findings`: passes when any earlier key of the entity is supported, and checks flip and cartwheel runs only
- ADR-O80: "a launch requires grounded support in the prior beat"

## Description
Read literally, A's backflip at 5.1 (launched from the airborne knee strike at 4.7, the source's own sequence) fails. Question: except it, re-time it, or read "prior beat" differently?

## Impact
Air-to-air launches pass silently.

## Proposed Fix
Backlog RV-24 (blocked on the question): the prior beat, every launch.

## Owner Ruling
ADR-O80; the question open

## Related
- PLAN-007
- ADR-O80

## Resolution
Open.
