# F-160 — The camera cards print rules against O92 and R-21

<!-- docs-version: 1.0 -->

## Type
contradiction

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- every anime prose prompt prints "Cut close on the receiver after a blow lands." (library/camera_conventions/anime.yaml) beside the hit holds
- every live-action prose prompt prints "Slow motion only around the peak of an action." (library/camera_conventions/live_action.yaml) while PLAYBACK_RAMP refuses slowed playback
- the cards still list slow, ramp and freeze playback (S-050 D3); no check reads the printed camera rules

## Description
The prompt tells the model to hold on both bodies and to cut close after the blow.

## Impact
Two camera instructions in one prompt disagree.

## Proposed Fix
Backlog RV-60: the two conventions and the slowed playbacks struck from the draft cards under O92; HIT_HOLD and PLAYBACK_RAMP read the printed camera rules too.

## Owner Ruling
none needed (O92; PLAYBACK_RAMP's reach beyond the fight is the builder's reading, listed for the owner)

## Related
- PLAN-007
- F-083
- ADR-O92
- RV-60

## Resolution
Open.
