# S-090 — Principal review 7: does the finished work match the plan?

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
docs/prompts/finish.md section 6 (after eight slices: RV-96, RV-95, RV-100, RV-99, RV-59a, RV-59b, RV-59d, RV-59c);
docs/prompts/principal_review.md (ADR-O99), docs/prompts/no_shortcuts.md; rulings O98, O99, O100, O101

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-090]

## Plan
Five fresh read-only reviewers (layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden
and the fight) follow the review prompt and the no-shortcuts prompt, each in its own extracted trees (nothing in the
worktree written); the builder checks their heaviest claims against the files, files each gap as a finding with a
slice or leaves it for the owner, and writes the verdict to docs/reports/2026-10-12-principal-review-7.md. This record
was kept outside the worktree while the reviewers read it, so they did not see these predictions.

Predictions, made after the reviewers were launched and before any report came back (11:06 by the clock):
1. The gate passes before the review: 731 tests (e0ec6fe).
2. Every reviewer's verdict is "partially", with no test tampering found.
3. The reviewers name this run's own slips: the chained commit that went in on a hygiene hit (S-087, corrected in
   d2c650c), the first 3.7 solve that left A out at its key (caught by S13), S-086's first measure on a broken Euler
   read-back (caught by the end-key test), S-087's bounds chosen in probes after its plan, and RV-59b marked done while
   its check waits.
4. The fight-breakers are named again: bodies through each other by contacts and B's crash through the floor (F-220),
   the climax (F-148), the volley (F-102).
5. Between four and ten new findings, at least one on an interpretation this run made (the straight root between
   keys, or the airborne rule between keys).

## Decisions
- D1 — The reviewers' heaviest claims were checked against the files before filing (the report's "Checked by the
  builder"): the 74-degree lean, the pickup words against the legend, B's 7.5 root clearing the descent, the nine
  lifted supports, the wizard's descent against c06, F-220's missing probe commands, the landing excused as airborne,
  B's crash cleared with the twist free, the camera floor's misses and false refusals, the knee's 0.0796 m and the
  tests' slack, the DAG's density lines, the commit fields, B's 2.95 mm at 4.4 and the wizard's overlapping Effort.
  Every one held. Level: covered (finish.md section 6).
- D2 — F-220's option (a) is answered as ADR-O109 (owner_default): the DAG's density rules call for explicit keys
  every 0.25-0.4 s at the knee strike and the kunai drive and on every support change (knowledge_dag_v1.md:253, 257,
  259, 261), and the option adds and sets nothing aside, so R-06 and finish.md section 4 have the run take it. Options
  (b) and (d) stay the owner's for whatever B's in-between keys cannot clear. F-220's title and evidence are corrected
  by a note; RV-59c and RV-59e are ready again behind RV-59f. Level: owner_default ADR (finish.md section 4).
- D3 — Nine findings filed (F-221 to F-229: gaps, each with a slice); F-210 reopened with F-187 and F-160 in part;
  corrections appended to S-083, S-085, S-087, S-088 and S-089 (a record is corrected by a note); F-053's late entries
  moved into its Description and the unlisted interpretations added (S-084, S-087, S-088, S-089); S-080's superseded
  entries marked. Level: covered.
- D4 — The queue: the builder's own loosenings first (RV-59h, RV-99b, RV-95b), then ADR-O109's keys (RV-59f), the
  turn (RV-108), the refusals between keys (RV-59e, RV-59c, RV-59g) and the wizard's landing (RV-107), then RV-97
  onward (backlog 38). Level: covered (finish.md section 6).
- D5 — The run's practice from S-091 (the report's list): negative results recorded like re-blocks; probes bounded by
  the rulings; a slice done only when its title is; a question the sources answer is answered; "covered" only where a
  ruling chooses; the commit fields; the staged scan before the gate; stated test tolerances. Level: covered (R-32,
  no_shortcuts.md).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| Reviewers fresh and read-only | PASS | five subagents with the protocol, each in extracted trees; `git status` was clean while they ran and this record was outside the worktree |
| Predictions written first | PASS | at 11:06, after the launch and before any report |
| Claims checked before filing | PASS | D1; the builder's own runs on an extracted e0ec6fe and on the worktree, read-only |
| Findings have slices | PASS | F-221 to F-229 each name one (RV-59g, RV-59h, RV-95b, RV-108, RV-107, RV-110, RV-111); F-210's is RV-99b |
| Owner rulings respected | PASS | ADR-O109 adds and sets nothing aside; F-220 (b), (d), F-215, F-111, F-148 stay the owner's |
| Records corrected, not rewritten | PASS | notes appended to five session records and seven findings; F-220's title restated with its old wording quoted in the note |
| Examples | PASS | none changed |
| Records | PASS | the review report; ADR-O109; backlog 38; map 24 (kernel log); PLAN-007; CHANGELOG; run report (row, ADR to confirm, questions) |
| Hygiene | see Verification | the staged scan runs first in the chained commit |

## Duration
from 11:06 (the plan's predictions) to 11:44 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- docs/reports/2026-10-12-principal-review-7.md (new); docs/decisions/ADR-O109 (new)
- docs/findings: F-221 to F-229 (new); F-220 (title, ruling, a correction); F-210 reopened; F-187, F-160 open in
  part; notes on F-053, F-089, F-134, F-206, F-207, F-215
- docs/sessions: corrections appended to S-083, S-085, S-087, S-088, S-089
- docs/plans/backlog.yaml 38; kernel/knowledge_map.yaml 24; PLAN-007; CHANGELOG; run report

## Verification
- before: S-089's chained gate at e0ec6fe: 731 passed (the rules reviewer re-ran it in a copy: 731)
- Prediction 1 held. Prediction 2 held (all five "partially", no tampering). Prediction 3 held in part (the hygiene
  slip, S-087's probe bounds and RV-59b's retitling were named; the 3.7 solve and the Euler read-back were not).
  Prediction 4 held (F-220's spans and the crash, F-148, the volley). Prediction 5 held (nine new findings; F-222 is
  on S-088's airborne rule). Predictions 4.5 of 5.
- the gate on this record (11:44:28): `scripts/verify.sh` exit 0, 731 passed in 72.45 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits (run first in the chained commit)
