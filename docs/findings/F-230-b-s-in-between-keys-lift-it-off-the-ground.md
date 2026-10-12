# F-230 — B's in-between keys lift it off the ground, sink its crash and name motions they do not make

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

## Layer
L4c

## Status
in progress

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- Principal review 8 (S-099), measured by the builder on 87804d2 with `interpolation.envelope_keys` and forward
  kinematics at 24 fps: B@6.45 soles 0.338 and 0.220 m up, B@6.7 soles 0.463 and 0.498 m up with the trunk 55.0 degrees
  off vertical; 16 frames from 6.3 to 7.5 with both soles over 0.05 m, none with the keys alone. S06 holds B grounded
  there and the S11 keys at 6.6 and 7.5 claim both feet. The commands free Sp.x and Sp.z with no foot goal
  (tests/test_inbetweens.py ARMS), and the legs hang from the spine (R-35).
- B's crash: the right sole 0.140 m under the floor at 8.625, both soles under it from 8.54 to 8.71, inside the 0.15 m
  allowance; CHANGELOG.md (RV-59e), DEV-35 and S-098 say the 8.75 in-between keeps the crash over the floor. Run with no
  allowance, the same five commands each miss 0.0 and B's lowest point from 8.54 to 8.96 is 0.009 m over the floor.
- B's root runs 9.68 m/s from 8.45 to 8.5, against 3.27 before and 2.15 after (an in-between 0.05 s from a key).
- The acrobat@3.55 right sole is 1.444 m up while S07 holds its right foot on the ground from 2.6 to 3.6.
- Names: acrobat@3.55 "kick_chambered" has the kicking knee at 5 degrees (straight); B@8.45 "shoulders_turning" turns
  the girdle 1.2 degrees less than the keys alone; B@6.45 and B@6.7 say nothing of the lean or the feet in the air.
- ADR-O109: an in-between "is checked like a key (joint limits, the floor, the bodies, its supports)";
  compiler/passes/derived/p13_motion.py checks no support and solver/contact_world.py (`inbetween_bodies`) gives
  "no supports".

## Description
The in-between keys of RV-59e and RV-59c cleared every overlap and every sink over the allowance, but nothing held
B's feet, so the arms-and-spine solve at 6.45 and 6.7 lifted B off the ground in a span every layer calls grounded;
the crash's in-between used the 0.15 m allowance meant for the owner's rows (F-215); and the names were written
before the poses were measured.

## Impact
The prompts print B hovering half a metre up, bent back 55 degrees, between two "steps" lines, under "support ... hold
at all times"; a foot sinks 14 cm mid-crash; words name motions the poses do not make.

## Proposed Fix
RV-59j: S13 refuses an in-between of a body S06 holds grounded at its instant when none of the supports its keys on
both sides claim (S11) sits on its surface within O72's 0.15 m (Claude's interpretation of "its supports", F-053); the
re-block solver's `--floor` keeps the repo's own keys and in-betweens over the floor with no allowance (F-215's
"either way"). B's 6.45, 6.7 and 8.75 are re-solved from recorded commands with a sole held; 8.45 is re-placed if its
pop stays; every in-between's name and description is written from its measured pose. The acrobat's 3.55 inside S07's
open support waits for RV-59g (F-221: where the takeoff lives).

## Owner Ruling
none needed (ADR-O109's Decision, O72, R-35)

## Related
- ADR-O109
- ADR-O110
- F-215
- F-220
- F-221
- RV-59j

## Resolution
In part by RV-59j (S-101): S13 refuses an in-between off the supports its keys on both sides claim
(INBETWEEN_SUPPORT); B's 6.45 and 6.7 are re-solved with both soles held where the declared interpolation puts them
(upright, and 22 degrees back), and an in-between at 7.375 clears the one frame (7.417) the 6.7 solve leaves; every
in-between's name and description is written from its measured pose. Left: the crash's 0.14 m under the floor between
keys, which a no-allowance solve trades for B's legs flung up at 8.75 (RV-59m, waiting for F-215 and the owner's
renders; the records that said "over the floor" are corrected); the acrobat's 3.55 inside S07's open support
(RV-59g); B's root at 9.68 m/s from 8.45 to 8.5 (listed, ADR-O110).
