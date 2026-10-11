# ADR-B2 — One compile is one clip

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-10

## Decided By
owner

## Scope
M1.0.3, M5.5

## Decision
One compile = one clip. Envelope carries `scene.chained_from: null` and `provenance.chained_from_envelope_hash: null` now; chaining is built at M5.5

## Context
Recorded in docs/plans/MASTER_PLAN.md, table "Decided this round (owner, 2026-10-10)", on 2026-10-10.

## Consequences
- Lands in: M1.0.3, M5.5.

## Alternatives Considered
- Not recorded at the time (migrated from the MASTER_PLAN table on 2026-10-11, owner O64).

## Supersedes
—

## Superseded By
—

## Related
- —
