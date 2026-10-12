# F-206 — S-080's pickups put a knee in the floor and the hands on it through a throw and a leap

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

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
Open.
