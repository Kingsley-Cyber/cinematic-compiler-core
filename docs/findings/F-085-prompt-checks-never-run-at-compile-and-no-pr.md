# F-085 — Prompt checks never run at compile, and no prompt can be a deliverable

<!-- docs-version: 1.0 -->

## Type
gap

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
- no module under compiler/, cli/, renderers/, planner/ or solver/ imports validators/prompt_validator.py or validators/checklist.py; only tests do
- validators/checklist.py: a DAG-excluded row without codes falls through to NOT CHECKED, and `deliverable` needs every row PASS or N/A
- every example's checklist.md: 0 of 20 prompts deliverable

## Description
R-19's checklist and the prompt codes guard only the four committed examples; a new scene compiled with `cinematic compile` is never checked, and the excluded rows make deliverability unreachable.

## Impact
The mission (every emitted prompt provably adheres to the DAG) holds for no new prompt.

## Proposed Fix
Backlog RV-11 (O94): excluded rows N/A; `cinematic compile` runs the prompt checks and the checklist on each prompt and refuses one that is not a deliverable.

## Owner Ruling
ADR-O94

## Related
- PLAN-007
- ADR-O94

## Resolution
Open.
