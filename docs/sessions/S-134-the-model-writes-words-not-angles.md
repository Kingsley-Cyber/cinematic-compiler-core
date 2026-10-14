# S-134 — The model writes each pose in words, the compiler the joint angles, the solver the contacts

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-010 Phase 2 (owner: "the LLM writes constraints, the solver writes angles")

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-134]

## Plan
1. solver/intent.py: the staff words to joint angles, the inverse of `pose_words`, inside the joint limits.
2. motion_plan 2.2: a key carries `words` (the model's) or `bones` (the owner's source, the solver's repair); S13
   resolves words to angles before its checks, which all run unchanged on the result.
3. The author: the model's S13 schema has words and no bones, its guide example is shown in words, its instructions
   (planner/prompts/euler_solving.txt) teach the words; the re-block solver puts the contacts on their targets.

Predictions, made before the change (19:53 by the clock):
1. Every example key reads back from its own words.
2. The examples written in words alone pass S13 with the solver, or leave little for the model.

## Decisions
- D1 — The solver kept is the repo's own (solver/reblock.py `solve_key`), PLAN-010's fallback, not mink: it already
  matches the skeleton's conventions, and words alone already land most contacts (below). mink stays an upgrade if
  the solver's speed or reach falls short. Level: covered (in the plan).
- D2 — The examples keep their angles: the reference fight's are the owner's source (ADR-O83, O118), the others are
  the solver's output; the words path is proven on them below and in tests/test_intent.py. Level: covered.
- D3 — A live run read files this session changed while it ran (its packet moved, then half-new code): runs go on a
  tree no session edits. Level: covered (a lesson, reported).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | solver/staff_geometry.py and solver/reblock.py through graft skeleton |
| Tests | PASS | tests/test_intent.py (7, under 100 ms each) |

## Duration
from 19:53 to 20:01

## Changes
- solver/intent.py (new); compiler/passes/derived/p13_motion.py; compiler/author.py; planner/prompts/euler_solving.txt;
  schemas/graphs/motion_plan.schema.json 2.2 (logged); every plan re-bound; examples, checklists; tests

## Verification
- Prediction 1 held: 73 of 73 keys.
- Prediction 2 held: in words alone, live action passes S13 as is; UGC has 3 contact misses the solver clears in 0.4 s;
  the wizard 4, of which the solver clears 3 and leaves one overlap to the model.
