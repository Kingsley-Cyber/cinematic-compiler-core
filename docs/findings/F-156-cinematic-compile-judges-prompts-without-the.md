# F-156 — cinematic compile judges prompts without the owner's render findings

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L6

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- validators/checklist.py `refusals` calls `judge_prompts` with no example name, so no render finding contests a PASS
- on the reference fight's own prompt texts it gives 38 PASS and 29 NOT CHECKED per prose prompt where examples/reference_fight/checklist.md gives 31 and 36 (rows M4, C1-C4, C9, C23)

## Description
The gate a new prompt meets is looser than the checklist the examples meet.

## Impact
Latent while 29 rows still block, but fight_works would be judged by the looser gate.

## Proposed Fix
Backlog RV-58: the compiler applies the render findings to every scene they name (by its query) and to every prompt of their genre and rows.

## Owner Ruling
none needed (ADR-O94, R-19)

## Related
- PLAN-007
- F-085
- RV-58

## Resolution
Open.
