# F-090 — The camera aims about 1 m too high since O72, and vertical framing is unchecked

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L5.5

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
- library/camera_grammar.yaml aim_height_m: 1.0, added to the root, which O72 made the pelvis (an aim near 2.0-2.2 m)
- validators/camera_validator.py places subjects on screen in x only; inserts aim at the entity, not their detail; CAMERA_COUPLING passes on part names
- the source's "ground level" shots (3.0, 9.0): the camera sits 1.1 to 1.9 m high, since it aims 1 m above the root
  (RV-09, S-050, left this to RV-15)
- about 16 of 37 contact moments project outside their shot's frame (the principal review, S-035 (docs/prompts/principal_review.md)); render.txt prints these camera positions
- the fifth principal review, S-072: c01 aims about 1 m above A's start and tilts with A, so A is in frame from frame 0, against the source's "A starts ABOVE the frame ... entering from top"

## Description
S-027 moved every root to the pelvis without recalibrating the camera's aim height, and no check looks at vertical framing.

## Impact
Shots aim over the fighters' heads; contacts fall out of frame.

## Proposed Fix
Backlog RV-15: aim at the body (from the pelvis) and an insert at its detail; VERTICAL_FRAMING at S16.

## Owner Ruling
none needed

## Related
- PLAN-007
- ADR-O72

## Resolution
Open.
