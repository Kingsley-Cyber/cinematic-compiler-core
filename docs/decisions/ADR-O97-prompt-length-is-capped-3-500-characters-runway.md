# ADR-O97 — Prompt length is capped: 3,500 characters (Runway), 1,000 words (BytePlus)

<!-- docs-version: 1.0 -->

## Status
superseded

## Date
2026-10-11

## Decided By
owner

## Scope
L6

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 10 (S-035): "Cap prompt length now. 3,500 chars for Runway, 1,000 words for BytePlus. Add the check."

## Context
F-088: prose_mixed runs to about 8,200 words and render.txt to about 70 KB; the DAG documents Runway seedance2 at 3,500 characters and BytePlus at no more than 1,000 words.

## Consequences
- Backlog RV-13: PROMPT_LENGTH refuses a prompt over 3,500 characters for Runway or 1,000 words for BytePlus.
- Fitting the prompts under the caps (RV-13b) waits on the owner's answer in F-088: what is dropped, against the owner invariant no_render_compression and R-16 (model-agnostic).

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
ADR-O111

## Related
- F-088
- R-16
- R-19
- PLAN-007
