# F-143 — The Euler convention reads the source's turned leans as rolls and its backflip as a front flip

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
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- ADR-Q6: intrinsic XYZ; solver/forward_kinematics.py and solver/quaternion.py apply R = Rx Ry Rz
- 3.0, root [20, 90, 0]: A faces B but its up axis tilts to (0, 0.94, 0.34), a sideways roll; the prose prints "body right-forward-high" (prose_mixed.txt) where the source asks for no lean that way; at 5.9, [80, -270, 0] lays A on its side
- 5.1-5.5: X from 0 to -360 at yaw -180 tips A's head toward its front (up axis (0, 0.81, -0.59) a tenth of the way in): a front flip where the source says AERIAL BACKFLIP
- tests/test_reference_fight_golden.py ROOT_TURNS' comment says the backflip "pitches A backward through 360"

## Description
Read in the intrinsic XYZ order, an X angle on a root already turned about Y rolls the body sideways instead of leaning it forward. The source's rows read as "turn, then lean".

## Impact
Every A row that turns and leans renders as a sideways tilt, and the backflip as a front flip.

## Proposed Fix
Owner question: did the source mean turn first, then lean? Keep ADR-Q6 and re-author those rows, or read the source's rotations in its own order (a convention change, R-09). It sets aside an owner ruling either way, so it waits (R-06).

## Owner Ruling
the question open (ADR-Q6 is the owner's)

## Related
- PLAN-007
- ADR-Q6
- F-111

## Resolution
Open.
