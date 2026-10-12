# F-213 — An insert or a framed prop without a point, and a prop an action names, go unframed

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L5.5

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- validators/camera_validator.py: an insert on a prop with no point falls back to aim_height_m above its target's
  pelvis, and nothing in its frame is checked (probe: c07 as an insert on the carried shuriken volley at 3.4: zero
  findings)
- compiler/passes/derived/p16_camera.py gives a carried prop no point, though renderers/prop_samples.track knows its
  carrier
- c22's action says 'the shuriken stay in the pillar'; they project at screen y +1.62; a prop an action names but the
  shot does not list is never framed
- c09 at 4.0 aims at the middle of B and the vanished A's carried pose

## Description
S16's framing reaches only props listed as subjects with a point, and an insert's detail without one silently falls
back to the old aim.

## Impact
Shots can promise props they do not show.

## Proposed Fix
Backlog RV-101: an insert's detail must have a point; a carried prop takes its carrier's point; a prop a shot's action
names is framed; a vanished body is no aim.

## Owner Ruling
none needed

## Related
- F-090
- RV-15b
- RV-101

## Resolution
Open.
