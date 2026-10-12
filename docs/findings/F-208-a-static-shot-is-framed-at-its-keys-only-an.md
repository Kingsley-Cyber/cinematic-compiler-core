# F-208 — A static shot is framed at its keys only and loses the hit holds' bodies between them

<!-- docs-version: 1.0 -->

## Type
gap

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
- S-081 (checked): c11, the static hold on the 4.7 knee (O92): at 5.1 A's head projects at y +2.59 and B's at +1.86;
  c20, the 8.5 drive: at 9.0 B's torso at -2.08 (the frame's edge is 1)
- validators/camera_validator.py `_framing` checks a static shot at the keys of the beats it lists; 16 of the fight's
  18 static shots list one beat, so they are checked at their first frame only
- VERTICAL_FRAMING checks part centres at |x|, |y| <= 1 with no margin; after S-076 seven shots hold a point at 0.95
  of the half-frame or more

## Description
A static camera holds through its whole window while the bodies move between keys, but S16 checks only the listed
keys, so both hit holds the owner named lose their bodies before the shot ends.

## Impact
The holds O92 asks for watch empty air.

## Proposed Fix
Backlog RV-97 (after RV-59): VERTICAL_FRAMING along a static shot's window, at frames along the declared
interpolation, with a margin by each part's radius; c11 and c20 re-authored.

## Owner Ruling
none needed (O92 rules the holds)

## Related
- F-090
- F-204
- ADR-O92
- RV-59
- RV-97

## Resolution
Open.
