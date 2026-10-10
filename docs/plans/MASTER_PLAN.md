# cinematic-compiler — micro plan (remaining work)

One plan. Tick a task when its test passes; when a whole step is done, move it to **Done** and strike it.
What each graph is for: [graph_types.md](../graph_types.md). DAG and write ownership: `kernel/layer_order.yaml`.

**Every step ends the same way:** schemas logged before code → `scripts/check.sh` PASS → graft/graphify
refreshed → one commit `Sxx: …` → HANDOFF.md updated.
**Every authored step** (S04, S08–S15, S16 frame parts) uses one loop: `prepare(envelope) → packet (sha256)` →
Claude writes JSON in-session → `submit(envelope, packet, json)` checks the packet hash, schema and the step's
gates → the pass writes only its paths. A failed gate allows 2 re-authoring attempts, recorded in provenance.
**Every step's tests:** schema, determinism across processes, completeness, non-invention, write scope, step checks.

---

## Done

- ~~Skeleton: layer DAG, envelope schema, DAG validator, pass write-scope check~~
- ~~Controls: schema / library / kernel hash logs, regeneration checks, `scripts/check.sh`~~
- ~~S01 intent (L0)~~ · ~~S02 brief (L0.5), 11 draft cards~~ · ~~S03 constraint, kernel = LBN-2.3 ∩ 2.4~~
- ~~Owner decisions: step IDs, `step_id`/`band`, constraint before events, effort before camera, entities at L0.5,
  `/intent` + `/scene`, post-gen as validation block, cards-only S02, in-session authoring, linear causality,
  closed state vocabulary~~
- ~~Graph catalog (graph_types.md); URCP removed; standalone repo~~

---

## Blockers (owner)

| Q | Question | Proposal used if you say "go" | Blocks |
|---|---|---|---|
| Q1 | Catalog: constraint graph lists beats per rule, but S03 runs before beats | S04 writes its own `beat_constraint` edge group | S04.6 |
| Q2 | State graph holds position/orientation, numbers arrive at S13 | Beat plan authors root `pos` + `facing` per actor per beat; S13 must match | S04.1, S06 |
| Q3 | Contact type: grip (graph table) vs possess (catalog, diagram) | `possess`; `body_part` says how (right_hand = held) | S07.1 |
| Q4 | Catalog beat has one actor; interactions have two | `actor` + `participants` | S04.1 |
| Q5 | L4c box Y=cartwheel, Z=spin vs kernel frame Y up / +Z forward | Kernel frame: X flip, Z cartwheel, Y spin | S13.4 |
| Q6 | Euler XYZ intrinsic/extrinsic, handedness | ask at M2 | S13.5 |
| R1 | Review: 11 draft cards, kernel scope (20/6/5/37), loose world match | — | nothing; drafts stay usable |

---

## M1 — events and substrate (S04–S07) → done when the courtyard example compiles through S07

### M1.0 DAG update
- [ ] M1.0.1 `kernel/layer_order.yaml` 1.5: owner table edges — temporal depends on constraint; S08→S09→S10 chain;
  camera depends on motion + effort; causal also writes `/quadrant`. Test: build order unchanged for anime,
  UGC order S08<S09<S10.
- [ ] M1.0.2 `kernel/build_ir_schema.py`: add `/quadrant` (owned by S05). Log schema change. Test: generation check.

### S04 temporal (L1 band, authored) — `nodes.beats`, `edges.temporal`
- [ ] S04.1 `schemas/graphs/beat_plan.schema.json` (authored input): `id, t, dur, event_type (action|hold|transition),
  actor, label, participants[{kind,id}], modes{actor_id: mode}, action, requires[], effects[], contacts[],
  causes[{to, causal_strength, why}]`, plus `pos`/`facing` per actor if Q2. Log.
- [ ] S04.2 `schemas/graphs/temporal_graph.schema.json`: beat node (copied fields) + temporal edge
  `id, from, to, relation (precedes|overlaps|starts_with), duration, gap`. Log.
- [ ] S04.3 `planner/beat_planner.py`: `prepare(envelope)` → packet {scene, entities (parts, capabilities, modes),
  props (parts, states), surfaces, applied constraints, state vocabulary, instructions, schema id}; sha256 of
  canonical JSON. Test: same envelope → same packet bytes.
- [ ] S04.4 `planner/prompts/beat_planning.txt`: authoring instructions shown in the packet. Test: packet embeds its hash.
- [ ] S04.5 `planner/dynamic_beat_validator.py`: ids unique; times ≥ 0 and inside `scene.duration_s` when known;
  participants/parts resolve to S02 items and card parts; filler rule (non-hold beat with no effect, no contact,
  no causal edge → reject); `mode_coherence` (mode is in the archetype card); `mode_transition` (a mode change
  needs a triggering beat). Tests: one negative case per rule.
- [ ] S04.6 `compiler/passes/mandatory/p04_temporal.py`: `submit(envelope, packet, plan)` → refuses wrong packet
  hash → writes `nodes.beats`, `edges.temporal` (computed: duration = from.dur, gap = to.t − from.end), and the
  `beat_constraint` group if Q1. Tests: write scope; mutated input untouched; temporal edges never authored.
- [ ] S04.7 `compiler/pipeline.py`: add `plans={...}` input; stop at S04 if no plan, returning the packet.

### S05 causal (L1 band, derived) — `edges.causal`, `/quadrant`
- [ ] S05.1 `schemas/graphs/causal_graph.schema.json`: edge `id, from, to, relation (causes), causal_strength
  (hard|soft), why`; quadrant `{causal{branching=0, parallel_effects, prerequisites}, style, quadrant, strata}`. Log.
- [ ] S05.2 `compiler/passes/mandatory/p05_causal.py`: edges from plan `causes`; checks: target exists, no cycles,
  hard → target starts at/after source end and one source effect satisfies a target `requires`; soft → target
  starts at/after source start.
- [ ] S05.3 Quadrant scoring (same file): parallel = most (effects + outgoing causes) of one beat (0–1→0, 2→1,
  3+→2); prerequisites = hard edges (0→0, 1–2→1, 3+→2); style = +1 style_reference, +1 any hold beat;
  quadrant A/B/C/D and strata per the owner table; `load_bearing` flag from intent/CLI (default off).
  Tests: one scene per quadrant.

### S06 state (L2 band, derived) — `nodes.states`, `edges.state_transition`
- [ ] S06.1 `kernel/state_vocabulary.yaml` (kernel log): actor support/posture/possession/condition/location;
  prop card states + holder + location; surface damage. Test: loader refuses unknown property or value.
- [ ] S06.2 `schemas/graphs/state_graph.schema.json`: entity-state node per entity per beat
  `{id, subject, beat, t, conditions{property: value|unknown}}` (+ pos/facing if Q2); transition
  `{id, from_state, to_state, trigger_event}`. Log.
- [ ] S06.3 `solver/prop_state_machine.py`: replay — `requires` read at `t`, `effects` commit at `t + dur`;
  initial value only from a first `requires`, else `unknown`; same-time conflicting effects rejected.
- [ ] S06.4 `compiler/passes/mandatory/p06_state.py` + `validators/continuity_validator.py`: no teleport (location
  changes only through an effect), no clone, no disappearance. Tests: each failure.

### S07 contact (L2 band, derived) — `nodes.contacts`, `edges.contact`
- [ ] S07.1 `schemas/graphs/contact_graph.schema.json`: contact-event `{id, t (beat end), contact_type
  (touch|possess|support|release per Q3), body_part, a{kind,id}, b{kind,id,part}, beat}`; edges
  `precedes` (same pair) and `releases` (release → the contact it ends). Log.
- [ ] S07.2 `compiler/passes/mandatory/p07_contact.py`: release needs an active same-pair contact; one hand holds
  one thing; touch is instant; parts from cards.
- [ ] S07.3 Cross-checks with S06: holder state agrees with active hand contacts; every prop state change has a
  contact event in its beat. Tests: each failure.

### M1 example
- [ ] M1.E1 `examples/wizard_vs_acrobat/` — query, packet, Claude-authored beat plan (~8 beats, 10 s, courtyard),
  envelope through S07; `tests/test_example_courtyard.py` recompiles it byte-for-byte.
- [ ] M1.E2 HANDOFF.md + graph_types.md status → M1 done.

---

## M2 — body (S11–S13) → done when the example has validated key poses

### S11 kinematic (L4a, authored)
- [ ] S11.1 `library/kinematic_cues.yaml` (draft, library log): values for support, balance, loading, bracing,
  yielding, weight transfer, tension, release, strain, restraint, breathing.
- [ ] S11.2 `schemas/graphs/kinematic_graph.schema.json`: node per actor per beat with those 11 fields; transition edges. Log.
- [ ] S11.3 `planner/prompts/kinematic_organization.txt` + prepare/submit in `compiler/passes/derived/p11_kinematic.py`.
- [ ] S11.4 `validators/kinematic_validator.py`: support agrees with S06 support state and S07 support contacts.

### S12 Bartenieff (L4b, authored)
- [ ] S12.1 `library/body_modes/` (core_distal, distal_core, same_side, cross_lateral; draft).
- [ ] S12.2 `schemas/graphs/bartenieff_graph.schema.json`: `{actor, beat, connectivity (breath, core-distal,
  head-tail, upper-lower, body-half, cross-lateral, cpcs:spiral), developmental_pattern, intent, initiation,
  follow_through, body_mode}`. Log.
- [ ] S12.3 `p12_bartenieff.py` + prompt; validator: values from vocabulary; `cpcs:` values flagged as extensions.

### S13 motion (L4c, authored + derived)
- [ ] S13.1 `schemas/graphs/motion_graph.schema.json`: key pose `{beat, t, name, pos, rot, bones{Sp, LUL, RUL, LL,
  RL, LA, RA, LFA, RFA, HD, NK}, axis_declaration, description}`; edge `follows {axis_declaration, slerp}`. Log.
- [ ] S13.2 `planner/prompts/euler_solving.txt` + `p13_motion.py` prepare/submit.
- [ ] S13.3 `solver/euler_solver.py` checks: 11 joints present; degrees; pos/facing match S04 (Q2).
- [ ] S13.4 Axis check: declared flip/cartwheel/spin axis matches the root rotation change (Q5).
- [ ] S13.5 `solver/quaternion.py` (needs Q6) and `solver/trajectory.py` (root path from key `pos`), both derived.

---

## M3 — feel and framing (S14–S15)

### S14 effort (L5, authored)
- [ ] S14.1 `library/laban_vocabulary.yaml` (draft): Effort weight light|strong, time sustained|sudden, space
  indirect|direct, flow free|bound; 8 effort actions; Shape and Space qualities kept separate.
- [ ] S14.2 `library/effort_modes/` (calm, desperate, trained; draft).
- [ ] S14.3 `schemas/graphs/effort_graph.schema.json`: interval `{actor, beats, effort{weight,time,space,flow},
  shape, space, intensity, effort_mode}`; edges `overlaps`. Log.
- [ ] S14.4 `p14_effort.py` + `laban_synthesis.txt`; validator: intervals cover each actor's beats; values from vocabulary.

### S15 camera (L5.5, authored)
- [ ] S15.1 Library (draft): camera_subdivisions, camera_grammar, camera_tempo, camera_idioms/, camera_conventions/.
- [ ] S15.2 `schemas/camera.schema.json` (node: 13 subdivisions + motivation{kind, ref}, all required) and
  `schemas/graphs/camera_graph.schema.json` (shot-to-shot edges). Log.
- [ ] S15.3 `p15_camera.py` + `camera_selection.txt`.
- [ ] S15.4 Validators: motivation ref resolves; 180-line (axis); camera–kinematic coupling; continuity; genre;
  subdivision coherence; intent weighting (impact, reveal, emotion, spatial, rhythm, product).

---

## M4 — render (S16) → done when the reference courtyard fight round-trips

- [ ] S16.1 Draft cards for the reference fight: ninja A/B variants, kunai, rope_dart, smoke_pellet,
  shuriken_volley, substitution_log, wooden pillar world.
- [ ] S16.2 `schemas/graphs/render.schema.json`: `{target, text, sha256, coverage}`; frame-part directives
  `{impact, smear, speedlines, holds, fx, ink}`. Log.
- [ ] S16.3 `renderers/anime_renderer.py`: deterministic projection into the LBN-2.x layout (variant, fps, dur, ax,
  key, negative, laban, actor tracks, prop tracks, cam, anime, rules); density from the quadrant.
- [ ] S16.4 Frame-part directives authored (smear only on the declared limb or prop).
- [ ] S16.5 Coverage: every applied constraint appears in rules or negatives.
- [ ] S16.6 Golden: the reference fight compiles and contains every kernel and reference-fight item; the owner
  renders (Claude never renders).

## M5 — UGC (S08–S10)
- [ ] S08 hand role: `grip_types.yaml`, `role_templates.yaml` (draft); schema `{interaction, agent_hand,
  support_hand, agent_grip, support_grip, role_invariant, duration}`; validator: roles hold across the interaction.
- [ ] S09 object state: schema `{object, beat, state_name}` + `transitions_to{trigger_contact}`; values from cards;
  every change triggered by a hand contact.
- [ ] S10 affordance: `library/affordances/` (clothing, food, electronics, cosmetics; draft); schema `(object,
  action){preconditions, postconditions, required_grip, duration}`; validator: each functional verb succeeds.
- [ ] M5.E `renderers/ugc_renderer.py` + glasses smoke test.

## M6 — tooling
- [ ] `cli/` compile, validate, graph inspect, kernel extract, ablate (ablate never renders).
- [ ] `compiler/replan_trigger.py`: failed gate → re-author the failing step; provenance replan fields.
- [ ] `kernel_extraction/` synergy_matrix, bridge_detector, layer_analyzer, kernel_compressor, ablation_runner.
- [ ] `schemas/modality/` live_action, anime, ugc_ad.

## M7 — when a video model is authorised
- [ ] S17 `validation.post_generation` object `{run_at, video_ref, checks[pose, object, state, affordance],
  verdict, replan_triggered, replan_scope, replan_target}` + `validators/post_generation/`.
- [ ] `renderers/conditioning/` pose, depth, flow, HOI emitters; live-action skeletal export.
