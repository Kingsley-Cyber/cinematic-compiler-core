# S-072 — Principal review 5: does the finished work match the plan?

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
docs/prompts/finish.md section 6 (after eight slices: RV-66, RV-67, RV-68, RV-69, RV-70, RV-71a, RV-71b, RV-72);
docs/prompts/principal_review.md (ADR-O99), docs/prompts/no_shortcuts.md; rulings O98, O99, O100, O101

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-072]

## Plan
Five fresh read-only reviewers (layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden
and the fight) follow the review prompt and the no-shortcuts prompt; the builder checks their heaviest claims against
the files, files each gap as a finding with a slice or leaves it for the owner, and writes the verdict to
docs/reports/2026-10-12-principal-review-5.md.

Predictions, made before the review (06:10 by the clock):
1. The gate passes before the review: 694 tests (5159dff).
2. Every reviewer's verdict is "partially" (fight_works and the deliverable gate still fail; the owner's questions
   stay open), with no test tampering found.
3. Fewer new gaps than review 4 (eighteen), most of them in what review 4's slices left: the structured camera rules'
   coverage, the decoy's anchor tolerance, the hits' breadth, and the records.
4. The fight-breakers review 4 listed (the volley, the climax grip, the aim, between-key overlaps) are named again.
5. Between five and twelve new findings.

## Decisions
- D1 — The reviewers' heaviest claims were checked against the files before filing: a mislabelled struck camera rule
  passes the card check; TELEPORT reads any prop change; the rope reads taut against the source; the RULES' continuity
  line promises a reappearance; the records' gate counts came before their gates. Every one held. Level: covered
  (finish.md section 6).
- D2 — Nine gaps filed with slices (F-187 to F-195; RV-85 to RV-93, RV-82b); the owner's open questions filed as
  question findings (F-196 to F-203), since the generated owner pages list only findings typed question. Level:
  covered.
- D3 — The queue is rebalanced toward the fight: the builder's own shortcuts (RV-85, RV-86), then RV-13 (O97: "now"),
  then the fight-breakers, then the remaining latent checks; RV-74 follows RV-54 and RV-22; RV-82's turn-plane part
  waits for the owner (RV-82b); backlog 28. Level: covered (finish.md section 6; PLAN-007; R-06).
- D4 — The run's practice from S-073 (F-194): the gate first and its output copied into the record; probe numbers
  reported as measured; each slice names its finding's class and checks the neighbours and its step's instructions;
  Duration says where it ends; titles carry their rulings. Level: covered (R-05; self_audit.md).
- D5 — Four findings reopened in part with carriers (F-130, F-160, F-173, F-177), as S-063 adopted. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the gate's own output is copied below, then the chained gate commits |
| One gap, right layer | PASS | records only: findings, backlog, PLAN-007, the review and run reports, CHANGELOG; no code or example changed |
| Predictions written first | PASS | the session file was created at 06:10, before the reviewers were launched |
| Claims checked | PASS | the probes in D1 (the card probe printed `True` for a mislabelled struck rule passing) |
| Tests | PASS | `git diff -- tests`: no change |
| Records | PASS | F-187 to F-203 filed; four findings reopened in part; backlog 28 resequenced; docs plane PASS |
| Hygiene | PASS | the scan over the staged diff, run before the commit (its output below) |

## Duration
from 06:10 (the plan) to the record's last edit at the time below; the gate and the commit follow (the reviewers ran
16 to 26 minutes each)

## Changes
- docs/reports/2026-10-12-principal-review-5.md (new); docs/findings F-187 to F-203 (new); F-090, F-130, F-155, F-160,
  F-169, F-171, F-172, F-173, F-177, F-180, F-186 noted or reopened
- docs/plans/backlog.yaml 28 (RV-82b, RV-85 to RV-93; resequenced); PLAN-007; CHANGELOG; the run report

## Verification
- before: S-071's gate at 5159dff: 694 passed
- the gate on this record (06:43:15): `scripts/verify.sh` exit 0, 694 passed in 74.18 s, docs plane PASS, check: PASS
- the hygiene scan over the staged diff: 0 hits (home paths, emails, keys)
- Prediction 1 held. Prediction 2 held (five "partially", no tampering). Prediction 3 failed: nine new gaps against
  review 4's eighteen, but in classes the eight slices left open (TELEPORT, the decoy, the printed camera words, the
  tap), not only the ones predicted. Prediction 4 held (the volley, the grip, the aim, the overlaps named again).
  Prediction 5 held in part: nine gap findings and eight question findings.
