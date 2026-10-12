# S-093 — RV-95b: the pickups judged as drawn, their stated bounds restored

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-95b (PLAN-007); findings F-223, F-226 (principal review 7); F-224 split off to RV-95c; rulings R-34 (a
whole-body quality reads every joint it depends on), O18 (A crouched on the ground at the pickups), O11 (the anime
limits), O72

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-093]

## Plan
S-083 stated its pickup bounds (every knee 0.08 m over the floor, every ankle 0.045 m, the head 0.2 m over the pelvis,
the trunk leaning 70 degrees or less), then relaxed the ankle's after the solve, gave the knee and head tests a
millimetre of slack, and checked the lean by a sum of X angles while the drawn trunk leans 74 degrees at 8.0 (F-223,
F-226). The class: a bound that moved to meet its data, and a quality measured on a stand-in for what the body draws.
1. The recorded commands state every bound S-083's plan stated, as goals the solver keeps: the knees over 0.08 m and
   the ankles over 0.045 m, the head over the pelvis by 0.2 m, and the lean as the chest over the pelvis by the
   spine's cosine of 70 degrees; each with the solver's 1 mm margin (its floors are soft), stated here before any
   solve. The twist stays inside the genre's limits (O11).
2. Both pickups re-solved from their recorded start keys (a62e551); a bound the solve cannot meet is reported with
   its number, not relaxed.
3. The tests read the lean from the trunk's vector and hold every bound without slack; S-078's lunge test says what
   it shows (the solver reaches a hand-chosen height), not a re-derivation.
4. F-224 (the words in the legend's frame, A's head toward B) is RV-95c: it needs a facing goal and F-111's frame.

Predictions, made before the change (12:01 by the clock):
1. The gate passes before the change: 734 tests (46f6f84, S-092's chained gate).
2. The 7.5 pickup meets the knee, head and lean bounds, but its ankles stay under 0.045 m (the foot is the shin's
   extension, F-219).
3. The 8.0 pickup cannot keep its trunk within 70 degrees while its hand reaches the kunai on the ground: one of the
   two misses, and is reported.
4. The fight's overlap frames between keys stay within 29 plus or minus 3, with no new sink; no camera shot is
   re-authored.
5. About 735 tests.

## Decisions
- D1 — The recorded commands state every bound S-083's plan stated, each floor with the solver's 1 mm margin (its
  floors are soft penalties): the knees over 0.08 m, the ankles over 0.045 m, the head 0.2 m over the pelvis, and the
  lean as the chest's height over the pelvis by 0.5 x cos 70 = 0.171 m (the trunk is the pelvis-to-chest segment,
  R-34). The spine is left to the anime limits (O11), so S-083's probe bound on Sp.x (-30..40) is gone. Level: covered
  (S-083's stated bounds; review 7's practice; O11).
- D2 — A bound the solve cannot meet is reported, not moved: the trunk leans 70.2 degrees at 7.5 and 71.2 at 8.0 (from
  A's own 0.57 m the hand cannot reach the ground within 70: the shoulder is about 0.74 m up, the arm 0.65 m long),
  and three ankles sit under the foot's 0.045 m (0.0385 and 0.0263 at 7.5, 0.0449 at 8.0). The test pins them as
  drawn; F-223 becomes the owner's question and F-215 carries the ankles. The re-solved keys replace S-083's: they are
  nearer every stated bound (7.5's ankles from 0.022 and 0.012 m; 8.0's lean from 74.0 degrees, its right ankle from
  0.038 m). Level: question (F-223, F-215).
- D3 — F-224 (the pickup words in the legend's frame, A's head toward B) is split to RV-95c: it needs a facing goal in
  the solver and meets F-111's question of the frame. Level: covered (one gap per slice).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | A's re-blocked pickups and their tests (L4c) |
| Predictions written first | PASS | the session file was written at 12:01, before any code |
| Bounds stated before the solve | PASS | D1's bounds and margin are in the plan, written before the commands ran |
| A re-block re-derives | PASS | the re-derivation test runs the new commands from the start keys and gets the committed bones |
| No slack, no moved bound | PASS | the knees and head asserted at their bounds exactly; the unmet lean and ankles pinned as drawn and asked (F-223, F-215) |
| Neighbours | PASS | S-078's test says what it shows (F-207); DEV-09 updated; the between-keys pin 29 to 28 frames; F-053's S-083 entry superseded |
| The step's instructions teach it | n/a | no check changed |
| Examples | PASS | the fight's 7.5 and 8.0 keys re-solved (DEV-09); outputs regenerated; the camera plan only re-bound |
| Records | PASS | F-226 resolved; F-223 a question; F-215 noted; backlog 39 (RV-95b done, RV-95c ready, RV-59f next); deviations.yaml 4; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first |

## Duration
from 12:01 (the plan) to 12:05 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- examples/reference_fight/plans/motion.json (A's 7.5 and 8.0 keys re-solved) and its outputs; deviations.yaml 4
- tests/test_reblock.py (the commands' bounds; the shape test by the trunk's vector, without slack; S-078's test
  reworded); tests/test_reference_fight_golden.py (GROUNDED_PICKUPS); tests/test_interpolation.py (28 frames)
- F-226 resolved; F-223 a question; F-215 and F-053 noted; backlog 39; PLAN-007; CHANGELOG; run report

## Verification
- before: S-092's chained gate at 46f6f84: 734 passed
- Prediction 1 held. Prediction 2 held in part (the knees and the head met and the ankles not, as said; the lean
  70.2, just over). Prediction 3 held (71.2 degrees with the hand 1 cm from the kunai; reported). Prediction 4 held
  (28 frames, no new sink, the camera only re-bound). Prediction 5 held in part (734: one under). Predictions 4 of 5.
- the gate on this record (12:05:11): `scripts/verify.sh` exit 0, 734 passed in 74.22 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first in the chained commit)
