# ADR-S6 — Navigate with graft and graphify first

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-10

## Decided By
owner

## Scope
all

## Decision
Before reading files, refresh and query the graft and graphify graphs (caches in the ignored `.graphs/`); read only the line ranges a change needs.

## Context
Owner rule (2026-09-21, restated 2026-10-10 in AGENTS.md). Recorded as an ADR on 2026-10-11 when the docs plane gave standing instructions their own files (owner O64).

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
