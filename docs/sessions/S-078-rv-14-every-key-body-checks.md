# S-078 — RV-14: every key keeps its bodies above the floor, its supports on their surfaces and its props in hand

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-14 (PLAN-007; split here into RV-14a and RV-14b, D3); findings F-089, F-062; rulings O72, O83, O10

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-078]

## Plan
CONTACT_WORLD (S13) measures each contact at its own onset only: nothing keeps a body above the floor, a support's
part on its surface after its first instant, or a held or embedded prop at its holder after it is taken (F-089; the
held prop's only check is 2 m from the holder's root at S04, F-062). The class: a contact that lasts, and a body that
must stay out of the floor, measured at every key, not once.
1. FLOOR_PENETRATION (new, S13): at every key, no body point (forward kinematics) lies more than O72's 0.15 m under the
   lowest floor's top.
2. CONTACT_WORLD measures an open support at every key of its performer while it lasts, the part to its surface's top.
3. CONTACT_WORLD measures a held prop at every sample of its hold where its holder has a key: the grip part to the
   sample; an embedded prop at every sample after it is embedded: the sample to the body part it went into.
4. Misses in repo-authored keys and samples are re-blocked; a miss in the owner's source rows waits (R-06, O10).
5. A contact between keys (by interpolation, F-089's last point) goes to RV-59, which models the interpolation.

Predictions, made before the change (07:58 by the clock):
1. The gate passes before the change: 703 tests (2335e8d, S-077's chained gate).
2. FLOOR_PENETRATION refuses between one and three keys in the four examples (the wizard example's acrobat at 8.6
   among them); none of the reference fight's, whose lowest points sit within 0.15 m of the ground.
3. Supports at every key miss at between two and six later keys in the reference fight (B's "both feet" at 4.7 among
   them) and at most two in each other example.
4. The held and embedded props miss at between zero and three samples in the reference fight; the UGC's glasses
   pass.
5. Every miss is in repo-authored keys or samples and is re-blocked without touching a source row; no prose prompt
   changes beyond the re-blocked keys' numbers; about 707 tests (703 and four).

## Decisions
- D1 — The floor is the lowest floor top, else the convention's ground (the UGC names no floor); a body is measured by
  its forward-kinematics points, not its capsules' surfaces, as CONTACT_WORLD measures a sole on a top, so a part may
  sink by its radius; the tolerance is O72's 0.15 m. Level: interpretation (F-053).
- D2 — A key's claimed supports are its S11 kinematic node's: the contacts alone missed the case F-089 names (B's feet
  bear weight with no support contact), and the live-action and UGC bodies have none. Each part is measured to the
  top its open support contact names, or to the floor; a claim on a surface that is not a floor waits for its faces
  (RV-22); a contact's onset stays measured with the contact, so the owner's exceptions keep covering it. Level:
  interpretation (F-053).
- D3 — RV-14 split: RV-14a (this) and RV-14b, a held or embedded prop at its holder at every sample, blocked on F-148:
  A's source right hand is 0.65-0.87 m from the kunai the source keeps in B's shoulder at 8.5-9.5 (no repo key or
  sample can close it without setting a source row aside, R-06, O10), and a rope dart's sample is its dart, which
  needs its line. Level: covered.
- D4 — Re-posed, all repo-authored, through the bones (the root stays the slot's pos): the wizard example's acrobat at
  8.6 into a deep bend (hips -43, knees 81: soles 0.017 m, from 0.185 m under; its description says "deep bend"), B's
  lunge at 3.4 and 3.7 by the hip alone (-70.17, -65.7: the front sole 0.034 and 0.039 m, from 0.158). A first fix
  that straightened B's knee made S15 read B's "rising" toward 4.0 as sinking (SHAPE_DIRECTION), so the knees stay.
  Level: covered (R-33).
- D5 — The S13 instructions taught none of the world checks; they now teach CONTACT_WORLD (the claims), BODY_OVERLAP
  and FLOOR_PENETRATION (F-195's class, for S13). Level: covered.
- D6 — A contact between keys goes to RV-59 (title and findings widened); RV-22 and RV-47 now depend on RV-14a.
  Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | S13 (L4c) reads its keys, S11's claims and S07's contacts; S04's anchors untouched |
| Predictions written first | PASS | the session file was written at 07:58, before any code or probe |
| New checks fire and stay silent | PASS | measured before the re-posing: FLOOR_PENETRATION 1 key, the claims 2 of 82 (39, 19, 16 and 8); after: none in the four examples; tests: the takeoff's old bend refused, 0.12 m passes and 0.22 m does not, a lifted claimed foot refused |
| Neighbours | PASS, with carriers | supports on a face (RV-22); held and embedded props (RV-14b, measured: the UGC's glasses, B's kunai and shuriken meet the hand; the climax's kunai and the rope dart do not); contacts between keys (RV-59); the shape check S15 runs on the re-posed keys |
| The step's instructions teach it | PASS | euler_solving.txt: the world checks and that the bones meet them |
| Tests changed with their data | PASS | `git diff -- tests`: two new tests and two rule-table rows; nothing removed or loosened |
| Examples | PASS | three keys re-posed; the plans rebound; the prose changes only on the re-posed keys' lines; checklist counts the same |
| Records | PASS | F-089 open in part (RV-14b, RV-22, RV-59); F-062 to RV-14b; F-053; map 18 (kernel log); backlog 31; PLAN-007 (its table brought up to date); CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |
Claim corrected before the commit: PLAN-007's slice table had not been updated since S-072 (RV-85, RV-86, RV-13, RV-15a
and RV-15b read open); it is now.

## Duration
from 07:58 (the plan) to 08:09 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/floor_penetration.py (new); solver/contact_world.py (`_claims`); compiler/passes/derived/p13_motion.py
  (the packet's floor_y; FLOOR_PENETRATION)
- planner/prompts/euler_solving.txt; tests/test_motion_solver.py (two tests, two rule rows)
- examples: reference_fight ninja_broad@b08, @b09; wizard_vs_acrobat acrobat@b12; every plan rebound and regenerated
- kernel/knowledge_map.yaml 18; backlog 31 (RV-14a done, RV-14b blocked, RV-16 next; RV-59, RV-22, RV-47); F-089;
  F-062; F-053; PLAN-007; CHANGELOG; run report

## Verification
- before: S-077's chained gate at 2335e8d: 703 passed
- Prediction 1 held. Prediction 2 held (one key: the acrobat at 8.6; the fight's lowest points 0.126 and 0.069 m
  under, within 0.15). Prediction 3 held in part: two misses in the fight and none elsewhere, but at B's lunge (3.4,
  3.7), not 4.7, which passes. Prediction 4 failed: five held samples miss in the fight (the kunai at 8.5, 9.0 and
  9.5; the rope dart at 8.0 and 9.5), not three or fewer; the UGC's glasses pass. Prediction 5 held in part: the
  kunai's misses are the source's (F-148), so not every miss could be re-blocked; the prose changes only on the
  re-posed keys; 707 tests. Predictions 3 of 5.
- the gate on this record (08:09:57): `scripts/verify.sh` exit 0, 707 passed in 75.35 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
