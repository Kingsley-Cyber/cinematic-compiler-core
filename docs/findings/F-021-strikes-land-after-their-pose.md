# F-021 — Strikes land after their pose

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
critical

## Layer
L1.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-06

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L1.1 Temporal. Current: a contact happens at its beat's end unless marked `at: start` (`p07_contact.contact_time`); every strike in the reference fight lands 0.4-0.5 s after its pose and impact frame. Target: one time per hit. Missing: strike, throw and release contacts at their pose (O23) and IMPACT_CONTACT_SYNC. Severity: critical. Files: the reference plans, `p17_render.check`, `validators/prompt_validator.py`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-02 (docs/plan.md).

## Owner Ruling
ADR-O23

## Related
- PLAN-003
- backlog M9-02

## Resolution
Open.
