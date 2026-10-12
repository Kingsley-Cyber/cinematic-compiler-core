# F-088 — Every prompt is over the length caps; fitting them needs the owner's call on what goes

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
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- examples/reference_fight/prose_mixed.txt: about 46 KB and 8,200 words; render.txt about 70 KB
- docs/sources/knowledge_dag_v1.md documents Runway seedance2 at 3,500 characters and BytePlus at no more than 1,000 words
- kernel/owner_invariants.yaml no_render_compression: nothing is summarized, truncated or dropped; R-16: the repo is model-agnostic, no model cards

## Description
O97 caps prompts now. No current prompt fits (the shortest prose prompt is over ten times the Runway cap). Meeting the caps means choosing what a capped prompt drops or compresses, which no_render_compression forbids, and naming target models, which R-16 leaves to M7. Questions: (1) which prompts carry the cap, every mode or new capped modes beside the full prompts; (2) what may a capped prompt drop; (3) does O97 amend R-16 for these two targets?

## Impact
Until answered, the check (RV-13) refuses every prompt.

## Proposed Fix
Backlog RV-13 (the check, ready) and RV-13b (fitting the prompts, blocked on this finding).

## Owner Ruling
ADR-O97 (the cap); the three questions open

## Related
- PLAN-007
- ADR-O97
- R-16

## Resolution
Open.
