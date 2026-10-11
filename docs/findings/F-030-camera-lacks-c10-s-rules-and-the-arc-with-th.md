# F-030 — Camera lacks C10's rules and the arc with the rotation

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L5.5

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-15

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L5.5 Camera. Current: 13 subdivisions, motivation, coupling, axis, genre cards. Missing: C10's six rules and three forbidden shots, the arc with the rotation (FR.5, O36), V5's wording. Severity: high. Files: `validators/camera_validator.py`, `library/camera_conventions/*.yaml`, the reference camera plan.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-13 (docs/plan.md).

## Owner Ruling
ADR-O36

## Related
- PLAN-003
- backlog M9-13

## Resolution
Open.
