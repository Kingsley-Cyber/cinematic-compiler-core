# S-030 — M9-06b: CONTACT_WORLD refuses a contact over 0.15 m; repo misses re-blocked, source misses excepted (O83)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-06b (PLAN-003 F5.2); findings F-025, F-070; rulings O24, O72, O83, O84, O85; rule R-33

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-030]

## Plan
F5.2: refuse a touch whose two world points lie farther apart than 0.15 m (O72) at the contact time; the prompt prints
both points. ADR-O83 (owner, 2026-10-11): "re-block the repo-authored misses, keep the source misses as exceptions
(calibrated to the trunk reading), exempt the artifacts, and push."

- S13 checks it, the first step that has the poses (R-10): its packet gains the contacts S07 wrote (touch, possess,
  support), the prop samples S04 wrote and the surfaces' tops; `solver/contact_world.py` measures from the packet and
  the authored keys as well as from an envelope. CONTACT_WORLD refuses a measurable miss over 0.15 m unless its actor
  is airborne or turning or its prop is moving at the instant (an artefact: reported, not refused, O83 point 3) or
  the motion plan lists the contact in `contact_world_exceptions` with its reason (O83 point 2; motion_plan schema
  1.1). An exception that names a contact that is not a refusable miss is refused too, so the list cannot go stale.
- The prompt code CONTACT_WORLD: every touch or hold of a prop or a body that S13 measures prints its two points as
  the envelope has them.
- Data, as R-33 deviations: the repo-authored side of each real miss moves (a pose, a root or a prop sample), never
  the source's A rows; the source's real misses become exceptions in the reference fight's motion plan and the golden
  test.

The real misses after M9-06c (docs/reports/2026-10-11-contact-world-misses-trunk.md) and the planned re-blocks:
1. b06_c4, 3.00, A's left hand holds the rope dart (0.34 m): the source's pose; the rope dart's sample there is the
   repo's, so the sample moves to the hand.
2. b06_c3, 3.00, A's right foot on the ground (1.54 m): the source's RUL against its own words; an exception.
3. b17_c1 and b17_c2, 6.60, B's hands catch A's left elbow (1.02, 0.73 m): B's arms re-posed.
4. b18_c3, 7.50, A's left hand takes the rope dart from the ground (0.89 m): A's row is the repo's (O18); its left
   arm re-posed, its root moved over the ground if the arm cannot reach.
5. b19_c1, 8.00, the dart on B's torso (1.55 m): the sample is the dart's (the prop's weight), which is wrapped on B
   since 7.6, so it moves to B's torso point; A keeps the rope's end.
6. b19_c2, 8.00, A's right hand takes the kunai at [0.6, 0, 4.0] (1.33 m): A's row is the repo's (O18, "runs to the
   kunai and takes it crouched"), so A's root moves to the kunai and the right arm reaches down.
7. b05_c2, 3.60, the acrobat's right foot kicks the wizard's torso (1.20 m): the right leg re-posed to kick high.
8. UGC b01_c1, b02_c1, b03_c1, b03_c2 (0.58, 0.52, 0.70, 0.16 m): the creator's arms re-posed to reach the glasses;
   the glasses at 5.50 sit on the face.
The eight artefact misses (b06_c1, b09_c1, b10_c1, b12_c1, b14_c1, b14_c2, b14_c3, wizard b02_c1) stay as they are.

Predictions, made before the change:
1. The gate passes before the change: 631 tests.
2. With the check on and no data changed, S13 refuses CONTACT_WORLD on 12 contacts: 7 in the reference fight, 1 in
   the wizard, 4 in the UGC demo, none in the live-action standoff.
3. After the re-blocks and the one exception, every example compiles; the miss list holds 1 excepted miss, 8
   artefacts and no refusable miss; within 0.15 m rises from 13 to about 23.
4. Re-posing changes some arm and leg words on the re-blocked keys (recorded as R-33 deviations); moving A's 8.00 root
   may make S04 or S16 refuse (uncertain), which would need a further re-block.
5. The prompt code fires on its break (a printed point removed) and on none of the 20 prompts; no checklist row
   changes result unless CONTACT_WORLD joins a row's codes (then that row's evidence changes, not its result).
6. About 637 tests.

## Decisions
- D1 — CONTACT_WORLD runs at S13 from its sealed packet, which gains the contacts S07 wrote (touch, possess, support),
  the prop samples S04 wrote and the surfaces' tops (`contact_world.packet_view`). Why: R-10 (S13 first has the
  poses), R-04 (an authored step is checked from its packet), plan F5.2 ("S13 check"). Level: covered.
- D2 — The exceptions live in the motion plan (`contact_world_exceptions`, contact id to reason; motion_plan schema
  1.1, logged), the golden test pins the set, and an exception naming anything but a real miss is refused. Why: O83
  point 2 needs the check to know them, and the S13 plan is where poses are authored. Alternatives: a list in the
  compiler (example data in code), a provenance flag on each key. Level: covered (O83); the place and the stale rule
  are interpretations (F-053).
- D3 — Artefacts (the actor airborne or turning, the prop moving) are not refused; the report's new CONTACT_WORLD
  column says "artefact: reported". Why: O83 point 3 (S-027's flags). Level: covered.
- D4 — The prompt code checks that both points are printed on the actor's staff line; the distance is S13's alone.
  Why: F5.2 ("the prompt must print both points"); the exceptions are in the plan, not the envelope. Level: covered.
- D5 — Rows C21 and C12 (the plan's section 6); the locators name `contact_world.refusals` and a prompt test that
  names the code (L-18). Level: covered.
- D6 — Each re-block is the least change of the repo-authored joints, and of the root over the ground with both soles
  kept on it where an arm could not reach, that brings the point within 0.06 m inside the genre's joint limits; found
  by a scratch optimiser that mirrors the forward kinematics, then measured by the repo's own at compile. Level:
  interpretation (F-053).
- D7 — The re-blocks: B at 6.6 steps 0.66 m toward A and straightens (pelvis 1.07 to 1.20) to take A's elbow with
  both hands overhead; A at 7.5 moves 0.31 m over the rope dart and crouches deeper (0.86 to 0.57), left arm down; A
  at 8.0 moves to the kunai (0.31 m in x, -0.87 m in z), crouches (0.81 to 0.59) and bends 85 degrees, right arm down;
  the acrobat at 3.6 kicks high (right hip -87, knee straight); the UGC creator's arms at 1.5, 3.5 and 5.5. Why: O83
  point 1, R-33. Level: covered.
- D8 — The samples: the rope dart at 3.0 in A's left hand (the source's pose kept); the rope dart at 8.0 on B's torso
  (the sample is the dart, the prop's weight, wrapped on B since 7.6; A keeps the rope's end, 1.82 m away, inside the
  2 m reach); the glasses at 5.5 and 8.0 on the face, 0.1 m in front of the head's centre (a resting prop keeps its
  place). Why: O83, R-33. Level: covered; the placements are interpretations (F-053).
- D9 — One source exception, b06_c3 (3.0, A's right foot 1.54 m over the ground: the source's RUL against its own
  words). b06_c4 (A's left hand on the rope dart at 3.0) is met by moving the repo's sample, not excepted. Why: O83
  ("re-block the repo-authored misses, keep the source misses as exceptions"): the miss's repo side moves, the
  source stays. Level: covered.
- D10 — F-071 (new): A's crouch at the kunai (z 4.23) puts B between A and the pillar, so the source's "A pulls B
  toward the pillar" at 8.0 now pulls away from it; the owner's call. Why: AGENTS.md section 12 (anything found and
  not fixed is a finding). Level: the owner's call (finding).
- D11 — Commit and push: the owner's "Then proceed with M9-06b ... and push". Level: covered.

The words and roots the re-blocks changed (R-33 deviations):

| Example | Key | Part | Before | Now |
|---|---|---|---|---|
| reference_fight | ninja_broad@b17 | left arm | forward-mid | forward-high |
| reference_fight | ninja_broad@b17 | left leg | forward-mid | forward-low |
| reference_fight | ninja_broad@b17 | left lower arm | folded 60 | folded 45 |
| reference_fight | ninja_broad@b17 | left lower leg | folded 45 | folded 30 |
| reference_fight | ninja_broad@b17 | right lower arm | folded 60 | folded 45 |
| reference_fight | ninja_broad@b17 | right lower leg | folded 30 | straight |
| reference_fight | ninja_broad@b17 | body | forward-high (15 lean) | None |
| reference_fight | ninja_broad@b17 | root | [-0.4, 1.07, 4.5] | [0.13, 1.2, 4.87] |
| reference_fight | ninja_lean@b19 | left arm | forward-low | forward-mid |
| reference_fight | ninja_lean@b19 | left lower arm | straight | folded 30 |
| reference_fight | ninja_lean@b19 | left lower leg | folded 90 | folded 105 |
| reference_fight | ninja_lean@b19 | right lower leg | folded 90 | folded 105 |
| reference_fight | ninja_lean@b19 | body | forward-mid (75 lean) | forward-mid (85 lean) |
| reference_fight | ninja_lean@b19 | root | [-0.1, 0.86, 3.2] | [-0.07, 0.57, 3.51] |
| reference_fight | ninja_lean@b20 | left lower leg | folded 75 | folded 90 |
| reference_fight | ninja_lean@b20 | right arm | forward-low | forward-mid |
| reference_fight | ninja_lean@b20 | right lower arm | straight | folded 30 |
| reference_fight | ninja_lean@b20 | right lower leg | folded 75 | folded 105 |
| reference_fight | ninja_lean@b20 | body | right-forward-mid (50 lean) | forward-mid (85 lean) |
| reference_fight | ninja_lean@b20 | root | [-0.2, 0.81, 5.1] | [0.11, 0.59, 4.23] |
| wizard_vs_acrobat | acrobat@b06 | right leg | right-forward-low | forward-mid |
| wizard_vs_acrobat | acrobat@b06 | right lower leg | folded 15 | straight |
| ugc_glasses_demo | ugc_creator@b02 | right lower arm | folded 90 | folded 75 |
| ugc_glasses_demo | ugc_creator@b03 | left arm | left-forward-mid | place-low |
| ugc_glasses_demo | ugc_creator@b03 | left lower arm | folded 120 | folded 105 |
| ugc_glasses_demo | ugc_creator@b04 | left arm | left-forward-low | forward-mid |
| ugc_glasses_demo | ugc_creator@b04 | left lower arm | folded 45 | folded 120 |

## Duration
about 120 minutes

## Changes
- `solver/contact_world.py` (`packet_view`, `measure_plan`, `artefact`, `refusals`; one measuring core),
  `compiler/passes/derived/p13_motion.py` (the packet's contact view, CONTACT_WORLD), `schemas/graphs/motion_plan.schema.json`
  1.1 (`contact_world_exceptions`; schema log), `validators/prompt_validator.py` (CONTACT_WORLD, `_world_checks`),
  `validators/contact_world_report.py` (the CONTACT_WORLD column, header)
- `kernel/knowledge_map.yaml` (C21, C12; kernel log), checklists regenerated
- plans: reference fight (B@b17, A@b19, A@b20 re-blocked; the rope dart's samples at 3.0 and 8.0; the exception),
  wizard (acrobat@b06), UGC (ugc_creator@b02, @b03, @b04; the glasses' samples at 5.5 and 8.0); re-bound; outputs
- tests: `test_motion_solver.py` (two breaks, the exception and artefact test), `test_dag_conformance.py` (a break; the
  AIRBORNE_PICKUP break's search text follows A's new support words), `test_forward_kinematics.py` (the pickup meets,
  every example passes, the prompt prints both points), `test_reference_fight_golden.py` (A's pickups, the re-blocked
  samples, the catch, the exception), `test_leg_frame_rewrites.py` (two keys re-posed again), `test_prop_track.py`
  (the glasses on the face)
- `docs/reports/2026-10-11-contact-world-after-m9-06b.md`; F-070 resolved; F-025 noted; F-071 (new); F-053; backlog
  (M9-06b done, M9-10 next); CHANGELOG; lesson L-24

## Verification
- before: `scripts/verify.sh` exit 0, 631 passed (S-029, 2085d5c)
- after: `scripts/verify.sh` exit 0, 639 passed (the first runs failed on a KeyError when the MOTION_JOINTS break
  removed a joint, lesson L-24; on two map locators that named a function without the code and a generic test, L-18;
  and on pins of data this slice moved on purpose, each updated with its reason); `make golden`: the reference
  fight's, the wizard's and the UGC demo's outputs changed on purpose (the re-blocks, the printed points); the live
  action standoff's only by its checklist
- Prediction 1 held. Prediction 2 held for the reference fight (7 refusals, the ones listed); the wizard's 1 and the
  UGC demo's 4 were measured, not seen refused (the rebind stops at the first refusing example). Prediction 3 held: 24
  of 33 meet (about 23 predicted), one exception, eight artefacts, no refusable miss. Prediction 4 held: 27 words and
  roots changed on the seven keys; nothing refused at S04 or S16. Prediction 5 failed on the checklist: CONTACT_WORLD
  on C12 moved that row from NOT CHECKED to FAIL on the four LBN prompts (LBN-2.4 prints no world points, as with the
  other prose-only codes); the break fires, no prose prompt fires it, and on the prose prompts C12 stays NOT CHECKED
  (renders F5 and F15). Prediction 6 held: 639.

## Next
M9-10 (F4.3/F4.4 B's active keys and the idle-fighter check).
