# S-073 — RV-85: a camera rule's words ask only what its fields ask, and a rule about a hit is a hit rule

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-85 (PLAN-007); findings F-187, F-160, F-177; rulings O92, R-21, R-30, O102

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-073]

## Plan
S-070 checked each camera rule's fields (its trigger and asks), not its words, which are what the prompt prints, and a
struck rule under a wrong or empty label passed (F-187, review 5). The class: any words a card can put before the
model or the S16 author.
1. A camera-term reader in the grammar's own vocabulary (scales, movements, playbacks) with the common synonyms the
   reviewers used (tight, ECU, detail shot, crash zoom, slow-mo, half speed, bullet time, overcrank, speed up, fast
   motion, push, whip, track, hold): every term a convention's statement or an idiom's prefer uses must be allowed by
   its asks (playback also by the card's list).
2. A rule whose words name a blow, hit, impact or strike, other than "between hits", carries the hit trigger, so
   O92's hold check applies to it whatever its label.
3. R-21 names the checks that enforce it now (CAMERA_CARD, CAMERA_RULES), with a version bump.
Neighbours checked: idioms as well as conventions; the S16 instructions (unchanged, RV-92 teaches the rules).

Predictions, made before the change (06:46 by the clock):
1. The gate passes before the change: 694 tests (cdc5c67).
2. Every current rule passes the words check except the knight's heavy-blow idiom, whose `when` names a blow under a
   heavy_move trigger; as a hit rule its steady low frame becomes a hold on every body present.
3. The reviewers' probes are refused whatever their labels: "Cut close on the receiver after a blow lands.", "Slow
   motion around the peak of every blow.", a crash-zoom ECU rule, a half-speed rule, "Cut to a close-up of the face as
   each blow lands." tagged hit.
4. No prompt text changes (no printed statement changes); no example file changes.
5. 696 tests (two tests added).

## Decisions
- D1 — A rule's printed words are read in the grammar's camera terms and their common synonyms (TERMS), and every term
  must be one its fields allow; playback terms meet the card's own list through the fields. Level: interpretation
  (F-053: the synonym list).
- D2 — A rule whose words name a blow, hit, impact or strike, "between hits" excepted, is a hit rule, so O92's hold
  applies to it whatever its label. Level: interpretation (F-053: the hit words).
- D3 — The check lives where the rules are written and runs when S16 loads a card, before anything is printed; the
  prompt still wants the card's rules word for word (CAMERA_RULES). No prompt-level word list returns: the card check
  is stronger than RV-60's and gates every printed rule. Level: covered (finish.md section 3: no capability weaker).
- D4 — The knight's heavy-blow idiom is a hit rule: "Hold a low, steady frame on both fighters so the armour's weight
  reads; no shaky texture." (version 3). Level: interpretation (R-30: drafts).
- D5 — R-21 names CAMERA_CARD and CAMERA_RULES among its enforcers (rules 7.1, docs log, agent_fix). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the camera cards' check where the cards are loaded (S16, L5.5) |
| Predictions written first | PASS | the session file was written at 06:46, before any code; the probes ran after the check was written |
| New checks fire and stay silent | PASS | on the committed cards only knight_weight_low fails; the five probes are refused; the "between hits" rule passes |
| Neighbours | PASS | idioms as well as conventions; the S16 instructions are RV-92's (unchanged here) |
| Tests changed with their data | PASS | `git diff -- tests`: two tests added |
| Examples | PASS | the live-action example's camera plan re-bound (its knight's idiom moved its packet; hash only) and its envelope; no prompt changed |
| Records | PASS | F-187 resolved, F-160 resolved again, F-177 noted; F-053; library log (knight 3), docs log (rules 7.1); backlog; PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |
Claim corrected before the commit: the knight card was edited before prediction 2 was measured; it was measured
afterwards on the committed cards (`git show HEAD:`), where only knight_weight_low failed.

## Duration
from 06:46 (the plan) to 06:48 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- planner/camera_library.py (TERMS, `terms`, the words and hit-word checks in `rule_problems`)
- library/camera_idioms/knight.yaml 3; docs/rules.yaml 7.1 (R-21)
- tests/test_camera_solver.py (two tests)
- the live-action example's camera plan re-bound and envelope regenerated
- F-187, F-160 resolved; F-177, F-053 noted; backlog (RV-85 done, RV-86 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-072's gate at cdc5c67: 694 passed
- Prediction 1 held. Prediction 2 held (only knight_weight_low on the committed cards). Prediction 3 held (the five
  probes refused). Prediction 4 held in part: no prompt changed, but the live-action example has a knight, so its camera
  plan re-bound. Prediction 5 held (696).
- the gate on this record (06:50:15): `scripts/verify.sh` exit 0, 696 passed in 73.96 s, check: PASS
- the hygiene scan over the staged diff: 0 hits (home paths, emails, keys)
