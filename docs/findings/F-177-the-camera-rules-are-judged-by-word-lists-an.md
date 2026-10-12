# F-177 — The camera rules are judged by word lists, and a hold by one field

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

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
- the fourth principal review, S-063 (docs/reports/2026-10-12-principal-review-4.md)
- validators/prompt_validator.py `camera_rule_problems`: tight, crash zoom, ECU, detail shot, slow-mo, bullet time, overcrank, half speed and a close-up in the sentence after the blow pass; "Keep the lens close to eye level so every contact reads wide." is refused
- library/camera_idioms/knight.yaml "Medium on the shield arm with a short hold at contact" passes the cards' O92 test; idiom cards load by archetype and the fight's are ninja_lean and ninja_broad, so ninja.yaml never reaches it (planner/camera_library.py)
- HIT_HOLD's hold is `movement.kind == static`, so a shaky handheld shot passes; the prompt's HIT_HOLD reads the "t impact: hold with " prefix, not the bodies after it

## Description
RV-60 and RV-57 check the camera's rules by sentences and a single field.

## Impact
A card or prompt can ask for what O92 struck in other words, and a plain rule can be refused.

## Proposed Fix
Backlog RV-71: the cards' rules as structured fields (trigger, scale, movement, playback) checked against the grammar; a hold is static on a locked or smooth rig; the prompt's check reads the printed bodies; idiom cards keyed to the scenes' archetypes. F-160 reopened in part.

## Owner Ruling
whether a smash cut or a whip onto the impact frame, or a shaky handheld shot, is a camera hold (listed)

## Related
- RV-71
- F-160
- F-155
- ADR-O92

## Resolution
Open in part (review 5, S-072): the hold's rig and bodies and the cards' fields are checked; the fields are not tied to the printed words (F-187, RV-85), the hold has no duration and its scale disagrees with the card (F-192, RV-90), and the owner's questions stand (F-197).
Before: RV-71a (S-069): a hit's hold is static on a locked or smooth rig at S16 and S17; the prompt's hold names its bodies;
archetype cards name their idiom card (ninja_lean, ninja_broad). RV-71b (S-070): each convention and idiom carries its
trigger and asks (camera_convention_card 1.1, camera_idiom_card 1.1), which planner/camera_library.py checks against the
grammar and owner O92 (CAMERA_CARD); the prompt prints the genre card's rules word for word (CAMERA_RULES), in place of
the word lists; the knight's shield hit is a hold on both fighters and anime's speed rule applies between hits
(tests/test_camera_solver.py::test_no_camera_card_slows_playback_or_puts_a_close_up_on_a_hit,
tests/test_prose_render.py::test_the_printed_camera_rules_follow_o92).
RV-85 (S-073): the words are tied to the fields (F-187 resolved); the hold's duration and scale (F-192, RV-90) and the owner's questions (F-197) remain.
