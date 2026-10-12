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
Open.
