# S-115 — ADR-O113: the graph map, and the graph-to-prompt reach measured

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Owner instruction (ADR-O113): if the graph has it, the prompt prints it; map first, migrate second, check third

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-115]

## Plan
1. Navigate with graft and graphify (built in a throwaway clone at f93262a: 145 files; graphify 8.5 s, no model).
2. Map every graph group against its schema section on the four examples and R20's envelope (validators/graph_map.py,
   docs/graph_map.md); migrate any drift.
3. Measure which graph fields the prose renderer reads (validators/graph_reach.py) and pin it as a floor.

Predictions, made before the change (02:05 by the clock):
1. The graphs have drifted from their schemas in several groups.
2. The prose reads under half of the graph fields.

## Decisions
- D1 — The map reads the schemas' own sections; the four section names that differ from the envelope's groups
  (camera_edges, motion_edges, applications, invariants) are written in the map. Level: covered.
- D2 — No migration: every group conforms, every section is closed, every group and section is mapped; the one
  declared field never filled (object_state.before_own_effects) is optional. Level: covered (measured).
- D3 — Reach is measured as the fields the prose renderer reads while it renders (a field never read cannot be
  printed); the render node is the output, not a graph. Level: interpretation (F-053 when kept).
- D4 — O47's frame clause is superseded by the owner's words; its turn-angle clause is a render result (R13, R18)
  and stands until the owner rules. Level: the owner's instruction, read narrowly where it meets a render result.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft and graphify used | PASS | graft grep GRAPH_SCHEMA, _graph.schema.json, /edges/, /nodes/: ~19k tokens saved |
| Tests | PASS | tests/test_graph_map.py (conformance, mapping, a planted drift, the reach floor, the map current) |

## Duration
from 02:05 to 02:40

## Changes
- validators/graph_map.py, validators/graph_reach.py, docs/graph_map.md, tests/test_graph_map.py; ADR-O113

## Verification
- Prediction 1 failed: no drift (33 groups conform; one optional field never filled). Prediction 2 held: the prose
  reads 89 of 220 fields (reference fight), 76 of 199, 68 of 204, 119 of 285; R20's envelope 77 of 209.
