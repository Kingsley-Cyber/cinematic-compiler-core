# F-038 — A short hold becomes a long inverted hang

<!-- docs-version: 1.0 -->

## Type
risk

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
AX4

## Evidence
R9, R10, R14

## Description
"Time slows … held for 3 frames" became a 1.75 s inverted hang** (P5); P4 hung inverted about 1.2 s unasked.

## Impact
Changes how a turn, a hold or the camera is worded for the model.

## Proposed Fix
W1: no hold or freeze in frames (BODY_HOLD_FRAMES).

## Owner Ruling
ADR-O47

## Related
- PLAN-003
- docs/render_tests/2026-10-11-seedance-axis/README.md

## Resolution
W1: no hold or freeze in frames (BODY_HOLD_FRAMES).
