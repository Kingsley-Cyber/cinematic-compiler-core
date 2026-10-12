# S-049 — RV-49: no body through another; a strike meets the target's surface (F-144)

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-49 (PLAN-007); findings F-144, F-151; rules R-18, R-33; rulings O83, O102, O107

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-049]

## Plan
F-144: no check keeps two bodies from occupying one place, and a strike is measured to the target's centre point. A
scan before the change (capsules with draft radii, every instant two bodies have keys) found nine overlaps: B at 3.4
(forearms, 0.026 m), 3.7 (B's trunk inside A's, 0.166 m), 4.4 (shins, 0.091 m), 4.7 (A's thigh through B's trunk,
0.208 m), 6.6 (B's forearm through A's arm, 0.07 m), 8.5 (B's head in A's trunk, 0.101 m), 9.0 and 9.5 (A's shin
through B's thigh, about 0.09 m), and the acrobat's foot through the wizard's trunk at 3.6 (0.166 m).
1. The body card gives each segment a radius (draft); forward kinematics builds capsules.
2. BODY_OVERLAP at S13: no capsule of one body within the radii of another's, at each instant both have keys.
3. CONTACT_WORLD measures a contact between two bodies from the part's surface to the target's.
4. The failing poses re-blocked on the repo-authored side (B; the acrobat), least change, then the gate.

Predictions, written after the scan and before the code (not into this file before the code: a process slip of the
kind F-128 names):
1. The gate passes before the change: 650 tests (186de1e, S-048's gate).
2. The new check refuses exactly the scan's eight reference-fight instants and the wizard's 3.6.
3. Measured surface to surface, the four body contacts (the knee at 4.7, the catch's two hands at 6.6, the kick at 3.6)
   read 0 m before the re-blocks, since each part sits inside its target.
4. Only B's and the acrobat's keys move; A's rows keep the source's numbers; the golden's re-blocked roots and B's end
   state move with them.

## Decisions
- D1 — Each segment is a capsule (its axis between two joints) with a draft radius on the body card: trunk 0.13,
  across the shoulders 0.06, across the hips 0.08, neck 0.05, head 0.10 (a sphere), upper arm 0.05, forearm 0.04,
  thigh 0.08, shin 0.055, foot 0.045; the anime body keeps the adult's girth (library/body_segments.yaml 5, schema
  3.1). Why: F-144's proposed fix, R-18. Alternatives: boxes or ellipsoids (more numbers, no source). Level: covered
  (the values are drafts for the owner, R-30).
- D2 — BODY_OVERLAP checks each instant both bodies have keys, allows no depth, and leaves out a body's own segments,
  points between keys (RV-47) and props (no extent: F-151, RV-54). Level: covered (the interpretation is in
  solver/body_overlap.py for owner review).
- D3 — A contact between two bodies runs from the part's surface (the radius of the segment its point ends: a hand the
  forearm's, a knee the thigh's) to the nearest capsule of the target part (the torso and shoulders when none is
  named); a part inside the target reads 0 m and is BODY_OVERLAP's to refuse; the printed target point is the surface
  point facing the part. Level: covered (F-144).
- D4 — The re-blocks move the repo-authored side (B; the source gives B only words; the acrobat), with the least change
  and a 0.01 m clearance, each sole kept at its height: B's left arm at 3.4; B held back at 3.7 (1.0 to 1.39 m in x,
  4.7 to 4.53 in z, the bow eased from 25 to 20 degrees) while A leans into the swap, then the lunge to the log at 4.0;
  B 0.09 m further at 4.4 with the trailing right leg swung in; B 0.24 m along the launch at 4.7 so A's knee meets the
  surface of B's back (0.009 m); B's hands on the surface of A's elbow at 6.6 (0.012 and 0.010 m); B's bow eased from
  40 to 30 degrees at 8.5; B lying 0.18 m aside at 9.0-9.5 rather than the right leg swung out 60 degrees (cost 0.037
  against 0.41); the acrobat's kick bent a little so the foot meets the wizard's chest (0.02 m). Level: covered (O83
  point 1, R-33).
- D5 — Shot c08 (3.7) steps back from 1.68 to 2.1 m, still a medium shot (frame height 1.44 m), so B, now further back,
  stays in frame (S16 refused it). Level: covered (R-33).
- D6 — The golden's records change with RV-49 (ADR-O102, R-33): REBLOCKED_ROOTS (B at 3.7, 4.4, 4.7, 8.5, 9.0, 9.5), B's
  end state in tests/test_prose_render.py, and B's 4.4 leg words in tests/test_leg_frame_rewrites.py (the right leg
  reads forward-low, not right-forward-low). Four tests added. Level: covered.
- D7 — A body through a prop is filed, not dropped: F-151 with RV-54 (props get an extent). Level: covered (no
  shortcuts: a gap is fixed, named with a slice, or asked).
- D8a — Held back at 3.7, B now stands from 3.4 to 3.7 under the source's "B charges forward" and charges in the
  3.7-4.0 lunge instead: A's 3.7 lean (read under ADR-Q6, F-143) fills the space ahead of B. Recorded as F-150's new
  item for RV-33, which re-stages B's track from the source's words. Level: covered (named with its slice).
- D8 — S-048 bumped the backlog to 21 for status changes alone, which docs/versioning.md does not ask for; 21 stays (a
  version is not reused); this slice's 22 is for RV-54's new item. Level: covered.

## Duration
about 33 minutes by the commit times (01:25 to 01:59); it read "about 2 hours (the re-block solves took about 10 minutes of it)" until RV-46
(S-056) corrected it (F-166)

## Changes
- library/body_segments.yaml 5 (radii), schemas/cards/body_segments.schema.json 3.1; solver/forward_kinematics.py
  (`joints`, `capsules`, `surface_gap`); solver/body_overlap.py (new, BODY_OVERLAP); solver/contact_world.py (surface
  to surface); compiler/passes/derived/p13_motion.py (radii in the packet; the check)
- examples/reference_fight/plans/motion.json, temporal.json (B's anchors at b09, b11, b12, b21, b22, b23), camera.json
  (c08); examples/wizard_vs_acrobat/plans/motion.json (acrobat@b06); every example re-bound; outputs regenerated
- tests: test_forward_kinematics.py (three tests), test_motion_solver.py (a BODY_OVERLAP break), and the moved records
  in test_reference_fight_golden.py, test_prose_render.py and test_leg_frame_rewrites.py
- kernel/knowledge_map.yaml 6 (T10, C21; 5 named a C21 locator the map test refused), docs/rules.yaml 5.1 (R-18); the
  four logs
- F-144 resolved; F-151 (new); backlog 22 (RV-49 done, RV-54 added, RV-09 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-048's gate at 186de1e: `scripts/verify.sh` exit 0, 650 passed
- after: `scripts/verify.sh` exit 0, 654 passed, check: PASS; `make golden` passed; S13 refuses nothing in any example and
  `compiler.rebind --write` re-bound every plan
- Prediction 1 held. Prediction 2 held for the reference fight (S13 refused exactly those eight); the wizard's 3.6 was
  re-blocked with them, not run alone. Prediction 3 held (0.0 m for all four before the re-blocks; after them 0.009 to
  0.02 m). Prediction 4 held, and B's 4.4 leg word moved too; not predicted: S16 refused c08 once B stood back at 3.7.

## Next
RV-09 (hits as camera holds, O92).
