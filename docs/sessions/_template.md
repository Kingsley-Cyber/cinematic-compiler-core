# S-NNN — <one line: what the session did>

<!-- docs-version: 3.0 -->

## Date
<YYYY-MM-DD>

## Agent
<agent and model>

## Gap
<backlog slice and finding IDs>

## Layer
<the layer that owns the fix (docs/layer_order.md)>

## Status
<in progress | applied | reverted | not started>

## Commit
<commit hashes, or the message tag [S-NNN]>

## Plan
<what was planned, with numbered predictions written here before any code changes, and the clock time they were
written>

## Decisions
<one line per choice the plan did not spell out (rule R-32): D<n> — <the choice> — Why: <the rule, ruling, DAG row
or AGENTS.md / CLAUDE.md section behind it, and the reason> — Alternatives: <what else, and why not> — Downstream:
<what it affects> — Level: <covered (a ruling, rule or the plan's own text makes this choice) | interpretation (none
does: also list it in F-053 for the owner) | proposed ADR-Onn>>

## Self-audit
<the self-audit (docs/prompts/self_audit.md) run before the commit: its verdict (READY TO PUSH or NOT READY), each
check with its evidence (a command and its deciding line, or file:line), the claims it found wrong and what was fixed;
required from S-055 (the docs plane refuses an applied session without it, R-03, R-31)>

## Duration
<by the clock, from the plan to the commit>

## Changes
- <file>

## Verification
- `scripts/verify.sh`: <pass | fail with output>
- `make golden`: <unchanged | changed on purpose: what>

## Next
<the next slice>
