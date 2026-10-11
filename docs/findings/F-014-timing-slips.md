# F-014 — Timing slips

<!-- docs-version: 1.0 -->

## Type
risk

## Severity
high

## Layer
L6

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F14

## Evidence
R2 (DAG rows C1, C2, E4)

## Description
In R2 most beats land 0.5–1 s late.

## Impact
Checklist rows C1, C2, E4 cannot pass while this holds.

## Proposed Fix
Judge renders with the drift in mind; see F-036 (AX2).

## Owner Ruling
ADR-O20

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
