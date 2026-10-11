# F-036 — Aerial timing is not followed: takeoffs come late

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
AX2

## Evidence
R6, R7, R8, R9, R10, R13, R14, R18, R19

## Description
Timing was not.** Launches came 0.25-0.75 s late (except P4) and landings 0.25-1.0 s off. P1-P3 asked for 2.5 s in the air, an apex near 7.7 m under gravity; the model filled the time with late launches, long inverted hangs (P4, P5) or an extra rotation (P3).

## Impact
Changes how a turn, a hold or the camera is worded for the model.

## Proposed Fix
Times stay in the prompt; renders are judged with the drift in mind (0.25-2.7 s; R19 the largest).

## Owner Ruling
none needed

## Related
- PLAN-003
- docs/render_tests/2026-10-11-seedance-axis/README.md

## Resolution
Open.
