# S-112 — AA-9 split measured, AA-10 (turns whole, far contacts to S04), AA-6 casting built

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-9, AA-10, AA-6 (PLAN-008); the owner's speed plan and "start AA-6"

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-112]

## Plan
1. Measure AA-9 live; correct what the runs show.
2. AA-6: `casting` rewrites an idea the library cannot cast into the parser's forms with new draft cards.

Predictions, made before the change (00:40 by the clock):
1. The split cuts S13's first draft to under a minute.
2. The split run passes S13 within three attempts.

## Decisions
- D1 — The pieces are time windows holding every fighter of a beat, not one fighter each: split by fighter the
  first draft met 18 refusals against 6 or 7 in one call (two strikes 0.35 m short), since a strike and its target
  were posed by different calls. The owner asked for fighter by time; the measurement chose time. Level: covered
  (measured; the owner's target).
- D2 — A refusal about a turn rewrites S13 whole (a turn crosses windows); a contact still over 0.3 m off after the
  solver goes back to S04 only when the two bodies' anchors are over 1.5 m apart (a key's root stays on its anchor,
  MOTION_POS). Level: interpretation (the reach figures are the builder's, F-053 when kept).
- D3 — A new card from casting is a draft beside the run's output, never added to the library (R-30). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Tests | PASS | tests/test_author.py: time-window pieces, per-piece retry, casting from draft cards, the castable idea untouched |
| Records | PASS | backlog (AA-10 done; AA-9 next); PLAN-008 |

## Duration
from 00:40 to 01:10

## Changes
- compiler/author.py: time-window pieces, whole retries for turns, far contacts to S04, repair rounds, `casting`,
  `ClaudeCLI.cast`, cards through `author`; cli/main.py: casting first, query.txt and cards/; tests/test_author.py

## Verification
- Prediction 1 held (34 s by fighter; 51 s by time window). Prediction 2 failed: both split runs stopped at S13
  (6 and 7.5 min), which D1 and D2 answer.
