# S-123 — The orphan split: every field a layer writes is read, printed, deleted or declared

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Owner, 2026-10-13: "Print the ones the renderer reads. Delete the ones no one ever will ... Frozen is temporary."
Approved split: print 21, delete 19, declare 12 as provenance.

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-123]

## Plan
1. Delete: the six one-value edge `relation` labels, the hand-role `gap`, the rules' enforcement, status, scope,
   origin and reference labels, the affordance's `satisfied` and `library`, the state's `pos_source`, the intent's
   parser diagnostics (missing, ambiguous, confidence).
2. Print: each face's emotion, family and onset (words and frames); the face changes with their cause; the UGC hand
   handoffs; each object change's from-state; the affordance's agent grip; each prop's materials.
3. Declare 12 provenance fields in kernel/data_flow.yaml; DATA_FLOW_ORPHAN fails the gate on any new orphan.

Predictions, made before the change (11:10 by the clock):
1. No phantom and no orphan left in the four examples.
2. A field no layer reads is still read outside the layers somewhere.

## Decisions
- D1 — `states.facing` is kept and declared, not deleted: chaining reads each performer's end-state facing for the
  next clip (planner/chaining.py), a reader no example exercises. Delete 18, not 19. Level: covered (reported).
- D2 — Valence, arousal, display rule and the AUs held off are declared, not printed as numbers: owner F4 keeps AU
  codes and valence numbers out of the prompt, and S14 already prints them as words (feeling, display, NOT). Level:
  the owner's ruling (F4).
- D3 — The intent's diagnostics leave the envelope, not the parser (the author's casting reads `ambiguous`); the
  envelope moves to MGRAPH-1.2 and the layer order to 1.8 (ADR-O106: a schema change bumps its version). Level:
  covered.
- D4 — Tests rewritten (ADR-O102): the deleted fields leave seven tests' assertions (affordance edge, state carry,
  intent equality, three rule-scope lookups now read the rule's source and the kernel's scope, the hidden-phrasing
  break's prop line); the dead-field test becomes the orphan gate's planted break. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft grep of every writer and reader before deleting |
| Tests | PASS | seven assertions rewritten; the orphan gate planted |

## Duration
from 11:10 to 12:40

## Changes
- compiler passes S01, S03, S05, S08, S09, S10, S13, S14; solver/prop_state_machine.py; renderers (prose, anime,
  ugc); validators/data_flow.py; nine graph schemas, the intent document and the envelope schema (logged; MGRAPH-1.2,
  layer order 1.8); kernel/data_flow.yaml (logged); examples, checklists, docs/graph_map.md; tests

## Verification
- Prediction 1 held: contract_problems() is empty on the four examples.
- Prediction 2 held: `states.facing` (chaining) and the intent's `ambiguous` (the author's casting, from the parser).
