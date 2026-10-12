# F-155 — HIT_HOLD reads O92 backwards: only holds the S17 author placed are judged

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
high

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
RV-57 (S-062): planner/hits.py finds the hits from the contacts (a touch on another performer's body; a strike,
deflect or parry on a prop another performer holds or threw; a catch of a body; a body touched by a blade another
performer holds); S16's packet lists them and the camera validator holds the camera on each (HIT_HOLD at S16), and
S17's `hit_hold`, the prose's holds and the prompt judge them with S17's holds, whatever S17 holds
(tests/test_hits.py, test_camera_solver.py::test_a_hit_from_the_contacts_is_a_camera_hold_at_s16,
test_render.py::test_a_hit_from_the_contacts_is_held_whatever_s17_holds,
test_prose_render.py::test_the_prompt_owes_a_hold_at_every_hit_whatever_s17_holds). The framing is still judged by
the shot's subjects and the horizontal projection; the vertical framing is RV-15's (F-090).
