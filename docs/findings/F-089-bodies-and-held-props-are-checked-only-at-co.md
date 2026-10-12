# F-089 — Bodies and held props are checked only at contact onsets, never against the floor

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
- examples/wizard_vs_acrobat acrobat@b12 (8.6): lowest point 0.185 m under the ground; A at 3.0 and 9.0: 0.06-0.07 m under
- solver/contact_world.py measures each contact at its own instant only; B's "both feet" support at 4.7 has the right foot 0.35 m up
- the held-prop reach is 2 m (F-062); 7 of 33 contacts are not measurable (no key at the instant, no sample, a surface's face)

## Description
Nothing keeps a body above the floor or a claimed support under the body after the contact's first instant, and a held or embedded prop can drift anywhere within 2 m.

## Impact
Feet sink, supports float and held props hang in the air (the kunai at the climax, F-084).

## Proposed Fix
Backlog RV-14: FLOOR_PENETRATION; supports measured at every key that claims them; a held or embedded prop at its holder's point at every sample (closing F-062); contacts between keys measured by interpolation.

## Owner Ruling
none needed (R-18)

## Related
- PLAN-007
- F-062
- F-084

## Resolution
Open in part: RV-14a (S-078) refuses a body point more than 0.15 m under the floor at any key (FLOOR_PENETRATION:
the lowest floor top, else the convention's ground), and CONTACT_WORLD measures every key's claimed supports (its S11
kinematic node), each part to the top its open support contact names or to the floor, not only a contact's onset.
Re-blocked, all repo-authored: the wizard example's acrobat at 8.6 (both soles 0.185 m under the ground, now a deep
bend), B's lunge at 3.4 and 3.7 (the front sole 0.158 m up, now planted by the hip). A's 0.126 and 0.069 m at 3.0 and
9.0 lie within the tolerance. Open: a held or embedded prop at its holder at every sample (RV-14b, blocked on F-148:
A's source right hand is 0.65-0.87 m from the kunai at 8.5-9.5; a rope dart's sample is its dart, which needs its
line); a support on a surface's face (RV-22); a contact between keys (RV-59).
Noted in S-081 (the sixth review): S-080 put A's right knee 0.109 m in the floor at 7.5, which the 0.15 m allowance
passes (F-206, F-215); between keys B's left sole goes 0.385 m under the floor at 8.75 (RV-59 now carries
FLOOR_PENETRATION between keys).
Noted in S-086 (RV-59a): between keys B's crash (8.5 to 9.0) sinks the left sole 0.385 m under the floor over nine
frames, the only body more than 0.15 m under it between keys in the four examples (RV-59c refuses it).
