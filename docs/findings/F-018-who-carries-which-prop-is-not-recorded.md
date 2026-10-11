# F-018 — Who carries which prop is not recorded

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L0.5

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-03

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L0.5 Expand. Current: entities, props and surfaces as nodes; archetype `equipment` (who carries which prop) is dropped, so a stowed prop cannot say whose gear it is (seen in M8.12b). Target: an edge group. Missing: `/edges/equipment` (entity → prop, from the cards) and optionally `/edges/placement` (prop or entity → surface at the start). Severity: medium. Files: `p02_brief.py`, `planner/query_expander.py`, `kernel/layer_order.yaml` (S02 writes).

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-03b (docs/plan.md).

## Owner Ruling
ADR-O63

## Related
- PLAN-003
- backlog M9-03b

## Resolution
Resolved in backlog M9-03b (session S-006) as O63 ruled: each prop node records `carried_by` at S02 (brief_nodes 1.1); no edge group at L0.5. The prose SCENE line says "carried by <label>" for gear on the body.
