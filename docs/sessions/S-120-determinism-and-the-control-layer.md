# S-120 — Determinism and the control layer: the prompt is the same from disk, from memory, in any key order

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
ADR-O116 (owner): the joint-order bug S-119 found, made impossible to return; six structural checks in one place

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-120]

## Plan
1. Measure every prompt of the examples and R20 with every key order reversed.
2. Declare the canonical joint order (motion_graph 1.4); one renderer constant held equal to the kernel's.
3. validators/determinism.py: JOINTS_IN_CANONICAL_ORDER and DETERMINISM; tests/test_control_validation.py gathers the
   six checks, the bug planted back to prove the check fires.

Predictions, made before the change (07:40 by the clock):
1. With S-119's fix, every prompt is the same in both key orders.
2. Before it, R20's LBN prompt from disk differs from its in-memory one.

## Decisions
- D1 — The serializer keeps sorting alphabetically (ADR-O116: every hash is taken over that form); readers are made
  order-free and DETERMINISM proves it for every object, not only joints. Level: covered; the owner asked for a
  canonical-order serializer, reported.
- D2 — S13 already writes the kernel order (`packet["joints"]`); no writer changes. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft grep of `bones` readers and writers before the edits |
| Tests | PASS | 802 passed; tests/test_control_validation.py new (13) |

## Duration
from 07:40 to 08:20

## Changes
- validators/determinism.py; tests/test_control_validation.py; renderers/anime_renderer.py, renderers/prose_renderer.py;
  schemas/graphs/motion_graph.schema.json (logged); ADR-O116

## Verification
- Prediction 1 held: the four examples and R20, all five prompts each, the same hash both ways (R20 LBN b1dd621f).
- Prediction 2 held: the code before S-119 renders R20's LBN from disk as 2a666b26, in memory b1dd621f.
