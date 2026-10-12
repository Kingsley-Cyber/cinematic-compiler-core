# ADR-O110 — Significant work only; then the owner renders the prompts and judges them by eye

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-12, while principal review 8 (S-099) was being checked: "What else is left?", "Anything
meaningful?", "I dont want you over optimizjng the little things just signiifcant and then j have to run the prompts
and assess with my eyes."

## Context
Principal review 8 found the in-between keys (ADR-O109) drawing B off the ground and into the floor, a prompt legend
that contradicts ADR-O84, and two checks this run loosened, among many smaller record and wording gaps. The backlog
holds 79 ready and 21 blocked items.

## Consequences
- Finish run 1 (ADR-O101) builds only what changes what a prompt tells the renderer, or a check this run loosened so
  that a visibly broken prompt would pass: review 8's F-230 to F-233, as RV-113, RV-59j, RV-59k and RV-59l. Then it
  stops and hands the owner the prompts to render, with their sizes against the caps (F-088).
- Review 8's smaller gaps (record wording, backlog titles, a test's exactness, a lean 1 degree over the repo's own
  bound) are listed in its report and wait; the backlog keeps every item.
- R-29 holds: the owner judges the renders; the repo never gives a render verdict.

## Alternatives Considered
- Work the whole backlog slice after slice (ADR-O101 as written): not the owner's choice now.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O101
- ADR-O109
- F-088
- PLAN-007
