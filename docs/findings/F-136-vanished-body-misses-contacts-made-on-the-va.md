# F-136 — VANISHED_BODY misses contacts made on the vanished body

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- planner/dynamic_beat_validator.py `_vanished` checks contacts the vanished actor makes, not contacts others make on it
- in memory (the S01-S09 reviewer): a B strike on A's torso at 4.0, while A is gone 3.7-4.4, passes S04

## Description
A body that is gone can still be struck.

## Impact
The substitution can be contradicted by the plan.

## Proposed Fix
Backlog RV-48: also refuse a contact whose target is the vanished body, and require a touched entity to be a participant.

## Owner Ruling
ADR-O18, ADR-O90

## Related
- PLAN-007
- F-081

## Resolution
Open.
