# F-204 — A moving shot is framed at its first beat only: S16 does not model a camera's path

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
- validators/camera_validator.py `_framing` (S-076, S-077): VERTICAL_FRAMING checks a static shot at every beat it
  lists, from the camera S16 derives at its first beat, and a moving shot at its first beat only
- 23 of the four examples' 41 shots move; two list later beats that nothing checks (the wizard example's c02, a
  tracking vault over three beats, and c05, a whip pan over two)
- `movement.path` is free text and the camera node carries one derived position, so no step knows where a moving
  camera is after its first beat (render.txt prints that one position)

## Description
S16 derives one camera per shot, at its first beat. A pan, tilt, track, dolly, orbit, crane or zoom moves it, but
nothing says how far or where to, so the framing of a moving shot's later beats is unchecked.

## Impact
A moving shot can lose a body or a prop after its first beat with no refusal; the model is told where the camera
starts, not where it goes.

## Proposed Fix
Backlog RV-94 (step camera): each movement kind's path from the fields it has (a pan or tilt turns in place to its
target; a track, truck or dolly keeps its offset from the target; an orbit sweeps the azimuth; a crane or pedestal
moves the height; a zoom the focal length), derived at every beat the shot lists and checked there by VERTICAL_FRAMING;
the path's extent where a field gives none is an interpretation for owner review.

## Owner Ruling
none needed

## Related
- F-090
- PLAN-007
- RV-94

## Resolution
Open.
