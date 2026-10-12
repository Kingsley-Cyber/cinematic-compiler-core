# S-100 — RV-113: every prose prompt's legend hangs the legs from the spine (ADR-O84)

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-113 (PLAN-007); finding F-231; rulings ADR-O84, R-35; ADR-O110

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-100]

## Plan
The [SPATIAL ANCHORS] frame line tells the renderer the legs hang from the root; forward kinematics hangs them from
the spine with the hip joints on the pelvis (ADR-O84, R-35), so every leaning key's leg numbers are printed for a
different body from the one S13 checked (F-231). The class: any prompt text stating the kernel's parenting.
1. The legend says root -> Sp -> arms, legs, NK -> HD, the hips on the pelvis, as forward kinematics composes them.
2. C29's note in the knowledge map follows (map 32, kernel log).
3. The examples are regenerated.

Predictions, made before the change (13:44 by the clock):
1. The gate passes before the change: 750 tests (4112532, S-099's chained gate).
2. Only that frame line changes, in the 16 prose prompts and the four envelopes' render text; no other line moves.
3. No test changes and no checklist row moves; 750 tests pass after.
4. Each prose prompt grows by 20 characters.

## Decisions
- D1 — The legend states forward kinematics' own chain (solver/forward_kinematics.py: root -> Sp -> NK -> HD, the arms
  and the legs; the hip joints on the pelvis, the thighs turning with the trunk): "root -> Sp -> arms, legs, NK -> HD;
  the hips sit on the pelvis". Level: covered (ADR-O84, R-35).
- D2 — Only the parenting changes; the legend's other words and the prompts' leg numbers stay as they are (the numbers
  were already the spine's). Level: covered (ADR-O110: significant only).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Predictions written first | PASS | at 13:44, before the edit |
| Owner rulings respected | PASS | ADR-O84 applied as written |
| Tests | PASS | none changed |
| Examples | PASS | the 16 prose prompts and four envelopes, the frame line only (`git diff -U0`: 16 lines out, 16 in) |
| Records | PASS | F-231 resolved; map 32 (kernel log); backlog 43; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 13:44 (the plan's predictions) to 13:45 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- renderers/prose_renderer.py: the [SPATIAL ANCHORS] frame line's parenting
- kernel/knowledge_map.yaml 32 (C29's note); kernel log
- examples: the 16 prose prompts and four envelopes (one line each)
- docs: F-231; backlog 43; PLAN-007; CHANGELOG; run report

## Verification
- before: S-099's chained gate at 4112532: 750 passed
- Prediction 1 held. Prediction 2 held (one line in each of the 16 prompts and four envelopes). Prediction 3 held
  (no test, no checklist row). Prediction 4 held (50,648 to 50,668 characters in the fight's mixed prompt).
  Predictions 4 of 4.
- the gate on this record (13:46:29): `scripts/verify.sh` exit 0, 750 passed in 106.66 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
