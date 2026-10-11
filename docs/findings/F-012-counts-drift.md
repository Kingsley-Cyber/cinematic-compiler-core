# F-012 — Counts drift

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L6

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F12

## Evidence
R5 (DAG rows C5, NEG)

## Description
R5 appears to show four shuriken in the pillar.

## Impact
Checklist rows C5, NEG cannot pass while this holds.

## Proposed Fix
COUNT_CONTRADICTION; the query counts five props (M8.12).

## Owner Ruling
ADR-O17

## Related
- PLAN-001
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by COUNT_CONTRADICTION (the checklist's caught_by; validators/checklist.py FINDINGS).
