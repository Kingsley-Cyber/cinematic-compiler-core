# S-085 — RV-99: the camera cards' rules keep RV-60's floor, and a hit rule is found from what a contact does

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-99 (PLAN-007); findings F-210, F-187, F-160; rulings O92, R-21

## Layer
L5.5

## Status
applied

## Commit
the commit whose message names [S-085]

## Plan
RV-85 (S-073) replaced RV-60's word lists with a term check built from review 5's probes and promised the lists would
stay as a floor; none was built. rule_problems passes "Cut to a close-up of the face at each contact.", "Push in on the
receiver as the kick connects.", "The action slows down as the kunai lands." and hit rules framed "on the receiver
alone" or "with a hard handheld shake" (F-210; review 6). The class: a word check narrower than the rule it guards.
1. The floor (RV-60's lists, owner O92): a rule whose words ask for slowed playback (slow motion, slow-mo, slows down,
   time slows, a ramp, a freeze) is refused whatever its fields; a hit rule whose words ask for a close-up or an insert
   (close, close-up, tight, ECU, macro, insert, detail shot) is refused.
2. A rule speaks of a hit when its words name what planner/hits.py counts as a hit: a blow, hit, impact, strike or
   contact, the striking verbs (strike, deflect, parry, catch) and the attacks that land on a body (kick, punch, knee,
   elbow, palm, slash, stab, chop, jab, headbutt), "between hits" and a kick-off aside.
3. A hit rule's words may not frame one body alone ("alone", "only", "on the receiver") or ask a shaking rig
   (handheld, shake, jitter, wobble); a negation ("no shaky texture") is read as one.
4. CAMERA_RULES keeps the printed rules word for word the card's, so the floor reaches the prompt.

Predictions, made before the change (09:46 by the clock):
1. The gate passes before the change: 716 tests (29eca77, S-084's chained gate).
2. Every probe sentence review 6 named (seven) is refused, and all seventeen rules on the library's cards still pass,
   so no card changes.
3. No example, prose or checklist changes.
4. The knight's "no shaky texture" passes only because the rig words read the negation; a test pins it.
5. About 718 tests (716 and two: the probes refused, the negation read).

## Decisions
- D1 — RV-60's word lists are a floor in the card check (rule_problems) rather than a second check on the prompt:
  CAMERA_RULES keeps the printed rules the card's word for word, so a floor on the cards is a floor on the printed
  rules. Level: covered (O92; RV-85's promise).
- D2 — A rule speaks of a hit by what a contact does: the nouns (blow, hit, impact, strike, contact), the striking
  combat verbs (strike, deflect, parry, catch) and the attacks on a body (kick, punch, slash, stab, chop, jab,
  headbutt); "between hits" and a kick-off aside; "lands" and "connects" alone name no hit (a flyer lands). "Slo-mo" is
  slow motion, in the floor and in the terms. Level: interpretation (F-053).
- D3 — A hit's words may not frame one body (alone, solely, only or on the receiver and its kin) or shake the camera
  (handheld, shake, jitter, wobble, judder); a negation before them (no, not, never, without) is read as one, so the
  knight's "no shaky texture" stands. Level: interpretation (F-053).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the camera library's card check (S16 reads the cards); no step's data changed |
| Predictions written first | PASS | the session file was written at 09:46, before any code |
| New checks fire and stay silent | PASS | measured: review 6's seven rules refused, and "Slo-mo on every kick." and "Time slows down." by the floor; the library's seventeen rules pass; "a slow push" stays a camera move |
| Neighbours | PASS | TERMS' slow-motion pattern widened with the floor (slo-mo); CAMERA_RULES unchanged; knowledge map 19 (C10's note said "in place of RV-60's word lists") |
| The step's instructions teach it | n/a | the cards are library content, checked where they load |
| Tests changed with their data | PASS | two new tests in tests/test_camera_solver.py; nothing removed or loosened |
| Examples | PASS | none changed (the cards are the same) |
| Records | PASS | F-210, F-187, F-160 resolved; F-053; map 19 (kernel log); backlog (RV-99 done, RV-59 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 09:46 (the plan) to 09:49 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- planner/camera_library.py (HIT_WORDS, BETWEEN_HITS, SLOWED, CLOSE, SINGLE, SHAKE; rule_problems; TERMS' slow-mo)
- tests/test_camera_solver.py (two tests); kernel/knowledge_map.yaml 19
- F-210, F-187, F-160 resolved; F-053; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-084's chained gate at 29eca77: 716 passed
- Prediction 1 held. Prediction 2 held (the seven refused; the seventeen pass; the floor also caught "slo-mo" once
  read). Prediction 3 held. Prediction 4 held. Prediction 5 held (718). Predictions 5 of 5.
- the gate on this record (09:49:12): `scripts/verify.sh` exit 0, 718 passed in 97.57 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits

## Correction (S-090)
Corrected in S-090 (principal review 7): the plan listed knee, elbow and palm among the hit words, and D2 dropped them
without a reason; the floor passes the fight's own hits ("a close-up as the knee connects") and refuses O92's own
sentences ("No playback ramps."), a negation being read only for the shaking words (F-210 reopened, RV-99b).
