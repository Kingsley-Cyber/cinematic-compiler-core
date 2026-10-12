# F-186 — Printed lines contradict the source or each other in the reference prompts

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L6

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
- RULES: "smoke pellet keeps smoke burst" to the end, beside A's 9.50 "smoke dissipating" and c22's "smoke thinning"; the source's "4.5 smoke begins dissipating" and "10 smoke gone" are dropped untyped
- A "drops in feet first" beside the source's "head pointing down" at 0.00
- render.txt prints "(toward B and ground)" beside "NOT toward B" at the deflect (F-122's remainder)
- the kunai sits on B's torso point, 0.21 m from the right shoulder O93 drives it into (F-084's remainder)
- B 0.00–1.60 "wait with kunai ... weight transfer none" beside B's 1.8 m of steps (the F-150 class)
- the fifth principal review, S-072: RULES print "From 8.50 to the end, rope dart keeps line taut" where the source ends "line trailing to B right shoulder" (dropped untyped), and the forward kinematics put A's hand 0.69-0.81 m from B's shoulder after 9.0
- the 5.50 throw of the volley prints as a strike (a double bow and "the 5.50 strike") where the 2.00 kunai throw prints as a release; "A keeps location ground" runs through A's vanish

## Description
Lines the slices did not touch still disagree with the source or with each other.

## Impact
The model reads two instructions for one moment.

## Proposed Fix
Backlog RV-84: each line follows the source or a typed deviation (with RV-51 for the untyped ones).

## Owner Ruling
none needed

## Related
- RV-84
- RV-51
- F-122
- F-084
- F-150
- ADR-O93

## Resolution
Open.
