# S-064 — RV-66: a substitution exempts only its decoy, the prop it places at its actor's anchor

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-66 (PLAN-007); findings F-169, F-130; rulings O12, O48, R-06, O102

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-064]

## Plan
RV-48a (S-057) let a substitution move any prop it changes to any place at its start (S04's `_swapped`) and change any
prop with no hand (S07's PROP_CHANGE_CONTACT), wider than its own label, "the log takes A's place" (F-169, review 4).
1. One function names a substitution's decoy: the prop it changes whose sample at its start lies within the contact
   tolerance (0.15 m, O72) of its actor's anchor, the nearest if more than one; at most one per substitution.
2. S04's swap exempts only the decoy's move; S07 exempts only the decoy's change. Other props a substitution changes
   need a contact, as in any beat. TELEPORT's exemption is unchanged (it asks for a prop change).
3. Break tests for the reviewers' probes; the existing swap test gives its substitution an actor anchored at the decoy.

Predictions, made before the change (05:24 by the clock):
1. The gate passes before the change: 684 tests (df35935).
2. The narrowed rule refuses the three probes (the log placed 2.5 m from A's place at 3.7: PROP_KINEMATICS; a resting
   pellet sample at 3.6 then the 3.7 sample in A's hand above it: PROP_KINEMATICS; b09 setting the untouched kunai
   embedded: S07's PROP_CHANGE_CONTACT) and passes the reference fight unchanged (the log lies 0.1 m from A's anchor).
3. One existing test pins the wide reading (S04's swap test, whose substitution has no actor anchor) and changes with
   the rule, recorded under ADR-O102; no other test changes.
4. No example, plan or prompt changes.
5. About 686 tests (684, an S04 break test, an S07 break test).

## Decisions
- D1 — A substitution's decoy is the prop it changes whose sample at its start lies within 0.15 m of its actor's
  anchor, the nearest if several. Level: interpretation (F-053: O72's contact tolerance read as "where A stood", O48).
- D2 — S04's swap and S07's PROP_CHANGE_CONTACT exemption read the same `decoy(beat)`; any other prop a substitution
  moves or changes needs a contact. Level: covered (F-169; the literal reading of O48).
- D3 — TELEPORT's exemption is unchanged: the substitution must still change a prop. Level: covered (the slice's
  scope; O12).
- D4 — The S04 swap test's substitution gains an actor anchored at the decoy, since the rule it pins now asks for the
  anchor; its far-anchor case is added. Level: covered (ADR-O102: the test changes with the rule, recorded here).
- D5 — The S04 instructions teach the decoy's definition, so the four temporal plans re-bind (hashes only). Level:
  covered (F-162: the instructions follow the code).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`: the commit exists only if the gate passed after the last edit |
| One gap, right layer | PASS | the decoy defined once at S04 (planner/dynamic_beat_validator.py) and read by S07; nothing else changed |
| Predictions written first | PASS | the session file was created before the first code edit; predictions inside at 05:24 |
| New checks fire and stay silent | PASS | `fight_codes` probes: the golden gives no PROP_KINEMATICS; the far log and the pellet's jump give PROP_KINEMATICS; cross_check refuses the kunai's change in b09 and passes the log's (the reviewers' probes passed the old code, S-063) |
| Tests changed with their data | PASS | `git diff -- tests`: one test's substitution case anchored (D4), two tests added; nothing skipped or deleted |
| Examples | PASS | the four temporal plans and envelopes changed in packet hashes only; no prompt or checklist verdict |
| Records | PASS | F-169 and F-130 resolved; F-053 narrowed; backlog (RV-66 done, RV-67 next); PLAN-007; CHANGELOG; run report |
| Hygiene | PASS | the scan over the staged diff before the commit |
Claim corrected before the commit: the first gate passed its 686 tests but stopped on docs/reference/code.md and
dependencies.md, stale after S07's new import of the decoy; `python -m kernel.build_docs` rebuilt them.

## Duration
about 3 minutes by the clock (05:23 to 05:26)

## Changes
- planner/dynamic_beat_validator.py (`decoy`, `_swapped`, DECOY_M); compiler/passes/mandatory/p07_contact.py (the
  exemption reads the decoy); planner/prompts/beat_planning.txt (the decoy's definition); docs/reference rebuilt
- tests: test_dynamic_beat_validator.py (one test anchored, one added), test_contact_pass.py (one added)
- the four temporal plans re-bound; the examples regenerated
- F-169, F-130 resolved; F-053 narrowed; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-063's gate at df35935: 684 passed
- after: the chained gate and commit
- Prediction 1 held. Prediction 2 held (the three probes refused; the golden unchanged, the log 0.1 m from A's anchor).
  Prediction 3 held (one test anchored). Prediction 4 held in part: no example data, prompt or verdict changed, but the
  four temporal plans re-bound because the instructions now teach the decoy, which the prediction did not foresee.
  Prediction 5 held (686).
