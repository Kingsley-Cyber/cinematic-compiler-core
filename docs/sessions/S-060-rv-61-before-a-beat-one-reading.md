# S-060 — RV-61: "before a beat" read one way: S10 reads the state before the beat's own effects; S09 carries instants

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-61 (PLAN-007); finding F-161; rulings O91, F-061, O102

## Layer
L2.7

## Status
applied

## Commit
the commit whose message names [S-060]

## Plan
S06 reads a beat's requirements before the beat's own effects (REPLAY_REQUIRES), but its snapshot at the beat's start
includes the beat's own at-start effects, and S10 reads that snapshot as the state before the interaction; S09 drops
each change's instant, so its trigger check can credit a hand that arrives after the change (F-161).
1. S06 computes the values before a beat's own effects with the same function REPLAY_REQUIRES uses, and a beat's
   snapshot records them where they differ (`before_own_effects`; state_graph 1.3, optional).
2. S09: each object state carries `state_before` (its internal state before that beat's own effects), and each change
   its instant `t`; OBJECT_STATE_TRIGGER credits only a hand contact at or before the change's instant in the
   triggering beat, or a hand holding the object at that instant (object_state_graph 1.1).
3. S10 reads preconditions in the first beat's `state_before` and postconditions in the next state's `state_before`
   (the state at that instant before the next beat acts).

Predictions, made before the change (04:10 by the clock):
1. The gate passes before the change: 675 tests (69bd2f0).
2. In the examples, `before_own_effects` appears only at beats whose own effects or at-start possess/release contacts
   change a value at their start (in the UGC: glasses@b01, holder none); every example still compiles and S10's two
   UGC interactions still pass with the same before and after states.
3. F-161's case (UGC b02's temples=open marked `at: start`): the old S10 refuses it (unfold needs folded, found
   open) and the new one passes it, crediting the right hand's hold at 1.5, not the touch at 3.5; the converse (a
   precondition met only by the beat's own at-start effect) passes the old S10 and is refused by the new one.
4. No prompt text and no authored plan's packet changes (the packets read fields of the states, not whole nodes);
   only the envelopes' S06 and S09 nodes change.
5. About 679 tests (675, one S06 test, one S09 test, two S10 tests).

## Decisions
- D1 — "Before a beat" is defined once, in S06: `value_at(..., before=beat)`, the function REPLAY_REQUIRES already
  used; a beat's snapshot keeps its results where they differ from the snapshot (`before_own_effects`, absent
  otherwise), so the envelopes grow only where a beat acts at its start. Level: covered (F-161: "as S06's
  requirements do").
- D2 — S09 copies that field for internal properties and each change's `t`; S10 reads `state` overlaid with it, so
  the existing tests that edit `state` keep their meaning. Level: covered (F-161).
- D3 — A postcondition is read at the next state before that state's beat acts, as a precondition is. Level:
  interpretation (F-053; the same reading, F-161's converse).
- D4 — S09 judges a change's trigger hand at the earliest instant among the transition's changes inside the triggering
  beat (a touch by then, or a hold at it). Level: interpretation (F-053).
- D5 — The schemas went 1.3 and 1.1 with `minProperties`, a keyword the repository's schema subset refuses; the log
  is append-only, so they went again to 1.4 and 1.2 without it. Level: covered (ADR-O106: a changed entry bumps).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 678 passed, check: PASS, after the last code edit |
| One gap, right layer | PASS | the reading of "before a beat" at S06 where it is defined, carried by S09 and read by S10; nothing else reads the new field |
| Predictions written first | PASS | written 04:10, before any edit; predictions 2 and 3 measured with the old S09 and S10 kept beside the new ones |
| New checks fire and stay silent | PASS | F-161's case: the old S10 refuses it, the new passes it with the hold as trigger; the converse: the old passes, the new refuses; the late-hand case: the old S09 credits the 3.5 touch, the new refuses |
| Tests changed with their data | PASS | `git diff -- tests`: three tests added; two import lines widened; no test edited, skipped or deleted |
| Examples | PASS | rebind moved nothing; only the reference fight's and the UGC's envelopes changed (six states gain the field); no prompt or checklist changed |
| Records | PASS | F-161 resolved; F-053 lists D3, D4; the schema log (four entries, D5); docs/reference rebuilt; backlog, PLAN-007, CHANGELOG, run report |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the predictions first said 04:16 for their time; the clock read 04:10, and the
file says so.

## Duration
about 9 minutes by the clock (04:07 to 04:16)

## Changes
- solver/prop_state_machine.py (`before_own_effects`); compiler/passes/derived/p09_object_state.py (the field, each
  change's `t`, the trigger by the change's instant); compiler/passes/derived/p10_affordance.py (`_before`)
- schemas/graphs/state_graph.schema.json 1.4, object_state_graph.schema.json 1.2 (schema log); docs/reference rebuilt
- tests: test_state_pass.py, test_object_state.py, test_affordance.py (one test each)
- examples/reference_fight and examples/ugc_glasses_demo envelopes regenerated
- F-161 resolved; F-053 noted; backlog (RV-61 done, RV-62 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-059's gate at 69bd2f0: `scripts/verify.sh` exit 0, 675 passed
- after: `scripts/verify.sh` exit 0, 678 passed, check: PASS
- Prediction 1 held. Prediction 2 held (the field at five reference-fight states and the UGC's glasses@b01, holder
  none; none in the wizard or live action; S10's UGC states unchanged). Prediction 3 held (both directions, and the
  hold credited at 1.5). Prediction 4 held (no plan or prompt moved). Prediction 5 held in part: 678, three tests.
