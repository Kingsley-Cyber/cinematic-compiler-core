# PLAN-004 — Checkable constraints and equipment

<!-- docs-version: 1.0 -->

## Status
blocked

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-11

## Intent
Make the constraint layer bind the beats instead of only travelling with them. Today a rule such as "B never stands
after 9.0" reaches S04 as prose in the authoring packet; nothing checks a beat against it, and the `constraint`
validator each layer declares only fixes the build order. This plan gives checkable rules a machine form at L1.5, runs
the declared validators after every layer that declares them, and records who carries which prop at L0.5.

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| F-019 (GAP-04) | L1.5 | high | open | checkable constraint form + CONSTRAINT_BEAT at S04/S06 |
| F-020 (GAP-05) | all | high | open | the declared `constraint` validator runs after S04, S06, S07, S11, S13 |
| F-018 (GAP-03) | L0.5 | medium | resolved | `carried_by` on prop nodes from the archetype card's equipment (O63) |

## Dependencies
- Backlog M9-02 (F5.3 strike timing) first (O61).

## Owner Rulings Needed
- Approval of the checkable constraint schema (O61): a constraint item gains an optional
  `check: {subject, property, value, from, to}`; rules that cannot be checked stay prose.

## Critical Path
1. M9-03b `carried_by` on prop nodes (no ruling needed; O63).
2. Owner approves the checkable constraint schema.
3. M9-03a CONSTRAINT_BEAT and the per-layer constraint run.

## Verification
- `scripts/verify.sh` and `make golden`; every golden rule written in checkable form passes, and a failure there goes
  to the owner (O59).

## Changelog
- 2026-10-11 — created from GAP-03/04/05 (O62, O63).
