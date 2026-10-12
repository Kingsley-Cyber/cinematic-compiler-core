# S-051 — RV-10: the kunai drive holds the kunai in B's shoulder; the catch is a grasp plus a throw (O93)

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-10 (PLAN-007); findings F-084, F-092, F-148; rulings O93, O22, O23, R-17, R-33, O102

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-051]

## Plan
O93 (owner): "Kunai drive holds the kunai in B's shoulder. The catch is a grasp plus a throw." The source: "8.5 A DRIVES
kunai into B right shoulder ... kunai STAYS in B shoulder", "kunai stays in B shoulder NOT released", "10 kunai
embedded in B right shoulder", "6.6 B catches A left elbow with both hands, B uses momentum to throw A toward pillar".
Today both print as instant strikes by B ("B after the 6.60 strike", "B after the 8.50 strike"), B's torso touches the
kunai at 8.5, and the kunai floats 1.2 m above the downed B from 9.0 (F-084).
1. 8.5: B's torso takes and keeps the kunai's blade (a possess at the beat's start, never released: the blade lodged in
   the shoulder, the torso point standing for the shoulder, which has no part of its own), while A's right hand keeps
   the handle (A's hold since 8.0); the kunai is embedded from 8.5 (`at: start`); its samples sit at B's torso point
   at 8.5, 9.0 and on to the end. (Changed during the slice: see D2.)
2. 6.6: B's hands take A's left arm (possess, verb catch) at 6.6 and let go at 6.8 (release, verb throw): b17 runs
   6.6-6.8, so the throw sends A on toward the pillar it reaches at 7.0.
3. A possess by a part that is not a hand prints "held in" (the blade in the shoulder); IMPACT_CONTACT_SYNC counts a
   possess that starts on an impact frame (a catch, a blade lodging); CONTACT_VERB lets a catch and a throw name a body
   (the owner's words), a disarm still a prop.

Predictions, made before the change:
1. The gate passes before the change: 660 tests (753ebff).
2. After it the reference prompts print no "B after the 6.60 strike" or "B after the 8.50 strike"; the kunai's track
   prints "8.50 held in B torso" and RULES "From 8.50 to the end, kunai stays embedded".
3. Without the two rule changes, IMPACT_CONTACT_SYNC refuses 6.6 and 8.5 (no touch there) and CONTACT_VERB refuses a
   catch and a throw of a body.
4. The kunai's 9.0 sample moves from [1.0, 1.3, 5.2] to B's torso point (y about 0.1 to 0.2); the 8.5 possess meets
   CONTACT_WORLD as the touch did (about 0.1 m).
5. Shortening b17 moves the reference fight's later packets (all re-bound); S11, S12 or S15 may refuse B's shorter 6.6
   slot (uncertain); test_prose_render's "From 9.00 ... kunai stays embedded" moves to 8.50 with O93 (ADR-O102).
6. A's right hand stays 0.5 to 0.7 m above B's shoulder at 9.0-10 under the source's own arm numbers: F-148's open
   question, not changed here.

## Decisions
- D1 — The catch: B's hands take A's left arm at 6.6 (possess, verb catch) and let go at 6.8 (release, verb throw);
  b17 runs 6.6-6.8, since a contact sits at its beat's start or end and at 7.0 A is already at the pillar. Level:
  covered (O93, the source's 6.6 row).
- D2 — The lodged kunai: a possess of the blade by B's torso replaced A's open hold in S04's `holds()`, which keeps one
  holder per prop, and so dropped A as the holder from 8.0 (PROP_KINEMATICS refused the pickup's move); the blade's
  meeting with B's shoulder stays a touch at 8.5, the kunai is embedded from 8.5 (`at: start`), its samples sit at B's
  torso point at 8.5, 9.0, 9.5 and 10.0, and A keeps it to the end. Recorded as evidence on F-092 for RV-17. Level:
  covered (O93; the shoulder is the torso point, as part_point reads it).
- D3 — A body that meets a blade another performer holds is struck by it, not striking with it: a touch on any held
  prop is no strike (renderers/prose_renderer.py `strike_contacts`), so B's 8.5 line prints a contact bow, not a
  DOUBLE BOW. Level: covered (O93: neither prints as an instant strike).
- D4 — IMPACT_CONTACT_SYNC counts a possess that starts on an impact frame, at S17 and in the prompt (a catch's
  "[contact: ... retained]" bow). Level: covered (O23's one time per hit; O93).
- D5 — CONTACT_VERB lets a catch and a throw name a body (never a surface); a disarm still names a prop; the combat
  verbs card says so (version 2, draft). Level: covered (O93 and the source: "B catches A left elbow", "throw A").
- D6 — Records moved with O93 (ADR-O102): the golden's CONTACT_VERBS (b17's catch and throw), the strike set and the
  embedded rule's time in tests/test_prose_render.py; one test added for the drive and the catch. Level: covered.
- D7 — The kunai's WHERE line still reads "8.00-10.00 held by A R hand": true, but it does not say the blade is in B;
  one possession model (RV-17, F-092) is where a prop held by a hand and lodged in a body can be written as both.
  Level: covered (named with its slice).

## Duration
about 1 hour

## Changes
- examples/reference_fight/plans/temporal.json (b17: 6.6-6.8, catch and throw; b21: the kunai embedded at 8.5; the
  kunai's samples at 8.5 to 10.0 on B's torso point); the reference fight re-bound; outputs and checklists regenerated
- planner/dynamic_beat_validator.py (CONTACT_VERB), compiler/passes/derived/p17_render.py and
  validators/prompt_validator.py (IMPACT_CONTACT_SYNC), renderers/prose_renderer.py (`strike_contacts`);
  library/combat_verbs.yaml 2 (library log)
- tests/test_reference_fight_golden.py (CONTACT_VERBS, a test), tests/test_prose_render.py (two pins)
- F-084 resolved; F-092 and F-148 noted; backlog (RV-10 done, RV-11 next); PLAN-007; CHANGELOG; run report

## Verification
- before: S-050's gate at 753ebff: `scripts/verify.sh` exit 0, 660 passed
- after: `scripts/verify.sh` exit 0, 661 passed, check: PASS; `make golden` passed
- Prediction 1 held. Prediction 2 held in part: no instant-strike line at 6.6 or 8.5 and "From 8.50 to the end, kunai
  stays embedded", but the track prints "8.50 touched by B torso", not "held in" (D2). Prediction 3 held in part: the
  prompt's IMPACT_CONTACT_SYNC refused 6.60 until a catch's bow counted, and CONTACT_VERB's text refuses a caught body;
  8.5 kept its touch, so nothing refused it there. Prediction 4 held in part: the 9.0 sample is at [1.36, 0.1, 5.48];
  the 8.5 contact meets at 0 m (the sample is at the torso point) and stays a touch. Prediction 5 held, with two pins
  not predicted (the golden's verbs, the strike set). Prediction 6 held (0.65 m at 8.5).

## Next
RV-11 (compile refuses non-deliverables, O94).
