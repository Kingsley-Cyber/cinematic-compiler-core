# F-155 — HIT_HOLD reads O92 backwards: only holds the S17 author placed are judged

<!-- docs-version: 1.0 -->

## Type
bug

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
- the third principal review, S-054 (docs/reports/2026-10-12-principal-review-3.md)
- compiler/passes/derived/p17_render.py `hit_hold` and validators/prompt_validator.py `_camera_checks` judge only the holds placed on impact frames; with the 4.7 hold dropped, a handheld whip pan on A alone at 4.7 passes S16 and S17 with no finding (two reviewers' probes)
- "both bodies in frame" is checked as the subject list and the horizontal screen x; with the aim 1 m above the pelvis (F-090) B has 9, 8, 3 and 1 of 19 joints in frame at 2.5, 4.7, 6.6 and 8.5, and the contact falls below the frame at 2.5 and 8.5
- ADR-O92's consequence put the check at S16, which sees the contacts

## Description
O92 says hits are holds; the check says a hold on an impact frame is a hit, so a scene with no authored hold escapes it, and the framing is judged in x only.

## Impact
A new fight's hits can be cut as inserts or moving shots, and "both bodies in frame" is printed on shots that frame the air above them.

## Proposed Fix
Backlog RV-57: hits found from the contacts (a strike or deflect on another performer's body or on a prop another performer threw or holds, a catch of a body, a body struck by a blade another holds), each a static hold on every body present at S16 and in the prompt, whatever S17 holds; the vertical framing with RV-15.

## Owner Ruling
none needed (O92)

## Related
- PLAN-007
- F-083
- F-090
- F-015
- ADR-O92
- RV-57
- RV-15

## Resolution
Open.
