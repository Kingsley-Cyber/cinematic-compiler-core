# PLAN-011 — The test diet: the suite brought within ADR-O119's budget

<!-- docs-version: 1.0 -->

## Status
not started

## Owner
owner

## Created
2026-10-13

## Updated
2026-10-13

## Intent
Shrink tests/budget_baseline.json to nothing: every test file within 20 tests and 200 lines, every test within 100 ms,
every check code named by a test (one valid and one invalid case per check, ADR-O119, R-37, R-38). On 2026-10-13 the
baseline held 13 files, 191 slow tests (243 of the suite's 249 seconds) and 19 untested codes.

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| Slow tests rebuild envelopes per test | tests | medium | open | session fixtures: each example compiled once per run |
| Files over 20 tests or 200 lines | tests | low | open | split by check; table-driven planted cases |
| 19 check codes named by no test | all | medium | open | one valid and one invalid case each |

## Dependencies
- ADR-O119 (the budget and its gate).

## Owner Rulings Needed
- None: deleting a test that tests framework behavior, duplicates another, tests an impossible condition or a
  pass-through, or can never fail is ruled (ADR-O119); each deletion is named in its commit.

## Critical Path
1. Session-scoped fixtures for the four examples' compiled envelopes (the largest share of the slow tests).
2. The 19 untested codes, a valid and an invalid case each.
3. Split the over-budget files by check; delete the duplicates found on the way.

## Verification
- `python scripts/test_budget.py` with the baseline shrinking each slice.

## Changelog
- 2026-10-13 — Created with ADR-O119.
