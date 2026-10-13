# S-119 — The graphs turn as one wheel: data-flow contract, cross-graph consistency, end-to-end tracer (ADR-O115)

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
ADR-O115 (owner): no check proved the graphs turn together

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-119]

## Plan
1. A tracer re-runs each layer on the envelope before it, logging every key it reads (held or looked for); writes come
   from the layer order's paths; phantom, optional, dead and dormant follow.
2. Run it on R20 first; fix the phantom inputs.
3. The contract (kernel/data_flow.yaml) is the four examples' measured flow; the gate fails a layer that flows
   otherwise, reads a phantom, or does not reproduce its own output.
4. Cross-graph consistency names every broken reference between graphs.

Predictions, made before the change (05:20 by the clock):
1. At least one layer reads a field no layer writes.
2. Every layer reproduces its own output from the stored envelope.

## Decisions
- D1 — Reads are measured, not hand-declared, then held by the gate: a declared list would drift from the code.
  Level: covered.
- D2 — R20's authored documents were not kept; its authored layers are traced to their packets, S17's document is
  rebuilt from the render node. Level: covered.
- D3 — A surface is named by its id and kind in CAUSE_REASON (it has no name or hint). The check accepts a surface's
  kind word as naming it; no example's verdict changes. Level: covered.
- D4 — `before_own_effects` is unexercised, not phantom: declared, written only when a beat's own effects change an
  object. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft grep and skeleton of the passes, the pipeline and the renderers before the reads |
| Tests | PASS | 789 passed; tests/test_data_flow.py new (14) |

## Duration
from 05:20 to 07:10

## Changes
- validators/data_flow.py, validators/cross_graph.py, kernel/data_flow.yaml (logged), kernel/schema_log.py;
  validators/cause_reason.py; renderers/anime_renderer.py; tests/test_data_flow.py; ADR-O115; the report

## Verification
- Prediction 1 held: S05 read surfaces' `name` and `hint` (all five envelopes); fixed.
- Prediction 2 failed: S17's LBN prompt took joint order from the dict; fixed, the examples unchanged.
