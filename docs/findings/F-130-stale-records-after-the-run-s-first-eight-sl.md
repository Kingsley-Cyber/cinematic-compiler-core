# F-130 — Stale records after the run's first eight slices

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
docs

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
- F-070's resolution says 24 of 33 contacts meet and eight artefacts are reported (now 31 of 33, none exempt); F-071 cites B's anchor [1.4, 1.18, 3.7] (now [2.2, 1.18, 3.47])
- PLAN-007 still lists F-119 as needing the owner (now answered), RV-33 as waiting and "tests change only on the owner's explicit ask"
- ADR-O83 has no amended-by line for O89; solver/contact_world.py's docstring calls the flags "the owner's measurement artefacts"
- F-015 (its slice RV-04 is done), F-052 and F-054 belong to no slice
- docs/plans/MASTER_PLAN.md and the S04 authoring prompt (compiler/prompts/beat_planning.txt) still say effects commit at t + dur, after RV-08; MASTER_PLAN's "a contact event in its beat" is widened in S07 to any active contact on the prop, unrecorded
- layer_order.yaml's declared reads differ from what the code reads (S04 reads /intent undeclared; S06 and S07 declare causal and do not read it; S09 declares library/affordances and does not read it)

## Description
Records the next session trusts disagree with the repo.

## Impact
Sessions navigate by stale facts.

## Proposed Fix
Backlog RV-46: correct each; F-015 to RV-09 (hits as holds, not inserts), F-052 and F-054 to RV-38; the declared reads go to RV-20 with F-095.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-070
- F-071
- F-015
- F-095

## Resolution
Open in part (review 5, S-072): the substitution's widening is narrowed (RV-66); any open hold by anyone still counts as a change's contact where MASTER_PLAN S07.3 asks for a contact in the beat (RV-93).
Before: Open in part (review 4, S-063): the stale records were corrected; the S07 widening it listed became the substitution's blanket exemption (F-169, RV-66).
Before: RV-46 (S-056): each stale record corrected at its file: F-070's and F-071's resolutions (the counts and the
anchor since), PLAN-007 (the test rule, the waiting list), ADR-O83 (amended by O89 and O104), solver/contact_world.py's
flags, docs/plans/MASTER_PLAN.md's commit times; F-015 assigned to RV-57, F-052 and F-054 to RV-38; the S04 prompt is
RV-48b's and the declared reads RV-20's (F-095).
Resolved again in RV-66 (S-064): the S07 widening is narrowed to the substitution's decoy (F-169).
