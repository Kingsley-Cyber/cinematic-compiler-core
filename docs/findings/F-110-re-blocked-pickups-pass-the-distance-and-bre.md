# F-110 — Re-blocked pickups pass the distance and break the move

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L4c

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
- A at 7.5 and 8.0 (S-030): trunk near horizontal, head at pelvis height, both hands at the floor at 7.5 (y 0.04, 0.00) while the support line says "steps forward alternating"
- at 8.0 A "hauls" B while leaning 85 degrees toward him; S11's support lists only feet

## Description
The least-change re-block met the contact but made A crawl, and the staff's support words do not say so.

## Impact
The pickups render as crawling or as a mismatch with the words.

## Proposed Fix
Backlog RV-35: the pickups crouch on the feet with one hand down; S11's support names a hand on the ground when it is.

## Owner Ruling
none needed

## Related
- PLAN-007
- F-075

## Resolution
Open in part, reopened by the sixth review (S-081): S-080's re-block left A's right knee 0.109 m in the floor at 7.5,
kept each pickup hand bearing weight through a throw (7.5-8.0) and a leap (8.0-8.5), left the pinned words describing
the old pose, and justified the 0.40 m crouch by a search that freed no spine twist: at 0.57 m with the twist free the
7.5 reach meets the rope dart at 66 degrees (F-206, RV-95). What follows is S-080's resolution.
Resolved by RV-35a (S-080): A crouches deeper at both pickups (pelvis 0.40 m, from 0.57 and 0.59) on planted soles,
one hand on its prop and the other off the floor (0.50 and 0.65 m), the head 0.36 and 0.27 m over the pelvis, the
trunk leaning 58 and 75 degrees (from 90 and 116); S04 gives each hand a support contact on the ground for its beat,
so S11 names it and the staff prints "both feet place-low + LEFT hand place-low" and "+ RIGHT hand". The values come
from solver/reblock.py with the goals S-080 records. A shallower lean needs longer arms (F-205, the owner's).
