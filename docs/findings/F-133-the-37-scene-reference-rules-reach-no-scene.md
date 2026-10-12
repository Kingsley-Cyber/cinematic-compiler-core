# F-133 — The 37 scene_reference rules reach no scene

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L1.5

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
- kernel/kernel_scope.yaml scopes them to "only the reference courtyard fight"
- compiler/passes/mandatory/p03_constraint.py maps scene_reference to no targets (pinned by tests/test_constraint_graph.py)
- so "B NEVER STANDS after 9.0", "THREE SHURIKEN" and "B THROWS KUNAI at 2.0" never reach S04's packet; F-019 cites one of them as reaching S04

## Description
Question: do the reference rules bind the reference scene at S03, or are they render-only?

## Impact
The golden's own rules never meet its constraint layer.

## Proposed Fix
Backlog M9-03a, with the answer.

## Owner Ruling
the question open

## Related
- PLAN-007
- F-019
- M9-03a

## Resolution
Open.
