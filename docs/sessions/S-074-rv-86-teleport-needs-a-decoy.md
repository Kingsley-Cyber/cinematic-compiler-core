# S-074 — RV-86: TELEPORT's exemption needs a decoy in the actor's place

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-86 (PLAN-007); finding F-188; rulings O12, O48, O102

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-074]

## Plan
RV-66 made `decoy(beat)` the rule for S04's swap and S07, but TELEPORT still exempts a substitution that changes any
prop, so an actor may jump after a substitution that leaves no decoy in its place (F-188, review 5; S-064 D3 called it
covered against O12's "decoy revealed"). The class: every exemption a substitution grants reads the same decoy.
1. TELEPORT exempts the actor's jump only when `decoy(before)` names a prop.
2. The validator's docstring and the S04 instructions say so.
Neighbours: the swap and S07 already read `decoy`; a substitution with no decoy that does not jump is F-189's (RV-87).

Predictions, made before the change (06:52 by the clock):
1. The gate passes before the change: 696 tests (41f73ca).
2. The narrowed exemption refuses the reviewers' probe (a kunai changed 5 m away, the actor 20 m in 0.5 s) and the
   test helper's substitution that changes a prop it places nowhere; the golden's b09 passes (its log at A's anchor).
3. The teleport test's substitution case gets an anchored decoy and a far case, recorded under ADR-O102; the four
   temporal plans re-bind for the instructions' sentence (hashes only); no prompt changes.
4. 697 tests (one parametrized case added).

## Decisions
- D1 — TELEPORT's exemption reads `decoy(before)`, the decoy S04's swap and S07 read; a substitution that changes a prop
  it does not place in the actor's stead no longer licenses the jump. Level: covered (O12: "decoy revealed"; F-188).
- D2 — The teleport test's substitution gains a decoy sample at the actor's anchor, since the rule now asks for one, and
  a far-decoy case is added. Level: covered (ADR-O102: the test changes with the rule, recorded here).
- D3 — A substitution with no decoy that does not jump stays F-189's (RV-87). Level: covered (the slice's scope).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | S04's TELEPORT, where the plan's jumps are first seen |
| Predictions written first | PASS | the session file was written at 06:52, before the code edits |
| New checks fire and stay silent | PASS | the far-decoy case fires; the golden's S04 codes are [] (fight_codes) |
| Neighbours | PASS | the swap and S07 already read `decoy`; the S04 instructions' teleport sentence follows; RV-87 holds the rest |
| Tests changed with their data | PASS | `git diff -- tests`: the teleport test's helper gains the decoy sample and one case (D2) |
| Examples | PASS | the four temporal plans re-bound for the instructions' sentence (hashes only) and their envelopes; no prompt changed |
| Records | PASS | F-188 resolved; backlog (RV-86 done, RV-13 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 06:51 (the plan) to 06:53 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- planner/dynamic_beat_validator.py (TELEPORT reads `decoy`; its docstring); planner/prompts/beat_planning.txt (the
  teleport sentence)
- tests/test_dynamic_beat_validator.py (the teleport test's decoy and far case)
- the four temporal plans re-bound and the examples regenerated
- F-188 resolved; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-073's gate at 41f73ca: 696 passed
- Prediction 1 held. Prediction 2 held (the far decoy fires; the golden's S04 codes are []). Prediction 3 held (the test
  changed with the rule; four temporal plans by hash; no prompt). Prediction 4 held (697).
- the gate on this record (06:54:43): `scripts/verify.sh` exit 0, 697 passed in 74.42 s, check: PASS
- the hygiene scan over the staged diff: 0 hits
