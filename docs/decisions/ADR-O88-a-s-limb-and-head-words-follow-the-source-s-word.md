# ADR-O88 — A's limb and head words follow the source's words

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 1 (S-035): "Follow the source's words. Flip the 21 limb words and 13 head words. Record each as an R-33 deviation."

## Context
F-080: the prompts print A's limbs and head opposite to the source's own words in about 21 of 88 limb words and on 13 head lines (at 1.10 all four limbs: the source says "L:arm fwd ... leg back; R:arm back ... leg fwd", the prompt the reverse), because the repo reads the source's numbers under Q6 while some rows' words follow the other sign (the DAG's X21, never ruled).

## Consequences
- Backlog RV-05: where an A row's word disagrees with the source's own word, that row's joint number is flipped so the derived word says what the source says; each flip is a recorded deviation in the golden test (R-33).
- b06_c3 (A's right foot at 3.0, the one CONTACT_WORLD exception) is measured again afterwards.

## Alternatives Considered
- Keep the numbers as read under Q6: not chosen.

## Supersedes
—

## Superseded By
—

## Related
- F-080
- ADR-O7
- ADR-Q6
- R-33
- PLAN-007
