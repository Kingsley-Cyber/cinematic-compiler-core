# ADR-S3 — Every prompt adheres to the knowledge DAG as a checklist

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L6

## Decision
Every prompt the compiler emits must provably adhere to the owner's knowledge DAG (docs/sources/knowledge_dag_v1.md, mapped in kernel/knowledge_map.yaml) row by row; a prompt that fails or leaves unchecked any applicable row is not a deliverable; a green test is not adherence.

## Context
Steering prompt of 2026-10-11 (the session mission). Recorded as an ADR on 2026-10-11 when the docs plane gave standing instructions their own files (owner O64).

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
