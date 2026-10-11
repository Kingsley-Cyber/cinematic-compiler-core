# F-025 — Contacts lack world points, striking surface and verb

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L2.2

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-10

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L2.2 Contact. Current: type, part, target part, time. Missing: world points (computed at L4c, F5.1), the striking surface (F3.1), the combat verb (F4.1, O22). Severity: high. Files: Contact schema (beat_plan, temporal_graph 1.4), `p07_contact.py`, S13 check.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-06 (docs/plan.md).

## Owner Ruling
ADR-O24

## Related
- PLAN-003
- backlog M9-06

## Resolution
Open.
