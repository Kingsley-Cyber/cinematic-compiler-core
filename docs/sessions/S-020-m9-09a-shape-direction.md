# S-020 — M9-09a: SHAPE_DIRECTION refuses a Shape quality the body contradicts (F9.1; O31, O73, O76)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09a (PLAN-003 F9.1); findings F-068, F-029; rulings O31, O73, O76, O75 (R-33)

## Layer
L5

## Status
applied

## Commit
the commit whose message names [S-020]

## Plan
The owner ruled (O73): refuse contradictions only, rewrite the twelve, leave the twenty-four that show neither until
M9-10; and (O76): an airborne, rotating body is not judged, the lean is the spine's relative to the root, a
whole-body check reads the whole body, and every single-joint read is audited. `solver/shape_direction.py` holds the
measure; S15 refuses a contradicted interval (its packet now carries each key's position and bones), and the prompt
code SHAPE_DIRECTION reads the printed Shape against the envelope.

Predictions, made before the change:
1. With airborne turns skipped, the three flight artefacts among the twelve (A 1.10-2.00, A's backflip 5.10-5.90,
   the acrobat's dodge flip) pass and nine contradictions remain.
2. After rewriting the nine, every example compiles; S15's packet change re-seals the four effort plans only.
3. The sixteen prose prompts and four render.txt change where a quality was rewritten; no prompt code fires.
4. No checklist row changes result (LMA and T6 gain a code; they stay as they are).

## Decisions
- D1 — Rewrite nine, not twelve. Why: under O76's flight rule the other three are flights the check does not judge;
  rewriting them would change correct data. Alternatives: the owner's twelve literally. Level: covered (O73 with
  O76).
- D2 — Each rewrite names the quality the body shows, the declared one's opposite: knight 2.50 advancing; B 2.50,
  B 5.90, A 5.90 rising; B 6.60 and the acrobat 2.60 spreading; A 7.00 and the UGC creator 0.00 retreating; B 7.50
  advancing. Why: R-33 (a slice rewrites the examples for its own check), O73. Level: covered.
- D3 — The measure (thresholds 0.1 m, 15 and 10 degrees, 0.15 spread; a span ends at the actor's next key; an
  interval with no next key and one key is not judged). Why: ADR-O73's proposal, accepted; R-34 (root position and
  rotation, support, spine, arms, knees). Level: interpretation (Claude's, for owner review; F-053).
- D4 — The single-joint audit (the owner's O76): see the table below; one defect, `head_heading`, becomes backlog
  M9-09g (it changes S14's and S16's numbers in every example). Level: covered (O76).

### The single-joint audit (O76, R-34)

| Read | Where | Verdict |
|---|---|---|
| The face's heading: root yaw + NK yaw + HD yaw | `solver/quaternion.head_heading` (S14 facial, S16 camera) | defect: skips the spine (Sp yaw) and reads a lying body's heading from yaws; composed through root, Sp, NK and HD it moves over 5 degrees on 28 of 73 keys, over 20 on 11; M9-09g |
| Posture from the root's up and forward axes | `solver/euler_solver.posture_problem` (MOTION_POSTURE) | by design: posture is the pelvis's (its "chest" is the root's forward axis) |
| The trunk's lean: root and Sp | `solver/staff_geometry.body_word` | whole chain |
| The head against the chest: NK, HD | `staff_geometry.head_word` | by design (relative to the chest) |
| A limb's direction from its upper joint, a fold from its lower joint | `staff_geometry.pose_words` | by design (Laban gestures read relative to the body) |
| The knees' fold for the support level | `prose_renderer` staff lines | by design (one word per side) |
| Joint limits per joint (NK and HD summed) | `euler_solver.limit_findings` | by design (a joint's own range) |
| The Euler numbers of every joint | `prompt_validator` | every joint |
| The root's uprightness for an inversion | `euler_solver._inversion_findings` | by design (the body is inverted when the pelvis is) |
| The root's height on a top | `dynamic_beat_validator._surface_heights` | by design (a range on the root until forward kinematics, M9-06) |
| Shape: root position and rotation, support, Sp, LA, RA, LL, RL | `solver/shape_direction` | whole body (R-34) |

## Duration
about 60 minutes

## Changes
- `solver/shape_direction.py` (new); `compiler/passes/derived/p15_effort.py` (SHAPE_DIRECTION; the packet keeps each
  key's position and bones); `validators/prompt_validator.py` (SHAPE_DIRECTION, `_shape_checks`)
- `examples/*/plans/effort.json`: nine Shape qualities; every effort plan re-bound; outputs and checklists regenerated
- tests: a break and two tests (test_effort_solver), a prompt break (test_dag_conformance), SHAPE_REWRITES (golden)
- `kernel/knowledge_map.yaml` LMA, T6 (kernel log); F-068 resolved; F-053; backlog (M9-09a done, M9-09g added);
  CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 609 passed (S-019, 60af33d)
- after: `scripts/verify.sh` exit 0, 614 passed (the first run failed on one line over 130 characters in a break)
- Prediction 1 held (the three flights pass; nine remain). Prediction 2 held (the four effort plans re-bound, no
  refusal). Prediction 3 held (twenty outputs, no prompt finding). Prediction 4 held (no row changed result).
- Found while building: a quality outside the vocabulary crashed the judge before EFFORT_VOCABULARY reported it (a
  break test); the judge now runs only on known qualities.

## Next
M9-09b (MOMENTUM_MISSING with anime hang time, O74).
