# F-007 — Airborne ground pickups split the hands

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L1.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F7

## Evidence
R3 rope two ways at ~7.5 s; R4 rope ending (DAG rows BIO, T7, C5, X2, X3)

## Description
Between 7.0 and 8.0 the prompt asks airborne A to snatch the rope dart (left hand), throw it to wrap B, take the kunai from the ground (right hand) and pull B toward the pillar. This is inherited from the golden (audit X2, X3).

## Impact
Checklist rows BIO, T7, C5, X2, X3 cannot pass while this holds.

## Proposed Fix
Ground the pickups at 7.5 and 8.0 (AIRBORNE_PICKUP, backlog M9-03).

## Owner Ruling
ADR-O18

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
