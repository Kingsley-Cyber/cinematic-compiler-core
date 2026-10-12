# S-057 — RV-48a: releases at their pose, a vanished body untouched, a resting prop moved only at a sample, a first place

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-48 (its S04 part, RV-48a; PLAN-007); findings F-135, F-136, F-138, F-139, F-158, F-165 (the log); rulings O23,
O12, O18, O48, O93, R-18, O102

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-057]

## Plan
Four latent S04 gaps (review 2) and one contradiction (review 3):
1. RELEASE_AT_POSE (F-135, O23): a throw, or a release of a prop or a body, happens at an instant where its actor has a
   key (the start of a beat that lists it); the catch's throw goes back on its pose: b17 runs 6.6-7.0 again and its two
   releases are `at: start` (F-158; the source flashes the throw at 6.6).
2. VANISHED_BODY (F-136): a contact on a vanished body inside its window is refused too, and a touched body must be a
   participant of its beat (BEAT_CONTACT).
3. PROP_KINEMATICS (F-138): a contact strictly between two samples that leaves a resting prop elsewhere is refused; a
   contact that moves it needs a sample at its instant. The substitution's decoy may appear in its new place at the
   substitution's start, where its actor touches it and the substitution changes its state (O12, O48: the log is
   deployed into A's place at the swap): the log gains a sample at 3.7 at A's former place.
4. PROP_FIRST_STATE (F-139): a prop's unknown first location is exempt only while it is held or carried.

Predictions, made before the change (03:26 by the clock):
1. The gate passes before the change: 665 tests (e0a04e7).
2. Before the data change the new rules refuse exactly b17's two releases (RELEASE_AT_POSE, at 6.8) and the log's move
   across 3.7 (PROP_KINEMATICS); the rest of the four examples pass all four.
3. After it the reference prompts print the throw's release at 6.60 and the log "at rest at [0.4, 1, 4.7]" from 3.70;
   A's and B's 6.60 Effort spans run to 7.00 again; no other example's prompts change.
4. The golden's catch test (releases at 6.8) moves with O23 (ADR-O102); four or five break tests are added: about 670
   tests.

## Decisions
- D1 — RELEASE_AT_POSE reads "at its key pose" as an instant where the actor has a key (the start of a beat that lists
  it), not as `at: start` alone: the UGC glasses' release at b03's end lands on the creator's 5.5 key. Level:
  interpretation (listed in F-053).
- D2 — b17 runs 6.6-7.0 again and B throws A on the catch's pose, 6.6, with the catch: the source flashes the throw at
  6.6, and O93's "a grasp plus a throw" fits one pose. Level: covered (O23, O93, the source).
- D3 — The log's swap: a substitution swaps a prop it changes into its new place at its start (a sample at 3.7, A's
  former place); A's hand touch of the log went, since the hand is at the pellet and missed the log by 0.8 m once it
  could be measured; S07 lets a substitution change its decoy without a contact. Level: interpretation (O12, O48;
  F-053).
- D4 — F-138's rule: a contact between two samples moves a resting prop only by taking hold of it (held at the second
  sample); a pickup between samples is a hold, not a jump. Level: interpretation (F-053).
- D5 — The test scene's cup lets go on b03's key pose with its place (`at: start`) and starts on the ground (F-139); the
  state tests' pins and the CONTACT_HAND break follow (the knight joins the beat, F-136). Level: covered (ADR-O102
  with O23 and the new rules).
- D6 — RV-48 split: RV-48a (this slice, RELEASE_AT_POSE) and RV-48b (S08's support hand, the S04 instructions);
  backlog 24. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 670 passed, check: PASS |
| One gap, right layer | PASS | the four rules at S04 (and S06's first place), where the beat plan is first seen; S07's swap exemption |
| Predictions written first | PASS | written 03:26 before any edit; prediction 2 was run on the old data before the fix |
| New checks fire and stay silent | PASS | four break tests pass; every example compiles (the rules refused only b17's releases and the log before the fix) |
| Tests changed with their data | PASS | `git diff -- tests`: the cup fixture (O23, F-139), two state pins, the CONTACT_HAND break (F-136), the golden's catch times (O23); no skip, no deletion |
| Examples | PASS | only the reference fight changed; `compiler.rebind` exit 0; B's 6.60 line prints the catch and the throw, the log rests at [0.4, 1, 4.7] from 3.70 |
| Records | PASS | DEV-29 (the swap) in the registry; RELEASE_AT_POSE on C21 (map 8, kernel log); F-053 lists D1, D3, D4 |
| Hygiene | PASS | the scan before the push |
Claim corrected before the commit: the swap rule first required the actor's hand on the decoy; the measured miss showed the hand belongs to the pellet, so the rule needs none (D3).

## Duration
about 14 minutes by the clock (03:26 to 03:41)

## Changes
- planner/dynamic_beat_validator.py (RELEASE_AT_POSE, VANISHED_BODY, BEAT_CONTACT, PROP_KINEMATICS and `_swapped`);
  validators/continuity_validator.py and compiler/passes/mandatory/p06_state.py (the first place);
  compiler/passes/mandatory/p07_contact.py (the decoy's change)
- examples/reference_fight/plans/temporal.json (b17; the log's 3.7 sample; b09's hand touch of the log removed); the
  reference fight re-bound and regenerated; examples/reference_fight/deviations.yaml (DEV-29)
- tests: test_dynamic_beat_validator.py (three tests), test_state_pass.py (one test, two pins), test_contact_pass.py
  (a break), test_reference_fight_golden.py (the catch's times, the log's swap), scenes.py (the cup)
- kernel/knowledge_map.yaml 8 (kernel log); F-136, F-138, F-139, F-158 resolved; F-135, F-165, F-131, F-053 noted;
  backlog 24 (RV-48a done, RV-48b next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-056's gate at e0a04e7: `scripts/verify.sh` exit 0, 665 passed
- after: `scripts/verify.sh` exit 0, 670 passed, check: PASS
- Prediction 1 held. Prediction 2 held (exactly b17's two releases and the log's move). Prediction 3 held, with a
  consequence not predicted: A's hand touch of the log became a measured 0.8 m miss and went (D3). Prediction 4 held
  in part: 670, but the test scene's cup moved too, with two state pins and one break.

## Next
RV-48b (S08's support hand; the S04 instructions rewritten).
