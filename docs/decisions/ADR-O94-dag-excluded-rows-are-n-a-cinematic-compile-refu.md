# ADR-O94 — DAG-excluded rows are N/A; cinematic compile refuses a non-deliverable prompt

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L6

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 7 (S-035): "DAG-excluded rows count as N/A. cinematic compile refuses a non-deliverable prompt."

## Context
F-085: the prompt checks and the checklist ran only in tests on the four examples, and DAG-excluded rows counted as NOT CHECKED, so no prompt could be a deliverable.

## Consequences
- Backlog RV-11: the checklist marks DAG-excluded rows N/A; `cinematic compile` runs the prompt checks and the checklist on every prompt it emits and refuses one that is not a deliverable (R-19).

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- R-19
- F-085
- PLAN-007
