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
applied

## Commit
a370f6f (D-01), 8312845 (D-02), 245f874 (D-03), bdeab49 (D-04) and the D-05 commit; every message names [S-002]

## Plan
Graft and graphify refreshed first (graft 907 nodes / 2,517 edges; graphify 6,819 / 9,882). Split the combined
artifacts into one file each, generate the indexes and canonical docs from their sources, make scripts/verify.sh the
single gate, then add the schemas, control and repeatability artifacts and CI. Predictions and results: the docs-plane
check passed on its first run, so a break test per check was added (all fire); the shared-schema embedding left
beat_plan and temporal_graph byte-identical as predicted and moved no packet; the Docker gate first failed on a stale
docs/reference/code.md after the pins (fixed, then PASS); all six workflow commands pass inside the image and the
nightly regeneration changed nothing.

## Duration
about 3 hours

## Changes
- `kernel/docs_plane.py`, `kernel/shared_schemas.py`, `kernel/schema_log.py` (docs log, digest)
- `AGENTS.md`, `CHANGELOG.md`, `docs/{for_the_owner,how_to_refactor,ownership,versioning,layer_order,rules,plan}.md`, `docs/rules.yaml`
- `docs/index/`, `docs/{plans,findings,decisions,sessions,renders}/`, `docs/reports/`, `docs/plans/backlog.yaml`
- `schemas/{layer_order,rules,beat,contact,rotation,genre_profile,motif}.schema.json`
- `scripts/verify.sh`, `scripts/check.sh`, `Makefile`, `.githooks/pre-commit`, `Dockerfile`, `.dockerignore`, `pyproject.toml`, `uv.lock`, `.github/`
- `tests/test_docs_plane.py`

## Verification
- `scripts/verify.sh`: pass (575 tests), locally and inside the Docker image
- `make golden`: unchanged (no example output changed in S-002)

## Next
Backlog M9-02: F5.3 strike, throw and release contacts at their pose (step temporal). Waiting on the owner: the
push, the checkable constraint schema (M9-03a) and the open questions in AGENTS.md section 7.
