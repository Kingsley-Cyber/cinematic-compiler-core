# ADR-B3 — Full, uncompressed, model-agnostic LBN render

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-10

## Decided By
owner

## Scope
M1.0.8, S16

## Decision
S16 outputs the full LBN-2.x prompt, uncompressed, model-agnostic; owner invariant `no_render_compression` (coverage 100%). Compression and model-specific renderers only after a target model is chosen. No vector database: every lookup is by exact id

## Context
Recorded in docs/plans/MASTER_PLAN.md, table "Decided this round (owner, 2026-10-10)", on 2026-10-10.

## Consequences
- Lands in: M1.0.8, S16.

## Alternatives Considered
- Not recorded at the time (migrated from the MASTER_PLAN table on 2026-10-11, owner O64).

## Supersedes
—

## Superseded By
—

## Related
- —
