# S-110 — AA-7: the resume cache; AA-8: Sonnet first, HIT_HOLD to the camera, the owner's fight as guide

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-7, AA-8 (PLAN-008); the owner's speed plan (2026-10-13)

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-110]

## Plan
1. AA-7: each accepted document kept under its packet's hash; a step whose packet is in the cache is not written.
2. AA-8: Sonnet writes S13, S15 and S16 first, Opus on a retry (S04 stays Opus); a refusal whose codes all belong
   to an earlier step (HIT_HOLD: the camera) goes there; anime ideas take the reference fight as the guide.

Predictions, made before the change (00:20 by the clock):
1. A re-run of the same idea writes no step (a test).
2. The live idea runs faster than S-109's 26.6 minutes.

## Decisions
- D1 — The cache keeps a document only once the pipeline has moved past it (the steps before a refusal, or all at
  the end): a cached document has passed its checks. Level: covered.
- D2 — Not taken from the owner's plan: S11/S12 and S15/S16 in parallel and S13 begun before S12 ends, since each
  reads the step before it (docs/layer_order.md). Level: covered (the layer order).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Tests | PASS | tests/test_author.py: a re-run from the cache writes nothing |
| Records | PASS | backlog (AA-7 done); PLAN-008; CHANGELOG |

## Duration
from 00:20 to 00:30

## Changes
- compiler/author.py (cache, routing, models, guide); cli/main.py (--cache, --no-cache); tests/test_author.py

## Verification
- Prediction 1 held. Prediction 2: the timed run is reported in S-111 with AA-8's measures.
