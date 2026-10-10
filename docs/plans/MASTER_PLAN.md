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

## Decided this round (owner, 2026-10-10)

| # | Decision | Lands in |
|---|---|---|
| Q1 | `beat_constraint` is a registered edge group at S04 (beats → constraints) | M1.0.1, S04.6 |
| Q2 | S04 root `pos` + `facing` are authoritative; S13 must reproduce them exactly or fail and replan | S04.1, S06.2, S13.3 |
| Q3 | Contact type `possess` (catalog wording); `body_part` says how it is held | S07.1 |
| Q4 | One `actor` per beat plus `participants` (catalog: "a timestamped event with an actor") | S04.1 |
| Q6 | Euler **intrinsic XYZ, right-handed**: +X pitch forward (nose down), +Y yaw left, +Z roll clockwise (right shoulder down); rest = upright, facing +Z, up +Y; carried in `scene.ax.rotation_convention` | M1.0.4, S13 |
| Q5 | Follows from Q6: flip about X (pitch), spin about Y (yaw), cartwheel about Z (roll) | S13.4 |
| A1 | Quadrant is scene metadata: `scene.quadrant`, written by S05 (most-specific owner wins inside `/scene`) | M1.0.1–3, S05.3 |
| A2 | Causal schema stays general; `scene.quadrant.linear: true` makes the validator reject out-degree > 1 | S05.2 |
| A3 | Kernel split: `invariants.yaml` + `state_vocabulary.yaml`, each with a schema and kernel-log entries | M1.0.4 |
| A6 | `nodes.render` is a projection group (`projection: true`); endpoint checks skip it | M1.0.1–3, S16.2 |
| A7 | `provenance.kernel_hash` in every envelope; a stale example fails the gate | M1.0.5 |
| A9 | M5 gets its own example (`examples/ugc_glasses_demo/`) | M5.E |
| A10 | CLI and replan trigger move to M1.5; modality schemas move to M1.0 (S04 needs them) | M1.0.6, M1.5 |
| B1 | **Genre** comes only from the query or `--genre`; missing → stop at S02 with "add --genre". **fps** = query/flag, else the genre schema's `default_fps`. **duration** = query/flag, else the beat plan's last beat end (S04 plans inside the genre's duration budget). Every scene value names its source; `default` marks a filled default | M1.0.3, M1.0.6, M1.0.7, S04 |
| B2 | One compile = one clip. Envelope carries `scene.chained_from: null` and `provenance.chained_from_envelope_hash: null` now; chaining is built at M5.5 | M1.0.3, M5.5 |
| B3 | S16 outputs the full LBN-2.x prompt, uncompressed, model-agnostic; owner invariant `no_render_compression` (coverage 100%). Compression and model-specific renderers only after a target model is chosen. No vector database: every lookup is by exact id | M1.0.8, S16 |

Notes on the decisions:
- Q6 as written is right-handed with +X = the performer's left, which matches the earlier notation work and
  Maya/Mixamo-style Y-up rigs. Unity is left-handed (+X right), so "matches Unity" does not hold; no change made.
- A7's staleness detection is done by `scripts/check.sh` (URCP is gone): every example's `kernel_hash` must equal
  the current kernel's.
- B1 replaces the S02 rule that took genre from a single-genre world card (genre is never inferred now).
  Duration is resolved at S04, so `/scene/duration_s` and `/scene/duration_source` are S04's carve-outs
  inside `/scene` (same most-specific-owner rule as `scene.quadrant`).
- B3: `kernel/invariants.yaml` is the LBN-2.3 ∩ 2.4 intersection, so owner-authored invariants such as
  `no_render_compression` live in `kernel/owner_invariants.yaml` and the generator merges them as `origin: owner`.
- Consequence of A2 + linear-only: branching is always 0, so a scene scores at most 4 and quadrant A (5–6) is
  unreachable until branching exists. Recorded, not blocking.
- Still open for review only (nothing blocked): R1 — 11 draft cards, kernel scope (20/6/5/37), loose world match.

---

## M1 — events and substrate (S04–S07) → done when the courtyard example compiles through S07

### M1.0 Foundations (before S04)
- [x] M1.0.1 `kernel/layer_order.yaml` 1.5: owner-table edges (temporal ← constraint; S08 → S09 → S10; camera ←
  motion + effort); every edge group declares `from`/`to` node groups; `beat_constraint` at S04 (beats → constraints);
  `/scene/quadrant` owned by causal; render group marked `projection: true`. Test: anime order unchanged, UGC
  S08 < S09 < S10.
- [x] M1.0.2 `validators/layer_dependency_validator.py`: edge endpoints must be node groups written at or before
  that step (projection groups skipped); nested ownership allowed only when the inner owner runs later — most
  specific owner wins, and `check_pass_writes` keeps the outer owner out of the inner path. Tests: each failure.
- [x] M1.0.3 Envelope schema: flat per-field sources (`genre_source`, `fps_source`, `duration_source`, … with values
  user | flag | default | beat_plan_end | card:<id>) replacing the `sources` map; `scene.quadrant` (incl. `linear`);
  `scene.ax.rotation_convention`; `scene.chained_from: null`; `provenance.kernel_hash`;
  `provenance.chained_from_envelope_hash: null`; render `projection` flag; carve-outs `/scene/duration_s`,
  `/scene/duration_source` (S04) and `/scene/quadrant` (S05). Log.
- [x] M1.0.4 Kernel split: `kernel/state_vocabulary.yaml` + `schemas/kernel_state_vocabulary.schema.json`;
  `kernel/conventions.yaml` (Q6 rotation convention) + schema; both in the kernel log; S02 copies the convention
  into `scene.ax.rotation_convention`. Test: unknown property/value refused; convention present in every scene.
- [x] M1.0.5 `compiler/pipeline.py` writes provenance (source prompt, versions, `kernel_hash` = sha256 of
  invariants + state vocabulary + conventions, pass history); determinism tests ignore timing fields;
  `scripts/check.sh` fails on any example whose `kernel_hash` is stale.
- [x] M1.0.6 `schemas/modality/{anime,live_action,ugc_ad}.schema.json`: per-genre active steps, required groups,
  authoring requirements, `default_fps` (anime 24, live_action 24, ugc_ad 30) and a draft `duration_budget_s`;
  the S04 packet carries the scene's modality rules. Log.
- [x] M1.0.7 S02 update: refuse with `GENRE_REQUIRED` ("add --genre") when genre is missing; drop the
  world-card genre rule; fill fps from `default_fps` with `fps_source: default`; stop writing duration.
  Tests: each source value; refusal lists the fix.
- [x] M1.0.8 `kernel/owner_invariants.yaml` + schema (`id, band, statement, check, layer, learned_from,
  kernel_version`), first entry `no_render_compression`; the kernel generator merges owner items as
  `origin: owner`, scope kernel. Kernel log.

### S04 temporal (L1 band, authored) — `nodes.beats`, `edges.temporal`
- [x] S04.1 `schemas/graphs/beat_plan.schema.json` (authored input): `id, t, dur, event_type (action|hold|transition),
  actor, label, participants[{kind,id}], modes{actor_id: mode}, pos{actor_id: [x,y,z]}, facing{actor_id: [x,y,z]},
  action, requires[], effects[], contacts[], causes[{to, causal_strength, why}]`. Log.
- [x] S04.2 `schemas/graphs/temporal_graph.schema.json`: beat node (copied fields) + temporal edge
  `id, from, to, relation (precedes|overlaps|starts_with), duration, gap`. Log.
- [x] S04.3 `planner/beat_planner.py`: `prepare(envelope)` → packet {scene, entities (parts, capabilities, modes),
  props (parts, states), surfaces, applied constraints, state vocabulary, instructions, schema id}; sha256 of
  canonical JSON. Test: same envelope → same packet bytes.
- [x] S04.4 `planner/prompts/beat_planning.txt`: authoring instructions shown in the packet. Test: packet embeds its hash.
- [x] S04.5 `planner/dynamic_beat_validator.py`: ids unique; times ≥ 0 and inside `scene.duration_s` when known;
  participants/parts resolve to S02 items and card parts; filler rule (non-hold beat with no effect, no contact,
  no causal edge → reject); `mode_coherence` (mode is in the archetype card); `mode_transition` (a mode change
  needs a triggering beat). Tests: one negative case per rule.
- [x] S04.6 `compiler/passes/mandatory/p04_temporal.py`: `submit(envelope, packet, plan)` → refuses wrong packet
  hash → writes `nodes.beats`, `edges.temporal` (computed: duration = from.dur, gap = to.t − from.end) and
  `edges.beat_constraint` (derived: a beat links every constraint applied to its actor or participants; scene-wide
  rules stay implicit). Tests: write scope; mutated input untouched; temporal and beat_constraint never authored.
- [x] S04.7 `compiler/pipeline.py`: add `plans={...}` input; stop at S04 if no plan, returning the packet.
- [x] S04.9 Duration: if the query/flag gave one, every beat must end within it; otherwise beats are planned inside
  the genre's `duration_budget_s` and S04 writes `scene.duration_s` = last beat end, `duration_source: beat_plan_end`.
- [x] S04.8 S04 packet and checks use the scene's modality schema (M1.0.6).

### S05 causal (L1 band, derived) — `edges.causal`, `scene.quadrant`
- [x] S05.1 `schemas/graphs/causal_graph.schema.json`: edge `id, from, to, relation (causes), causal_strength
  (hard|soft), why` — branching allowed by the schema; `scene.quadrant` `{linear, causal{branching, parallel_effects,
  prerequisites}, style, quadrant, strata, load_bearing}`. Log.
- [x] S05.2 `compiler/passes/mandatory/p05_causal.py`: edges from plan `causes`; checks: target exists, no cycles,
  out-degree ≤ 1 while `linear` is true (owner: linear only, so S05 sets `linear: true`),
  hard → target starts at/after source end and one source effect satisfies a target `requires`; soft → target
  starts at/after source start.
- [x] S05.3 Quadrant scoring (same file): parallel = most (effects + outgoing causes) of one beat (0–1→0, 2→1,
  3+→2); prerequisites = hard edges (0→0, 1–2→1, 3+→2); style = +1 style_reference, +1 any hold beat;
  quadrant A/B/C/D and strata per the owner table; `load_bearing` flag from intent/CLI (default off).
  Tests: one scene per quadrant.

### S06 state (L2 band, derived) — `nodes.states`, `edges.state_transition`
- [x] S06.1 `kernel/state_vocabulary.yaml` (kernel log): actor support/posture/possession/condition/location;
  prop card states + holder + location; surface damage. Test: loader refuses unknown property or value.
- [x] S06.2 `schemas/graphs/state_graph.schema.json`: entity-state node per entity per beat
  `{id, subject, beat, t, pos, facing, conditions{property: value|unknown}}` (pos/facing copied from S04); transition
  `{id, from_state, to_state, trigger_event}`. Log.
- [x] S06.3 `solver/prop_state_machine.py`: replay — `requires` read at `t`, `effects` commit at `t + dur`;
  initial value only from a first `requires`, else `unknown`; same-time conflicting effects rejected.
- [x] S06.4 `compiler/passes/mandatory/p06_state.py` + `validators/continuity_validator.py`: no teleport (location
  changes only through an effect), no clone, no disappearance. Tests: each failure.

### S07 contact (L2 band, derived) — `nodes.contacts`, `edges.contact`
- [x] S07.1 `schemas/graphs/contact_graph.schema.json`: contact-event `{id, t (beat end), contact_type
  (touch|possess|support|release), body_part, a{kind,id}, b{kind,id,part}, beat}`; edges
  `precedes` (same pair) and `releases` (release → the contact it ends). Log.
- [x] S07.2 `compiler/passes/mandatory/p07_contact.py`: release needs an active same-pair contact; one hand holds
  one thing; touch is instant; parts from cards.
- [x] S07.3 Cross-checks with S06: holder state agrees with active hand contacts; every prop state change has a
  contact event in its beat. Tests: each failure.

### M1 example
- [x] M1.E1 `examples/wizard_vs_acrobat/` — query, packet, Claude-authored beat plan (~8 beats, 10 s, courtyard),
  envelope through S07; `tests/test_example_courtyard.py` recompiles it byte-for-byte.
- [x] M1.E2 HANDOFF.md + graph_types.md status → M1 done.

---

## M1.5 — tooling M2 needs
- [x] M1.5.1 `cli/compile.py` (`cinematic compile <query|file> --genre … --until …`), `cli/validate.py`,
  `cli/graph.py` (inspect a group); entry point `cinematic` in pyproject.
- [x] M1.5.2 `compiler/replan_trigger.py`: a failed gate in an authored step re-issues that step's packet with the
  findings (max 2); provenance `replan_count` / `replan_layers`. Tests: success on attempt 2; stop after 2.

---

## M2 — body (S11–S13) → done when the example has validated key poses

### S11 kinematic (L4a, authored)
- [x] S11.1 `library/kinematic_cues.yaml` (draft, library log): values for support, balance, loading, bracing,
  yielding, weight transfer, tension, release, strain, restraint, breathing.
- [x] S11.2 `schemas/graphs/kinematic_graph.schema.json`: node per actor per beat with those 11 fields; transition edges. Log.
- [x] S11.3 `planner/prompts/kinematic_organization.txt` + prepare/submit in `compiler/passes/derived/p11_kinematic.py`.
- [x] S11.4 `validators/kinematic_validator.py`: support agrees with S06 support state and S07 support contacts.

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
- [ ] S13.3 `solver/euler_solver.py` checks: 11 joints present; degrees; key pose root `pos` equals S04 exactly and
  `rot` agrees with S04 `facing`; a mismatch fails the step and triggers re-authoring (replan), never a silent fix.
- [ ] S13.4 Axis check: flip about X, spin about Y, cartwheel about Z; the declared axis must match the root
  rotation change.
- [ ] S13.5 `solver/quaternion.py` (intrinsic XYZ, right-handed, from `scene.ax.rotation_convention`) and
  `solver/trajectory.py` (root path from key `pos`), both derived. Tests: known rotations round-trip.

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
- [ ] S16.2 `schemas/graphs/render.schema.json` (projection group, no edges): `{target, text, sha256, coverage}`; frame-part directives
  `{impact, smear, speedlines, holds, fx, ink}`. Log.
- [ ] S16.3 `renderers/anime_renderer.py`: deterministic projection into the full LBN-2.x layout (variant, fps, dur,
  ax, key, negative, laban, actor tracks, prop tracks, cam, anime, rules); uncompressed, no length budget, no
  model-specific formatting; quadrant density decides prose detail, never drops graph content.
- [ ] S16.4 Frame-part directives authored (smear only on the declared limb or prop).
- [ ] S16.5 Coverage (`no_render_compression`): every node group and every applied constraint has an entry in the
  render; anything missing fails the step.
- [ ] S16.6 Golden: the reference fight compiles and contains every kernel and reference-fight item; the owner
  renders (Claude never renders).

## M5 — UGC (S08–S10)
- [ ] S08 hand role: `grip_types.yaml`, `role_templates.yaml` (draft); schema `{interaction, agent_hand,
  support_hand, agent_grip, support_grip, role_invariant, duration}`; validator: roles hold across the interaction.
- [ ] S09 object state: schema `{object, beat, state_name}` + `transitions_to{trigger_contact}`; values from cards;
  every change triggered by a hand contact.
- [ ] S10 affordance: `library/affordances/` (clothing, food, electronics, cosmetics; draft); schema `(object,
  action){preconditions, postconditions, required_grip, duration}`; validator: each functional verb succeeds.
- [ ] M5.E `examples/ugc_glasses_demo/`: query, packet, Claude-authored beat plan, envelope through S10, render via
  `renderers/ugc_renderer.py`; recompiles byte-for-byte like M1.E1.

## M5.5 — clip chaining
- [ ] S02 accepts an optional previous envelope; S06 starts from its final states; S07 from its active contacts;
  S05 reads its unresolved causes; `chained_from` fields filled; cross-clip continuity tests (damage, props, camera).

## M6 — deferred tooling
- [ ] `kernel_extraction/` synergy_matrix, bridge_detector, layer_analyzer, kernel_compressor, ablation_runner
  (ablation never renders; the owner renders).

## M7 — when a target video model is chosen and authorised
- [ ] S17 `validation.post_generation` object `{run_at, video_ref, checks[pose, object, state, affordance],
  verdict, replan_triggered, replan_scope, replan_target}` + `validators/post_generation/`.
- [ ] `renderers/conditioning/` pose, depth, flow, HOI emitters; live-action skeletal export.
- [ ] Per-model compression renderer (a separate pass over the full S16 output; the core never compresses).
