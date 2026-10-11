# F-010 — The opening is not followed

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
F10

## Evidence
R1–R5 (DAG rows M1, C9); R19 (probe V6)

## Description
A starts standing or crouched on the pillar top in R1, R2, R4 and R5, instead of falling from above the frame (R3 got it).

## Impact
Checklist rows M1, C9 cannot pass while this holds.

## Proposed Fix
Opening from above in V6's wording (backlog M9-08; R19 kept A off the pillar).

## Owner Ruling
ADR-O21

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Caught by ENTRANCE_UNSTATED (the checklist's caught_by; validators/checklist.py FINDINGS): A starts at root y=10 and
lands on the 8 m top at 0.60 (O21, M9-08a, S-015), and every prompt says, in V6's wording that R19 followed, that A's
feet touch the pillar top at 0.60, not earlier, with no A standing on the pillar at the start (M9-08b, S-016). The
full-fight render (M9-17) is the owner's test of it.
