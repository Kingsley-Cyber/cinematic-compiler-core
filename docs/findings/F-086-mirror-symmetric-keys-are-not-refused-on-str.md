# F-086 — Mirror-symmetric keys are not refused on strikes and action beats

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

## Layer
L4c

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
- 18 of 73 keys mirror within 5 degrees: 11 in the reference fight (6 of them the source's A rows), 7 in the wizard
- docs/plans/006-ten-asymmetric-things.md (S-034, before correction) called item 1 "never mirrored"

## Description
O87 says Naruto fights are never mirrored; nothing refuses a mirrored key where it matters.

## Impact
A strike can render as a mirrored, dance-like pose.

## Proposed Fix
AS-04 amended (O95): MIRRORED_ACTION refuses a mirror-symmetric key on a strike or action beat, not on an idle guard; A's six symmetric source rows and B's five guards stay.

## Owner Ruling
ADR-O95

## Related
- PLAN-006
- ADR-O87
- ADR-O95

## Resolution
Open.
