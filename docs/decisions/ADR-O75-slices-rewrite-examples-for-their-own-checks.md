# ADR-O75 — Slices may rewrite the examples to pass their own new checks

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
Owner, in chat, 2026-10-11: "Policy: Yes — slices may rewrite examples to pass their own new checks, recorded as
deviations. No per-change ruling. Add this to AGENTS.md as rule R-33."

What ADR-O71 said for every other change stays: a change an accepted ADR or the slice text covers goes ahead; a
change neither covers nor a new check needs goes ahead only as a small leaf (fewer than three waiting), else the
slice parks; the layer order, the rules, a card leaving draft and a render verdict always park.

## Context
Autopilot run 1 stopped after two slices parked for one cause (S-017, S-018): each new check refused example data
authored before it. The owner answered the policy question in the run report.

## Consequences
- Rule R-33 (rules 3.0); docs/prompts/autopilot.md section 5 (2.0).
- A slice's own new check no longer parks the slice when the examples fail it: the slice rewrites them, recorded
  in the golden test and the session file, and reports each one.

## Alternatives Considered
- A ruling per change (ADR-O71's rule 2 and 3 for these changes): rejected by the owner.

## Supersedes
ADR-O71

## Superseded By
—

## Related
- PLAN-003
