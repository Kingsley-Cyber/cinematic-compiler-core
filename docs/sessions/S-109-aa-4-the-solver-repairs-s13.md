# S-109 — AA-4: the solver repairs S13 before the model retries; AA-3: the first idea end to end

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-4, AA-3 (PLAN-008); ADR-O112

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-109]

## Plan
S-108's live run stopped at S13 after three model attempts, its last refusal a forearm 0.045 m into the other body.
1. `repair_motion`: for S13's contact, overlap and floor refusals, one finding at a time with S13 re-checking: a missed
   contact at a key re-blocks the key with the touching part on its target's surface (a body's at its radius off the
   surface); an overlap at a key re-blocks it with its root on its anchor, its soles and touching parts held; an
   overlap between keys places an in-between one frame off any key; other findings are left for the model, which
   then reads the repaired document.
2. One solver repair per attempt, logged as a call; refusals marked on every call of the attempt.
3. A generic line in the author's brief: only values the packet lists.

Predictions, made before the change (23:20 by the clock):
1. On the wizard example without its in-betweens the solver alone clears S13.
2. The live idea compiles to the end within three S13 attempts.

## Decisions
- D1 — A key's root stays on its S04 anchor in a repair (MOTION_POS); only an in-between's root moves. Level:
  covered (S13's own check).
- D2 — A body contact's target is the nearest point of the target's surface, offset by the touching part's radius,
  so a strike touches without entering (BODY_OVERLAP allows no depth). Level: covered (RV-49, R-18, O72).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Predictions written first | PASS | at 23:20 |
| Tests | PASS | tests/test_author.py: the repair clears the wizard's overlaps (in-betweens 3.54167 and 3.70833), a mixed refusal, the model-only case; the retry and exhaustion tests read the model's calls |
| Records | PASS | backlog (AA-3, AA-4 done; AA-6 next); PLAN-008; CHANGELOG |

## Duration
from 23:20 to 00:05

## Changes
- compiler/author.py: repair_motion, the repair in the loop, refusal marking, the brief; tests/test_author.py

## Verification
- Prediction 1 held (S13 refuses nothing; in-betweens at 3.54167 and 3.70833, beside the hand-made 3.55 and 3.7).
- Prediction 2 held: "6 seconds anime fight scene: ninja versus knight in a moonlit bamboo courtyard" compiled
  (S04 1 attempt; S11 2; S12 2; S13 2, the solver repairing between them; S15 1; S16 1; S17 2): 12 calls, 26.6 min,
  $4.06 at list price on the subscription. Prose prompts 18,755 to 22,950 characters; 3 checklist rows FAIL (M4 among
  them), 29 NOT CHECKED.
