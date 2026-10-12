# F-081 — The vanish is half-checked: A keeps supports and a hold while gone

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
- examples/reference_fight/envelope.json: A's foot supports b06_c2 and b06_c3 stay open from 3.0 to their releases at 4.7, and the rope dart's hold b06_c4 from 3.0
- prose_mixed.txt line 130 "3.00-5.90 held by A L hand" and line 246 "A is gone from 3.70 until A reappears at 4.40 (substitution): no A body, pose or support in between"
- planner/dynamic_beat_validator.py VANISHED_BODY checks only other beats that list, anchor or touch the vanished actor

## Description
ADR-O18 X9 says no body or support while A is gone, but the contacts that started before the vanish run straight through it.

## Impact
The prompt contradicts itself during the substitution.

## Proposed Fix
Backlog RV-06 (O90): A's supports and holds end at 3.7; the rope dart rests on the ground until 7.5; VANISHED_BODY refuses a vanished actor's open supports and holds.

## Owner Ruling
ADR-O90

## Related
- PLAN-007
- ADR-O18
- ADR-O90

## Resolution
RV-06 (S-042, O90): at the substitution (3.7) A's feet and left hand let go; the rope dart drops from the hand and lies on
the ground from 4.0 until A takes it at 7.5 (the 5.9 release and its sample are gone); A reappears at 4.4 on both feet.
VANISHED_BODY refuses a vanished body's support or hold left open while it is gone
(tests/test_dynamic_beat_validator.py::test_a_vanished_body_lets_go_of_its_supports_and_holds). A's rows from 4.4 to
6.3 no longer hold the rope dart and the slide's rule says it was left at the substitution, each recorded in the golden
test (ROPE_DART_WORDS, VANISH_RULE); the 7.5 crouch and B's 7.5 anchor moved with the dart; shot c10 is full so A's
feet show.
