# S-106 — ADR-O112: the automatic author planned (PLAN-008)

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Owner instruction in chat (ADR-O112); PLAN-008

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-106]

## Plan
Record the owner's instruction (the compiler writes its own authored steps) and plan it against the code: the nine
authored nodes, the packets they already seal, GateFailed's findings, and the backlog slices AA-1 to AA-5.

Predictions, made before the change (15:24 by the clock):
1. The docs plane accepts PLAN-008 and the new slices; no code or example changes; the gate passes at 753.

## Decisions
- D1 — The owner's design note is read as intent, not spec (the owner's words). Where it differs from the code the
  plan follows the code: S05-S07 are derived, not authored; S13's poses are authored and repaired by the solver, not
  solved from nothing; S17's projection is automatic and only its render plan is authored. Level: the owner's
  instruction (ADR-O112).
- D2 — The first slice runs no model: a replay backend proves the loop on the four examples, so nothing is spent
  before the owner picks the live backend. Level: covered (finish.md: no paid call without the owner).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Owner rulings respected | PASS | ADR-O112 quotes the owner; the live backend waits for the owner's choice |
| Records | PASS | ADR-O112; PLAN-008; backlog (AA-1 next) |

## Duration
from 15:24 to 15:30

## Changes
- docs/decisions/ADR-O112; docs/plans/008-automatic-author.md; docs/plans/backlog.yaml

## Verification
- Prediction 1: see the chained gate.
