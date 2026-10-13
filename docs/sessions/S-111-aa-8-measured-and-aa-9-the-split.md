# S-111 — AA-8 measured live; AA-9: the pose step in parallel pieces

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-8, AA-9 (PLAN-008); the owner's speed plan

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-111]

## Plan
1. Time AA-8 live on the same idea as S-109.
2. AA-9: `ClaudeCLI` writes S13 in pieces of at most three slots, one fighter and one time window each, in parallel;
   the pieces are merged; a retry writes again only the pieces that hold a refused slot.

Predictions, made before the change (00:30 by the clock):
1. AA-8's run is faster than 26.6 minutes.
2. The split merges every slot and a retry redoes only the refused piece (an offline test).

## Decisions
- D1 — A piece owns its fighter's time from its first slot to the next piece's; an in-between inside that time is
  its. Level: covered (ADR-O109: an in-between is one entity's).
- D2 — The pieces are written without each other's poses; the solver repair and S13's checks join them. Level:
  covered (the owner's plan; AA-4).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Tests | PASS | tests/test_author.py: the pieces and the per-piece retry |
| Records | PASS | backlog (AA-8 done, AA-9 next); PLAN-008 |

## Duration
from 00:30 to 00:45

## Changes
- compiler/author.py: `_split_motion`, `_call`, PIECE; tests/test_author.py

## Verification
- Prediction 1 held: 10.2 min, $2.08 at list price (S04 61 s; S11 32 s; S12 21 s, no retry; S13 189 s Sonnet,
  33 s solver, 100 s Opus; S15 24 s and 35 s; S16 105 s; S17 10 s); the prose prompts 38 PASS, 0 FAIL, 29 NOT
  CHECKED. Prediction 2 held (offline).
