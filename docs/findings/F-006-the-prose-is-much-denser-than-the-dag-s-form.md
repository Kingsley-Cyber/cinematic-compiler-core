# F-006 — The prose is much denser than the DAG's format

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
F6

## Evidence
R1, R3, R5 (DAG rows C2, C3, C4, FM6, D4/D9)

## Description
Staff lines average 386 characters (every limb and fold, every line); the staff alone is 16.6 KB; whole prompts 38–49 KB. The DAG's staff lines (D9) name only the limbs that matter (~120–200 characters), density is adaptive (dense on impacts, sparse on travel), and "never make every frame explicit — it bloats the prompt". The dense lines were Claude's reading of the no-compression rule, which applies to the LBN projection.

## Impact
Checklist rows C2, C3, C4, FM6, D4/D9 cannot pass while this holds.

## Proposed Fix
D9-style staff lines, density adaptive (backlog M9-12).

## Owner Ruling
ADR-O19

## Related
- PLAN-003
- docs/reports/2026-10-11-renders-and-dag-adherence.md section 3

## Resolution
Open: no code catches it yet.
