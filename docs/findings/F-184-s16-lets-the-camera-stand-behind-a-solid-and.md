# F-184 — S16 lets the camera stand behind a solid and shoots a flip edge-on

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- c20 (8.5–9.0) stands about 0.59 m behind the pillar's axis on its line to A (the pillar's footprint is not in the data; the reviewer assumed a 0.15 m radius at x 0); S16 checks no occlusion
- c12 (azimuth −166.8) looks along +Z while A flips about X at 5.1, so the flip's arc is seen end-on; A's row says the backflip plane is the vertical screen plane

## Description
S16 judges subjects, scale and side, not what stands between the camera and the subject or which way a turn faces.

## Impact
A hit hold can show a pillar, and the backflip can read as a hop.

## Proposed Fix
Backlog RV-82: surfaces carry their footprints and S16 refuses a line to a subject through a solid; a shot on a turn with a declared plane looks along the turn's axis.

## Owner Ruling
whether a declared turn plane overrides the 180-degree side for its beat's shot (listed)

## Related
- RV-82
- F-090
- F-145

## Resolution
Open.
