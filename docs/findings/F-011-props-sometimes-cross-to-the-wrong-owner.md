# F-011 — Props sometimes cross to the wrong owner

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L2.1

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F11

## Evidence
R4 (DAG rows C5, C24)

## Description
A holds a kunai at 0.0 (it is B's) in R4.

## Impact
Checklist rows C5, C24 cannot pass while this holds.

## Proposed Fix
PROP_FIRST_STATE prints who holds each prop at the start (M8.12).

## Owner Ruling
none needed

## Related
- PLAN-001
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by PROP_FIRST_STATE (the checklist's caught_by; validators/checklist.py FINDINGS).
