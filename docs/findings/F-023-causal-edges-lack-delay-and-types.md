# F-023 — Causal edges lack delay and types

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L1.2

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-08

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L1.2 Causal. Current: `causes` edges, hard or soft, one per beat (owner: linear), reasons checked. Missing: the cause-to-effect delay (derivable), `enables`/`blocks`/`triggers` types at S05 (S10 has `enables` for UGC). Severity: medium. Files: `p05_causal.py`, `prose_renderer._causal`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-15 (docs/plan.md).

## Owner Ruling
none needed

## Related
- PLAN-003
- backlog M9-15

## Resolution
Open.
