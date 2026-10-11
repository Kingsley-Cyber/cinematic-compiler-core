# F-016 — Intent drops the query's literal starts, counts and anchors

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L0

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
GAP-01

## Evidence
docs/reports/2026-10-11-layer-order-verification.md, Phase 2

## Description
Layer L0 Intent. Current: S01 parses duration, fps, genre, setting, entities and props; it records "geometry_anchors" as missing, so the query's literal starts ("A starts ABOVE the frame, falling from y=10"), counts and pillar height constrain nothing. Target: literal anchors and counts parsed with evidence spans. Missing: `parsed.starts`, `parsed.counts`, `parsed.anchors`. Severity: high (renders F10 opening, F12 count). Files: `planner/intent_parser.py`, `schemas/.../intent`.

## Impact
See the report's Phase 3 (impact) and Phase 3.5 (cascade) for this gap.

## Proposed Fix
Backlog slice M9-08 (docs/plan.md).

## Owner Ruling
ADR-O21

## Related
- PLAN-003
- backlog M9-08

## Resolution
Open.
