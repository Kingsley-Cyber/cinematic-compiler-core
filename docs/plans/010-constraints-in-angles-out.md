# PLAN-010 — Constraints in, angles out: the model declares what each limb does, a CPU solver computes the pose

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
owner

## Created
2026-10-13

## Updated
2026-10-13

## Intent
Stop paying for impossible briefs and for joint angles. Today S13's model writes every joint angle of every key (11
joints x 3 numbers), the checks reject what does not land, and the solver patches it: 80-90 % of a run's time and cost,
and the two R20-idea runs (2026-10-13) died there, the second on a brief no pose could meet (the ninja's right foot
striking the knight and standing on the floor at 2.5 s). After this plan: S04 declares each limb's one job at each
instant and refuses a contradiction before any pose is written; the S13 model writes intent (targets, roles and the
Laban direction words for the free limbs), never angles; a CPU inverse-kinematics solver computes the angles, so
contacts land by construction. Everything runs on the Mac's CPU: no GPU, no GPU model (owner, 2026-10-13).

## Targets (measured on the R20 idea, "6 seconds anime fight scene: ninja versus knight in a moonlit bamboo courtyard")
| Measure | Now (two runs) | Target |
|---|---|---|
| Run reaches a prompt | 0 of 2 | yes, first run |
| S13 time per attempt | 52-492 s | under 60 s |
| S13 refusals per run | 3 (all attempts) | at most 1 |
| Whole run | 12-27 min, no prompt | under 8 min |
| List cost | $4.54-5.30 | under $2 |
| Gate per commit | 4.5-5 min | about 1 min |

## Phase 0 — Enablers (about 15 min; one commit; done S-132)
1. pytest-xdist: the gate runs on six of the ten cores (owner; `-n 6` in pyproject.toml): 4.5 min to 1.5 min.
2. The owner's standing approval (2026-10-13), recorded in docs/rules.yaml: an approved plan runs to its end; it
   stops only on a failed gate, a new decision, or a bug that changes the plan.

## Phase 1 — No impossible brief reaches S13 (about 45 min; two commits)
3. ONE_PART_ONE_JOB (R20 next action 3). S04's beat plan gains `roles`: for each performer, each limb that has a job
   in the beat: `{limb, role: support | strike | block | carry, target, at}` (a limb with no entry is free). Declared,
   not inferred (owner). S04 refuses a limb with two roles at one instant, counting the roles still open from earlier
   beats (a support stays until its release).
4. CONSTRAINT_SATISFIABLE (S04). A beat's roles must be meetable before any pose exists:
   - roles and contacts agree (every strike, support and carry has its contact, and the reverse);
   - a strike's target lies within the striker's reach from its anchor (the limb's length plus the trunk's, from
     library/body_segments.yaml), else S04 moves the bodies (AA-10's rule, moved earlier);
   - a support stands on a surface the body is over (S-122's boxes);
   - one body's two targets at one instant lie within its span.
   A refusal is an S04 retry: one Opus call on the beat plan, not three S13 attempts.

## Phase 2 — The model writes intent, the solver writes angles (about 2-3 h; four commits)
5. The pose solver: mink (Apache-2.0, CPU, MuJoCo's kinematics; github.com/kevinzakka/mink), behind
   solver/pose_solver.py. A MuJoCo model of the 11-joint skeleton is generated from library/body_segments.yaml (the
   genre's lengths, the capsules' radii, library/joint_limits.yaml). Tasks per key: each role's limb on its target
   (hard), each support's sole on its surface (hard), the root on its S04 anchor (hard), the free limbs toward their
   intent directions (soft), joint limits, no body through another (collision pairs). Fallback if mink does not fit:
   solver/reblock.py `solve_key`, already the repo's (no new dependency).
6. Intent words to angles: each Laban direction and level ("L arm forward-high", "lower arm folded 45") maps to a
   target direction for its limb, the inverse of solver/staff_geometry.py `pose_words`; a test round-trips every word.
7. S13's plan schema (motion_plan 3.0): per key, the pose's name and description, the turn and axis, and the intent
   words for each limb with no role; no `bones`. S13 builds each key by solving it; every existing S13 check runs on
   the solved key unchanged (they read the resulting pose).
8. The four examples migrate: their intent words are read from their current angles (`pose_words`), their keys
   re-solved; their prompts change where the solved pose differs. The reference fight's source poses stay authored
   (ADR-O83, O118): a key may still carry `bones` when the owner's source gives them (an escape hatch, the source only).

## Phase 3 — Prove it (about 15 min; one run)
9. Re-run the R20 idea. Report: the prompt with every line marked by the step that wrote it, the time and cost of each
   step against the targets above, and what the checks still flag. The owner renders it and judges by eye.

## Later (triaged from the owner's items 6-25; none blocks Phases 0-3)
- Next: an author budget (a run stops at a set cost or time), per-step retry budgets, structured refusals (each
  finding names its step and field), cost tracking per run in the report, a run diff (two runs' prompts side by side).
- After: AA-6 casting every hint (R20 next action 7), the lesson log (each render's verdict to a rule), one vocabulary.
- Owner rulings first: auto-render (spends render credits), reference verification, sound, environment state,
  character state, style cache, prompt compression (ADR-O111 removed the length cap; compression would reverse it).
- Dropped: OmniControl and InterGen (they need a GPU; owner, 2026-10-13).

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| An impossible brief reaches S13 | S04 | critical | open | 3, 4 |
| The model writes joint angles | S13 | high | open | 5-8 |
| The gate takes 5 min | gate | medium | open | 1 |

## Dependencies
- S-130, S-131 (the solver's surface skin and its retry fix).

## Owner Rulings Needed
- Roles declared at S04 (owner's words) also mean contacts are written twice (roles and contacts); CONSTRAINT_SATISFIABLE
  keeps them equal. The alternative, roles derived from contacts, writes once. Default here: declared, as ruled.
- The examples' prompts change in Phase 2 (solved poses); the reference fight keeps its source poses.

## Critical Path
1. Phase 0 (enablers) -> 2. Phase 1 (ONE_PART_ONE_JOB, CONSTRAINT_SATISFIABLE) -> 3. re-run the R20 idea once (a prompt
   should come out now, angles still the model's) -> 4. Phase 2 (pose solver, intent words, motion_plan 3.0, the
   examples) -> 5. Phase 3 (re-run, report).

## Verification
- `scripts/verify.sh` (all cores); each check planted in its own test; the R20 idea's run report against the targets.

## Changelog
- 2026-10-13 — Owner: go; six workers; the times are an agent's, not a person's (3.5-4.5 h in all).
- 2026-10-13 — Created from the R20 idea's two failed runs, the owner's five critical items and items 6-25, and the
  owner's "no GPU".
