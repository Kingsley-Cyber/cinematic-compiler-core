# F-164 — A prop let go from rest gets an invented downward speed

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L1.1

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- S-042 D3: the dropped rope dart leaves A's hand at 3.7 with v [0, -2.25, 0], and the spent pellet with v [0, -1.83, 0], so both land on the 4.0 beat; nothing throws them
- ADR-O90's words: "The rope dart is on the ground at 3.7 until A picks it up at 7.5"; from rest at 1.12 m it would land near 4.18

## Description
No rule says a released prop that is not thrown starts at rest.

## Impact
The prop tracks print speeds no hand gave.

## Proposed Fix
Backlog RV-63: a release without a throw starts its prop at rest (PROP_KINEMATICS); the dart's and the pellet's drops re-timed; O90's "on the ground at 3.7" asked of the owner first.

## Owner Ruling
the question open (O90's timing)

## Related
- PLAN-007
- F-081
- ADR-O90
- ADR-O91
- RV-63

## Resolution
Open.
