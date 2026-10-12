# F-083 — Hits are slow-motion close-up inserts, and most of the source's holds are not printed

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L5.5

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
Open.
