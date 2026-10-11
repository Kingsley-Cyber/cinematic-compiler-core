# F-041 — Holds given in frames are stretched

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
P1

## Evidence
R10, R11, R14

## Description
Holds in frames are stretched:** every frame-count hold so far became 0.85-1.75 s (R10, R11, R14).

## Impact
The printed wording decides what the model draws.

## Proposed Fix
BODY_HOLD_FRAMES (W1)

## Owner Ruling
ADR-O47

## Related
- PLAN-003
- backlog M9-01
- docs/render_tests/2026-10-11-m9-probes/README.md

## Resolution
BODY_HOLD_FRAMES (W1); built in backlog M9-01 (commit 7cc69f8).
