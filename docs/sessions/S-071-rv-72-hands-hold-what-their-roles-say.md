# S-071 — RV-72: S08 refuses an undeclared hand holding the object; S09 credits a release only at the change

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-72 (PLAN-007); findings F-173, F-137, F-161

## Layer
L2.5

## Status
applied

## Commit
the commit whose message names [S-071]

## Plan
S08's role lock reads the hands' contacts but not their holds, so a one_hand unfold passes while the other hand holds
the glasses throughout (library/role_templates.yaml: the other hand stays off the object); S09 credits a release made
before a change as the hand on the object (F-173, review 4).
1. S08: a hand of the actor holding the object at the start of any of the interaction's beats is one of its declared
   hands, or HAND_ROLE_SWAP.
2. S09: a release counts as the trigger only at the change's instant; earlier, the hand has already let go.

Predictions, made before the change (06:06 by the clock):
1. The gate passes before the change: 692 tests (6dc911b).
2. Both probes (a one_hand unfold whose right hand holds the glasses; a release at 3.5 as the only hand on the glasses
   for the 5.5 change) pass today and are refused after (HAND_ROLE_SWAP, OBJECT_STATE_TRIGGER).
3. The UGC example passes unchanged; no example changes.
4. 694 tests (two tests added).

## Decisions
- D1 — S08's role lock reads the holds at the interaction's beat starts as well as its contacts: an undeclared hand of
  the actor holding the object is refused. Level: covered (library/role_templates.yaml: the other hand stays off the
  object; F-173).
- D2 — S09 credits a release as the trigger only at the change's instant; a hand that let go earlier is not on the
  object. Level: covered (F-161's resolution, now true).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`, after a first gate run read the count |
| One gap, right layer | PASS | S08's role lock and S09's trigger (L2.5, L2.6) |
| Predictions written first | PASS | the session file was written at 06:06 before the code edits |
| New checks fire and stay silent | PASS | the old S08 and S09 return nothing on the two probes; the new ones refuse them; the UGC plans pass |
| Tests changed with their data | PASS | `git diff -- tests`: two tests added |
| Examples | PASS | `compiler.rebind` and `compiler.examples` report nothing; no example file changed |
| Records | PASS | F-173 resolved, F-137 and F-161 resolved again; backlog (RV-72 done, RV-73 next); PLAN-007; CHANGELOG; the run report (and RV-71b's row corrected to 4.5/5, as its session says) |
| Hygiene | PASS | the scan over the staged diff before the commit |

## Duration
about 2 minutes by the clock (06:05 to 06:07)

## Changes
- compiler/passes/derived/p08_hand_role.py (the holds), p09_object_state.py (the release's instant)
- tests: test_hand_role.py, test_object_state.py (one test each)
- F-173 resolved; F-137, F-161 resolved again; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-070's gate at 6dc911b: 692 passed
- after: `scripts/verify.sh` exit 0, 694 passed, check: PASS
- Prediction 1 held. Prediction 2 held (both probes pass the old code and are refused). Prediction 3 held. Prediction
  4 held (694).
