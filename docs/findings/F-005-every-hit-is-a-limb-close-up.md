# F-005 — Every hit is a limb close-up

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L5.5

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F5

## Evidence
R2 "hits could've been better", "knife kick as a key frame"; R3 deflect drawn as a hand (DAG rows C10, C12, C25)

## Description
The 2.5 deflect, 4.7 knee and 8.5 kunai drive are "smash cut to insert" on the striking limb, so the hit shows without its target. The DAG holds on hits with both bodies in frame ("hold 3 frames on kunai/foot impact", "profile kick impact").

## Impact
Checklist rows C10, C12, C25 cannot pass while this holds.

## Proposed Fix
Hold hits with both bodies in frame, no limb inserts (backlog M9-13; W1 prints the hold where the shot allows).

## Owner Ruling
ADR-O47

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
