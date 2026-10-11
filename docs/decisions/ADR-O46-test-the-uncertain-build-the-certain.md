# ADR-O46 — Test the uncertain, build the certain

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
M9

## Decision
Test the uncertain, build the certain: a change gets a render only if it is uncertain, visual and not verifiable without a render; everything else is built and moved past. M9 gets six 5 s probes now (docs/render_tests/2026-10-11-m9-probes: V1 deflect on time, V2 hidden log and substitution, V3 one backflip, V4 apex hold, V5 hit held with both bodies, V6 opening from above) and one full-fight render after the build; no fixed seed (supersedes O45's eight)

## Context
Recorded in docs/plans/MASTER_PLAN.md, table "Knowledge DAG and structured prose (owner, 2026-10-11)", on 2026-10-11.

## Consequences
- Lands in: M9.

## Alternatives Considered
- Not recorded at the time (migrated from the MASTER_PLAN table on 2026-10-11, owner O64).

## Supersedes
ADR-O45

## Superseded By
—

## Related
- ADR-O45
