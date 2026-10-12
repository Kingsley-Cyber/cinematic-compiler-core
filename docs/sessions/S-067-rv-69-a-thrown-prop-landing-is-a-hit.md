# S-067 — RV-69: a body touched by a prop another performer threw is a hit, whatever the verb

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-69 (PLAN-007); finding F-175; rulings O92, R-21

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-067]

## Plan
planner/hits.py counts a prop's contact as a hit only with a striking verb, or a stabbing blade another performer still
holds, so a kunai B threw landing in A, written as the golden writes the 8.5 drive (A's torso as side a, no verb), owes
no camera hold (F-175, review 4).
1. A fifth kind: a touch between a performer and a prop another performer threw and no one holds, whatever the verb
   and whichever side names the body. The struck-with-a-verb kind keeps its label.
2. The breadth F-175 leaves to the owner (held weapons without stab, grapples, pins, touches outside combat, three or
   more performers) is not built.

Predictions, made before the change (05:41 by the clock):
1. The gate passes before the change: 686 tests (210285d).
2. The probe becomes a hit; every example's hits stay the same (the reference fight's 2.5, 4.7, 6.6 twice and 8.5; the
   wizard's 3.6).
3. No example, plan or prompt changes.
4. 687 tests (one test added).

## Decisions
- D1 — A fifth kind of hit: a touch between a performer and a prop another performer threw and no one holds, whatever
  the verb and whichever side names the body; a thrown weapon landing in a body is a hit by any reading of O92.
  Level: interpretation (F-053).
- D2 — The rest of F-175's breadth is not built and stays the owner's (R-06: deciding it would set O92's scope).
  Level: covered (R-06).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | planner/hits.py, which S16, S17 and the prompt read |
| Predictions written first | PASS | the session file was written at 05:41 before the code edit in the same command |
| New checks fire and stay silent | PASS | the probe is a hit; tests/test_hits.py's pinned lists for the four examples still pass |
| Tests changed with their data | PASS | `git diff -- tests`: one test added |
| Examples | PASS | `compiler.rebind` reports nothing moved and `compiler.examples` matches; no example file changed |
| Records | PASS | F-175 open in part with the owner's part named; F-053 noted; backlog (RV-69 done, RV-70 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 1 minutes by the clock (05:40 to 05:41)

## Changes
- planner/hits.py (the fifth kind); tests/test_hits.py (one test)
- F-175 noted (open in part); F-053 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-066's gate at 210285d: 686 passed
- after: `scripts/verify.sh` exit 0, 687 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the probe a hit; the examples' hits unchanged). Prediction 3 held (no example
  file changed). Prediction 4 held (687).
