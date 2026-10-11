# F-019 — Beats are not checked against the constraint rules

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L1.5

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-04

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L1.5 Constraint. Current: constraints reach S04 only through the authoring packet; `beat_constraint` edges record which constraints apply to a beat's bodies and props; nothing checks that a beat obeys a constraint's rule (the rules are prose, e.g. "B never stands after 9.0"). Target: constraints shape and bind the beats. Missing: a machine form for checkable constraints (subject, property, value, window) and a check at S04/S06. Severity: high. Files: `p03_constraint.py`, `kernel/invariants.yaml` form, `planner/dynamic_beat_validator.py`, `p06_state.py`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-03a (docs/plan.md).

## Owner Ruling
ADR-O62

## Related
- PLAN-003
- backlog M9-03a

## Resolution
Open.
