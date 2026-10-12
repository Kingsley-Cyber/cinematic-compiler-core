# F-085 — Prompt checks never run at compile, and no prompt can be a deliverable

<!-- docs-version: 1.0 -->

## Type
gap

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
RV-11 (S-052, O94): a row the DAG excludes is N/A unless a code checks it (P3.2-5 and P4.2-1 keep their
ROOT_EXACT_PRESENT verdict, owner O3), so every prompt's N/A count rose by 11; the checklist judges the prompts of any
envelope (validators/checklist.py `judge_prompts`, `refusals`); `cinematic compile` runs it on every prompt it emits
and refuses one that is not a deliverable, exit 5 with nothing written (cli/main.py;
tests/test_cli.py::test_compile_refuses_a_prompt_that_is_not_a_deliverable_and_stops_for_a_packet,
tests/test_checklist.py::test_dag_excluded_rows_are_not_applicable_unless_a_code_checks_them). No prompt is a
deliverable yet (0 of 20), so a full compile is refused until the rest of the plan lands.
