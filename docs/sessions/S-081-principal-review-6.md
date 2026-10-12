# S-081 — Principal review 6: does the finished work match the plan?

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
docs/prompts/finish.md section 6 (after eight slices: RV-85, RV-86, RV-13, RV-15a, RV-15b, RV-14a, RV-16, RV-35a);
docs/prompts/principal_review.md (ADR-O99), docs/prompts/no_shortcuts.md; rulings O98, O99, O100, O101

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-081]

## Plan
Five fresh read-only reviewers (layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden
and the fight) follow the review prompt and the no-shortcuts prompt; the builder checks their heaviest claims against
the files, files each gap as a finding with a slice or leaves it for the owner, and writes the verdict to
docs/reports/2026-10-12-principal-review-6.md.

Predictions, made before the review (08:39 by the clock):
1. The gate passes before the review: 711 tests (3cdfb4d).
2. Every reviewer's verdict is "partially", with no test tampering found; the moved pins of S-078 and S-080 read as
   fixtures moving with recorded changes (ADR-O102).
3. The reviewers name the run's own slips: the knowledge map's version logged before its locator (S-076), the solver
   drafted before S-080's plan, PLAN-007's table left stale from S-073 to S-077, and S-076's camera values chosen by a
   scratch search (F-127's class).
4. The fight-breakers are named again: the climax's held kunai (F-148), the volley (F-102), bodies between keys
   (F-159), and the pickups' deep lean (F-205).
5. Between five and twelve new findings, at least one of them on a tolerance or measure this run chose (the floor's
   0.15 m, points rather than surfaces, the claimed supports).

## Decisions
- D1 — The reviewers' heaviest claims were checked against the files before filing (the report's "Checked by the
  builder"): the static holds lose their bodies, the knee in the floor, the solver's order dependence, the 0.57 m
  crouch reaching at 66 degrees, the camera words' gaps, the three supports printed, O21 against the opening, the
  cameras behind the pillar. Every one held. Level: covered (finish.md section 6).
- D2 — Thirteen findings filed (F-206 to F-218: eleven gaps with slices, two questions); F-090, F-110, F-187, F-160
  and F-091 reopened in part with carriers; F-127's resolution corrected; the review's corrections appended to S-078
  and S-080 as dated notes (a record is corrected by a note, never rewritten). Level: covered.
- D3 — The queue: the builder's own regressions first (RV-96, RV-95, RV-100, RV-99), then the fight-breakers (RV-59,
  RV-97, RV-98, RV-101, RV-103a to RV-103c, RV-17 pulled forward), then the rest (backlog 33). RV-87 waits for F-196
  (it would answer Q1-Q3); RV-90's scale part (RV-90b) waits for F-197 Q3; RV-14b and RV-15c were split so the repo's
  parts are ready (RV-14c, RV-103b). Level: covered (finish.md section 6; R-06).
- D4 — The run's practice from S-082 (the report's list): re-blocks recorded as commands from the pre-re-block key, a
  tolerance stated with what it lets pass, every example rewrite typed, a key-only check named with its between-keys
  carrier, a new check run against the owner's rulings before it lands. Level: covered (R-05).
- D5 — F-202 Q3 (the opening) is answered by O21, "A starts above the frame", so RV-98 builds it instead of waiting.
  Level: covered (R-06 asks only where the decisions are silent).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the gate's own output is copied below, then the chained gate commits |
| One gap, right layer | PASS | records only: findings, backlog, PLAN-007, the review and run reports, CHANGELOG, two appended corrections; no code or example changed |
| Predictions written first | PASS | the session file was written at 08:39, before the reviewers were launched |
| Claims checked | PASS | the probes in D1, run in the scratchpad against the committed envelope and code |
| Tests | PASS | `git diff -- tests`: no change |
| Records | PASS | F-206 to F-218; five reopened; nineteen noted; backlog 33; PLAN-007; the review and run reports; CHANGELOG |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 08:39 (the plan) to 09:14 (the record's last edit before the gate; the gate and the commit follow); the reviewers
ran 19 to 27 minutes each

## Changes
- docs/reports/2026-10-12-principal-review-6.md (new); docs/findings F-206 to F-218 (new)
- F-090, F-110, F-187, F-160, F-091 reopened in part; F-127 corrected; F-053, F-088, F-089, F-092, F-097, F-134, F-145,
  F-155, F-159, F-172, F-188, F-189, F-194, F-195, F-196, F-197, F-200, F-202, F-205 noted
- docs/plans/backlog.yaml 33 (RV-95 to RV-105, RV-103a to RV-103c, RV-14c, RV-90b; RV-87 blocked; RV-14b, RV-15c,
  RV-59 and RV-90 retitled; RV-17 and RV-59 moved); PLAN-007; CHANGELOG; the run report
- docs/sessions/S-078 and S-080: corrections appended

## Verification
- before: S-080's chained gate at 3cdfb4d: 711 passed
- Prediction 1 held. Prediction 2 held (all five "partially"; no tampering; the moved pins read as fixtures moving with
  recorded data). Prediction 3 held in part: the solver drafted before S-080's plan, S-076's scratch camera search and
  PLAN-007's stale table were named; the map's version logged before its locator was not. Prediction 4 held (F-148,
  F-102, F-159 and F-205 named). Prediction 5 held in part: thirteen new findings, over the twelve predicted; one is
  the floor tolerance this run chose (F-215). Predictions 4 of 5.
- the gate on this record (09:14:54): `scripts/verify.sh` exit 0, 711 passed in 83.94 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
