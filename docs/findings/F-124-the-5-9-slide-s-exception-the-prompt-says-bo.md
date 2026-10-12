# F-124 — The 5.9 slide's exception: the prompt says both feet support while the soles are 0.35-0.55 m up

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- S-039 listed b14_c2 and b14_c3 in contact_world_exceptions under ADR-O83 point 2; until O89 the slide passed as an artefact
- examples/reference_fight/prose_mixed.txt: "5.90 A: SUPPORT both feet" with the soles 0.55 and 0.35 m above the ground under the anime body
- the owner's M9-06b words (S-030): "keep the source misses as exceptions (calibrated to the trunk reading)" (corrected in RV-46: the
  owner's words, ADR-O83)

## Description
The slide is the owner's own row (root y 0.6, both legs folded, "support=both feet"); its numbers lift the soles off the ground. The owner's M9-06b words keep the source's misses as exceptions, but the prompt then says both feet support.

## Impact
The words and the numbers of one line disagree.

## Proposed Fix
Owner question: keep the exception as the owner's M9-06b words say, re-pose the source's 5.9 row, or re-read its support.

## Owner Ruling
the question open (the owner's M9-06b words cover the exception; the printed contradiction is the question)

## Related
- PLAN-007
- ADR-O83
- ADR-O89
- F-111

## Resolution
Open.
