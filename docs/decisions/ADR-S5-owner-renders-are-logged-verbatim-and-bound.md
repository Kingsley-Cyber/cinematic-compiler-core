# ADR-S5 — Owner renders are logged verbatim and bound to the prompt hash

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
docs

## Decision
Each owner render is logged bound to the exact prompt bytes (sha256), with the owner's verdict word for word and Claude's frame notes kept separate.

## Context
Steering prompt of 2026-10-11. Recorded as an ADR on 2026-10-11 when the docs plane gave standing instructions their own files (owner O64).

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
