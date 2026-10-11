# F-026 — Airborne bodies are not held to gravity

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L4a

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-11

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L4a Kinematic. Current: support plus ten cues per slot; TELEPORT at S04 for speed. Missing: an airborne body following gravity between keys unless a hang or float is declared (F9.2, O34). Severity: high. Files: `p11_kinematic.check`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-09 (docs/plan.md).

## Owner Ruling
ADR-O34

## Related
- PLAN-003
- backlog M9-09

## Resolution
Open.
