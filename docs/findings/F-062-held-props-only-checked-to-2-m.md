# F-062 — A held prop is only checked to within 2 m of its holder

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
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
Self-audit of M9-03 (session S-004): the rope dart's held sample at 8.0 stayed at [0.4, 1.3, 4.0] after A moved to
[-0.2, 0.6, 5.1], 1.44 m from A's root and at neither A's hand nor B's shoulder; PROP_KINEMATICS passed it.

## Description
PROP_KINEMATICS holds a held prop within REACH_M = 2 m of its holder's root anchor (planner/dynamic_beat_validator.py,
an interpretation). A held prop left behind when its holder moves passes unless it ends up more than 2 m away; the
self-audit caught one such sample by hand.

## Impact
The prop track can print a held prop away from the hand that holds it, and the model may draw it there.

## Proposed Fix
Check a held prop against the holding hand's world position once forward kinematics exists (backlog M9-06,
CONTACT_WORLD), or tighten the held distance to an arm's reach; part of M9-04's positions work.

## Owner Ruling
none needed (O8 holds prop positions to the holder; the 2 m reach is Claude's interpretation)

## Related
- PLAN-003
- backlog M9-04
- backlog M9-06
- backlog RV-14b (S-078 measured every held sample: the UGC's glasses, B's kunai and shuriken meet the hand; the
  climax's kunai misses by 0.65-0.87 m, F-148; the rope dart's dart is not at the hand by design, it needs its line)

## Resolution
Open. The one sample the audit found was moved into A's left hand ([0.2, 0.9, 4.9], 0.54 m from the root).
