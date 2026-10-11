# F-022 — Airborne pickups of resting props

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L1.1

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-07

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L1.1 Temporal. Current: a possess contact may take a prop resting on a surface while its body has no support (audit X2/X3, renders R3/R4). Missing: AIRBORNE_PICKUP; the reference b18-b20 re-authored (O18). Severity: high.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-03 (docs/plan.md).

## Owner Ruling
ADR-O18

## Related
- PLAN-003
- backlog M9-03

## Resolution
Resolved in backlog M9-03 (session S-004): A lands crouched by the rope dart (7.5) and by the kunai (8.0) before taking them; AIRBORNE_PICKUP (S11 and the prompt) refuses a pickup with no support or out of reach.
