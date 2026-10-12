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
