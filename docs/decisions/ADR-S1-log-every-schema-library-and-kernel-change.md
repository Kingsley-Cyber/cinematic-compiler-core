# ADR-S1 — Log every schema, library and kernel change

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-10

## Decided By
owner

## Scope
Schema control

## Decision
Every `schemas/**/*.schema.json`, library card and kernel file change is recorded in its append-only, hash-chained log (`python -m kernel.schema_log`); drafts stay `status: draft` until the owner approves.

## Context
Owner rule of 2026-10-10, carried in AGENTS.md 'Schema control'. Recorded as an ADR on 2026-10-11 when the docs plane gave standing instructions their own files (owner O64).

## Consequences
- Cited by docs/rules.yaml.

## Alternatives Considered
- None recorded.

## Supersedes
—

## Superseded By
—

## Related
- docs/rules.md
