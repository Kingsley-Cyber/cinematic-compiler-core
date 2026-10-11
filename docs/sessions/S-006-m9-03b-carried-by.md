# S-006 — M9-03b: each prop records who carries it (carried_by, O63)

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-03b; finding F-018 (GAP-03); ruling ADR-O63

## Layer
L0.5

## Status
applied

## Commit
the commit whose message names [S-006]

## Plan
S02 already reads each archetype card's `equipment` to add missing props, then forgets whose gear it is. Write it on
the prop node: `carried_by` is the one scene entity whose archetype card lists the prop's card in its equipment, or
null when none does or when several do (an interpretation: shared gear has no single carrier). Contract:
`schemas/graphs/brief_nodes.schema.json` 1.0 to 1.1, the field required (string or null), logged. Use: the SCENE line
"Props at the start" says "carried by <label>" for a prop that starts with no holder and no known location (gear on
the body), so the prompt says where it is (W4); a prop held, or resting somewhere known, keeps its phrase.

Predictions, made before the change:
1. Reference fight: kunai and shuriken volley carried by ninja_broad; rope dart, smoke pellet and substitution log by
   ninja_lean; every prop in the other three examples null (their archetype cards list no equipment).
2. The reference SCENE line gains "carried by A" for the rope dart and the smoke pellet and "carried by B" for the
   shuriken volley; the kunai stays "held by B R hand" and the log "on the ground"; the other examples' prompts stay
   byte-identical.
3. The brief_nodes version moves packets that embed props, so the re-bind writes plan hashes in more than one
   example; every render.txt stays byte-identical (LBN-2.4 does not print carried_by).

## Duration
about 30 minutes

## Changes
- `planner/query_expander.py`: `carried_by` per prop; `schemas/graphs/brief_nodes.schema.json` 1.1 (logged)
- `renderers/prose_renderer.py`: "carried by <label>" in the SCENE first states for gear on the body
- `tests/test_reference_grounding.py`: the mapping and the shared-gear rule
- examples rewritten (reference prose; reference and UGC envelopes); finding F-018 resolved

## Verification
- `scripts/verify.sh` before the change: pass (3c08307); after: pass (582 tests)
- Self-audit before the commit: READY TO COMMIT; one mechanical fix applied (the renderer's "gear on the body"
  reading labelled as an interpretation; output unchanged)
- Predictions: (1) held: ninja_broad carries the kunai and shuriken volley, ninja_lean the rope dart, smoke pellet and
  log; the UGC glasses are null (the wizard and live-action scenes have no props). (2) held: the reference SCENE line
  gained "carried by A" twice and "carried by B" once; the kunai and the log kept their phrases; the other examples'
  prompts are byte-identical. (3) half wrong: no packet moved (the authored steps' packets do not carry the props'
  new field), so the re-bind wrote nothing; every render.txt is byte-identical as predicted.

## Next
M9-04 (prop physics and positions).
