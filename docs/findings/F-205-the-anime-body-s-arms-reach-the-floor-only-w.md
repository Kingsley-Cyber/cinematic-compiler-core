# F-205 — The anime body's arms reach the floor only with the trunk leaning 58 to 75 degrees

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- S-080 (RV-35a): with the anime body (owner O85: legs 1.25 times the adult's, a 1.22 m standing pelvis) and its draft
  arm (upper arm 0.30 m, forearm 0.35 m), A's floor pickups at 7.5 and 8.0 needed the pelvis at 0.40 m and the trunk
  leaning 58 and 75 degrees (root and spine) for one hand to reach its prop; at the 0.57 m crouch S-029 set, no lean
  under 80 degrees reaches it (solver/reblock.py, the session's search)
- the arm-to-leg ratio is 0.53 (0.65 m against 1.22 m); O85 lengthened the legs and left the arms

## Description
Should the anime body's arms grow with O85's legs (0.65 m to about 0.81 m at the same 1.25), or stay as drafted?

## Impact
Every floor reach in an anime scene bends the trunk deep; longer arms would move every hand point in the anime
examples and re-open their CONTACT_WORLD and BODY_OVERLAP measures.

## Proposed Fix
The owner's answer: a body card change and the re-blocks it brings, or none.

## Owner Ruling
needed

## Related
- ADR-O85
- F-110
- RV-35a

## Resolution
Open.
