# F-083 — Hits are slow-motion close-up inserts, and most of the source's holds are not printed

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L5.5

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
- prose_mixed.txt lines 180, 186 and 195: "smash_cut to insert ... 85 mm telephoto" at 2.5, 4.7 and 8.5, played x0.25; x0.5 ramps at 3.7, 5.5 and 6.6
- the source's anime.holds lists ten holds; the prose prints one (6.6); renderers/prose_renderer.py drops a hit's hold when its shot is a close-up or frames fewer than two bodies
- the source's camera words ("0 ... fov45", "9.5 slow push in crouch fov35") against about 54 degrees and an 18 mm wide shot in the golden

## Description
R-21 and O47 want a hit held by the camera with both bodies in frame, never a close-up; the golden cuts to inserts and changes playback speed inside a fixed 10 s clip.

## Impact
The hits read as cutaways; slow motion cannot fit a fixed timeline.

## Proposed Fix
Backlog RV-09 (O92): the three hits are camera holds framing both bodies; no playback ramps; HIT_HOLD and PLAYBACK_RAMP at S16; the source's other camera directives followed as recorded deviations.

## Owner Ruling
ADR-O92

## Related
- PLAN-007
- ADR-O92
- ADR-O47
- F-005

## Resolution
RV-09 (S-050, O92): the hits at 2.5, 4.7 and 8.5 are static camera holds with both fighters in frame at
35 mm (full, medium_wide and medium), no insert, no slow motion, and every shot plays at normal x1 (the ramps at 3.7,
5.5 and 6.6 went). S16 refuses a slowed shot (PLAYBACK_RAMP, validators/camera_validator.py); S17 refuses a hit that is
no camera hold on the bodies (HIT_HOLD, compiler/passes/derived/p17_render.py: at S17, where hits are its impact
frames, not at S16 as ADR-O92's consequence line put it); the prompt checks both (validators/prompt_validator.py). The
prose prints all four holds on hits (2.5, 4.7, 6.6, 8.5). The camera grammar's impact intent follows O92
(library/camera_grammar.yaml 2), and the wizard example's kick (3.6) and landing (5.2) are holds too. The source's
lenses are kept: fov45 at 0 and the slow push in at fov35 from 9.5, now its own shot. Its "ground level" at 3.0 and
9.0 waits for RV-15 (F-090: the camera aims 1 m above the root). Tests:
tests/test_render.py::test_a_hit_is_a_camera_hold_on_the_bodies,
tests/test_prose_render.py::test_hits_are_camera_holds_and_nothing_plays_slow,
tests/test_reference_fight_golden.py::test_the_hits_are_held_and_the_source_lenses_kept.
Corrected in RV-46 (S-056, review 3): HIT_HOLD judges only the holds S17 placed (F-155, RV-57); "both fighters in
frame" is checked across the frame only, with the camera aimed above them (F-090, RV-15); the camera cards still print
"cut close" and "slow motion" (F-160, RV-60).
