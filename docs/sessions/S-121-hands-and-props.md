# S-121 — Hands and props: every hand empty or holding a named prop on every line; no rule for a prop the scene lacks

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
R20 next action 1 (owner: "work on hands and props"): the kunai; F-234

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-121]

## Plan
1. S06 writes each performer's hands at every state: a prop is in a hand when its holder at that state is the
   performer and the performer's last possess contact on it names the hand; otherwise the hand is empty.
2. S17 prints them on every staff line ("hands: L empty, R kunai").
3. S03 applies a kernel prop rule only when the scene holds every prop it names (F-234), and a card rule marked
   `requires_prop` only when the scene holds that prop; the ninja, broad ninja, lean ninja and UGC creator cards mark
   theirs.
4. The movement legend names only the combat verbs the prompt uses (R20 printed "THROW" with no throw).

Predictions, made before the change (08:30 by the clock):
1. R20's lines say both hands empty, and its prompt loses the thrown-weapon rule and "THROW".
2. Only the UGC example's temporal plan moves its packet (its rules change).

## Decisions
- D1 — Hands are a field of S06's performer states (state_graph 1.5), derived from the props' holders and the possess
  contacts; S17 only prints them. Level: covered (next actions 1).
- D2 — `requires_prop` on card invariants (archetype_card 1.2; `any` or an object card id). Level: covered.
- D3 — A rewritten test: tests/test_constraint_graph.py's completeness test takes the two scoping rules (ADR-O102
  deviation); a new test pins them. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft skeleton of S06 and grep of the possess and holder code before the edits |
| Tests | PASS | completeness test rewritten for the scoping; the pinning test new |

## Duration
from 08:30 to 09:40

## Changes
- compiler/passes/mandatory/p03_constraint.py, p06_state.py; renderers/prose_renderer.py; schemas (state_graph 1.5,
  archetype_card 1.2) and four cards (logged); kernel/data_flow.yaml (logged); the UGC temporal plan re-bound;
  examples, checklists, docs/graph_map.md; tests/test_constraint_graph.py; F-234 resolved

## Verification
- Prediction 1 held: R20 re-run through S06 and S17 prints "hands: L empty, R empty" on every line and "(STRIKE)"; S03
  no longer applies the thrown-weapon rule to it.
- Prediction 2 held: `compiler.rebind` re-bound ugc_glasses_demo temporal only.
