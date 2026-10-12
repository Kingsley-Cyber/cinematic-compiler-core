# F-160 — The camera cards print rules against O92 and R-21

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
medium

## Layer
L5.5

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- every anime prose prompt prints "Cut close on the receiver after a blow lands." (library/camera_conventions/anime.yaml) beside the hit holds
- every live-action prose prompt prints "Slow motion only around the peak of an action." (library/camera_conventions/live_action.yaml) while PLAYBACK_RAMP refuses slowed playback
- the cards still list slow, ramp and freeze playback (S-050 D3); no check reads the printed camera rules

## Description
The prompt tells the model to hold on both bodies and to cut close after the blow.

## Impact
Two camera instructions in one prompt disagree.

## Proposed Fix
Backlog RV-60: the two conventions and the slowed playbacks struck from the draft cards under O92; HIT_HOLD and PLAYBACK_RAMP read the printed camera rules too.

## Owner Ruling
none needed (O92; PLAYBACK_RAMP's reach beyond the fight is the builder's reading, listed for the owner)

## Related
- PLAN-007
- F-083
- ADR-O92
- RV-60

## Resolution
Open in part (review 5, S-072): the struck sentences are gone, but no check reads the printed rule words since S-070 (F-187, RV-85).
Before: Open in part (review 4, S-063): the struck sentences are gone, but the check that replaced them is a word list that misses plain violations and misfires on plain rules; F-177, RV-71.
Before: RV-60 (S-059): anime's "Cut close on the receiver after a blow lands.", live action's "Slow motion only around the
peak of an action." and the ninja idiom's insert on a landing blade are struck from the draft cards, and every
convention card's playback is [normal] (card_version 2, library log); the prompt validator reads the printed "Camera
rules:" line for both codes (validators/prompt_validator.py camera_rule_problems;
tests/test_prose_render.py::test_the_printed_camera_rules_follow_o92,
tests/test_camera_solver.py::test_no_camera_card_slows_playback_or_puts_a_close_up_on_a_hit). The UGC card's list
follows PLAYBACK_RAMP's reach to every scene, the builder's reading listed in F-053.
Resolved again in RV-71b (S-070): the word lists gave way to the cards' structured rules and the word-for-word check (F-177).
Resolved again in RV-85 (S-073): the cards' words are read against their fields (F-187).
