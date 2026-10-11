# S-005 — The self-audit prompt (/self-audit)

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-06 (PLAN-005); ruling ADR-O68

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-005]

## Plan
The owner asked for a prompt to invoke at the end that makes the agent check its own work against the repo's
workflow. One source of truth, docs/prompts/self_audit.md (frozen, docs log), with a thin Claude Code command
`.claude/commands/self-audit.md` pointing at it; AGENTS.md step 9 and rule R-31 make it part of the protocol.
Prediction: the docs plane check and the gate pass with the new frozen files logged.

## Duration
about 20 minutes

## Changes
- `docs/prompts/self_audit.md`, `.claude/commands/self-audit.md`, `docs/decisions/ADR-O68-*.md`
- `AGENTS.md` (1.1: step 9, map row, checklist line), `docs/rules.yaml` (1.1: R-31), `kernel/schema_log.py` (frozen
  patterns), `docs/plans/backlog.yaml` (D-06), CHANGELOG

## Verification
- `scripts/verify.sh`: pass (see the commit); first use: the self-audit of M9-03 found four problems, all fixed before
  M9-03 was committed (session S-004)

## Next
M9-03b (carried_by on prop nodes).
