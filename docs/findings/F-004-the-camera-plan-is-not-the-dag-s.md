# F-004 — The camera plan is not the DAG's

<!-- docs-version: 1.0 -->

## Type
drift

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
F4

## Evidence
R1 13 cuts vs R2 2 cuts from the same plan (DAG rows C10, C11, C25, V3, V6, E2)

## Description
21 shots in 10 s (one every ~0.5 s), from the golden's 21 `cam` lines plus Claude's S16 authoring; the prose writes each as "cut to …". The DAG's example camera has 11 lines in 10 s: orbits, a crane rise, a dolly-in, holds of 3–5 frames on hits, and a height/depth change every ≤ 2 s.

## Impact
Checklist rows C10, C11, C25, V3, V6, E2 cannot pass while this holds.

## Proposed Fix
Re-author the camera to the DAG's D9 shape in V5's wording (backlog M9-13).

## Owner Ruling
ADR-O25

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
