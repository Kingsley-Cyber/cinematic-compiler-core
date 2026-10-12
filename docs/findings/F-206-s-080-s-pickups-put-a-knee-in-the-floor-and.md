# F-206 — S-080's pickups put a knee in the floor and the hands on it through a throw and a leap

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the sixth principal review, S-081 (docs/reports/2026-10-12-principal-review-6.md): all five reviewers
- examples/reference_fight envelope: ninja_lean@b19 right knee at y -0.109 (its surface -0.164); the lowest point
  there was -0.005 before S-080; FLOOR_PENETRATION's 0.15 m passes it (F-215)
- temporal.json b19 and b20 (S-080): the left hand bears weight from 7.5 to 8.0 while b19 has it whip the rope dart to
  B; the right hand from 8.0 to 8.5 while A rises 1.1 m with the kunai
- render.txt prints three supports on A's 7.5 and 8.0 rows (the slot's, 'grounded', and the pinned words' 'both
  feet'); the pinned words (DEV-10, GROUNDED_DESCRIPTIONS) still describe the old numbers
- S-080 D2's case for the 0.40 m crouch compared unlike searches: at the 0.57 m crouch, with the spine twist free, the
  7.5 reach meets the rope dart within 0.031 m at 66 degrees with both knees above the floor (S-081, checked); D2 also
  misquotes O18
- S-080 set its pickup thresholds (trunk under 80 degrees, head 0.2 m) after the solve, looser than its prediction (70
  degrees, 0.25 m)

## Description
S-080 ended the crawl but kept a knee through the floor, put the throwing and leaping hands on the floor for whole
beats, left the pinned words describing the old pose, and justified the lower crouch with a search the committed
solver does not reproduce.

## Impact
The pickups render with a knee in the floor, a hand planted through a throw, and words that contradict the numbers;
the anchor change rests on a wrong claim.

## Proposed Fix
Backlog RV-95 (after RV-96): re-block the pickups with the reproducible solver, every body point above the floor by
its radius, the crouch height decided from a recorded command, the hand on the floor only at the pickup's instant (a
touch, not a support through the beat), the words re-written to the numbers (DEV-10).

## Owner Ruling
none needed

## Related
- F-110
- F-205
- F-215
- RV-95
- PLAN-007

## Resolution
Resolved by RV-95 (S-083): both pickups re-blocked by solver/reblock.py from commands S-083 records, run from the keys
S-080 committed, and a test re-derives them: A crouches at its own 0.57 m at both (the highest root, searched down
from 0.57 and 0.59, at which every bound holds), both soles on the floor, every knee 0.08 m over it, the grasping hand
within 0.005 m of its prop, the other hand 0.59 and 1.0 m up, the head 0.23 and 0.20 m over the pelvis, the trunk at
58.6 and 70 degrees (8.0 twists 70 degrees to reach across). The hand is no support: S-080's four S04 contacts and two
S11 hand supports are gone, so the rows print one support. The pinned words say the new numbers (bent N = 15 N
degrees). The ankle bound the plan set (0.045 m) proved unattainable in this body model, whose foot is the shin's
extension (F-219).
Corrected in S-090 (principal review 7): "every knee 0.08 m" holds to a millimetre's slack only: A's right knee at 7.5
is 0.0796 m, and the test allows 1e-3 (F-226); the trunk leans 74 degrees at 8.0, not the 70 the X angles sum to
(F-223); the words read in the trunk's frame (F-224). RV-95b carries them.
