# HANDOFF — cinematic-compiler (core)

Updated 2026-10-10. This folder (`~/Documents/cinematic-compiler-core`) is the working repo: full git history, no
URCP and no Beads. The old `~/Documents/cinematic-compiler` is superseded and can be deleted once you're happy.
No remote; nothing has been pushed.

## CLI
`cinematic compile "<query>" [--genre G] [--until NODE] [--plans DIR] [--packet-out F] [--chain-from PREV.json]` (exit 3 = an authored step needs
a document, 4 = a gate failed and a replan request was written, 2 = refused); `cinematic validate <envelope>`;
`cinematic graph <envelope> <group>`.

## Resume in three commands
```bash
mise exec -- uv sync --locked
scripts/check.sh
DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore
```

## Built (S01–S17; milestones M1, M1.5, M2, M3, M3.5, M4, M5, M5.5)
| Step | What it compiles | Code |
|---|---|---|
| S01 intent (L0) | query + flags → Intent Document at `/intent`; literal only, evidence per value, `missing`/`ambiguous` | `planner/intent_parser.py`, `compiler/passes/mandatory/p01_intent.py` |
| S02 brief (L0.5) | intent + library cards → `/scene`, entities, props, surfaces; cards only, no model | `planner/query_expander.py` + resolvers, `p02_brief.py` |
| S03 constraint | kernel + world + archetype rules → constraints, constraint_application, `/invariants` | `p03_constraint.py`, `kernel_extraction/control_inventory.py` |
| S04 temporal | authored beat plan (in-session, hash-bound packet) → beats, temporal, beat_constraint, duration | `planner/beat_planner.py`, `planner/dynamic_beat_validator.py`, `p04_temporal.py` |
| S05 causal | beat causes → causal edges (linear) + `scene.quadrant` | `p05_causal.py` |
| S06 state | replay → states per subject per beat + transitions | `solver/prop_state_machine.py`, `validators/continuity_validator.py`, `p06_state.py` |
| S07 contact | contact events, lifecycle, holder/prop-change cross-checks | `p07_contact.py` |
| S08 hand role (L2.5, UGC) | authored interactions: verb, object, hands, grips, role template; roles locked, no swaps, no double-booked hand | `p08_hand_role.py`, `library/grip_types.yaml`, `library/role_templates.yaml` |
| S09 object state (L2.6, UGC) | derived internal card states; every change tied to a hand contact and an interaction | `p09_object_state.py` |
| S10 affordance (L2.7, UGC) | derived proof per verb: pre/postconditions, grip, duration; `enables` edges | `p10_affordance.py`, `library/affordances/` |
| S11 kinematic (L4a) | authored per entity per beat: support + 10 cues; support agrees with S06/S07 | `p11_kinematic.py`, `library/kinematic_cues.yaml` |
| S12 Bartenieff (L4b) | authored coordination: connectivity, pattern, initiation, follow-through, body mode; `cpcs:` labelled | `p12_bartenieff.py`, `library/bartenieff_vocabulary.yaml`, `library/body_modes/` |
| S13 motion (L4c) | authored Euler key poses (root pos = S04, heading = S04 facing, 11 kernel joints, declared turn axes, S06 posture) → derived quaternions, follows edges (Euler delta, slerp vs euler_axis, root trajectory) | `p13_motion.py`, `solver/{euler_solver,quaternion,trajectory}.py` |
| S14 facial (L4d, live_action + ugc_ad) | authored FACS faces per entity per beat: units even or per side (bounded, named patterns), absent units, valence/arousal −1…1, emotion label, display rule, gaze, salience, onset; checks against face profiles (costume occlusion), the body's tension and the libraries; render prints words only | `p14_facial.py`, `validators/facial_validator.py`, `library/facs_*.yaml`, `library/emotion_families.yaml` |
| S15 effort (L5) | authored LMA intervals per entity (Effort factors, effort action checked against weight x time x space, Shape, Space, intensity in the effort mode's range) → overlaps edges | `p14_effort.py`, `library/laban_vocabulary.yaml`, `library/effort_modes/` |
| S16 camera (L5.5) | authored shot list: 13 subdivisions + motivation per shot; geometry derived (camera position, axis side, frame height, screen x); checks: tiling, coverage, motivation refs, 180-line, camera–kinematic coupling, composition, 30° cuts, genre card, subdivision coherence, intent + tempo | `p15_camera.py`, `validators/camera_validator.py`, `solver/camera_geometry.py`, `planner/camera_library.py`, `library/camera_*` |
| S17 render (L6, projection) | authored frame parts (impact, smear on a declared limb/prop only, speedlines, holds, fx, ink) + the full LBN-2.4-ADV-LMA projection of every graph, uncompressed, item-level coverage 100% | `p16_render.py`, `renderers/anime_renderer.py`, `renderers/ugc_renderer.py` |
| M5.5 chaining | `--chain-from PREV.json`: S02 records the previous clip (end states, open contacts, unresolved causes, last shot); S06/S07 start from it; S16 cuts from its last shot | `planner/chaining.py` |

Pipeline: `python -m compiler.pipeline "<query>" [--genre anime] [--until contact] [--plans DIR]`; the genre comes
from the flag or the query's literal parse and decides which steps run; an authored step with no plan exits 3 and
prints (or `--packet-out`) its packet.

Examples (each recompiles byte-for-byte in the gate and has a `render.txt` ready to paste into a video model):
- `examples/wizard_vs_acrobat/` — anime courtyard fight, 13 beats, 11 shots.
- `examples/reference_fight/` — golden: the LBN reference ninja fight compiled from its preface; `render.txt`
  contains all 68 kernel + reference items and A's reference roots exactly.
- `examples/ugc_glasses_demo/` — UGC: a creator unfolds and puts on glasses (faces: a genuine, slightly one-sided
  smile at the reveal); UGC renderer.
- `examples/live_action_standoff/` — live action: wizard vs knight (the knight's glare, the wizard's one-sided
  contemptuous smirk, a suppressed fear micro-expression); live-action renderer.
**The four render.txt files are ready for you to render; Claude never renders.**
Kernel = the 68 controls both LBN-2.3-ADV and LBN-2.4-ADV-LMA state (`kernel/sources/`), scoped per item.

## Reference docs (generated)
[docs/reference/](docs/reference/README.md): the step DAG as a diagram plus every step's inputs, outputs, code, plan
schema, prompt and data files ([dependencies.md](docs/reference/dependencies.md)); every schema field by field
([schemas.md](docs/reference/schemas.md)); every library/kernel data file ([library.md](docs/reference/library.md));
code imports and external packages ([code.md](docs/reference/code.md)). `python -m kernel.build_docs` rewrites them;
the gate fails when they are stale.

## Controls
Three append-only, hash-chained logs (`schemas/schema_log.jsonl`, `library/library_log.jsonl`,
`kernel/kernel_log.jsonl`); generated files checked against regeneration; examples recompile byte-for-byte; reference docs current; 378 tests; all in `scripts/check.sh`.

## Owner decisions so far
Step IDs S01–S18 carry order (renumbered 2026-10-11, F2: S14 = facial) (L labels are names); keys `step_id`/`band`; constraint built after S02 and before
the event graphs; effort (L5) before camera (L5.5); entity definitions at L0.5, state tracks at L2; S01 writes
`/intent`, S02 writes `/scene`; post-generation stays `validation.post_generation`; S02 cards only (no model);
starter cards drafted by Claude; kernel = LBN-2.3 ∩ 2.4; beat plans written in-session (no paid API);
linear causality only; closed kernel state vocabulary. Full log: `docs/layer_dependency.md`, plans in `docs/plans/`.

## Waiting for owner review (draft)
- 20 library cards (archetypes, worlds, objects), all `status: draft` — 11 starters plus the reference-fight set
  (ninja_lean, ninja_broad, five props, bamboo_courtyard_pillar) and ugc_creator.
- `kernel/kernel_scope.yaml`: kernel 20, per-actor 6, per-prop 5, reference fight only 37.
- Draft libraries: `library/kinematic_cues.yaml`, `library/bartenieff_vocabulary.yaml` (developmental patterns are a
  disclosed interpretation; `cpcs:spiral` is a labelled extension), `library/body_modes/` (4 cards), `library/laban_vocabulary.yaml`, `library/effort_modes/` (calm, desperate,
  trained), camera library (`camera_subdivisions`, `camera_grammar`, `camera_tempo`, `camera_conventions/` x3,
  `camera_idioms/` x5), `grip_types`, `role_templates`, `library/affordances/` x4 — all numbers and rules are drafts.
- Reference-fight deviations from its own data (recorded in MASTER_PLAN S16.6): 10.0 hold row has no beat;
  possession tracked on props only; shuriken embed at 5.9; smoke dissipation not a state.
- S13.6 posture cross-check is an agent addition (plan silent). Q6 note: under intrinsic XYZ a flip is pure-X only
  when facing ±Z (see MASTER_PLAN notes); no change made.

## Open questions and next work
M1–M5.5 are built (see **Done** in [docs/plans/MASTER_PLAN.md](docs/plans/MASTER_PLAN.md)).
- **M3.5 face layer is done** (owner decisions F1–F4): renumbered (S14 facial; effort S15, camera S16, render S17,
  post-generation S18), S14 for live_action and ugc_ad, camera face checks, words-only faces in the render.
  Face libraries and face profiles are drafts; the research notes are in `library/facs_asymmetry_bounds.yaml`.
- **M6 needs your definitions before it can be built.** The plan names five tools (`synergy_matrix`,
  `bridge_detector`, `layer_analyzer`, `kernel_compressor`, `ablation_runner`) but never says what each computes, and
  compression/ablation touch B3 (no compression before a target model) and the no-render rule.
- **M7** waits for a chosen and authorised target video model (S18 post-generation, conditioning emitters,
  per-model compression).
- Agent additions to review: S13.6 posture check, S15.5 geometry/composition rules, S04 duplicate-participant
  check, the reference-fight deviations above.
