# PLAN-005 — The docs plane

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-11

## Intent
Make the repo carry its own memory: AGENTS.md is the operating manual, five indexes map every plan, finding,
decision, session and render (one file each), the canonical docs (layer order, rules, plan) are generated from the
code and data so they cannot drift, docs/for_the_owner.md explains everything in plain English, and one gate
(scripts/verify.sh) refuses drift on every commit, in CI and nightly (owner O64-O67).

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| D-01 | docs | high | done | five indexes, templates, one file per artifact (migration) |
| D-02 | docs | high | done | layer_order.md, rules, plan.md, for_the_owner.md, how_to_refactor.md, ownership, versioning, CHANGELOG, CODEOWNERS, AGENTS.md, verify.sh, Makefile, pre-commit hook, docs freeze log |
| D-03 | docs | medium | done | seven schemas (O65): layer_order, rules, beat, contact, rotation (shared, embedded by kernel/shared_schemas.py), genre_profile and motif (drafts; F-060) |
| D-04 | docs | medium | open | pinned pyproject and uv.lock, Dockerfile |
| D-05 | docs | medium | open | six GitHub workflows, the nightly regeneration PR |

## Dependencies
- None: it documents and gates what exists.

## Owner Rulings Needed
- None open (O64-O67).

## Critical Path
1. D-01 indexes and migration.
2. D-02 canonical and control docs, AGENTS.md and the gate.
3. D-03 schemas.
4. D-04 repeatability.
5. D-05 CI.

## Verification
- `scripts/verify.sh` (docs plane check included) before every commit.

## Changelog
- 2026-10-11 — created (O64-O67).
