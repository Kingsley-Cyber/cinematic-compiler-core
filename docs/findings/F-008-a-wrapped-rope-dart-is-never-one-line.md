# F-008 — A wrapped rope dart is never one line

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L6

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F8

## Evidence
R3, R4 (DAG rows C5, C7, C31)

## Description
Its track says "8.00 p[0.4, 1.3, 4] held by A" with the dart on B; nothing says it runs from A's left hand to B's shoulder. Also a doubled word: "rope dart dart".

## Impact
Checklist rows C5, C7, C31 cannot pass while this holds.

## Proposed Fix
PROP_LINE_MISSING and DOUBLED_WORD (M8.12).

## Owner Ruling
none needed

## Related
- PLAN-001
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by PROP_LINE_MISSING, DOUBLED_WORD (the checklist's caught_by; validators/checklist.py FINDINGS).
