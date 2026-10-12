# F-215 — May a body point sit up to 0.15 m under the floor, or only by its radius?

<!-- docs-version: 1.0 -->

## Type
question

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
- solver/floor_penetration.py (S-078) allows O72's 0.15 m on forward-kinematics points; its docstring speaks of a part
  sinking by its radius (thigh 0.08 m, foot 0.045 m)
- it passes S-080's knee 0.109 m under the floor (F-206) and the source rows at 3.0 (a sole 0.126 m under) and 9.0
  (0.069 m)
- O72's 0.15 m is also CONTACT_WORLD's tolerance and the decoy's distance

## Description
Is O72's 0.15 m also the floor's allowance on points, or must each part's surface stay above the floor (which would
refuse A's source rows at 3.0 and 9.0, F-148's class)?

## Impact
The floor check either hides sinking parts or refuses the golden's source rows.

## Proposed Fix
The owner's answer; RV-95 keeps the repo's re-blocks above the floor by their radii either way.

## Owner Ruling
needed

## Related
- ADR-O72
- F-089
- F-148
- F-206

## Resolution
Open.
Corrected in S-090 (principal review 7): this finding's evidence said RV-95 keeps the repo's re-blocks above the floor
by their radii either way; A's ankles at 7.5 sit 0.012 and 0.022 m over the floor against the foot's radius of 0.045
(S-083 relaxed its 0.045 m bound after the solve, F-226).
Noted in S-093 (RV-95b): with S-083's stated 0.045 m ankle bound restored in the recorded commands, A's ankles reach
0.0385 and 0.0263 m at 7.5 and 0.0484 and 0.0449 m at 8.0: the foot, the shin's extension (F-219), cannot keep its
surface off the floor in A's deepest crouch. Whether a point within 0.15 m or a surface is the floor's measure decides
whether that stands.
