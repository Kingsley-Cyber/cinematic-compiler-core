# F-235 — A contact with a surface's face is not measured; the reference fight's wall push is off its pillar

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
all

## Status
resolved

## Reported
2026-10-13

## Reporter
agent

## Legacy ID
—

## Evidence
- solver/contact_world.py: a touch on any surface but a floor, and a support on a surface with no top, is "a
  surface's face (no top to meet)" and is not measured; a support on a top is measured vertically only.
- S-122 gave every surface boxes. Measured against them, the reference fight's own pillar contacts miss: at 0.60 A's
  feet stand on the top at z 5.31, 0.39 m in front of a 0.6 m pillar centred at z 6 ("pillar at z=6", its card); at
  7.00 the wall push puts the left foot inside the pillar (z 5.96) and the right foot 0.96 m in front of it (z 4.76)
  with the root at z 5.9, inside it.
- The wizard example's back-first slam (5.20) fits its pillar's boxes (S-122 placed the pillar from it).

## Description
Without the faces measured, a body can meet a wall or pillar anywhere; SURFACE_REACH (S04) bounds it to 1.5 m of the
surface, not to its face.

## Impact
A wall run, a slam or a push off a pillar can land in the air beside it; the prompt prints the pillar's place and a
contact that does not reach it.

## Proposed Fix
CONTACT_WORLD measures every surface contact to the nearest point of the surface's boxes (a top for a support from
above, a face otherwise), within its 0.15 m. The reference fight's pillar contacts then need its pillar's size or its
motion re-authored: the owner's ruling (which is the reference's truth: the pillar at z=6, or A's feet).

## Owner Ruling
Owner, 2026-10-13: "move the pillar to fit the feet. The fight is the truth; the backdrop serves it ... Record
as a deviation. Turn on side measurement."

## Related
- F-230
- R20 next action 2

## Resolution
S-124: CONTACT_WORLD measures every contact with a surface but a floor to the nearest point of its boxes (top or
face). The reference pillar's box is fitted to the fight's own feet: x -0.3 to 0.3, z 5.3 to 5.95, y 0 to 8 (its back
face at the source's z=6); the 0.60 landing (0.002 m) and the 1.10 run down its face (0.10, 0.01 m) meet it. The 7.00
wall push's feet (1.09 and 0.59 m off) cannot meet any one box together with the earlier feet; they are the owner's
exceptions (kernel/contact_world_exceptions.yaml, ruling F-235), the recorded deviation.
