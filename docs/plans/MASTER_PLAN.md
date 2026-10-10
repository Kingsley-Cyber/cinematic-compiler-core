# cinematic-compiler — master build plan

Merges the owner's conceptual plan (repo tree, layer DAG and corrected table, envelope, graph table, quadrants,
camera subdivisions, key pose / frame part / Laban / implied pose) with the route already built.
Detailed S04–S07 specs: [s04-s07-l1-l2.md](s04-s07-l1-l2.md). Layer DAG: `kernel/layer_order.yaml`.
What each graph is for (owner catalog): [graph_types.md](../graph_types.md).

**Built:** S01 intent, S02 query expansion, S03 constraint graph — 167 tests, schema/library/kernel hash logs,
`scripts/check.sh` gate. Current state and open questions: [HANDOFF.md](../../HANDOFF.md).

## 1. The route (one row per step)

Order lives in step IDs; L labels are the owner's names. "Authored" = written in-session by Claude from a
hash-bound packet (no paid API), then checked; "derived" = deterministic code, invents nothing.

| Step | Owner label | Node group | Edge group | Depends on (owner table) | Made by | Status |
|---|---|---|---|---|---|---|
| S01 | L0 | `/intent` | — | user query | derived (regex) | built |
| S02 | L0.5 | entities, props, surfaces (+ `/scene`) | — | S01 | derived (library cards) | built |
| S03 | constraint (was L1.5) | constraints (+ `/invariants`) | constraint_application | S02 | derived (kernel + cards) | built |
| S04 | L1 | beats | temporal | S03 | **authored** beat plan (LLM call #1) | planned M1 |
| S05 | L1 | (beats, shared) | causal (+ `/quadrant`) | S04 | derived | planned M1 |
| S06 | L2 | states | state_transition | S05 | derived (replay) | planned M1 |
| S07 | L2 | contacts | contact | S06 | derived (lifecycle) | planned M1 |
| S08 | L2.5 UGC | hand_role | hand_role_transition | S07 | authored + checks | M5 |
| S09 | L2.6 UGC | object_state | object_state_transition | S08 | authored + checks | M5 |
| S10 | L2.7 UGC | affordance | affordance_dependency | S09 | authored + checks | M5 |
| S11 | L4a | kinematic | kinematic_transition | S07 (+S08–S10 if UGC) | authored | M2 |
| S12 | L4b | bartenieff | bartenieff_transition | S11 | authored | M2 |
| S13 | L4c | motion (key poses) | motion | S12 | authored key poses + derived quaternion/trajectory | M2 |
| S14 | L5 | efforts | effort | S13 | authored | M3 |
| S15 | L5.5 | camera | camera | S13 + S14 | authored + camera rules | M3 |
| S16 | L6 | render | — | all | derived projection + authored frame-part directives | M4 |
| S17 | L6.5 | — (`validation.post_generation`) | — | S16 + video | deferred: needs an authorised video model | M7 |

## 2. Conceptual plan → repo (what changed, and why)

| Conceptual plan says | In the repo | Why / decided by |
|---|---|---|
| Fractional layer numbers order the layers | Step IDs S01–S17 order them; L labels are names | owner |
| Constraint at L3 / L3a / L1.5 | S03, after S02, before the event graphs, checked at every later step | owner |
| Camera L4.5 before effort L5 | Effort (S14) then camera (S15, label L5.5) | owner |
| `actors` group | `entities` (definitions at L0.5); states/contacts at L2 | owner |
| `layer` / `step` keys | `band` / `step_id` everywhere | owner |
| p02_temporal = temporal + causal; p03_entity_tracking = state + contact | One pass per graph, named from its step ID (p04_temporal … p07_contact) | owner (step IDs) |
| UGC: object_state and affordance both from contact (earlier table) | Owner's latest table chains them: S08 → S09 → S10 | owner; **layer_order 1.5 change, first M1 commit** |
| Camera depends on L2 + L4a + L4c | Latest table: S13 + S14; S15 still reads states, contacts and kinematic through them | owner |
| "14 composable subdivisions" (13 listed) | 13 subdivisions + required `motivation` | owner_default |
| Laban graph fields "effort, space, shape, weight, time, flow" | LMA kept distinct: Effort = weight, time, space, flow (two poles each); Shape and Space separate; Body/Bartenieff at S12 | owner_default (LMA concept) |
| Bartenieff list includes "spiral" | Not one of the six total-body-connectivity patterns; kept as a labelled `cpcs:` extension, not native LMA | owner_default (extension rule) |
| Kernel = v2.3 + v2.4 intersection | 68 shared controls quoted from both LBN prompts; per-item scope (draft) | owner; built |
| Branching scored by quadrants | Linear only for now; branching score 0 | owner |
| Beat planner = LLM call #1 | Authored in-session, packet-hash bound | owner (no preference) |
| Post-gen block | `validation.post_generation` (verdicts, not atoms); object shape lands at S17 | owner |
| Key pose / frame / frame part / Laban / implied pose | Key poses authored at S13; frame-part directives authored at S16; Laban at S14; frames and implied poses never authored — constrained by S11 + S12 + S14 | owner |

## 3. Machinery every step reuses

1. **Authoring loop** (S04, S08–S15, S16 frame parts): `prepare` writes a canonical packet (sha256) →
   Claude authors JSON in-session → `submit` checks the packet hash, schema and semantic gates → the pass writes
   only its groups. A failed gate allows at most 2 targeted re-authoring attempts; each is recorded in
   `provenance.replan_count` / `replan_layers`. Authored files live with the scene (`examples/<scene>/`).
2. **Gates:** schema, determinism (byte-identical across processes), completeness, non-invention, write scope,
   plus the step's own checks.
3. **Control:** schema log, library log, kernel log; `scripts/check.sh` before each commit; graft and graphify
   refreshed; one commit per step.
4. **Quadrant and strata** (S05): causal score (branching 0, parallel effects, prerequisites) + style score →
   quadrant A–D → strata. S16 uses them to decide how much graph and prose to emit (A full/full, B full/medium,
   C minimal/full, D minimal/minimal). "Load-bearing" (stratum 4) is a CLI/intent flag, default off.
5. **Provenance:** the pipeline records pass history; timing fields are kept out of the determinism comparison.
6. **Library (all drafted by Claude, `status: draft`, hash-logged):** per step in section 4.
7. **Golden fixtures:** the owner's reference courtyard fight (both LBN prompts) is the anime golden: compiling
   it must reproduce every kernel item and every reference-fight item in the S16 output. Plus
   `wizard_vs_superman_query.txt` and the UGC glasses smoke test.

## 4. Steps S04–S17

**S04–S07 (M1)** — as in [s04-s07-l1-l2.md](s04-s07-l1-l2.md), plus from the conceptual plan:
beat participants carry an archetype `mode` (L1 capability-mode selection); `mode_coherence` (mode is in the
archetype card) and `mode_transition` (a mode change needs a triggering beat) run at S04.

**S08 hand role (UGC).** Nodes: interaction `{id, beats, agent_hand, support_hand, grip_types, role_invariant}`;
edges `role_preserved` with `handoff_event`. Checks: the agent hand has the grip contact; roles hold through the
interaction; grip types come from the object card and `library/grip_types.yaml`. Library: grip_types,
role_templates.

**S09 object state (UGC).** Nodes: object-state `{id, object, state_name, from_t, to_t}`; edges `transitions_to`
with `trigger_contact`. Checks: values from the object card; every transition is triggered by a hand contact on
that object.

**S10 affordance (UGC).** Nodes: `(object, action)` `{preconditions, postconditions, typical_duration}`; edges
`requires`. Checks: every functional verb in the beats has its preconditions true before and postconditions true
after. Library: affordances (clothing, food, electronics, cosmetics).

**S11 kinematic (L4a).** Nodes per actor per beat: support, balance, loading, bracing, yielding, weight transfer,
tension, release, strain, restraint, breathing. Checks: support agrees with S06 support state and S07 support
contacts; cue values from `library/kinematic_cues.yaml`. This is what constrains the implied pose.

**S12 Bartenieff (L4b).** Nodes per actor per beat: connectivity pattern (breath, core-distal, head-tail,
upper-lower, body-half, cross-lateral; `cpcs:spiral` extension), developmental pattern, intent, body mode.
Checks: values from the vocabulary; body mode from `library/body_modes/`.

**S13 motion (L4c).** Key pose per beat in the LBN key shape:
`{beat, t, name, pos, rot, bones{Sp, LUL, RUL, LL, RL, LA, RA, LFA, RFA, HD, NK}, axis_declaration, description}`
(joint names from the kernel key); edges `follows` with `axis_declaration` and `slerp_params`. Derived:
quaternion conversion (p23) and root trajectory (p24). Checks: all 11 joints present; Euler degrees XYZ (kernel);
the axis declaration matches the root rotation change; contacts and support agree with pose height. Needs Q1 and Q2.

**S14 effort (L5).** Effort intervals per actor:
`{beats, effort{weight, time, space, flow}, shape, space, intensity, effort_mode}`; edges `overlaps`. Checks:
values from `library/laban_vocabulary.yaml`; intervals cover the actor's beats; effort mode from
`library/effort_modes/`. LMA words only here, never written into a notation column as native.

**S15 camera (L5.5).** Camera beat per beat: `{at, action_beat, motivation{kind, ref}}` plus 13 required
subdivisions (framing, angle, position, movement, movement quality, support, relation to action, lens, focus,
composition, playback, blur, editing). Motivation kind: beat type, entity focus, contact event, effort quality,
spatial geometry, narrative intent, genre convention — its `ref` must resolve. Edges: shot-to-shot editing and
continuity. Checks: 180-line (axis), camera–kinematic coupling (frames what changes in the beat),
continuity, genre conventions, intent weighting (impact, reveal, emotion, spatial, rhythm, product). Library:
camera_grammar, camera_subdivisions, camera_tempo, camera_idioms, camera_conventions.

**S16 render (L6).** Derived projection to the anime text prompt in the LBN-2.x structure (variant, fps, dur, ax,
key, negative, laban, actor key tracks, prop tracks, cam, anime{impact, smear, speedlines, holds, fx, ink},
rules); live-action and UGC text after. Authored frame-part directives (smear scoped to the declared limb or prop,
speedlines, holds, ink). `nodes.render` items `{target, text, sha256, coverage}`; coverage proves every applied
constraint reaches the rules or negative block. Pose/depth/flow/HOI emitters and skeletal export deferred.
Library: fx_presets, style_tags, negatives per genre.

**S17 post-generation (L6.5).** Deferred until a video model is authorised. Block shape per owner: `run_at,
video_ref, checks[pose, object, state, affordance], verdict, replan_triggered, replan_scope, replan_target`.

## 5. Milestones

| M | Steps | Done when |
|---|---|---|
| M1 | layer_order 1.5 (UGC chain), S04–S07 | courtyard wizard-vs-acrobat compiles through S07 |
| M2 | S11–S13 (+ quaternion, trajectory) | key poses for the example validate |
| M3 | S14–S15 | effort and 13-part camera beats validate |
| M4 | S16 anime + quadrant density | reference courtyard fight round-trips; first full prompt (owner renders) |
| M5 | S08–S10 + UGC render | glasses smoke test compiles |
| M6 | CLI, replan trigger, kernel-extraction extras (synergy, bridges, ablation — never renders) | `cinematic compile` end to end |
| M7 | S17 + conditioning emitters | when a video model is authorised |

Anime path first (it matches the reference prompt the owner reports renders well); UGC after.

## 6. Open questions (only these; everything else follows the plan or a recorded default)

1. **Axis declarations contradict the kernel frame.** The L4c box says "X=backflip, Y=cartwheel, Z=spin", but the
   kernel is `Y_up` with fighters facing `+Z`: about Y is a spin and about Z (forward) is a cartwheel.
2. **Euler XYZ interpretation** for the quaternion pass: intrinsic or extrinsic, and which handedness
   (the earlier notation work used +X = performer's left).
