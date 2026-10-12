# F-082 — O78 was applied backwards: the smoke bursts on landing at 4.0

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

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
- the principal review, S-035 (docs/prompts/principal_review.md)
- the source: "3.7 A deploys smoke pellet at current position p[0.4,1.1,4.7] SMOKE BURST"
- the golden throws the pellet down at 3.7 and bursts it on the ground at 4.0 (S-024 D1; tests/test_reference_fight_golden.py PELLET)
- ADR-O78: "The smoke pellet must fall after bursting"; the prose prints the smoke "sealed until 4.00" while FX, rules and camera say 3.70

## Description
S-024 read O78 as "bursts as it lands" around S06's beat-end commit (F-061), which reverses the owner's order.

## Impact
The swap's smoke cover arrives after the swap.

## Proposed Fix
Backlog RV-07 (O91), after RV-08 (F-061): the burst at 3.7 at A's body; the spent pellet falls and rests.

## Owner Ruling
ADR-O91

## Related
- PLAN-007
- ADR-O78
- ADR-O91
- F-065
- F-061

## Resolution
Open.
