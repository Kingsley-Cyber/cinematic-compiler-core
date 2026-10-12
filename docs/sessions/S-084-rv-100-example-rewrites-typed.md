# S-084 — RV-100: this run's example rewrites typed as deviations; R-19 cites O97

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-100 (PLAN-007); finding F-212; rulings O97, R-33, ADR-O102

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-084]

## Plan
S-076 re-authored eleven of the reference fight's shots, S-078 re-posed B's lunge at 3.4 and 3.7, and S-080 and S-083
moved A's pickup rows; their commits said "Deviations: none" or named the rewrites only in prose, deviations.yaml did
not change, and DEV-09 still cites the rulings of S-030's re-block (F-212; review 6). R-19 defines a deliverable without
O97's cap, which RV-13 added. The class: a change to the golden that the golden's registry does not show.
1. The golden test records S-076's shot changes (REAUTHORED_SHOTS: each changed field) and S-078's lunge (B_LUNGE: the
   two hips), each held to the plans by a test, and each typed in deviations.yaml with its rulings.
2. DEV-09 and DEV-10 say what RV-95 did and cite its rulings (O18, O72, O11).
3. The registry's header names what it still does not record (the earlier camera values, B's other joints, the props'
   points: RV-51).
4. R-19 cites O97 and PROMPT_LENGTH (rules 7.2, the docs log).
5. The wizard, live-action and UGC examples have no source to depart from, so their rewrites stay in the session
   records.

Predictions, made before the change (09:40 by the clock):
1. The gate passes before the change: 715 tests (09aae39, S-083's chained gate).
2. The registry test passes with two new records and two new entries (DEV-32, DEV-33), and refuses either one alone.
3. No example, prose or checklist changes.
4. rules.md and the AGENTS.md block that prints the rules change with R-19; the docs plane passes.
5. About 717 tests (715 and two: the shots and the lunge held to the plans).

## Decisions
- D1 — A rewrite of the golden is typed as the registry types it: a record in the golden test (REAUTHORED_SHOTS: each
  field S-076 changed; B_LUNGE: the two hips S-078 moved), a test that holds the plans to it, and an entry with its
  type and rulings (DEV-32: re-blocked, O72 and O92; DEV-33: re-blocked, O72). Level: covered (R-33, ADR-O102).
- D2 — DEV-09 cites the rulings the pickups now rest on (O18 for the crouch, O72 for the hand at the prop, O11 for the
  limits the solver keeps), and DEV-10 the words' rule. Level: covered.
- D3 — The wizard, live-action and UGC examples are the repo's own, with no source to depart from, so their rewrites
  (S-076's shots, S-078's acrobat at 8.6) stay recorded in the session files; R-19 names O97. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the golden's registry, its test and one rule's text; no data changed |
| Predictions written first | PASS | the session file was written at 09:40, before any change |
| New behaviour, old behaviour | PASS | the registry test without DEV-32 names REAUTHORED_SHOTS missing, without DEV-33 B_LUNGE (measured); the new test holds both to the plans |
| Neighbours | PASS | DEV-09 and DEV-10 against S-083's pins; the registry's header against RV-51's remaining scope; R-19 in rules.md and AGENTS.md |
| The step's instructions teach it | n/a | records, not a step |
| Tests changed with their data | PASS | two new records and one new test in tests/test_reference_fight_golden.py; nothing removed or loosened |
| Examples | PASS | deviations.yaml only (version 2); no plan, prose or checklist changed |
| Records | PASS | F-212 resolved; F-147 and F-200 noted; rules 7.2 (docs log); backlog (RV-100 done, RV-99 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 09:40 (the plan) to 09:41 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- tests/test_reference_fight_golden.py (REAUTHORED_SHOTS, B_LUNGE and a test); examples/reference_fight/deviations.yaml
  (version 2: DEV-32, DEV-33; DEV-09, DEV-10; the header)
- docs/rules.yaml 7.2 (R-19 cites O97; the docs log); rules.md and AGENTS.md regenerated
- F-212 resolved; F-147, F-200 noted; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-083's chained gate at 09aae39: 715 passed
- Prediction 1 held. Prediction 2 held (measured: either entry dropped, the registry test names its record). Prediction
  3 held. Prediction 4 held (rules.md, AGENTS.md; the docs plane passes). Prediction 5 held in part: 716, not 717
  (one test holds both records). Predictions 4.5 of 5.
- the gate on this record (09:41:44): `scripts/verify.sh` exit 0, 716 passed in 95.72 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
