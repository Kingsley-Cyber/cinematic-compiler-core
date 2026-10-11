# F-009 — Props are drawn before they are used

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
F9

## Evidence
Log on the ground from 0.5–1.5 s in R1–R5 (DAG rows C5, C23, H3)

## Description
SCENE lists the substitution log with the other props and never says it is hidden until 3.70.

## Impact
Checklist rows C5, C23, H3 cannot pass while this holds.

## Proposed Fix
Props known from the first beat (PROP_FIRST_STATE, M8.12); the log stands as a post from 0.00 (O48, W4).

## Owner Ruling
ADR-O48

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by PROP_FIRST_STATE (the checklist's caught_by; validators/checklist.py FINDINGS).
