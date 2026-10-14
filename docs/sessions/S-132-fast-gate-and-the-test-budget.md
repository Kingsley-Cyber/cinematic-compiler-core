# S-132 — The gate on six cores; the test budget in the gate; an approved plan runs to its end (ADR-O119)

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
PLAN-010 Phase 0; ADR-O119 (owner: "add this to your agent.md ... and ensure to implement them")

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-132]

## Plan
1. pytest-xdist 3.8.0, six workers.
2. R-36 (an approved plan runs to its end), R-37 (tests come from the checks), R-38 (the budget) in docs/rules.yaml,
   so AGENTS.md carries them.
3. scripts/test_budget.py in the gate, with tests/budget_baseline.json, which may only shrink; PLAN-011 shrinks it.

Predictions, made before the change (19:26 by the clock):
1. The suite passes in parallel unchanged, about a third of the time.
2. Timing at the 100 ms line wobbles under six workers.

## Decisions
- D1 — A ratchet, not a hard cut: the budget enforced at once would fail the gate until about 200 tests are rewritten;
  the baseline holds today's excess and the gate refuses it growing or going stale. Level: covered (reported).
- D2 — A test new to the slow list is re-timed alone before it fails; a baselined one leaves the list under 50 ms:
  six workers' load is not a test's cost, and no flapping at the line. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | the gate script and the test layout read directly (no code navigation needed) |
| Tests | PASS | tests/test_test_budget.py new (4): at baseline, a new or grown excess, a stale entry, a new untested code |

## Duration
from 19:26 to 19:50

## Changes
- pyproject.toml, uv.lock; scripts/verify.sh, scripts/test_budget.py, tests/budget_baseline.json, tests/conftest.py,
  .gitignore; docs/rules.yaml 7.4 (logged); ADR-O119; PLAN-010 (times, status), PLAN-011; tests/test_test_budget.py

## Verification
- Prediction 1 held: 833 passed in 91 s (was 4.5 min).
- Prediction 2 held: two tests crossed 100 ms in a second run and passed alone.
