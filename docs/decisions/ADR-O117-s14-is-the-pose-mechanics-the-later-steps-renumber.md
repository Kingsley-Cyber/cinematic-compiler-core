# ADR-O117 — S14 is the pose mechanics; the steps after motion renumber

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-13

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-13, on PLAN-009's naming: "A — renumber. The new step is S14." The pose mechanics step
(`pose_mechanics`, band L4e, computed from the motion keys) runs after S13 motion; the later steps move up one.

| Step | Before | After |
|---|---|---|
| pose mechanics | — | S14 |
| facial | S14 | S15 |
| effort | S15 | S16 |
| camera | S16 | S17 |
| render | S17 | S18 |
| post-generation | S18 | S19 |

## Context
Step IDs read `S` and two digits (schemas/layer_order.schema.json); the F2 renumber of 2026-10-11 (facial into S14)
is the precedent.

## Consequences
- The code, tests, schemas, prompts, kernel files (layer order 1.9, knowledge map, the owner invariants' "S18 output
  is uncompressed") and the open backlog items read the new numbers; the pass files are p15_facial, p16_effort,
  p17_camera, p18_render.
- Records written before this (sessions, findings, decisions, done backlog items, the master plan, the hash logs) keep
  the numbers they were written with: read them through this table.
- The envelope moves to MGRAPH-1.3 (its groups and tags change).

## Alternatives Considered
- B, a step S13.5 with nothing else moving: one exception to the step-ID pattern.

## Supersedes
—

## Superseded By
—

## Related
- docs/plans/009-pose-mechanics.md
