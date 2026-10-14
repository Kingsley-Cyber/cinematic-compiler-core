# ADR-O119 — Tests come from the checks and keep a budget; the gate runs on six cores; an approved plan runs to its end

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-13

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-13: "Stop writing tests. Generate them. ... For each check: write one test that verifies the
valid case, one test that verifies the invalid case. The test must test one behavior, test the goal not the
implementation, fail if the check is wrong, run in under 100ms. Delete every test that tests framework behavior,
duplicates another test, tests an impossible condition, tests a pass-through function, can never fail. ... Add a test
budget: under 20 tests per file, under 200 lines per file, under 100ms per test, one behavior per test. Enforce it in
the gate." And: the gate runs on six of the Mac's ten cores (pytest-xdist); "once I OK a plan, run all of it without
asking. Report at the end. Only stop if the gate fails, a new decision is needed, or you find a bug that changes the
plan."

## Context
On 2026-10-13 the suite had 833 tests in 56 files: 10 files over 20 tests, 8 over 200 lines, 187 tests over 100 ms
(243 of its 249 seconds), and 19 of the 210 check codes the compiler raises named by no test.

## Consequences
- scripts/test_budget.py runs in the gate: every file within 20 tests and 200 lines, every test within 100 ms, every
  check code named by a test; tests/budget_baseline.json holds the files, tests and codes over budget on 2026-10-13,
  which may only shrink (a baseline entry back within budget must be removed, so the list cannot go stale).
- New and rewritten tests meet the budget; the baseline's tests are rewritten or deleted slice by slice (PLAN-011).
- The gate's pytest runs with `-n 6` (pyproject.toml addopts).

## Alternatives Considered
- The budget enforced on every test at once: the gate would fail until about 200 tests are rewritten.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O102
