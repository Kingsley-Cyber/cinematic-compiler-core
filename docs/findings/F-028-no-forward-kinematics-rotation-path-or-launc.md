# F-028 — No forward kinematics, rotation path or launch check

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L4c

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-13

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L4c Motion. Current: Euler keys, joint limits, declared and named turns, root trajectory. Missing: forward kinematics and world joint points (F5.1), the derived rotation path (FR.1, printed per O47 as one named turn), the launch-before-turn check (FR.4, here, not S11). Severity: high. Files: new `solver/forward_kinematics.py`, a segment-length card (logged), `solver/euler_solver.py`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-05 (docs/plan.md).

## Owner Ruling
ADR-O33

## Related
- PLAN-003
- backlog M9-05

## Resolution
Built: forward kinematics and world points (F5.1, solver/forward_kinematics.py, M9-06a), the derived rotation path
printed as one named turn (FR.1, ROTATION_PATH_UNSTATED) and the launch before a turn (FR.4, AIRBORNE_WITHOUT_LAUNCH in
solver/euler_solver.py, M9-09c). Closed in RV-04 (S-044).
