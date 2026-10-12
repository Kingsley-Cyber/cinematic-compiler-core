# S-101 — RV-59j: an in-between keeps its keys' supports; B's in-betweens stand, and its crash stays over the floor

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59j (PLAN-007); finding F-230; rulings O72, R-18, R-35; ADR-O109; ADR-O110

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-101]

## Plan
ADR-O109 checks an in-between "like a key (joint limits, the floor, the bodies, its supports)", but S13 checked no
support, so the arms-and-spine solves at 6.45 and 6.7 lifted both of B's soles 0.22 to 0.5 m in a span both keys say
B stands on; and B's crash used the 0.15 m allowance meant for the owner's rows (F-230). The class: any in-between
of a body its keys hold on a surface.
1. S13 refuses an in-between whose keys on both sides claim a common support (S11) when none of those parts is within
   O72's 0.15 m of its surface (its open support contact's surface, else the floor), measured as CONTACT_WORLD
   measures a key's claims (INBETWEEN_SUPPORT).
2. The re-block solver's `--floor` keeps contact points over the floor by its margin, with no allowance: it places only
   the repo's keys (F-215's "either way"). [Dropped in the slice, D4: split to RV-59m.]
3. B's 6.45 and 6.7 re-solved from recorded commands with both soles held where the declared interpolation puts them
   and the legs free; B's 8.75 re-solved with the new floor term; the seven in-betweens re-derive in order.
4. Every in-between's name and description written from its measured pose.

Predictions, made before the change (13:53 by the clock):
1. The gate passes before the change: 750 tests (cf8aae5, S-100's chained gate).
2. INBETWEEN_SUPPORT refuses exactly B@6.45 and B@6.7 on the committed plans.
3. With both soles held and the legs free, 6.45 and 6.7 clear A with a miss of 0.0; B's trunk at 6.7 leans under 35
   degrees.
4. With no allowance, B's lowest point from 8.5 to 9.0 is at or over the floor.
5. 751 tests (one new refusal test); the floor term's acrobat assertion still holds.

## Decisions
- D1 — INBETWEEN_SUPPORT: an in-between's supports are those both its keys claim (S11); one of them within O72's
  0.15 m of its surface (its open support contact's surface, else the floor, as CONTACT_WORLD measures a key's claims)
  is enough, so a body may step between its keys; keys that share no claimed support ask for none. On the committed
  plans it refuses B@6.45 (soles 0.338 and 0.220 m) and B@6.7 (0.463 and 0.498 m) and nothing else. Level:
  interpretation (F-053, S-101 entry).
- D2 — B at 6.45 and 6.7 holds both soles where the declared interpolation puts them (goals at the floor), the arms,
  spine, root and legs free. 6.45 clears A with only the soles' 3 mm left. At 6.7 every bound on the root left an
  overlap with A's flying legs (recorded negatives, each `--free` arms, spine and legs with both soles held, `--clear
  ninja_lean`): root x within 0.05 m of its line, miss 0.002943; within 0.126 m, 0.001235; root height free (a
  duck), 0.002562 and 0.001183; the other side, 0.004658; the root not free, 0.004771. Height-only foot goals clear it
  but slide the root 0.43 to 0.77 m off its line at 5.5 to 8.2 m/s and skate the soles 0.5 to 0.7 m. So the root
  moves 0.19 m, which leaves one frame (7.417) where B's right thigh meets A's head by 0.01 m. Level: covered
  (ADR-O109, R-18, O72).
- D3 — That frame is cleared by an in-between at 7.375 with both soles held, not by re-blocking B's 7.5 key: a
  re-block of b19 and the 6.7 in-between would each be solved against the other, so neither recorded command could
  re-derive. ADR-O109 asks for a re-pose of the repo's keys first; b19's was not tried, recorded here (review 8 lists
  the precondition as unshown). Level: a departure from ADR-O109's order, recorded for the owner.
- D4 — B's crash keeps its pose. A no-allowance floor term clears it (B's lowest point 0.009 m over the floor) but
  flings B's legs 1.2 to 1.5 m up at 8.75 with the trunk at 98.9 degrees; bounded (Sp.x from -15, the root within
  0.1 to 0.2 m), it twists the right thigh 75 degrees and stays 0.006 m under. The prompt's 8.75 line already has B's
  soles on the floor (0.019 and -0.018 m); the 0.14 m sink is between keys in the repo's own interpolation. The floor
  change is split to RV-59m before this slice closed (blocked on F-215 and the owner's renders) and the records that
  said "over the floor" are corrected (CHANGELOG, DEV-35, S-098). Level: covered (ADR-O110).
- D5 — Every in-between's words from its measured pose: B@6.45 hands_up_guard (upright, both hands high), @6.7
  arms_overhead (22 degrees back, arms overhead), @7.375 steps_past_a, @8.45 crouched_shift (hunched forward, the root
  0.3 m aside; "shoulders turning" turned the girdle 1.2 degrees less than its line); 4.75 and 8.75 keep theirs, which
  match; the acrobat@3.55 leg_rising_high (the knee at 5 degrees, not chambered), @3.7 kick_extended. Level: covered
  (ADR-O109: printed in the prompt; the instructions now say so).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Predictions written first | PASS | at 13:53, before the edit |
| The class, not the probe | PASS | INBETWEEN_SUPPORT reads every in-between of every example; the test plants one off its supports |
| Negative results recorded | PASS | D2's six probes with their free sets, bounds and misses; D4's two crash solves |
| Owner rulings respected | PASS | O72's 0.15 m; F-215's allowance left to the owner (RV-59m); A's rows untouched |
| Tests | PASS | one case added; the recorded commands for 6.45, 6.7, 7.375 and their misses pinned as printed (DEV-35, ADR-O102); B_INBETWEENS re-pinned |
| Examples | PASS | the fight's in-betweens and every prompt line naming one; the wizard's two names; all four plans re-bound |
| Records | PASS | F-230 in progress; F-053; DEV-35 (deviations 6); map 33 (kernel log); backlog 44; S-098 corrected; CHANGELOG; PLAN-007; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 13:53 (the plan's predictions) to 14:13 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- compiler/passes/derived/p13_motion.py: INBETWEEN_SUPPORT; solver/contact_world.py: `inbetween_claims`
- planner/prompts/euler_solving.txt: the supports and the words from the pose
- examples: the fight's in-betweens (6.45, 6.7 re-solved; 7.375 added; names), the wizard's two names; the four
  motion plans re-bound; the prompts and envelopes regenerated
- tests/test_inbetweens.py (a support case; the recorded commands and their misses); tests/test_reference_fight_golden.py
  (B_INBETWEENS)
- kernel/knowledge_map.yaml 33; examples/reference_fight/deviations.yaml 6; docs: F-230, F-053, S-098, backlog 44,
  CHANGELOG, PLAN-007, run report

## Verification
- before: S-100's chained gate at cf8aae5: 750 passed
- Prediction 1 held. Prediction 2 held (B@6.45 and B@6.7 only). Prediction 3 failed in part: 6.45 cleared with the
  soles' 3 mm left, 6.7 did not clear alone (D2, D3); B leans 22.3 degrees at 6.7, under 35. Prediction 4 held as a
  measurement (0.009 m over the floor), but the slice keeps the crash (D4). Prediction 5 held (751; the floor term is
  unchanged). Predictions 4.5 of 5.
- the gate on this record (14:16:28): `scripts/verify.sh` exit 0, 751 passed in 161.10 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
