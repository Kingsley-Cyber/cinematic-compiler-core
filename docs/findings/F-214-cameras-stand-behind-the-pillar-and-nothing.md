# F-214 — Cameras stand behind the pillar and nothing checks a line of sight

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
- S-081 (checked): 12 of the fight's 22 cameras stand at z > 6, behind the pillar at the courtyard's back (c03 to c09,
  c18 to c22)
- c20's line of sight crosses z = 6 at x 0.49, y 1.74, within the x-band of A's own pillar contacts; the pillar has no
  extent yet (F-097)

## Description
No check keeps a camera inside the set or its subjects unoccluded.

## Impact
The climax shot may look through the pillar.

## Proposed Fix
Backlog RV-102 (after RV-22): a camera stands inside the set and sees its subjects past the pillar's extent.

## Owner Ruling
needed for the pillar's footprint (F-097)

## Related
- F-097
- RV-22
- RV-102

## Resolution
Open.
