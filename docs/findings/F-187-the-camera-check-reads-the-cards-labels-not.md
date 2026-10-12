# F-187 — The camera check reads the cards' labels, not the words the prompt prints

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
high

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
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- planner/camera_library.py `rule_problems` reads a rule's `trigger` and `asks`, never its `statement`, which is what the prompt prints; S-072's probe: "Cut close on the receiver after a blow lands." tagged fast_move with empty asks passes, and so does a slow-motion rule with empty asks (knight.yaml, live_action.yaml and ugc_ad.yaml carry such rules)
- validators/prompt_validator.py CAMERA_RULES compares the printed rules with prose_renderer.camera_rules, the renderer's own output, so it holds by construction; RV-60's word lists, which read the words, were removed in S-070
- docs/rules.yaml R-21 still lists HIT_HOLD and PLAYBACK_RAMP as reading the printed rules

## Description
S-070 moved the O92 check off the words the model reads onto labels the builder writes, a capability weaker than the one it replaced (finish.md section 3, ADR-O102).

## Impact
A card can print a rule against O92 under a compliant label, and no code fires.

## Proposed Fix
Backlog RV-85: a rule's statement may ask only what its fields ask (each camera term it uses, in the grammar's words and their common synonyms, is allowed by its asks), and the word lists stay as a floor on the printed rules; R-21 lists CAMERA_RULES and CAMERA_CARD. F-160 and F-177 reopened in part.

## Owner Ruling
whether a card's rule is its printed words or its fields (listed, F-197)

## Related
- RV-85
- F-160
- F-177
- ADR-O92

## Resolution
Open.
