# ADR-S4 — Predict before each check; ask only on silence or contradiction

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
all

## Decision
Predict the outcome before each check and say whether it held; ask the owner only where the DAG or the decisions are silent or contradict, in one line; otherwise act.

## Context
Steering prompt of 2026-10-11; owner 2026-10-10 ('don't ask what the plan says'). Recorded as an ADR on 2026-10-11 when the docs plane gave standing instructions their own files (owner O64).

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
