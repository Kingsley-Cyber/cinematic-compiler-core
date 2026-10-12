# F-096 — PASS cells are inflated: rows pass on codes that cover part of the row

<!-- docs-version: 1.0 -->

## Type
bug

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
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- validators/checklist.py: a row with codes and status enforced or excluded passes when its codes pass, whatever part of the DAG row they cover
- M2 passes on PROSE_STALE and M4 on lexical codes (M4 passes for the wizard and UGC though F-003 says it cannot while it holds); rows whose notes admit unchecked parts (T1, T8, T9, T11, C13) pass; C12 (F-074)
- the render-finding contests (validators/checklist.py FINDINGS) stop at F1-F15; F-010 was resolved without the owner's verdict on R19

## Description
The per-prompt checklist overstates how close each prompt is to the DAG.

## Impact
PASS is not proof; R-19's evidence is inflated.

## Proposed Fix
Backlog RV-21: a row passes only when its codes cover the whole DAG row (the map says which); contests read every open render finding; F-010 reopened until the owner's verdict on R19.

## Owner Ruling
none needed (R-19)

## Related
- PLAN-007
- F-003
- F-010
- F-074

## Resolution
Open.
