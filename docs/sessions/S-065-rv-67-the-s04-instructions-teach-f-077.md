# S-065 — RV-67: the S04 instructions and the validator teach F-077's rule and O48's standing log

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-67 (PLAN-007); findings F-170, F-162; rulings O8, O48, R-24

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-065]

## Plan
The S04 instructions and planner/dynamic_beat_validator.py's docstring say a resting prop moves when a contact on it
at the second sample picks it up or knocks it down; the code refuses that (F-077: the contact takes or strikes the prop
where it rests, so it is still there at that instant). The first-state example says "deployment hidden", where O48's
log stands in the scene before the swap (F-170, review 4).
1. Both texts say: a prop at rest is still where it rested at a contact's instant; a contact between two samples moves
   it only by taking hold of it; any other move needs a sample at the contact's instant.
2. The example reads "deployment standing".
3. The temporal plans re-bind (the instructions are in the S04 packet).

Predictions, made before the change (05:31 by the clock):
1. The gate passes before the change: 686 tests (6224ecb).
2. Only the two texts change; the rebind moves the four temporal plans (hashes only); no prompt, verdict or test
   changes.
3. The gate stays at 686 tests.

## Decisions
- D1 — The two texts state F-077's rule as the code applies it: a resting prop is still in its place at a contact's
  instant, a contact between two samples moves it only by taking hold, any other move needs a sample at the contact.
  Level: covered (F-077, F-138; the code's own comment).
- D2 — The first-state example reads "deployment standing", the golden's own first state since O48. Level: covered
  (O48, R-24).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | the S04 instructions and the S04 validator's docstring; no code path changed |
| Predictions written first | PASS | the session file was created before the edits; predictions inside at 05:31 |
| New checks fire and stay silent | N/A | no check changed |
| Tests changed with their data | PASS | `git diff -- tests`: none |
| Examples | PASS | the four temporal plans and envelopes changed in packet hashes only |
| Records | PASS | F-170 resolved, F-162 resolved again with its limit stated; backlog (RV-67 done, RV-68 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 1 minutes by the clock (05:30 to 05:31)

## Changes
- planner/prompts/beat_planning.txt (F-077's rule; "deployment standing"); planner/dynamic_beat_validator.py (the
  docstring); the four temporal plans re-bound; the examples regenerated; docs/reference rebuilt
- F-170 resolved; F-162 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-064's gate at 6224ecb: 686 passed
- after: `scripts/verify.sh` exit 0, 686 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the two texts; the four temporal plans' hashes). Prediction 3 held (686).
