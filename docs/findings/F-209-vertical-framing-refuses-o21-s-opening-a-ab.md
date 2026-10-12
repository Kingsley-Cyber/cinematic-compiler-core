# F-209 — VERTICAL_FRAMING refuses O21's opening, A above the frame

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

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
- ADR-O21: 'A starts above the frame at root y=10'
- S-081 (decisions reviewer, probe_opening.py): c01 aimed at the pillar is refused (CAMERA_VOCABULARY), framed on B
  with A to enter (CAMERA_COUPLING), at the midpoint with A above (VERTICAL_FRAMING); the committed c01 has A in frame
  from frame 0
- F-090 was resolved with c01 sent to F-202 Q3, which O21 already answers

## Description
A new check refuses what an owner ruling requires: the opening cannot start with A above the frame.

## Impact
The golden's opening contradicts O21, and no plan can meet both.

## Proposed Fix
Backlog RV-98: a declared entrance (a subject entering the frame during the shot) may start outside it, checked from
its entering instant; c01 re-authored to start with A above the frame (O21).

## Owner Ruling
ADR-O21 (applies)

## Related
- ADR-O21
- F-090
- F-202
- RV-98

## Resolution
Open.
