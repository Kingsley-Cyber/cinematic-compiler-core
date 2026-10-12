# F-169 — A substitution exempts any prop it changes, anywhere

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L1.1

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- planner/dynamic_beat_validator.py `_swapped`: any prop a substitution beat changes may stand anywhere at the substitution's start; the reviewers' probes (the log 2.5 m from A's place, the pellet 1.2 m off the ground at 3.7, the untouched kunai set embedded by b09) pass S04 to S07
- compiler/passes/mandatory/p07_contact.py `cross_check`: every prop change in a substitution beat is exempt from PROP_CHANGE_CONTACT; with A's touch of the pellet removed, S07 stays silent, while the docstring and planner/prompts/beat_planning.txt say "its own decoy"

## Description
RV-48a (S-057) built the decoy's swap as a licence for every prop the substitution names in its effects, wider than its own label ("the log takes A's place").

## Impact
A substitution re-opens the kind of exception door RV-43 shut at S13: a prop may jump or change with no hand.

## Proposed Fix
Backlog RV-66: the exemption names one decoy, the prop the substitution places at its actor's anchor at its start (within the contact tolerance); only that prop's move and change are exempt; a break test for each probe.

## Owner Ruling
none needed to narrow it (O48: A swaps places with it); whether a substitution may change other props without a hand is listed for the owner

## Related
- RV-66
- F-138
- F-130
- ADR-O12
- ADR-O48
- PLAN-007

## Resolution
RV-66 (S-064): `decoy(beat)` (planner/dynamic_beat_validator.py) names a substitution's decoy, the prop it changes
whose sample at its start lies within 0.15 m of its actor's anchor; S04's swap and S07's PROP_CHANGE_CONTACT exempt that
prop alone, and the S04 instructions say so. The reviewers' probes are refused
(tests/test_dynamic_beat_validator.py::test_a_substitution_swaps_only_its_decoy,
tests/test_contact_pass.py::test_a_substitution_changes_only_its_decoy_with_no_hand). Whether a substitution may move or
change other props without a hand stays listed for the owner.
