# S-050 — RV-09: hits are camera holds with both bodies in frame; no playback ramps (O92)

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-09 (PLAN-007); findings F-083, F-005, F-015, F-090; rulings O92, O47, R-17, R-21, R-33, O102

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-050]

## Plan
O92 (owner): "Camera hold with both bodies in frame at 2.5, 4.7, 8.5. No playback ramps. Hits are holds, not
inserts." The three hits were 85 mm slow-motion smash-cut inserts and three shots ramped at x0.5 inside a fixed 10 s
(F-083); the prose printed one hold of four (6.6); the source's fov45 at 0 and its push in at fov35 from 9.5 were a
35 mm and an 18 mm shot.
1. S16 refuses a shot that plays other than normal x1 (PLAYBACK_RAMP); S17 refuses a hit (a hold on an impact frame)
   whose shot is not a static camera hold on every body present, or is a close-up or insert (HIT_HOLD); the prompt
   checks both.
2. The hit shots re-authored as holds; the ramps removed; the source's lenses followed (R-17).

Predictions: none were written into this file before the code (a process slip of the kind F-128 names, the second in
a row; the next slice writes them first). What the design assumed: the foot (2.5) needs a full shot, the knee (4.7) a
medium_wide and the torso (8.5) a medium; the checklist moves only where a prompt cannot show a camera section (LBN).

## Decisions
- D1 — A hit is a hold on an impact frame (S17's frame parts: 2.5, 4.7, 6.6 and 8.5 in the reference fight, 3.6 and 5.2
  in the wizard example), as the prose's hold lines already read it; HIT_HOLD runs at S17, the first step that sees the
  shots and the impact frames (ADR-O92's consequence line put it at S16), and in the prompt. Level: covered (plan
  v1.2: a check sits at the first step that can see its data).
- D2 — A camera hold is a static shot whose subjects include every body present at the hit (a vanished one is not,
  O18), at no close-up or insert. Level: covered (R-21, O92; the reading is in p17_render.hit_hold).
- D3 — PLAYBACK_RAMP refuses any shot that plays other than normal x1, at S16 and in the prompt; the genre cards keep
  their playback vocabularies, since a fixed-length clip, not the genre, rules out speed changes. Level: covered (O92).
- D4 — The camera grammar's impact intent follows O92: medium, medium_wide or full, and no slowed playback (version 2).
  Level: covered (the owner's ruling over the draft card's impact row).
- D5 — The hit shots: c05 full at 3 m (the foot shows), c11 medium_wide at 2.2 m (the knee), c20 medium at 1.8 m (the
  torso), each 35 mm, static, aimed at the midpoint from across the fighters' line and clear of the 30-degree rule; the
  ramps at 3.7, 5.5 and 6.6 go; the wizard example's kick at 3.6 and landing at 5.2 become full holds on both bodies.
  Level: covered (R-33).
- D6 — The source's lenses are followed (R-17, F-083's proposed fix): c01 at 43.46 mm (fov45); 9.0 to 10.0 split into a
  low static hold on the crash (c21, full, 9.0-9.5) and the slow push in at 57.09 mm (fov35, c22, 9.5-10.0); c15 is the
  source's medium (at 2.1 m). The source's "ground level" at 3.0 and 9.0 needs the camera's aim fixed first: added to
  F-090 for RV-15. Level: covered.
- D7 — R-21 takes O92 (rules 6.0): no insert on a hit and no playback speed change, enforced by HIT_HOLD and
  PLAYBACK_RAMP. Level: covered (owner O92).
- D8 — Records changed with O92 (ADR-O102): the golden's shot count (21 to 22, and a test of the holds and lenses), two
  camera rule cases (a slowed playback is PLAYBACK_RAMP's now; the impact intent no longer asks for one), and the
  wizard camera's sides (the kick's on-axis insert is a hold from the left). F5 is caught by HIT_HOLD, so F-005 is
  resolved; F-015 (the deflect's wording) stays open. Level: covered.

## Duration
about 1.5 hours

## Changes
- validators/camera_validator.py (PLAYBACK_RAMP), compiler/passes/derived/p17_render.py (HIT_HOLD),
  validators/prompt_validator.py (both, in the prompt), planner/prompts/camera_selection.txt (the hit and playback rule)
- library/camera_grammar.yaml 2 (the impact intent); kernel/knowledge_map.yaml 7 (C10, C25); docs/rules.yaml 6.0
  (R-21); validators/checklist.py (F5 caught by HIT_HOLD); the three logs
- examples/reference_fight/plans/camera.json (c01, c05, c08, c11, c13, c15, c16, c20, c21, c22 new),
  examples/wizard_vs_acrobat/plans/camera.json (c04, c06); every example re-bound; outputs and checklists regenerated
- tests: test_render.py, test_prose_render.py and test_reference_fight_golden.py (one test each), test_camera_solver.py
  (a PLAYBACK_RAMP case, two cases and the sides moved with O92), test_dag_conformance.py (two breaks)
- F-083 and F-005 resolved; F-090 noted; backlog (RV-09 done, RV-10 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-049's gate at 649ddd7: `scripts/verify.sh` exit 0, 654 passed
- after: `scripts/verify.sh` exit 0, 660 passed, check: PASS; `make golden` passed
- The design's assumptions held (full, medium_wide and medium show the three contacts; the prose checklist counts did
  not move; C10 went from NOT CHECKED to FAIL on each LBN prompt, which has no camera section). Not foreseen: the
  grammar card's impact row, which asked for close-ups and slow motion, and the wizard example's two impact shots.

## Next
RV-10 (the kunai drive and the catch, O93).
