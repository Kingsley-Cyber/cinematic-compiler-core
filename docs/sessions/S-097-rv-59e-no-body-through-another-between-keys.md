# S-097 — RV-59e: no body through another at any frame between keys

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-59e (PLAN-007); findings F-159, F-220; rulings R-18 (no body through another), O72, O18, ADR-O109 (in-between
keys on the repo's side); the DAG's density rules (docs/sources/knowledge_dag_v1.md:253-261)

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-097]

## Plan
BODY_OVERLAP judges the keys only; between them the fight's bodies overlap in 24 frames over six spans and the wizard
example's in 5 over two (docs/reports/2026-10-12-between-keys.md). With in-between keys at S13 and in the prompts
(S-094, S-095), the repo can clear its own side. The class: a key-only check of a motion drawn between keys.
1. S13 refuses BODY_OVERLAP at every frame between keys (the scene's fps, every body posed by the declared
   interpolation through its keys and in-betweens, a vanished body left out), naming the span's bodies.
2. The repo's side cleared from recorded commands, run in order from the plan at 5f01e0e, each bounded by the joint
   limits (O11), its goals the clearance (and the floor where B falls), no contact moved: B's 7.5 root first (the
   descent from the pillar involves no contact); then in-between keys of B's by each contact (the knee at 4.7, A's
   cartwheel elbow and the catch at 6.3-6.6 and after it, the drive at 8.5, the crash), and of the acrobat's around
   its kick at 3.6. A's rows (the owner's) take none; a span only they could clear stays F-220's.
3. The in-betweens and the moved root typed as deviations (DEV-35, DEV-36); a test re-derives every command.

Predictions, made before the change (12:35 by the clock):
1. The gate passes before the change: 746 tests (5f01e0e, S-096's chained gate).
2. The new check, run on the examples before any re-block, refuses exactly the report's frames: 24 in the fight and
   5 in the wizard example, none in the other two.
3. B's 7.5 root moved about 0.3 m clears the descent (7.21-7.42) with no new overlap from 7.5 to 8.0.
4. With at most six in-betweens of B's and two of the acrobat's, every remaining overlap clears, so the check lands
   with the examples green; none is placed on A.
5. About 752 tests.

## Decisions
- D1 — S13's BODY_OVERLAP between keys: every frame of the scene's fps strictly inside the keys' range, each body posed
  by the declared interpolation through its keys and in-betweens, a vanished body left out; a frame where every body
  stands at a key or an in-between is judged there; one refusal per pair of spans at its deepest frame, naming both
  spans. Level: covered (R-18).
- D2 — The commands' order and free sets: the in-betweens by the catch first (6.45, 6.7), then the knee (4.75), the
  drive (8.45) and the crash (8.75, with the floor term); each frees the limbs in the way, the spine and the root (the
  legs too at the crash; for the acrobat, the kicking leg, the hips, the spine and the root), inside the joint limits
  (O11), its only goals the clearance (and the floor), no contact moved. B's 7.5 root, solved first, moved 1.1 m in z
  chasing the frames after the catch it cannot reach; solved after the 6.7 in-between it moved 1.25 mm, so it was
  dropped and the anchor kept. Level: covered (ADR-O109; review 7's practice: the rulings' bounds).
- D3 — The prose prints the in-betweens inside [MOTION CONTROL]: S-095's own section failed the Master Template (C19,
  V8, GR) in every prose mode once an example carried in-betweens; inside the motion control the checklist is as it
  was. S-095's test follows (the lines' place). Level: covered (the DAG's Master Template).
- D4 — Each in-between's name and description say what its solved pose does (B's guard lifts and opens; the arms
  follow through the throw; the kicking leg recoils), written after the solve from the pose. Level: covered (the
  author's fields).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the staged scan, the gate and the commit |
| One gap, right layer | PASS | S13's check and the repo's motion data (L4c), the prose's place for the in-betweens (L6) |
| Predictions written first | PASS | the session file was written at 12:35, before any code |
| The check fires and stays silent | PASS | measured: before the in-betweens it refused exactly the report's spans (six in the fight, two in the wizard example); after them nothing in the four examples; a test plants the acrobat's kick without its in-betweens |
| A re-block re-derives | PASS | a test runs the seven commands in order from the plans without in-betweens and gets every committed pose; misses 0 each |
| No owner row moved | PASS | every in-between is B's or the acrobat's; A's keys and anchors unchanged |
| Neighbours | PASS | the knowledge map (a BODY_OVERLAP locator; Conservation laws; 30); body_overlap.py's and the report's docstrings; the between-keys report regenerated (no span left); the checklist as it was |
| The step's instructions teach it | PASS | euler_solving.txt: no overlap at any frame between keys |
| Tests changed with their data | PASS | three new tests; the report's pins to none; test_render's row count counts the in-betweens; S-095's test follows the lines' place; the floor-term test now checks the crash both ways (it sinks without the 8.75 in-between, not with it; the gate caught the stale claim); nothing loosened |
| Examples | PASS | the fight's (DEV-35) and the wizard's motion plans gain in-betweens; their prompts print them; every motion plan re-bound |
| Records | PASS | F-159, F-220 resolved; F-089 noted; S-095 corrected; backlog (RV-59e done, RV-59c next); deviations.yaml 5; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first, on the added lines |

## Duration
from 12:35 (the plan) to 12:43 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- compiler/passes/derived/p13_motion.py (`_between_keys`); planner/prompts/euler_solving.txt
- renderers/prose_renderer.py (the in-between lines inside [MOTION CONTROL])
- examples: the fight's five and the wizard's two in-between keys; every motion plan re-bound; prompts and
  checklists regenerated; deviations.yaml 5 (DEV-35); docs/reports/2026-10-12-between-keys.md
- tests: test_inbetweens.py (three new; S-095's moved), test_interpolation.py, test_render.py, test_reblock.py (the
  crash both ways), test_reference_fight_golden.py (B_INBETWEENS)
- solver/body_overlap.py, validators/between_keys_report.py (docstrings); kernel/knowledge_map.yaml 30
- F-159, F-220 resolved; F-089; S-095's correction; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-096's chained gate at 5f01e0e: 746 passed
- Prediction 1 held. Prediction 2 held. Prediction 3 failed (B's 7.5 root did not move: the 6.7 in-between cleared
  the descent). Prediction 4 held (five of B's, two of the acrobat's, none of A's; the check lands). Prediction 5
  failed (749: three under). Predictions 3 of 5.
- the gate on this record (12:45:53): `scripts/verify.sh` exit 0, 749 passed in 101.97 s, docs plane: PASS, check:
  PASS (the first run, 12:43:46, failed on the floor-term test's stale claim about the crash)
- the hygiene scan over the staged diff's added lines: 0 hits (run first in the chained commit)
