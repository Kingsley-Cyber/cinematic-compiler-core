# F-223 — The pickups' lean is checked by an angle sum the drawn body does not hold

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
- Principal review 7 (S-090, the golden), re-run by the builder: A's trunk (pelvis to chest) leans 74.0 degrees from
  vertical at 8.0 and 70.1 at 7.5; tests/test_reblock.py's shape test says "the trunk leaning 70 degrees or less" but
  sums two X angles (70.0 and 58.6), and RV-95's commands cap Sp.x at 40.
- The 8.0 solve reached the kunai by twisting the spine: Sp [40, 70.375, 27.125], a 70-degree twist against the human
  limit of 45 (the anime 75).
- The prose prints "body forward-mid (75 lean)" at 8.0 (examples/reference_fight/prose_mixed.txt:56).
- R-34: a check of a whole-body quality (a lean) reads every joint it depends on.

## Description
The test that holds A's pickups to a 70-degree lean reads the sum of two X angles, while the trunk the body draws
leans 74 degrees and twists 70.

## Impact
The pickup is a deep twisted lunge that the test reports as within its bound.

## Proposed Fix
RV-95b: judge the lean by the trunk vector and the twist against the genre's limit; re-solve with them as goals, or
report the numbers to the owner with F-205 (the anime arm).

## Owner Ruling
the question open: keep the drawn lean (70.2 and 71.2 degrees) or change what the reach needs (a lower crouch than A's own 0.57 m, or F-205's longer anime arm)

## Related
- F-206
- F-205
- R-34
- RV-95b

## Resolution
Open.
Open in part after S-093 (RV-95b): the lean is now read from the trunk's vector, and the pickups were re-solved from
their recorded commands with the 70-degree bound stated as the chest's height over the pelvis: the trunk leans 70.2
degrees at 7.5 and 71.2 at 8.0, the hand within 7 and 10 mm of its prop, the 8.0 spine twisted 71.4 degrees inside the
anime limit of 75 (O11). From A's own 0.57 m the hand cannot reach the ground within 70 degrees (the shoulder sits
about 0.74 m up, the arm 0.65 m long), so the bound is the owner's question rather than one to move; the test pins the
drawn lean.
