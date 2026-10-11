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
- ~~M1 (S04–S07), M1.5 (CLI, replan trigger), M2 (S11 kinematic, S12 Bartenieff, S13 motion), M3 (S14 effort,
  S15 camera), M4 (S16 render + reference-fight golden), M5 (S08 hand role, S09 object state, S10 affordance,
  UGC glasses demo), M5.5 (chaining), M3.5 (renumber; S14 facial; four examples through S17)~~

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
- Q6 consequence (S13, recorded, no change): intrinsic XYZ applies X first, so changing the X angle rotates about
  world X. A flip is about the performer's own lateral axis only when the performer faces ±Z; at other headings a
  pure-X flip is oblique. The courtyard backflip (heading −29°) is such a flip; its S04 facing (+29° at landing)
  agrees with it. Heading-first orders (YXZ) would avoid this; the convention stays the owner's.
- Still open for review only (nothing blocked): R1 — 11 draft cards, kernel scope (20/6/5/37), loose world match.

### Face layer (owner, 2026-10-11)

| # | Decision | Lands in |
|---|---|---|
| F1 | A facial step (FACS action units + valence/arousal) runs for `ugc_ad` and `live_action` only; anime waits for its own stylized expression vocabulary | M3.5 F.1 |
| F2 | Renumber so the face is S14: effort S14→S15, camera S15→S16, render S16→S17, post-generation S17→S18 (step IDs carry order; no fractions) | M3.5 R |
| F3 | Valence and arousal both on −1…1 (circumplex) | M3.5 F.4, F.6 |
| F4 | The render describes faces in words only; AU codes and numbers stay in the envelope | M3.5 F.8 |

Design calls from the concept review (agent, recorded for owner review):
- The face reads head pose and gaze from motion, so it sits after S13 at band L4d (not a sibling of L4c).
- No facial → effort edge: LMA Effort stays weight/time/space/flow; "subtle vs overt" lives in the face as intensity
  plus display rule.
- No `confidence` field (faces are authored, there is no solver); `salience` (carries_beat | supporting | background)
  tells the camera which faces it must show.
- The face–body check applies only to `display_rule: genuine` (masked/suppressed faces may disagree with the body).
- Costume occlusion: archetype cards gain a `face_profile` (visible regions, dominant side, emotional range).
- The concept's asymmetry claims are checked against published sources before the bounds become approved
  (Ekman, Hager & Friesen 1981 found deliberate expressions more asymmetric than spontaneous ones; Ekman's contempt
  is a one-sided AU14, not AU12). Until then the bounds table is a draft.

### Knowledge DAG and structured prose (owner, 2026-10-11)

The owner's DAG (`docs/sources/knowledge_dag_v1.md`, mapped in `kernel/knowledge_map.yaml`) is the compiler and
workflow for writing the owner's prompts in structured prose: dependency chains plus graph QA/QC for the final
outputs. Spec: [M8_DAG_PROSE.md](M8_DAG_PROSE.md).

| # | Decision | Lands in |
|---|---|---|
| O1 | Keep LBN-2.4 unchanged and compile structured prose alongside it, composed as the DAG says | M8.2-M8.3 |
| O2 | Compile all four movement modes (pure staff, Mixed, Upgraded Mixed, Euler-heavy); no per-scene choice | M8.2 |
| O3 | Prose leaves out "root exact" and states "Laban support and contacts primary; Euler precision override"; LBN-2.4 keeps the kernel rule | M8.2 |
| O4 | The repo layer order stands (effort after motion); the prose is built from the atoms the graphs hold | M8.0 map |
| O5 | One local commit per slice when the gate passes; no push without the owner | all |
| O6 | A conformance test checks the final prompts against every mandatory and required map row by semantic codes | M8.4 |

| O7 | Knee sign follows Q6 geometry: knee flexion = +X (0..135), elbow flexion = -X; the reference fight's golden negative knees are normalised to +|X| (recorded deviation) | M8.6 |
| O8 | Prop positions and velocities are authored on S04 beats (like body positions); S06 carries them; PROP_KINEMATICS holds v to positions and gravity unless the genre block declares a float | M8.8 |
| O9 | LBN-2.4 actor rows become named fields {t, label, pos, rot, joints, desc} (all values kept) | M8.5 |
| O10 | The golden (reference fight) passes conformance with nothing set aside: its fx 'dust ring' become 'dust burst' (the kernel negative 'no ring' stays), knees as O7, prop p/v consistent with gravity | M8.6-M8.9 |
| O11 | Joint limits: the owner's human ROM table (cited AAOS / Kendall / Norkin & Levangie) mapped onto the kernel joints; anime may exceed by up to +30 degrees for shoulder, hip, knee, spine and neck | M8.6 |
| O12 | Teleport: a body faster than 25 m/s between keys is a teleport, refused unless its beat is a declared substitution (decoy revealed, the body reappears at a declared position) | M8.7 |
| O13 | The five prompts per example (LBN-2.4 and the four prose modes) are fragments of one complete prompt: one content set in the DAG's template (C19), the mode as a setting (Euler blocks filled or left empty, DAG §2.14), detail adaptive (C2). The checklist judges all five and their union (Any) | M8.10 |
| O14 | Not applicable only for T3 and T4 (superseded by T5 in the DAG) and C26's 14 unnamed states; T5 is checked on the prompt (section order, precedence; build order per O4); menus count only where selected: V4/V5 by the request, C14-C17 by mode, C11 by genre | M8.10 |

Still open: P3.2-6 PRESERVE_AXIS (S16's 180-degree rule) — the owner's call.

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
- [x] S12.1 `library/body_modes/` (core_distal, distal_core, same_side, cross_lateral; draft).
- [x] S12.2 `schemas/graphs/bartenieff_graph.schema.json`: `{actor, beat, connectivity (breath, core-distal,
  head-tail, upper-lower, body-half, cross-lateral, cpcs:spiral), developmental_pattern, intent, initiation,
  follow_through, body_mode}`. Log.
- [x] S12.3 `p12_bartenieff.py` + prompt; validator: values from vocabulary; `cpcs:` values flagged as extensions.

### S13 motion (L4c, authored + derived)
- [x] S13.1 `schemas/graphs/motion_graph.schema.json`: key pose `{beat, t, name, pos, rot, bones{Sp, LUL, RUL, LL,
  RL, LA, RA, LFA, RFA, HD, NK}, axis_declaration, description}`; edge `follows {axis_declaration, slerp}`. Log.
- [x] S13.2 `planner/prompts/euler_solving.txt` + `p13_motion.py` prepare/submit.
- [x] S13.3 `solver/euler_solver.py` checks: 11 joints present; degrees; key pose root `pos` equals S04 exactly and
  `rot` agrees with S04 `facing`; a mismatch fails the step and triggers re-authoring (replan), never a silent fix.
- [x] S13.4 Axis check: flip about X, spin about Y, cartwheel about Z; the declared axis must match the root
  rotation change.
- [x] S13.5 `solver/quaternion.py` (intrinsic XYZ, right-handed, from `scene.ax.rotation_convention`) and
  `solver/trajectory.py` (root path from key `pos`), both derived. Tests: known rotations round-trip.
- [x] S13.6 (agent addition, plan silent) Root agrees with the S06 posture when no posture change is in progress
  (standing/crouching/kneeling upright, inverted upside down, prone/supine level); MOTION_POSTURE.

---

## M3 — feel and framing (S14–S15)

_Renumbered by F2 (2026-10-11): effort is now S15, camera S16, render S17, post-generation S18. The task labels below keep the numbers they were built under._


### S14 effort (L5, authored)
- [x] S14.1 `library/laban_vocabulary.yaml` (draft): Effort weight light|strong, time sustained|sudden, space
  indirect|direct, flow free|bound; 8 effort actions; Shape and Space qualities kept separate.
- [x] S14.2 `library/effort_modes/` (calm, desperate, trained; draft).
- [x] S14.3 `schemas/graphs/effort_graph.schema.json`: interval `{actor, beats, effort{weight,time,space,flow},
  shape, space, intensity, effort_mode}`; edges `overlaps`. Log. (Added: `effort_action` checked against weight x time x
  space; `latent` for an inactive factor; the interval id and time span are derived.)
- [x] S14.4 `p14_effort.py` + `laban_synthesis.txt`; validator: intervals cover each actor's beats; values from vocabulary.

### S15 camera (L5.5, authored)
- [x] S15.1 Library (draft): camera_subdivisions, camera_grammar, camera_tempo, camera_idioms/, camera_conventions/.
- [x] S15.2 `schemas/camera.schema.json` (node: 13 subdivisions + motivation{kind, ref}, all required) and
  `schemas/graphs/camera_graph.schema.json` (shot-to-shot edges). Log.
- [x] S15.3 `p15_camera.py` + `camera_selection.txt`.
- [x] S15.4 Validators: motivation ref resolves; 180-line (axis); camera–kinematic coupling; continuity; genre;
  subdivision coherence; intent weighting (impact, reveal, emotion, spatial, rhythm, product).
- [x] S15.5 (agent additions, plan silent) Shots tile the scene in time; the camera is placed by derived geometry
  (aim = target + aim height, azimuth/elevation/distance) so side, frame height and screen x are computed, not
  claimed; composition placement must agree with the projected screen side; contact onsets in a shot must be
  visible at its scale; `validation.camera_kinematic_coupling` is set to pass when S15 passes. Side convention:
  left = left hand of an observer at the first entity (by id) facing the second.

---

## M4 — render (S16) → done when the reference courtyard fight round-trips

_Renumbered by F2 (2026-10-11): effort is now S15, camera S16, render S17, post-generation S18. The task labels below keep the numbers they were built under._


- [x] S16.1 Draft cards for the reference fight: ninja A/B variants, kunai, rope_dart, smoke_pellet,
  shuriken_volley, substitution_log, wooden pillar world.
  (Built: ninja_lean / ninja_broad, kunai, rope_dart, smoke_pellet, shuriken_volley (count 3), substitution_log,
  bamboo_courtyard_pillar. To ground the reference preface: S01 reads cast lines "A: <description>" and
  "props (<list>)"; S02 adds archetype `equipment` as props after the query's own and picks a world only when its
  `required_terms` appear; S03 turns card negatives (and object invariants) into constraints.)
- [x] S16.2 `schemas/graphs/render.schema.json` (projection group, no edges): `{target, text, sha256, coverage}`; frame-part directives
  `{impact, smear, speedlines, holds, fx, ink}`. Log.
- [x] S16.3 `renderers/anime_renderer.py`: deterministic projection into the full LBN-2.x layout (variant, fps, dur,
  ax, key, negative, laban, actor tracks, prop tracks, cam, anime, rules); uncompressed, no length budget, no
  model-specific formatting; quadrant density decides prose detail, never drops graph content.
- [x] S16.4 Frame-part directives authored (smear only on the declared limb or prop).
- [x] S16.5 Coverage (`no_render_compression`): every node group and every applied constraint has an entry in the
  render; anything missing fails the step.
  (Built on the courtyard: `renderers/anime_renderer.py` projects every graph into the LBN-2.4-ADV-LMA layout; kernel
  per-actor/per-prop controls are regenerated for the cast (labels A, B… in S02 order), never copied; the owner
  render control is enforced by coverage, not printed; examples write `render.txt` next to `envelope.json`.)
- [x] S16.6 Golden: the reference fight compiles and contains every kernel and reference-fight item; the owner
  renders (Claude never renders).
  (Built: `examples/reference_fight/` compiles from the reference preface with in-session plans for S04 and
  S11–S16; `tests/test_reference_fight_golden.py` finds all 68 kernel + reference items in `render.txt` (kernel 20,
  per-actor 6, per-prop 5, reference-only 37), A's roots and joints equal the reference rows, the anime directives
  survive. Recorded deviations from the reference data: A's 10.0 hold row has no beat (beats end at the scene end);
  possession is tracked on props only (A holds two props at once); the shuriken embed commits at 5.9 (end of the
  throw beat) instead of 6.3 and smoke dissipation is not a state (no contact triggers it); the reference's own
  wording is kept verbatim where it disagrees with itself (kunai pickup "at 8.0 during crash landing").)

## M5 — UGC (S08–S10)
- [x] S08 hand role: `grip_types.yaml`, `role_templates.yaml` (draft); schema `{interaction, agent_hand,
  support_hand, agent_grip, support_grip, role_invariant, duration}`; validator: roles hold across the interaction.
  (Built as an authored step: interactions name verb (an object-card affordance), object, actor, consecutive beats,
  hands, grips, role template; checks also forbid a hand serving two overlapping interactions; the role invariant
  is derived. The pipeline now reads the genre from the query's literal parse to choose the steps, so UGC-only
  steps run without --genre. Example `examples/ugc_glasses_demo/` (creator card added) through S08.)
- [x] S09 object state: schema `{object, beat, state_name}` + `transitions_to{trigger_contact}`; values from cards;
  every change triggered by a hand contact.
  (Built derived: internal states = the object card's own state properties from S06 (holder/location stay in S06);
  each change names its trigger beat, the hand contact on the object (or `held:<entity>.<hand>` when a holding hand
  carries it) and the S08 interaction; a change with no hand or outside every interaction fails S09.)
- [x] S10 affordance: `library/affordances/` (clothing, food, electronics, cosmetics; draft); schema `(object,
  action){preconditions, postconditions, required_grip, duration}`; validator: each functional verb succeeds.
  (Built derived: one proven verb per S08 interaction — library entry for (object card, verb), preconditions in the
  S09 state at the start, postconditions after the end, the agent grip equals the required grip, duration in range;
  `enables` edges link verbs on the same object. Electronics/cosmetics entries are for objects with no card yet
  (`card: pending`).)
- [x] M5.E `examples/ugc_glasses_demo/`: query, packet, Claude-authored beat plan, envelope through S10, render via
  `renderers/ugc_renderer.py`; recompiles byte-for-byte like M1.E1.
  (Built: lift, unfold (i01), put on (i02), show; S11–S16 authored in-session; `renderers/ugc_renderer.py` shares
  the LBN projection with the anime renderer and adds a `ugc` block (hand roles, object-state tracks, proven
  affordances, enables, frame parts); S16 picks the renderer by genre; `render.txt` written.)

## M5.5 — clip chaining
- [x] S02 accepts an optional previous envelope; S06 starts from its final states; S07 from its active contacts;
  S05 reads its unresolved causes; `chained_from` fields filled; cross-clip continuity tests (damage, props, camera).
  (Built: `--chain-from envelope.json` (pipeline and CLI). S02 alone reads the previous clip (current kernel, compiled
  through S07, same world, else CHAIN_STALE / CHAIN_INCOMPLETE / CHAIN_WORLD) and writes `scene.chained_from`: end
  states, contacts still open, unresolved causes (non-hold beats that cause nothing), last shot. S06 starts from the
  end states (a first requirement must agree); S07 re-opens the carried contacts at t=0 (`chain_c<n>`, beat `chain`);
  S05 records `quadrant.carried_causes`; S15's first shot cannot open and obeys the axis and jump-cut rules against
  the previous last shot; S04's packet shows the chain; the render adds a `chained_from` block.)

## M3.5 — face (S14 facial, L4d) → done when the UGC demo and a live-action example render faces in words (done)

Order of work: R (renumber, no content change) → F.1–F.6 (the facial step) → F.7–F.8 (camera and render read it) →
F.9 (examples) → F.10 (docs). One commit per block; the gate passes after each.

### R — renumber (F2), one commit, zero content change
- [x] R.1 `kernel/layer_order.yaml` 1.6: effort S15, camera S16, render S17, post_generation S18;
  `kernel/version.py` LAYER_ORDER_VERSION; regenerate `schemas/cinematic_ir.schema.json` (group defs follow).
- [x] R.2 Rename modules `p14_effort`→`p15_effort`, `p15_camera`→`p16_camera`, `p16_render`→`p17_render`
  (pass-history names follow the step ID); update STEP constants, pipeline imports, tests.
- [x] R.3 Plan schemas: `effort_plan` step const S15, `camera_plan` S16, `frame_parts_plan` S17; step numbers in
  schema titles/descriptions; log every changed schema (reason "F2 renumber").
- [x] R.4 Step numbers in prompts, code docstrings, library header comments (library log entries); provenance
  `basis` texts and log reasons stay as written (historical records).
- [x] R.5 Examples: re-seal the S15–S17 packets of all three examples (the packet carries `step_id`), regenerate
  envelopes. **Proof of no content change: all three `render.txt` files are byte-identical before and after.**
- [x] R.6 `docs/layer_dependency.md` decision rows F1–F4; graph_types, HANDOFF, AGENTS, docs/reference regenerated.
  (Done: 37 files shifted S14–S17 → S15–S18 (task labels like S16.6 untouched), modules renamed p15_effort,
  p16_camera, p17_render, layer order 1.6, owner invariant names S17, plans re-bound (only packet_sha256 and step_id
  moved: S04 for the owner rule text, S15–S17 for the step ID); all three render.txt byte-identical.)

### S14 facial (L4d, authored; ugc_ad + live_action)
- [x] F.1 DAG 1.7: node `facial` {step_id S14, band L4d, when [ugc_ad, live_action], depends_on [brief, causal,
  kinematic, motion], writes [/nodes/facial, /edges/facial_transition]}; edge endpoints facial → facial; camera
  and render gain `facial` as a dependency (skipped where inactive, like S08–S10); effort does not.
  Tests: anime order unchanged; ugc_ad and live_action place S14 between S13 and S15.
- [x] F.2 Libraries (draft, library log, each with a schema):
  - `library/facs_action_units.yaml`: the FACS action units (number, name, face region, may be one-sided,
    render words for the action and for its absence, e.g. AU12 "lip corners pulled up" / "no smile"); intensity scale
    A–E with words (trace, slight, marked, severe, maximum). Basis: FACS (Ekman, Friesen & Hager 2002) unit names;
    the words are drafted.
  - `library/facs_asymmetry_bounds.yaml`: maximum left/right difference per AU in intensity steps; named patterns
    (AUs, rule, valence and arousal ranges on −1…1) — draft until F.2b.
  - `library/emotion_families.yaml`: emotion labels → family, valence and arousal ranges, typical AUs
    (informational), and the word bands the render uses for valence and arousal (F4).
- [x] F.2b Verify the asymmetry and micro-expression claims against published sources (no paid API); record each
  source in the library file's basis; anything unsupported stays a labelled draft value.
  (Done 2026-10-11: deliberate expressions are more asymmetric than spontaneous ones (Ekman, Hager & Friesen 1981;
  Hager & Ekman 1985, via summaries); contempt = one-sided AU12 + AU14 on the same side (Ekman & Friesen 1986;
  Matsumoto & Ekman 2004); micro-expressions < 500 ms with onset < ~260 ms (Yan et al. 2013); FACS 2002 A-E words and
  R/L/U/A side notation. No source gives per-unit maximum asymmetry: `max_step_difference` stays the concept's draft.)
- [x] F.3 `face_profile` on archetype cards (schema change, logged): visible regions (brows, eyes, cheeks, nose,
  mouth, jaw), dominant side (left | right | none), emotional range (families), resting valence/arousal. Draft
  profiles for every archetype card; S02 copies it onto the entity (brief schema). A ugc/live-action entity with no
  profile is refused at S14 (FACE_PROFILE_MISSING).
- [x] F.4 `schemas/graphs/facial_plan.schema.json` (authored, one node per slot): `slot, aus[], inactive_aus[],
  valence, arousal, emotion_label, display_rule (genuine | masked | suppressed | posed), gaze_target, salience,
  onset (rapid | slow | hold | micro), onset_frames, description`. An AU is either symmetric `{au, intensity,
  bilateral: true}` or one-sided `{au, left_intensity, right_intensity, bilateral: false, asymmetry: {dominant_side,
  magnitude, pattern | null}}`. `facial_graph.schema.json`: nodes plus derived words; edges `facial_transition`
  `{from, to, onset, onset_frames, trigger}` (trigger = the beat's incoming causal edge, or null). Logged.
- [x] F.5 `compiler/passes/derived/p14_facial.py` + `planner/prompts/facial_acting.txt`: packet = slots (beat, role,
  label, action), the kinematic cues the face reads (tension, breathing, strain, release), head pose (root rot, HD
  and NK bones, heading), what each beat reacts to (incoming causal edges), face profiles and the three libraries.
  Registered as authored (pipeline + replan trigger).
- [x] F.6 `validators/facial_validator.py` (one test per rule):
  - FACS_AU — unit in the library; intensities A–E; exactly one of the symmetric or one-sided forms; bilateral flag
    agrees with the form.
  - FACS_ASYMMETRY — magnitude = the left/right step difference; dominant side = the stronger side; within the
    unit's bound; a named pattern's rule holds.
  - FACS_OCCLUSION — every active unit's region is visible in the entity's face profile.
  - FACS_CONTRADICTION — no unit is both active and listed inactive.
  - VALENCE_RANGE — valence and arousal in −1…1; the label exists and is in the archetype's emotional range; for a
    genuine display, valence and arousal sit inside the label's ranges.
  - FACIAL_KINEMATIC — genuine display only: arousal ≥ 0.5 needs kinematic tension moderate or high; arousal ≤ −0.5
    needs relaxed or moderate (draft thresholds).
  - FACIAL_GAZE — gaze target is a scene entity or prop, `camera`, or `none`.
  - FACIAL_TRANSITION — `hold` keeps the previous node's units; `micro` lasts at most 0.5 s in frames at the scene fps.
  - FACIAL_COVERAGE — one node per slot.
  Derived: each node's words from the libraries; transition edges between an entity's consecutive slots.

### Camera and render read the face
- [x] F.7 Camera (S16) checks, only when the packet carries faces (anime packets unchanged):
  - FACE_FRAMING — a face with salience `carries_beat` is shown by a shot covering its beat at a scale that shows the
    head (not an insert on another part), and the face turns toward the camera: the angle between the head heading
    (root heading + NK/HD yaw) and the direction to the camera is under 90°.
  - FACE_ASYMMETRY_VISIBLE — a one-sided unit's dominant hemiface faces the camera, unless the shot is frontal
    (within `frontal_deg` of the face, new draft value in camera_grammar, logged).
  (Built: the camera packet carries the faces only for scenes that have them (anime packets unchanged except the new
  grammar value); head heading = root heading + neck and head yaw (shared helper); every camera plan re-bound, the
  anime render.txt files byte-identical.)
- [x] F.8 Render (S17), words only (F4): each actor row gains `FACE:` (unit words with intensity words and which side
  is stronger), `NOT:` (inactive-unit words), the feeling (label + valence/arousal word bands), display rule and gaze
  in words. No AU codes and no valence/arousal numbers in the text (test: no `\bAU\d+` in any render).
  F.8b live_action gets its own genre block (frame parts under `frames`, not `anime`) via the shared projection.
  (Built with S14: rows gain `FACE` / `FACE (carries the beat)`, `NOT`, the feeling in word bands, display rule,
  gaze by render label, and the authored description, which the validator keeps free of unit codes. F.8b: `renderers/live_renderer.py`
  puts live-action frame parts under `frames`.)

### Examples and docs
- [x] F.9 `examples/ugc_glasses_demo/`: facial plan for its four slots (the reveal carries the beat with a genuine,
  slightly one-sided smile); camera plan re-sealed and checked by F.7; render.txt updated.
- [x] F.9b New `examples/live_action_standoff/` (wizard and knight, existing cards and world): 3–4 beats S04–S17
  authored in-session, including one masked face and one one-sided expression; render.txt for the owner.
- [x] F.10 graph_types row S14 Facial; HANDOFF; docs/reference regenerated; layer_dependency rows.
  (Done: the glasses demo and `examples/live_action_standoff/` (wizard vs knight, 4 beats: the knight's glare, the
  wizard's one-sided contemptuous smirk, a suppressed fear micro-expression, the set jaw) compile through S17 with
  faces in words; render.txt written for the owner. M3.5 complete.)

## M8 — structured-prose prompts + DAG conformance → done when every mandatory and required map row passes
Spec and codes: [M8_DAG_PROSE.md](M8_DAG_PROSE.md).
- [x] K1 knowledge-DAG map: frozen copy, 109-row map, coverage test, kernel log guards the map
- [x] M8.0 plan + owner decisions O1-O4 recorded in the map
- [x] M8.1 staff geometry atoms (direction, level, fold, support words, turn signs); levels follow the owner's
  laban-notation lookup (mid inside +-45 degrees, place within 10 of vertical)
- [x] M8.2 prose renderer: SCENE, MOVEMENT LANGUAGE, FORMAT, staff in four modes, RULES, NEGATIVES; four examples
  carry `prose_<mode>.txt` (render.txt byte-identical); render schema 1.1 logged
- [x] M8.3 remaining sections (implied guidance, motion control, spatial anchors, props, causal links, camera, genre)
  + render intent and time-bounded rules (lasting effects, end states, spans, strike separation, six T10 laws)
- [x] M8.4 prompt validator (37 semantic codes) + map `codes`/`gaps` + conformance test: the four examples build
  S01-S17, all 16 prose prompts pass except one KNOWN owner-source contradiction (reference_fight 'dust ring' vs
  'no ring', audit X29); every code fires on its break. Mandatory 17/27 enforced, required 9/15.
- [x] M8.5 named fields in LBN-2.4 actor rows (O9)
- [x] M8.6 joint limits (O11, O7): library/joint_limits.yaml + S13 JOINT_LIMIT; 47 example values normalised · [x] M8.7 teleport + substitution (O12): S04 TELEPORT (25 m/s), event_type substitution (reference b09) · [x] M8.8 prop p/v + gravity (O8): S04 prop_samples + PROP_KINEMATICS; both prompts print p/v · [x] M8.9 golden passes conformance, KNOWN emptied (O10): fx 'dust ring' -> 'dust burst'
- [x] M8.10 per-prompt DAG checklist (O13, O14): `validators/checklist.py` judges every prompt (LBN-2.4 + four prose
  modes) on all 84 rows (PASS / FAIL / NOT CHECKED / N/A with evidence, a section a code reads must be present) plus
  the union of the five; `examples/<name>/checklist.md` next to the prompts, kept current by tests/test_checklist.py;
  `python -m validators.checklist --gate` refuses any prompt with FAIL or NOT CHECKED. Day one: 0 of 20 prompts are
  deliverables; prose 37 PASS / 0 FAIL / 41-42 NOT CHECKED, LBN 4-6 PASS / 44-47 FAIL; union 40 PASS (reference fight).
- [ ] M8.11+ close the rows in the queue's order: causes, camera, body and props, density and format, the rest. Derivable: PROP_TWO_HOLDERS (C5, S07), POST_CONTACT_MISSING (C21),
  PHRASING_MISSING (LMA, T6), MOMENTUM_MISSING (C22, T10), CHAIN_ORDER (KC), ANTICIPATION_MISSING (KF),
  SHOT_TRANSITION_MISSING (C25), PROP_KINEMATICS (C31). Need the owner: JOINT_LIMIT ranges (BIO, T7; the DAG gives
  none), TELEPORT speed bound and the substitution exemption (T10). By design partial: T3/T4 (superseded orders),
  T5 (O4), C26 (14 unnamed F2 states).

## M6 — deferred tooling
- [ ] `kernel_extraction/` synergy_matrix, bridge_detector, layer_analyzer, kernel_compressor, ablation_runner
  (ablation never renders; the owner renders).

## M7 — when a target video model is chosen and authorised
- [ ] S17 `validation.post_generation` object `{run_at, video_ref, checks[pose, object, state, affordance],
  verdict, replan_triggered, replan_scope, replan_target}` + `validators/post_generation/`.
- [ ] `renderers/conditioning/` pose, depth, flow, HOI emitters; live-action skeletal export.
- [ ] Per-model compression renderer (a separate pass over the full S16 output; the core never compresses).
