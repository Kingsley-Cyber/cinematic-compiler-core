# ADR-O70 — Autopilot runs: slice after slice, every decision logged

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
A prompt the owner invokes has the agent work the backlog end to end without stopping between slices, updating the
statuses and the bootstrap, testing every slice, and logging every decision it makes with the reason, from AGENTS.md
and CLAUDE.md: docs/prompts/autopilot.md, invoked as `/autopilot` in Claude Code. A run goes on until no slice is
ready (owner's choice). Invoking it is the owner's "commit it" for each slice that clears the gate and the
self-audit, for that run only; it never grants a push, a render or a paid model API call.

## Context
Owner request of 2026-10-11: "give me a prompt that has you working e2e without stopping and ensures you update
statuses, and bootstraps and tests and also ensures any decision you make is logged properly and why based on agent
md / claude md". Asked when a run should stop, the owner chose "When no slice is ready".

## Consequences
- Rule R-32: every decision goes in the session file's Decisions section with the rule, ruling or DAG row behind it;
  the session template gains that section.
- The bootstrap README sends a resumed session back into a running run (its run report in `docs/reports/`).
- The working agreements record the commit grant; pushes stay per push, on the owner's word.

## Alternatives Considered
- Keep "commit it" per slice: rejected by the owner's request to work without stopping.

## Supersedes
—

## Superseded By
—

## Related
- PLAN-005
- ADR-O71
- docs/prompts/autopilot.md
