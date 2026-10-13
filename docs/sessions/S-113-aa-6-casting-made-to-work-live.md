# S-113 — AA-6: casting made to work live (the kunoichi on a rooftop)

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-6 (PLAN-008)

## Layer
L0.5

## Status
applied

## Commit
the commit whose message names [S-113]

## Plan
Two live runs of "a kunoichi in a dark blue outfit sprints across a moonlit rooftop ..." stopped at casting (three
refusals each). Correct what they show.

Predictions, made before the change (01:05 by the clock):
1. With the exact query form, actionable refusals and the matching fixed, the idea casts a performer and a place.

## Decisions
- D1 — The cast brief states the one form S01 reads ('. A: <card name>, <looks>.' after a full stop; the place
  named once, in the closing 'On a <world card name>'), with an example; a refusal quotes what the parser read,
  including a place it read twice. Level: covered (S01's own patterns).
- D2 — A new world card takes the kernel's axes (the model wrote a sentence for `ground`: WORLD_AX_CONFLICT) and
  drops `required_terms`, which S02 compares against the raw query words, punctuation and all ('rooftop,' never
  equals 'rooftop'), so a card the model wrote right never matched. A card that passed its schema is kept across
  attempts. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Tests | PASS | tests/test_author.py (casting) |
| Records | PASS | this record |

## Duration
from 01:05 to 01:20

## Changes
- compiler/author.py: the cast brief, its refusals, world cards' axes and terms, cards kept across attempts

## Verification
- Prediction 1 held: one cast call (11 s) gave "6 seconds anime. A: ninja, slim kunoichi in a dark blue outfit,
  sprints at full speed, vaults a low chimney and lands crouched, drawing her kunai in one swift motion. On a moonlit
  rooftop, holding a kunai." with a new draft world card (moonlit_rooftop); S02 cast the ninja, the kunai and the
  roof floor, the low chimney and the night backdrop.
