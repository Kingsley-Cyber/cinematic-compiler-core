# S-002 — The docs plane: AGENTS.md, five indexes, canonical docs, verify.sh, schemas, control and CI

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
PLAN-005 (owner O64-O67): backlog D-01 to D-05

## Layer
docs

## Status
in progress

## Commit
the commits whose message names [S-002]

## Plan
Graft and graphify refreshed first (graft 907 nodes / 2,517 edges; graphify 6,819 / 9,882). Split the combined
artifacts into one file each, generate the indexes and canonical docs from their sources, make scripts/verify.sh the
single gate, then add the schemas, control and repeatability artifacts.

## Duration
in progress

## Changes
- `kernel/docs_plane.py`, `docs/index/`, `docs/{plans,findings,decisions,sessions,renders}/`, `docs/reports/`

## Verification
- `scripts/verify.sh`: run before each commit

## Next
Backlog M9-02 (F5.3 strike timing).
