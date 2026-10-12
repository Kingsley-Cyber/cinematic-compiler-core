# F-082 — O78 was applied backwards: the smoke bursts on landing at 4.0

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L1.1

## Status
resolved

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
RV-07 (S-048, O91): a beat effect may take effect at its beat's start (`at: start`, schemas/beat.schema.json
1.3), and S06 commits it then (solver/prop_state_machine.py `commit_time`). b09's smoke burst and the log's deployment
take effect at 3.7, as the source says; the spent pellet leaves A's right hand at 3.7 and rests on the ground from 4.0.
The prompts print "smoke sealed until 3.70", "3.70 smoke sealed -> burst" and "From 3.70 to the end, smoke pellet keeps
smoke burst" (tests/test_reference_fight_golden.py::test_the_smoke_bursts_at_a_s_body_and_the_spent_pellet_falls_and_rests,
tests/test_state_pass.py::test_an_effect_marked_at_start_takes_effect_at_its_beat_start).
