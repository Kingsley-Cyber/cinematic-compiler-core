# ADR-O98 — The gate: six conditions, two of them new

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
Owner, in chat, 2026-10-11: "add this to the claude md." with:

```yaml
gate:
  - layer_order_matches_plan
  - rules_match_dag
  - golden_passes
  - no_shortcuts_survive
  - soul_check_passes        # NEW
  - fight_works              # NEW
```

## Context
After the principal review (S-035): the gate (scripts/verify.sh) passed while no prompt was a deliverable.

## Consequences
- CLAUDE.md carries the gate. scripts/verify.sh enforces part of it; backlog RV-39 adds soul_check_passes (the principal review's recorded verdict) and fight_works (an owner render verdict bound to the deliverable prompt's hash).

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- ADR-O99
- F-115
- R-19
- R-29
- PLAN-007
