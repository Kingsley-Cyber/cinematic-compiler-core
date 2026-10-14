# S-136 — A side-pointing arm's angles stay inside the schema bound

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (claude-opus-5-5)

## Gap
The owner's Fist of the North Star run (anime) stopped at S13 on all three attempts: TARGET_SCHEMA at
keys/2/bones/LA/0. S-134's word-to-angle search turned "left-mid" (an arm straight out to the side) into a pitch of
-222: there every pitch reads the same, ties went to the lowest pitch, and the refinement stepped past -180.

## Layer
L4c

## Status
applied

## Commit
[S-136]

## Plan
Written 20:34.
1. Prediction: with ties broken toward rest and the search kept inside -180..180, "left-mid" gives [0, 0, 90] and no
   direction word leaves the bound; every word still reads back.

## Decisions
- D1 — Ties go to the angles nearest rest (|pitch| + |roll|) — Why: the plainest pose that reads as the word —
  Alternatives: wrap the angle into range (a pitch of 138 sits outside the shoulder's limits) — Downstream: S13 keys
  in words — Level: interpretation.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` |
| The test fails without the fix | PASS | tests/test_intent.py: 1 failed before, 8 passed after |

## Duration
from 20:34 to 20:40

## Changes
- solver/intent.py (`_search`); tests/test_intent.py (one test)

## Verification
- Prediction 1 held: left-mid [0, 0, 90], right-mid [0, 0, -90]; no word out of range.

## Next
Re-run the owner's idea.
