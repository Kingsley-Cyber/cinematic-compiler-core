# S-007 — The bootstrap directory (docs/bootstrap/, /bootstrap)

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-07 (PLAN-005); ruling ADR-O69

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-007]

## Plan
Before a compaction, the owner asked for a bootstrap the agent references in every future session, pointed to by
AGENTS.md and CLAUDE.md. It holds no hand-kept state: state.md is generated (versions, last sessions, next slices,
slices left, open rulings, serious findings, next free IDs); the rest records what the repo does not (the folders and
push command, the owner's working agreements, the lessons already paid for). Prediction: the generated state names
M9-04 as next and 23 M9 slices left, and the gate passes with the new frozen files logged.

## Duration
about 30 minutes

## Changes
- `docs/bootstrap/{README,environment,working_agreements,lessons}.md`, generated `docs/bootstrap/state.md`
  (`kernel/docs_plane.py`), `.claude/commands/bootstrap.md`, ADR-O69
- `AGENTS.md` 1.2 (map row, step 1), `CLAUDE.md`, `docs/ownership.md` 1.1, `kernel/schema_log.py` (frozen README),
  backlog D-07, CHANGELOG

## Verification
- `scripts/verify.sh`: see the commit

## Next
M9-04 (prop physics and positions).
