# F-153 — No compile can ever emit: render.txt cannot pass the Master Template rows

<!-- docs-version: 1.0 -->

## Type
question

## Severity
high

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
- ADR-O1 keeps LBN-2.4 (render.txt) unchanged; ADR-O13 reads it against the Master Template, so 46 of its 50 FAIL rows are layout gaps ("the prompt has no [SCENE]")
- cli/main.py refuses unless all five prompts are deliverables (validators/checklist.py `refusals`, S-052)

## Description
O1 and O94 as built cannot both hold: render.txt never becomes a deliverable, so `cinematic compile` refuses every scene that reaches its prompts, now and after every other fix.

## Impact
fight_works and `cinematic compile` cannot pass without a ruling.

## Proposed Fix
Waits for the owner: render.txt's layout rows N/A, deliverability judged on the union of the five fragments (O13's Any column), or render.txt must pass as it is. Then RV-56.

## Owner Ruling
the question open

## Related
- PLAN-007
- F-085
- ADR-O1
- ADR-O13
- ADR-O94
- RV-56

## Resolution
Open.
