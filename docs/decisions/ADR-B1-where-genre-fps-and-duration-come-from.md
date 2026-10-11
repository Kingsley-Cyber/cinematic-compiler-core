# ADR-B1 — Where genre, fps and duration come from

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-10

## Decided By
owner

## Scope
M1.0.3, M1.0.6, M1.0.7, S04

## Decision
**Genre** comes only from the query or `--genre`; missing → stop at S02 with "add --genre". **fps** = query/flag, else the genre schema's `default_fps`. **duration** = query/flag, else the beat plan's last beat end (S04 plans inside the genre's duration budget). Every scene value names its source; `default` marks a filled default

## Context
Recorded in docs/plans/MASTER_PLAN.md, table "Decided this round (owner, 2026-10-10)", on 2026-10-10.

## Consequences
- Lands in: M1.0.3, M1.0.6, M1.0.7, S04.

## Alternatives Considered
- Not recorded at the time (migrated from the MASTER_PLAN table on 2026-10-11, owner O64).

## Supersedes
—

## Superseded By
—

## Related
- —
