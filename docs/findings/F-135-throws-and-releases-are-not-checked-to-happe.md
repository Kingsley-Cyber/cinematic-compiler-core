# F-135 — Throws and releases are not checked to happen at their pose, and the S04 prompt teaches the old timing

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- ADR-O23: "Strike, throw and release contacts happen at their key pose (at: start)"; only strikes are checked, at S17 (compiler/passes/derived/p17_render.py)
- compiler/prompts/beat_planning.txt says effects and contacts commit at t + dur and that a contact happens at its beat's end; it never explains prop samples, PROP_SUPPORT, SURFACE_HEIGHT or standing_leg_m

## Description
An author following the prompt writes the timing the checks were built to remove.

## Impact
Throws can leave a prop at the wrong instant; new scenes repeat old mistakes.

## Proposed Fix
Backlog RV-48: S04 refuses a throw or a prop release that is not at its pose; the S04 prompt rewritten to today's rules (it needs no layer-order ADR, so it leaves RV-20).

## Owner Ruling
ADR-O23

## Related
- PLAN-007
- ADR-O23
- F-095

## Resolution
Open.
