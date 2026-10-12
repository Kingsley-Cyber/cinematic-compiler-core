# F-226 — S-083's tolerances moved after its solve, two tests carry slack, and one claims a re-derivation it does not do

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- Principal review 7 (S-090, rules; decisions): S-083 stated an ankle bound of 0.045 m (the foot's radius) and relaxed
  it to "over the floor" after the solve; with the stated bound the recorded commands give ankles 0.038/0.025 m at 7.5
  and 0.048/0.044 m at 8.0, so 8.0 did not need it.
- A's right knee at 7.5 is 0.0796 m against the stated 0.08 (F-206); tests/test_reblock.py asserts `>= 0.08 - 1e-3`,
  and S-083 loosened the head's `>= 0.2` to `>= 0.2 - 1e-3` (the data, 0.2265 and 0.2001, did not need it), while its
  self-audit says its bounds tightened (checked by the builder).
- tests/test_reblock.py's S-078 test claims a re-derivation from goals whose height (0.034) is the committed sole's;
  DEV-33 calls the values hand choices (F-207 resolved).
- F-215 tells the owner "RV-95 keeps the repo's re-blocks above the floor by their radii either way": the ankles sit
  0.012 to 0.022 m over the floor against the foot's radius of 0.045.

## Description
A bound stated before a solve was relaxed after it, two test bounds carry an unstated millimetre, and one test claims
a re-derivation it does not do.

## Impact
The tests pass on data that misses the bounds the records state.

## Proposed Fix
RV-95b: make the knee floor hard and re-solve, remove the head's slack, restore the 0.045 m ankle bound where the body
can meet it or put the relaxation to the owner (F-215, F-219), and pin S-078's values as hand choices.

## Owner Ruling
the ankle relaxation is F-215's question

## Related
- F-206
- F-207
- F-215
- F-219
- RV-95b

## Resolution
Resolved in S-093 (RV-95b): the recorded commands state every bound S-083's plan stated, each floor with the solver's
1 mm margin stated before the solve (knees 0.08 m, ankles 0.045 m, the head 0.2 m over the pelvis, the trunk within 70
degrees by the chest's height), and both pickups were re-solved from their start keys. The tests hold the knees and
the head without slack (0.0851 m the lowest knee) and pin, for the owner, what is not met: the ankles at 7.5 (0.0385,
0.0263 m) and the 8.0 right ankle (0.0449 m), F-215 and F-219; the lean, F-223. S-078's test says what it shows: the
solver reaches a hand-chosen height.
