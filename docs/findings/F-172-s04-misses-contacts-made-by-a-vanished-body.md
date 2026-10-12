# F-172 — S04 misses contacts made by a vanished body or by a body outside its beat

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- planner/dynamic_beat_validator.py `_vanished` scans beats that start inside the vanish window; probes: A touching B at 4.0 from the end of its own substitution beat, or at 3.9 from a beat that began at 3.4, pass S04 to S07
- BEAT_CONTACT checks side b only: B touching the pillar in A's beat b18, which does not list B, passes, and S13 cannot measure it (F-131)

## Description
F-136's fix covered contacts on the vanished body, not contacts by it, and the beat check reads one side.

## Impact
A vanished body can act while gone, and a body can touch something in a beat it is not in.

## Proposed Fix
Backlog RV-73: every contact by the vanished actor timed inside its window is refused; side a is the beat's actor or a participant.

## Owner Ruling
none needed (O18, O90)

## Related
- RV-73
- F-136
- F-131
- ADR-O18
- ADR-O90

## Resolution
Open.
