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
Open.
