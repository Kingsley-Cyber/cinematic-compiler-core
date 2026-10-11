# ADR-O45 — M9 render budget: eight fight renders

<!-- docs-version: 1.0 -->

## Status
superseded

## Date
2026-10-11

## Decided By
owner

## Scope
M9

## Decision
Render budget for M9: at most eight fight renders, one after each of these slices: F5.3 strike timing, F6.3 grounded pickups, F2/F6.1 prop physics and visibility, FR.1/FR.3 rotation path, F5.1/F5.2 world contact, O19 D9 lines, C10 camera, part 3 words. Fixed model, seed and length; each judged against its scorecard (docs/render_tests/m9_render_plan.md). Other slices ride along unisolated in the next render; no baseline render, no axis re-runs

## Context
Recorded in docs/plans/MASTER_PLAN.md, table "Knowledge DAG and structured prose (owner, 2026-10-11)", on 2026-10-11.

## Consequences
- Lands in: M9.
- Superseded by O46: six 5 s probes and one full-fight render replace the eight fight renders.

## Alternatives Considered
- Not recorded at the time (migrated from the MASTER_PLAN table on 2026-10-11, owner O64).

## Supersedes
—

## Superseded By
ADR-O46

## Related
- ADR-O19
