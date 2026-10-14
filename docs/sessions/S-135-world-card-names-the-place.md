# S-135 — The wasteland world card; S01 reads a world card's name as a place

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (claude-opus-5-5)

## Gap
The owner's Fist of the North Star run stopped at casting on all three attempts: the model set the scene "On a desolate
wasteland" and S01 read no place, because its place nouns were a fixed list in code that the world cards never fed.

## Layer
L0

## Status
applied

## Commit
[S-135]

## Plan
Written 20:12. The owner: "create a card only for the world and redo the flow again".
1. Prediction: with a `desolate_wasteland` world card and S01 reading the last word of each world card's name as a place
   noun, "on a desolate wasteland" reads as the setting and casting passes.
2. Prediction: no other parse changes; the gate passes unchanged.

## Decisions
- D1 — The built-in PLACE_NOUNS list stays, joined by the world cards' names — Why: the owner asked for the card only;
  removing the list is the larger casting redesign — Alternatives: delete the list (breaks queries naming places with
  no card) — Downstream: S01 reads library/worlds at first parse — Level: interpretation.
- D2 — Only the names' last words count, not match_terms — Why: match_terms hold words like "keep" that read as verbs
  — Alternatives: match_terms too (false places) — Downstream: none — Level: interpretation.
- D3 — The new tests go in their own file — Why: the test budget refuses growth in an existing file (ADR-O119) —
  Alternatives: raise the baseline (the budget only shrinks) — Downstream: none — Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh`: 852 passed; test budget PASS; docs plane PASS |
| Card logged | PASS | library/library_log.jsonl seq 111, created, 1:draft |
| Tests | PASS | tests/test_place_cards.py (2: a carded place reads, an uncarded one does not) |

## Duration
from 20:12 to 20:25

## Changes
- library/worlds/desolate_wasteland.yaml (new, draft, logged); planner/intent_parser.py (`place_nouns`);
  tests/test_place_cards.py (new); docs/reference regenerated

## Verification
- `scripts/verify.sh`: pass
- Prediction 1: checked by the re-run of the owner's idea (below the commit).
- Prediction 2 held: the planner tests pass unchanged.

## Next
The re-run of "a fist of the north star inspired 10sec fight scene"; the owner's full fix prompt.
