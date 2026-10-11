# F-020 — Declared constraint validators do not run per layer

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-05

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
All layers. Current: `validated_by: [schema, invariants, constraint]` on S04-S17 is enforced as an ordering (S03 first) and the names are checked against a registry, but no generic `constraint` or `invariants` validator runs per layer; each step runs its own checks. Target: declared validators execute. Missing: a per-layer constraint pass that applies GAP-04's checkable constraints to that layer's output. Severity: high. Files: `planner/dependency_graph.py`, `compiler/pipeline.py`.

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
