# S-052 — RV-11: DAG-excluded rows are N/A; `cinematic compile` refuses a prompt that is not a deliverable (O94)

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-11 (PLAN-007); finding F-085; rulings O94, O3, O13, O14, R-19, O102

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-052]

## Plan
O94 (owner): "DAG-excluded rows count as N/A. cinematic compile refuses a non-deliverable prompt." Today the prompt
checks and the checklist run only in tests, on the four examples (F-085); the 13 DAG-excluded rows count as NOT
CHECKED, so no prompt can be a deliverable; `cinematic compile` writes any prompt it makes.
1. The checklist marks a DAG-excluded row N/A, unless a code checks it (P3.2-5 and P4.2-1, ROOT_EXACT_PRESENT): there
   the code still judges, since its FAIL is a breach of an owner ruling (O3), not an excluded idea.
2. The checklist judges the prompts of any envelope (not only the examples on disk); `cinematic compile` runs it on
   every prompt it emits and refuses (exit 5, nothing written) unless every prompt is a deliverable (R-19), printing
   each prompt's counts and the rows that keep it from being one.

Predictions, made before the change:
1. The gate passes before the change: 661 tests (a6cc43c).
2. Every prompt's N/A count rises by 11 (the excluded rows no code checks, from NOT CHECKED); P3.2-5 and P4.2-1 keep
   their verdicts; still 0 of 20 prompts are deliverables.
3. `cinematic compile` of the wizard example to its prompts exits 5, writes nothing to stdout and names the rows that
   fail; a compile that stops before S17 behaves as before (exit 0, 2, 3 or 4).
4. tests/test_cli.py's first test changes with O94 (ADR-O102): the full compile is refused; a compile to the camera
   step reproduces the pipeline's envelope. About 662 tests.

## Decisions
- D1 — A row the DAG excludes is N/A unless a code checks it: P3.2-5 and P4.2-1 keep ROOT_EXACT_PRESENT's verdict,
  since a FAIL there is a prompt breaking owner O3, not an excluded idea. Level: covered (O94; the reading is in
  validators/checklist.py and R-19).
- D2 — The checklist judges the five prompts of any envelope (`judge_prompts`); the examples pass their files on disk,
  `cinematic compile` the envelope's own projection, which no render finding names. Level: covered (O94).
- D3 — `cinematic compile` refuses with exit 5 and writes nothing when a prompt is not a deliverable, printing each such
  prompt's counts and its first rows that are neither PASS nor N/A; a compile that stops before S17 emits no prompt and
  is unchanged. Level: covered (O94: "refuses").
- D4 — tests/test_cli.py's first test changes with O94 (ADR-O102): the full compile is refused, a compile to the camera
  step reproduces the pipeline; test_checklist's N/A test allows O94's rows; one test added. Level: covered.
- D5 — R-19 takes O94 (rules 7.0) and names cli/main.py among its enforcers. Level: covered (owner O94).

## Duration
about 6 minutes by the commit times (02:29 to 02:36); it read "about 30 minutes" until RV-46
(S-056) corrected it (F-166)

## Changes
- validators/checklist.py (excluded rows N/A, `judge_prompts`, `refusals`), cli/main.py (exit 5)
- docs/rules.yaml 7.0 (R-19; docs log); every example's checklist.md regenerated
- tests/test_cli.py (the first test, ADR-O102), tests/test_checklist.py (the N/A test, one test added)
- F-085 resolved; backlog (RV-11 done, RV-12 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-051's gate at a6cc43c: `scripts/verify.sh` exit 0, 661 passed
- after: `scripts/verify.sh` exit 0, 662 passed, check: PASS; `make golden` passed
- Prediction 1 held. Prediction 2 held (N/A from 6 to 17 on every prompt, 5 to 16 in the UGC example; NOT CHECKED down
  by 11; 0 of 20 deliverables). Prediction 3 held (exit 5, empty stdout, the rows named). Prediction 4 held (662).

## Next
RV-12 (the 6.3 cartwheel is a full turn, O96).
