# S-082 — RV-96: the re-block solver re-derives a re-block from its record

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-96 (PLAN-007); findings F-207, F-127; rulings O11 (the joint limits), O72

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-082]

## Plan
solver/reblock.py (S-080) moves the free joints one at a time in the order it is given, so its answer depends on that
order (28.6 degrees apart for S-080's 8.0 key), it loads no joint limits though its docstring says it does, and its
CLI starts from the already re-blocked key and takes no goal weight, so no record re-derives a re-block (F-207; review
6). The class: a tool that claims reproducibility its inputs do not carry.
1. The search takes, at each step, the best move among all free components (ties broken by the components' sorted
   names), so the caller's order cannot change the answer.
2. The genre's joint limits (library/joint_limits.yaml, widened for anime, O11) bound every free component; a stated
   bound narrows them.
3. The CLI takes the start key from a motion plan file or a git revision, the root's height, weighted goals
   (`part=x,y,z@w`, `part.y=h@w`) and the free set, and prints the command it ran with the result.
4. S-078's three values are recorded as hand choices (they were), and S-080's pickups wait for RV-95, which re-blocks
   them with this solver from a recorded command and a re-derivation test.

Predictions, made before the change (09:18 by the clock):
1. The gate passes before the change: 711 tests (5060261, S-081's chained gate).
2. The new search gives the same bones for every order of the free list, in a test that shuffles it.
3. No example, prose or checklist changes: the solver is not run on the examples in this slice.
4. From the pre-S-080 8.0 key at 0.40 m with S-080's goals, the new search lands more than 1 degree from the committed
   key in some joint (a different search, a different local answer); RV-95 replaces those keys.
5. About 714 tests (711 and three: order, limits, the CLI's start and weights).

## Decisions
- D1 — The search is a steepest descent: at each step size it takes the best of every free component's two moves, ties
  broken by the components' sorted names, so the caller's order cannot change the answer; the cost is unchanged (the
  squared degree changes plus 1e8 per square metre of weighted miss). Level: interpretation (F-053).
- D2 — The genre's joint limits (library/joint_limits.yaml, widened for anime, O11) bound every free component, and a
  stated bound narrows them; a sum limit (NK+HD) is not enforced, which the docstring says. Level: covered (O11).
- D3 — The command takes the start key from a plan file or a git revision, with the root's height when a re-block moves
  it, weighted goals (`@w`) and the free set, and prints itself with its result, which `solve` reproduces. S-078's
  three values stay as the hand choices they were (S-078's correction; typed in RV-100); S-080's pickups are
  re-blocked from a recorded command in RV-95. Level: covered (F-207's fix).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the re-block tool (S13's data is authored with it); no step, example or check changed |
| Predictions written first | PASS | the session file was written at 09:18, before any code |
| New behaviour, old behaviour | PASS | measured: from the pre-S-080 8.0 key, the free list in two orders gives identical bones, 16.1 degrees from the committed key; tests: three orders agree, the knee stops at its 165-degree limit (220 without it), the printed command reproduces `solve` |
| Neighbours | PASS | the solver's only users are its tests and the recorded re-blocks; the S-080 test of the pickups' shape is unchanged (RV-95 re-blocks them) |
| The step's instructions teach it | n/a | a tool, not an authored step |
| Tests changed with their data | PASS | `git diff -- tests`: three new tests in tests/test_reblock.py; nothing removed or loosened |
| Examples | PASS | none changed |
| Records | PASS | F-207 open in part (RV-95); F-127 and F-053 noted; backlog (RV-96 done, RV-95 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 09:18 (the plan) to 09:22 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- solver/reblock.py (the search, the limits, the command); tests/test_reblock.py (three tests)
- F-207; F-127; F-053; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-081's chained gate at 5060261: 711 passed
- Prediction 1 held. Prediction 2 held (measured in the probe and pinned by the test). Prediction 3 held (no example,
  prose or checklist changed). Prediction 4 held: 16.1 degrees from the committed 8.0 key in one joint. Prediction 5
  held (714). Predictions 5 of 5.
- the gate on this record (09:22:07): `scripts/verify.sh` exit 0, 714 passed in 79.03 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
