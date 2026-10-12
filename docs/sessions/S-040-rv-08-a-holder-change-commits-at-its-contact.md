# S-040 — RV-08: a holder change commits at its contact's instant, not the beat's end

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-08 (PLAN-007); finding F-061; rulings O23, O101, O102

## Layer
L2.1

## Status
applied

## Commit
the commit whose message names [S-040]

## Plan
F-061: S06 commits every effect at its beat's end, so since O23 (a throw lets go at its pose, `at: start`) the kunai's
track prints the release at 2.00 and the holder change at 2.50, and S07 carries a special case that keeps the prop in
the hand at an at-start release. RV-03 needs the same fix: the creator takes the glasses at the first frame (the
possess `at: start` of b01) while S06 still says nobody holds them until 1.5 (S07 refused it: HOLDER_CONTACT). So RV-08
comes first and RV-03 depends on it.
1. S06 (solver/prop_state_machine.py): a prop's holder change commits at the instant of its beat's possess (to the
   new holder) or release (to none) of that prop; an entity's possession change likewise at its own possess or
   release; every other effect still commits at the beat's end. A beat's requirements are read before its own
   commits, so a change at the beat's own start does not break them.
2. S07: the special case for an at-start release goes; the holder cross-check then reads S06's state as it is.

Predictions, made before the change:
1. The gate passes before the change: 641 tests (b2ace41).
2. After it, the kunai's holder change B -> none moves from 2.50 to 2.00, with its release; no other holder change in
   the four examples moves (they sit on contacts at their beats' ends).
3. Only the reference fight's outputs change (the kunai's state lines); every example compiles.
4. 642 tests: a test that a possess at its beat's start shows the new holder at that start and keeps the beat's own
   requirement; no existing test changes unless it pins the kunai's 2.50 holder line.

## Decisions
- D1 — RV-08 goes before RV-03, which now depends on it: RV-03's pickup at the first frame needs the holder to change at
  its contact. Why: R-10 (fix at the owning layer: S06), finish.md section 5. Level: covered.
- D2 — What moves: a prop's holder change, at its beat's possess (to the new holder) or release (to none) of that
  prop, and an entity's possession change at its own; every other effect stays at the beat's end. Why: F-061's fix
  names the holder change and possession mirrors it; location, temples, worn and damage describe the beat's action
  over its span. Alternatives: every effect of a beat with a contact at that contact (too broad); the smoke's burst
  (RV-07, O91). Level: covered (F-061, O23).
- D3 — A beat's requirements are read before its own effects, so a change at its own start keeps them true. Why: cause
  then effect within one beat. Level: covered.
- D4 — Each state transition records `t`, the instant its changes take effect (state_graph 1.1, schemas log), and the
  three renderer sites print it instead of rebuilding times from beat ends. Why: one source for the time. Level:
  covered.
- D5 — S07's special case for an at-start release goes, and its test is rewritten to the new semantics (the holder is
  none at the release's instant; a holder kept past it is refused). Why: F-061's fix moves what the test pinned
  (ADR-O102). Level: covered.

## Duration
about 50 minutes

## Changes
- solver/prop_state_machine.py (`commit_time`, requirements before own effects, transition `t`);
  schemas/graphs/state_graph.schema.json 1.1 (logged); renderers/anime_renderer.py, renderers/prose_renderer.py (read
  `t`); compiler/passes/mandatory/p07_contact.py (special case removed; docstring)
- tests/test_state_pass.py (new test), tests/test_contact_pass.py (the at-start release test rewritten)
- examples regenerated (the reference fight's kunai line; the wizard's and UGC's envelopes gain `t`)
- F-061 resolved; backlog 15 (RV-08 done, RV-03 depends on it); lesson L-28 (supersedes L-14); CHANGELOG

## Verification
- before: 641 passed at b2ace41 (S-039's gate)
- after: `scripts/verify.sh` exit 0, 642 passed; `make golden` passed; `compiler.rebind` silent
- Prediction 1 held. Prediction 2 held (B -> none at 2.00; no other holder change moved). Prediction 3 held in part:
  only the reference fight's text changed, but the wizard's and UGC's envelopes changed too (each transition's new
  `t`). Prediction 4 held in part: 642 tests, but one existing test changed besides (the at-start release test pinned
  S07's special case).

## Next
RV-03 (the UGC pickup on the table; it depends on this slice).
