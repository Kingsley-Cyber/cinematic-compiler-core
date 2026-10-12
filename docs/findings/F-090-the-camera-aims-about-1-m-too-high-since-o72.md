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
Backlog RV-15: aim at the body (from the pelvis) and an insert at its detail; VERTICAL_FRAMING at S16. Split in S-076:
RV-15a (the aim at the body and VERTICAL_FRAMING), RV-15b (an insert's detail and a framed prop).

## Owner Ruling
none needed

## Related
- PLAN-007
- ADR-O72

## Resolution
Open in part: RV-15a (S-076) aims each shot at the middle of the extent of the parts its scale shows of its target
(both axis performers for `midpoint`), from S13's keys carried in S16's packet, and VERTICAL_FRAMING refuses a part
the scale shows that projects outside the frame, up and down as well as across, at every beat a static shot lists and
at a moving shot's first beat; a subject's screen side is its pelvis's. The examples' refused shots were re-authored
(eleven in the reference fight, two each in the wizard and live-action examples, one in the UGC). Measured after:
no contact moment projects outside its shot's frame (the reference fight 0 of 28, from 15; the wizard 0 of 7, from
3; the UGC 0 of 3, from 1), and the source's "ground level" shots sit 0.72 m (3.0) and 0.19 m (9.0) high, from 1.90
and 1.14 m. Open: an insert still aims 1 m above its target's pelvis, a framed prop is not checked, and the camera schemas'
`position` text still reads "target + aim height" (RV-15b, one major bump for both); a
moving shot is checked at its first beat only, since S16 does not model a camera's path; c01 frames A from frame 0,
against the source's "A starts ABOVE the frame" (F-202 asks the owner).
