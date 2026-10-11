# F-031 — Render wording the model does not follow

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
critical

## Layer
L6

## Status
in progress

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-16

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L6 Render. Current: LBN-2.4 and four prose modes, 44 prompt codes, the checklist. Missing: the probe wording rules W1-W4 (O47-O49), IMPACT_CONTACT_SYNC, D9 lines (O19), the one complete prompt (O13). Severity: critical (every render so far failed on wording the model does not follow). Files: `renderers/prose_renderer.py`, `validators/prompt_validator.py`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-02 (docs/plan.md).

## Owner Ruling
ADR-O47

## Related
- PLAN-003
- backlog M9-02

## Resolution
W1-W4 built (backlog M9-01, commit 7cc69f8); IMPACT_CONTACT_SYNC, D9 lines and the one complete prompt remain.
