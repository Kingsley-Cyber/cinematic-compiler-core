# F-174 — The S04 and S08 packets lack what their checks read

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- planner/beat_planner.py: the S04 packet's props carry no `carried_by`, yet its instructions and S06's PROP_FIRST_STATE use it
- compiler/passes/derived/p08_hand_role.py: the S08 packet carries the cards' verbs and grips, not the affordance entries (required grip, duration) S10 refuses it by, and S09 and S10 refusals route back to S08; probe: an unfold with a two_hand_temple grip passes S08 and S10 refuses it (AFFORDANCE_GRIP)

## Description
R-04's sealed authoring holds for structure, not yet for content: with the query (F-167), the golden's S04 and S08 plans could not have been written from their packets alone.

## Impact
A new scene's author cannot meet checks the packet does not show.

## Proposed Fix
Backlog RV-78: S04's packet gives each prop's carried_by; S08's gives the (card, verb) affordance entries; hand_roles.txt teaches OBJECT_STATE_* and AFFORDANCE_*.

## Owner Ruling
none needed

## Related
- RV-78
- F-167
- RV-64
- R-04

## Resolution
Open.
