# S-099 — Principal review 8: does the finished work match the plan?

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
docs/prompts/finish.md section 6 (after eight slices: RV-59h, RV-99b, RV-95b, RV-59f, RV-59i, RV-108, RV-59e, RV-59c);
docs/prompts/principal_review.md (ADR-O99), docs/prompts/no_shortcuts.md; rulings O98, O99, O100, O101

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-099]

## Plan
Five fresh read-only reviewers (layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden
and the fight) follow the review prompt and the no-shortcuts prompt, each in its own extracted trees; the builder
checks their heaviest claims against the files, files each gap as a finding with a slice or leaves it for the owner,
and writes the verdict to docs/reports/2026-10-12-principal-review-8.md. This record stays outside the worktree while
they read.

Predictions, made before the reviewers were launched (12:56 by the clock):
1. The gate passes before the review: 750 tests (87804d2).
2. Every reviewer's verdict is "partially", with no test tampering found.
3. The reviewers name at least two of this run's own choices as unflagged or loose: RV-59e's title promised B's 7.5
   root re-block that never happened; S-095's prose section broke the Master Template until S-097 moved it; RV-108
   changed the drawn path of three of A's source spans without the owner; the in-between keys' names and descriptions
   were written after the solve.
4. The fight-breakers are named again: the climax (F-148), the volley (F-102), the open supports between keys
   (F-221), and the pickups' lean and words (F-223, F-224).
5. Between three and eight new findings.

## Decisions
- D1 — The reviewers' heaviest claims were re-run by the builder on trees it extracted itself (the report's "Checked
  by the builder"): B's float and its crash, RV-59h's loosening by two planted contacts on 871d7ce and 87804d2, the
  camera floor's eleven phrasings on 1380170 and 87804d2, the two in-between holes, RV-108's redraw of A's spins, the
  pickups' weighted re-solve and the zero-allowance crash re-solve, B's root speed. All held but one ("A facing B",
  not reproduced, not filed). Level: covered (finish.md section 6).
- D2 — The owner's instruction mid-review is recorded as ADR-O110 (owner): significant work only, then the owner
  renders. Level: owner ruling.
- D3 — What counts as significant under ADR-O110: what changes what a prompt tells the renderer, and a check this run
  loosened (a regression of an owner rule). Four findings filed (F-230 to F-233) with five slices (RV-113, RV-59j,
  RV-59k, RV-59l, RV-99c); F-210 reopened; everything else review 8 found is listed in the report, not filed.
  Level: interpretation of the owner's word (ADR-O110 names the test; the list is the builder's).
- D4 — The queue: RV-113 next (every prompt), then RV-59j, RV-59k, RV-59l, RV-99c; RV-59g back to ready. Then the run
  stops for the owner's renders (ADR-O110). Level: covered (ADR-O110).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Reviewers fresh and read-only | PASS | five subagents with the protocol, each in extracted trees; `git status` was clean while they ran and this record was outside the worktree |
| Predictions written first | PASS | at 12:56, before the launch |
| Claims checked before filing | PASS | D1; the builder's own runs on extracted 871d7ce, 1380170 and 87804d2 (scratchpad), read-only |
| Findings have slices | PASS | F-230 RV-59j; F-231 RV-113; F-232 RV-59k; F-233 RV-59l and RV-99c |
| Owner rulings respected | PASS | ADR-O110 recorded verbatim; ADR-O84 applied by F-231; ADR-O109, F-088, F-143 stay the owner's |
| Examples | PASS | none changed |
| Records | PASS | the review report; ADR-O110; F-230 to F-233; F-210 reopened; backlog 42; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 12:56 (the plan's predictions) to 13:40 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- docs/reports/2026-10-12-principal-review-8.md (new); docs/decisions/ADR-O110 (new)
- docs/findings: F-230 to F-233 (new); F-210 reopened
- docs/plans/backlog.yaml 42; PLAN-007; CHANGELOG; run report

## Verification
- before: S-098's chained gate at 87804d2: 750 passed (the rules and S01-S09 reviewers re-ran it in copies: 750)
- Prediction 1 held. Prediction 2 held (all five "partially"; no test deleted, skipped or xfailed, though S-097
  loosened two assertions). Prediction 3 held (RV-59e's root, S-095's section, RV-108's redraw of A's spans and the
  in-betweens' words were all named). Prediction 4 held in part (F-221 and F-223 named; F-148, F-102 and F-224 not).
  Prediction 5 held (four new findings, F-210 reopened). Predictions 4 of 5, one in part.
- the gate on this record (13:40:49): `scripts/verify.sh` exit 0, 750 passed in 106.20 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first, and again in the chained commit)
