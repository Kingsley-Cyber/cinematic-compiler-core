# HANDOFF — cinematic-compiler (core)

Updated 2026-10-10. This folder (`~/Documents/cinematic-compiler-core`) is the working repo: full git history, no
URCP and no Beads. The old `~/Documents/cinematic-compiler` is superseded and can be deleted once you're happy.
No remote; nothing has been pushed.

## CLI
`cinematic compile "<query>" [--genre G] [--until NODE] [--plans DIR] [--packet-out F]` (exit 3 = an authored step needs
a document, 4 = a gate failed and a replan request was written, 2 = refused); `cinematic validate <envelope>`;
`cinematic graph <envelope> <group>`.

## Resume in three commands
```bash
mise exec -- uv sync --locked
scripts/check.sh
DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore
```

## Built (S01–S07, S11–S16; milestones M1, M1.5, M2, M3, M4)
| Step | What it compiles | Code |
|---|---|---|
| S01 intent (L0) | query + flags → Intent Document at `/intent`; literal only, evidence per value, `missing`/`ambiguous` | `planner/intent_parser.py`, `compiler/passes/mandatory/p01_intent.py` |
| S02 brief (L0.5) | intent + library cards → `/scene`, entities, props, surfaces; cards only, no model | `planner/query_expander.py` + resolvers, `p02_brief.py` |
| S03 constraint | kernel + world + archetype rules → constraints, constraint_application, `/invariants` | `p03_constraint.py`, `kernel_extraction/control_inventory.py` |
| S04 temporal | authored beat plan (in-session, hash-bound packet) → beats, temporal, beat_constraint, duration | `planner/beat_planner.py`, `planner/dynamic_beat_validator.py`, `p04_temporal.py` |
| S05 causal | beat causes → causal edges (linear) + `scene.quadrant` | `p05_causal.py` |
| S06 state | replay → states per subject per beat + transitions | `solver/prop_state_machine.py`, `validators/continuity_validator.py`, `p06_state.py` |
| S07 contact | contact events, lifecycle, holder/prop-change cross-checks | `p07_contact.py` |
| S11 kinematic (L4a) | authored per entity per beat: support + 10 cues; support agrees with S06/S07 | `p11_kinematic.py`, `library/kinematic_cues.yaml` |
| S12 Bartenieff (L4b) | authored coordination: connectivity, pattern, initiation, follow-through, body mode; `cpcs:` labelled | `p12_bartenieff.py`, `library/bartenieff_vocabulary.yaml`, `library/body_modes/` |
| S13 motion (L4c) | authored Euler key poses (root pos = S04, heading = S04 facing, 11 kernel joints, declared turn axes, S06 posture) → derived quaternions, follows edges (Euler delta, slerp vs euler_axis, root trajectory) | `p13_motion.py`, `solver/{euler_solver,quaternion,trajectory}.py` |
| S14 effort (L5) | authored LMA intervals per entity (Effort factors, effort action checked against weight x time x space, Shape, Space, intensity in the effort mode's range) → overlaps edges | `p14_effort.py`, `library/laban_vocabulary.yaml`, `library/effort_modes/` |
| S15 camera (L5.5) | authored shot list: 13 subdivisions + motivation per shot; geometry derived (camera position, axis side, frame height, screen x); checks: tiling, coverage, motivation refs, 180-line, camera–kinematic coupling, composition, 30° cuts, genre card, subdivision coherence, intent + tempo | `p15_camera.py`, `validators/camera_validator.py`, `solver/camera_geometry.py`, `planner/camera_library.py`, `library/camera_*` |
| S16 render (L6, projection) | authored frame parts (impact, smear on a declared limb/prop only, speedlines, holds, fx, ink) + the full LBN-2.4-ADV-LMA projection of every graph, uncompressed, item-level coverage 100% | `p16_render.py`, `renderers/anime_renderer.py` |

Pipeline: `python -m compiler.pipeline "<query>" [--genre anime] [--until contact] [--plans DIR]`; an authored step
with no plan exits 3 and prints (or `--packet-out`) its packet. Example: `examples/wizard_vs_acrobat/` (through S16; plans for S04, S11–S16 written in-session; the prompt is `examples/wizard_vs_acrobat/render.txt`).
Golden: `examples/reference_fight/` — the LBN reference ninja fight compiled from its preface; its `render.txt` contains all 68 kernel + reference items and A's reference roots exactly. **Both render.txt files are ready for you to render; Claude never renders.**.
Kernel = the 68 controls both LBN-2.3-ADV and LBN-2.4-ADV-LMA state (`kernel/sources/`), scoped per item.

## Controls
Three append-only, hash-chained logs (`schemas/schema_log.jsonl`, `library/library_log.jsonl`,
`kernel/kernel_log.jsonl`); generated files checked against regeneration; examples recompile byte-for-byte; 345 tests; all in `scripts/check.sh`.

## Owner decisions so far
Step IDs S01–S17 carry order (L labels are names); keys `step_id`/`band`; constraint built after S02 and before
the event graphs; effort (L5) before camera (L5.5); entity definitions at L0.5, state tracks at L2; S01 writes
`/intent`, S02 writes `/scene`; post-generation stays `validation.post_generation`; S02 cards only (no model);
starter cards drafted by Claude; kernel = LBN-2.3 ∩ 2.4; beat plans written in-session (no paid API);
linear causality only; closed kernel state vocabulary. Full log: `docs/layer_dependency.md`, plans in `docs/plans/`.

## Waiting for owner review (draft)
- 11 library cards (`library/`), all `status: draft`.
- `kernel/kernel_scope.yaml`: kernel 20, per-actor 6, per-prop 5, reference fight only 37.
- Draft libraries: `library/kinematic_cues.yaml`, `library/bartenieff_vocabulary.yaml` (developmental patterns are a
  disclosed interpretation; `cpcs:spiral` is a labelled extension), `library/body_modes/` (4 cards), `library/laban_vocabulary.yaml`, `library/effort_modes/` (calm, desperate,
  trained), camera library (`camera_subdivisions`, `camera_grammar`, `camera_tempo`, `camera_conventions/` x3,
  `camera_idioms/` x5) — all numbers and rules are drafts.
- Reference-fight deviations from its own data (recorded in MASTER_PLAN S16.6): 10.0 hold row has no beat;
  possession tracked on props only; shuriken embed at 5.9; smoke dissipation not a state.
- S13.6 posture cross-check is an agent addition (plan silent). Q6 note: under intrinsic XYZ a flip is pure-X only
  when facing ±Z (see MASTER_PLAN notes); no change made.

## Open questions and next work
All six questions are decided (see **Decided this round** in
[docs/plans/MASTER_PLAN.md](docs/plans/MASTER_PLAN.md)). Next task: **M5 UGC (S08–S10)** + `examples/ugc_glasses_demo/`. Completed work is struck through
under **Done**.
