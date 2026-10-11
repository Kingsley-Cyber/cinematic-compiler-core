# ADR-O68 — Self-audit before a commit or push

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
A prompt the owner can invoke at the end of a slice or session makes the agent validate its own work against the
repo's workflow before a commit or push: docs/prompts/self_audit.md, invoked as `/self-audit` in Claude Code. It is
read-only, re-derives every claim with evidence, and ends with a verdict (ready to commit, ready to push, not ready).

## Context
Owner request of 2026-10-11 ("design a prompt for me to invoke at the end where you validate based on your
implementations workflow and repo, like checking your own work"), after slices M9-02 and M9-03 in which the agent's
predictions partly failed (an S16 refusal not predicted; AIRBORNE_PICKUP first placed at the wrong step).

## Consequences
- AGENTS.md section 8 step 9 runs the self-audit before asking the owner to commit or push; rule R-31.
- The prompt is a frozen doc (docs log); `.claude/commands/self-audit.md` only points at it.

## Alternatives Considered
- A checklist inside AGENTS.md only: rejected, the audit needs its own steps and report format.

## Supersedes
—

## Superseded By
—

## Related
- PLAN-005
- docs/prompts/self_audit.md
