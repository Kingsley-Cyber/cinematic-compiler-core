# Layer order: verification, gaps, impact, cascade, plan map, simulation (2026-10-11)

The owner gave a corrected layer order (L0 → L6.5) and asked whether it was ingested as a trickle-down dependency.
Everything below was checked against `kernel/layer_order.yaml` (version 1.7), the passes and the validators on disk at
`8125483` (pushed). Rule: verify, then gap, then impact; never paper over.

## Phase 1 — Verification

**1. Is the corrected order the repo's order?** Yes, step for step, with one extra layer in the repo:

| Corrected order | Repo step (`kernel/layer_order.yaml`) | Nodes · edges written | Depends on (declared, enforced) |
|---|---|---|---|
| L0 Intent | S01 `intent` (band L0) | `/intent` document · none | — |
| L0.5 Query expand | S02 `brief` (L0.5) | `/nodes/entities`, `/nodes/props`, `/nodes/surfaces`, `/scene` · none | intent |
| L1.5 Constraint | S03 `constraint` (band "constraint") | `/nodes/constraints`, `/invariants` · `/edges/constraint_application` | brief |
| L1.1 Temporal | S04 `temporal` (L1) | `/nodes/beats`, `/scene/duration_s` · `/edges/temporal`, `/edges/beat_constraint` | brief, constraint |
| L1.2 Causal | S05 `causal` (L1) | beats shared, `/scene/quadrant` · `/edges/causal` | temporal |
| L2.1 State | S06 `state` (L2) | `/nodes/states` · `/edges/state_transition` | temporal, causal |
| L2.2 Contact | S07 `contact` (L2) | `/nodes/contacts` · `/edges/contact` | temporal, causal, state |
| L2.5 Hand role (UGC) | S08 `hand_role` (L2.5), `when: [ugc_ad]` | `/nodes/hand_role` · `/edges/hand_role_transition` | contact |
| L2.6 Object state (UGC) | S09 `object_state` (L2.6), UGC | `/nodes/object_state` · `/edges/object_state_transition` | hand_role |
| L2.7 Affordance (UGC) | S10 `affordance` (L2.7), UGC | `/nodes/affordance` · `/edges/affordance_dependency` | object_state |
| L4a Kinematic | S11 `kinematic` (L4a) | `/nodes/kinematic` · `/edges/kinematic_transition` | state, contact, UGC steps, constraint |
| L4b Bartenieff | S12 `bartenieff` (L4b) | `/nodes/bartenieff` · `/edges/bartenieff_transition` | kinematic |
| L4c Motion (Euler) | S13 `motion` (L4c) | `/nodes/motion` · `/edges/motion` | kinematic, bartenieff |
| *(not in the corrected list)* | S14 `facial` (L4d), `when: [live_action, ugc_ad]` | `/nodes/facial` · `/edges/facial_transition` | brief, causal, kinematic, motion |
| L5 Effort (Laban) | S15 `effort` (L5) | `/nodes/efforts` · `/edges/effort` | motion |
| L5.5 Camera | S16 `camera` (L5.5) | `/nodes/camera` · `/edges/camera` | motion, effort, facial |
| L6 Render | S17 `render` (L6, projection) | `/nodes/render` · none | every layer above |
| L6.5 Post-gen validate | S18 `post_generation` (L6.5) | `/validation/post_generation` · none | render |

Enforcement on disk: step ids rise with build order (`validators/layer_dependency_validator.check_layer_order`);
`depends_on` becomes ordering edges and an unconditional dependency may not be inactive (`planner/dependency_graph.edges`);
a conditional step's dependencies must run in every modality it runs in; each pass may write only its declared paths
(`check_pass_writes`, WRITE_SCOPE); `validated_by: constraint` makes S03 run before every step that names it
(`ORDERING_VALIDATORS`). The pipeline runs the steps in this order and the gate recompiles every example through it.

**2. Did I ingest it?** In the code, yes: every slice today ran through this order (`compiler/pipeline.run`;
`compiler/rebind` walks `load()["nodes"]` in order). In my written outputs, partly. The deconfliction plan quotes the
order correctly (section 3: "S01 intent, S02 brief, S03 constraint, S04 temporal (authored beats), S05 causal, S06
state, S07 contact, S08 hand role (UGC), S09 object state, S10 affordance, S11 kinematic, S12 Bartenieff, S13 motion
(Euler keys), S14 facial, S15 effort (LMA), S16 camera, S17 render"), but **several fixes were placed without the
trickle-down rule** (a step can only check data from its own layer or above):

| Plan fix | Where I put it | Why that breaks the order | Correct layer |
|---|---|---|---|
| FP.1 Bartenieff agrees with the pose | S12 check "reading S13 keys" | S12 (L4b) runs before S13 (L4c); the keys do not exist yet | S13 |
| FR.4 launch before an aerial turn | "S11 or S13" | turns are declared at S13; S11 cannot see them | S13 |
| F4.4 IDLE_FIGHTER | "S04 or S15" | it reads effort actions, which exist from S15 | S15 |
| FP.12 silhouette | no step named | needs world joint points (S13) and the camera (S16) | S16 |
| F4.5 CHAIN_ORDER | S12 "checks proximal to distal" | if it compares against the pose, the pose is S13 | S13 (offsets authored at S12) |
| F9.3 anticipation, F9.4 reaction | no step named | they read poses (S13) and efforts (S15) | S15 |

**3. Do my outputs reflect the seven facts?**

| Fact | Repo | My outputs |
|---|---|---|
| Constraints before beats | S03 before S04; the S04 packet carries every constraint with its targets (`planner/beat_planner.py:37`) | yes (section 3 order) |
| Camera after effort | S16 depends on effort; the camera packet reads efforts (motivation `effort_quality`) | yes |
| Temporal and causal separate | S04 and S05, separate edge groups on shared beats | yes |
| Every layer has nodes and edges | no: L0, L0.5, L6 and L6.5 have no edge group; L1.2 has no node group of its own | not stated by me, and the corrected list itself gives render and post-gen "(none)" |
| UGC layers conditional | `when: [ugc_ad]` on S08-S10 | partly (S08 labelled UGC; S09, S10 not) |
| Entity registry explicit at L0.5 | `/nodes/entities` written by S02 | implied ("S02 brief"), not named |
| Render nodes explicit at L6 | `/nodes/render` | yes |

**4. Differences, not papered over.** (a) The repo has L4d facial (S14, live action and UGC; owner decisions F1, F2);
the corrected list omits it. (b) The corrected list labels constraint L1.5 and temporal L1.1, numbers that sort the
other way; the repo's step ids carry the order (S03 before S04), so the sequence agrees. (c) "Every layer has nodes AND
edges, no exceptions" contradicts the list's own "render + (none)" and "report + (none)". (d) Rule 9 ("if the golden
fails a new check, the check is wrong") contradicts O26 (the owner kept O7, O10, O17, O18, O21, which fix the golden
where it contradicts its own words or the DAG). Both (c) and (d) go to the owner.

## Phase 2 — Gap analysis (repo as it exists)

| Layer | Exists | Location | Nodes | Edges | Order | Gap | Severity |
|---|---|---|---|---|---|---|---|
| L0 Intent | yes | `p01_intent.py`, `planner/intent_parser.py` | document only | none | correct | GAP-01, GAP-02 | high |
| L0.5 Expand | yes | `p02_brief.py`, `planner/query_expander.py` | present | missing | correct | GAP-03 | medium |
| L1.5 Constraint | yes | `p03_constraint.py`, `kernel_extraction/control_inventory.py` | present | present | correct | GAP-04, GAP-05 | high |
| L1.1 Temporal | yes | `p04_temporal.py`, `planner/beat_planner.py`, `planner/dynamic_beat_validator.py` | present | present | correct | GAP-06, GAP-07 | critical |
| L1.2 Causal | yes | `p05_causal.py`, `validators/cause_reason.py` | shared beats | present | correct | GAP-08 | medium |
| L2.1 State | yes | `p06_state.py`, `solver/prop_state_machine.py`, `validators/continuity_validator.py` | present | present | correct | GAP-09 | medium |
| L2.2 Contact | yes | `p07_contact.py` | present | present | correct | GAP-10 | high |
| L2.5 Hand role (UGC) | yes | `p08_hand_role.py` | present | present | correct, conditional | none against the list | — |
| L2.6 Object state (UGC) | yes | `p09_object_state.py` | present | present | correct, conditional | none against the list | — |
| L2.7 Affordance (UGC) | yes | `p10_affordance.py` | present | present | correct, conditional | none against the list | — |
| L4a Kinematic | yes | `p11_kinematic.py` | present | present | correct | GAP-11 | high |
| L4b Bartenieff | yes | `p12_bartenieff.py` | present | present | correct | GAP-12 | medium |
| L4c Motion | yes | `p13_motion.py`, `solver/euler_solver.py` | present | present | correct | GAP-13 | high |
| L4d Facial | yes (repo only) | `p14_facial.py` | present | present | correct, conditional | GAP-18 | low |
| L5 Effort | yes | `p15_effort.py` | present | present | correct | GAP-14 | high |
| L5.5 Camera | yes | `p16_camera.py`, `validators/camera_validator.py` | present | present | correct, sequential | GAP-15 | high |
| L6 Render | yes | `p17_render.py`, `renderers/*` | present | none (as listed) | correct | GAP-16 | critical |
| L6.5 Post-gen | declared only | `kernel/layer_order.yaml` S18; no pass | missing | none (as listed) | correct | GAP-17 | low (O40) |
| all layers | — | `layer_order.yaml` `validated_by` | — | — | — | GAP-05, GAP-19 | high / low |

GAP-01 — Layer L0 Intent. Current: S01 parses duration, fps, genre, setting, entities and props; it records
"geometry_anchors" as missing, so the query's literal starts ("A starts ABOVE the frame, falling from y=10"), counts and
pillar height constrain nothing. Target: literal anchors and counts parsed with evidence spans. Missing: `parsed.starts`,
`parsed.counts`, `parsed.anchors`. Severity: high (renders F10 opening, F12 count). Files: `planner/intent_parser.py`,
`schemas/.../intent`.

GAP-02 — Layer L0 Intent. Current: a document at `/intent`, no node or edge group. Target per rule 10: nodes and edges.
Missing: both, by design. Severity: low; owner ruling (Phase 1, difference c).

GAP-03 — Layer L0.5 Expand. Current: entities, props and surfaces as nodes; archetype `equipment` (who carries which
prop) is dropped, so a stowed prop cannot say whose gear it is (seen in M8.12b). Target: an edge group. Missing:
`/edges/equipment` (entity → prop, from the cards) and optionally `/edges/placement` (prop or entity → surface at the
start). Severity: medium. Files: `p02_brief.py`, `planner/query_expander.py`, `kernel/layer_order.yaml` (S02 writes).

GAP-04 — Layer L1.5 Constraint. Current: constraints reach S04 only through the authoring packet; `beat_constraint`
edges record which constraints apply to a beat's bodies and props; nothing checks that a beat obeys a constraint's rule
(the rules are prose, e.g. "B never stands after 9.0"). Target: constraints shape and bind the beats. Missing: a
machine form for checkable constraints (subject, property, value, window) and a check at S04/S06. Severity: high.
Files: `p03_constraint.py`, `kernel/invariants.yaml` form, `planner/dynamic_beat_validator.py`, `p06_state.py`.

GAP-05 — All layers. Current: `validated_by: [schema, invariants, constraint]` on S04-S17 is enforced as an ordering
(S03 first) and the names are checked against a registry, but no generic `constraint` or `invariants` validator runs per
layer; each step runs its own checks. Target: declared validators execute. Missing: a per-layer constraint pass that
applies GAP-04's checkable constraints to that layer's output. Severity: high. Files: `planner/dependency_graph.py`,
`compiler/pipeline.py`.

GAP-06 — Layer L1.1 Temporal. Current: a contact happens at its beat's end unless marked `at: start`
(`p07_contact.contact_time`); every strike in the reference fight lands 0.4-0.5 s after its pose and impact frame.
Target: one time per hit. Missing: strike, throw and release contacts at their pose (O23) and IMPACT_CONTACT_SYNC.
Severity: critical. Files: the reference plans, `p17_render.check`, `validators/prompt_validator.py`.

GAP-07 — Layer L1.1 Temporal. Current: a possess contact may take a prop resting on a surface while its body has no
support (audit X2/X3, renders R3/R4). Missing: AIRBORNE_PICKUP; the reference b18-b20 re-authored (O18). Severity: high.

GAP-08 — Layer L1.2 Causal. Current: `causes` edges, hard or soft, one per beat (owner: linear), reasons checked.
Missing: the cause-to-effect delay (derivable), `enables`/`blocks`/`triggers` types at S05 (S10 has `enables` for UGC).
Severity: medium. Files: `p05_causal.py`, `prose_renderer._causal`.

GAP-09 — Layer L2.1 State. Current: actor support, posture, possession, condition, location; prop and surface states.
Missing: wounds, costume damage, exhaustion (O44); the reference fight never sets surface damage (O28). Severity: medium.
Files: `kernel/state_vocabulary.yaml` (logged), reference plans.

GAP-10 — Layer L2.2 Contact. Current: type, part, target part, time. Missing: world points (computed at L4c, F5.1),
the striking surface (F3.1), the combat verb (F4.1, O22). Severity: high. Files: Contact schema (beat_plan,
temporal_graph 1.4), `p07_contact.py`, S13 check.

GAP-11 — Layer L4a Kinematic. Current: support plus ten cues per slot; TELEPORT at S04 for speed. Missing: an airborne
body following gravity between keys unless a hang or float is declared (F9.2, O34). Severity: high. Files:
`p11_kinematic.check`.

GAP-12 — Layer L4b Bartenieff. Current: vocabulary, slot coverage, own parts, body-mode coherence. Missing: agreement
with the pose; that check reads L4c and must sit at S13 (my plan put it at S12). Severity: medium.

GAP-13 — Layer L4c Motion. Current: Euler keys, joint limits, declared and named turns, root trajectory. Missing: forward
kinematics and world joint points (F5.1), the derived rotation path (FR.1, printed per O47 as one named turn), the
launch-before-turn check (FR.4, here, not S11). Severity: high. Files: new `solver/forward_kinematics.py`, a
segment-length card (logged), `solver/euler_solver.py`.

GAP-14 — Layer L5 Effort. Current: vocabulary, the eight Laban actions from weight × time × space, effort modes.
Missing: Laban direction against the motion (F9.1, O31), phrasing and drives (FP.6, O43), IDLE_FIGHTER (F4.4, here, not
S04). Severity: high. Files: `p15_effort.check`.

GAP-15 — Layer L5.5 Camera. Current: 13 subdivisions, motivation, coupling, axis, genre cards. Missing: C10's six
rules and three forbidden shots, the arc with the rotation (FR.5, O36), V5's wording. Severity: high. Files:
`validators/camera_validator.py`, `library/camera_conventions/*.yaml`, the reference camera plan.

GAP-16 — Layer L6 Render. Current: LBN-2.4 and four prose modes, 44 prompt codes, the checklist. Missing: the probe
wording rules W1-W4 (O47-O49), IMPACT_CONTACT_SYNC, D9 lines (O19), the one complete prompt (O13). Severity: critical
(every render so far failed on wording the model does not follow). Files: `renderers/prose_renderer.py`,
`validators/prompt_validator.py`.

GAP-17 — Layer L6.5 Post-gen. Current: declared in the order (S18), no pass and no validators. Missing: everything.
Severity: low now (deferred to M7 by O40; it needs a chosen model and API).

GAP-18 — Layer L4d Facial. Current: in the repo, not in the corrected list. Missing: the owner's ruling whether the
corrected list omits it on purpose (anime does not run it). Severity: low.

GAP-19 — All layers. Current: L0, L0.5, L6, L6.5 have no edge group; L1.2 has no node group of its own. Rule 10 says
every layer has both, the list itself says otherwise. Missing: the owner's ruling; GAP-03 is the only edge group with a
known use. Severity: low.

## Phase 3 — Impact analysis

| Gap | Schema | Validator | Pipeline | Render | Golden |
|---|---|---|---|---|---|
| 01 | intent schema: parsed starts, counts, anchors | S04 refuses a start that disagrees with the query | S01 output grows; S04 reads it | A starts where the query says | k_preface items recorded (O17, O21) |
| 02 | none unless ruled | none | none | none | none |
| 03 | scene/entity schema: `/edges/equipment`; layer_order S02 writes | S06 first states may say "stowed on A" | S02 writes an edge group | props in a fighter's gear are drawn on them | no change |
| 04 | constraint item gains an optional checkable form | new CONSTRAINT_BEAT at S04/S06 | S03 output richer; S04/S06 check it | rules like "B never stands after 9.0" hold | golden must declare its checkable rules |
| 05 | none | the declared `constraint` validator runs per layer | pipeline calls it after each step | same as 04 | same as 04 |
| 06 | none (`at` exists) | IMPACT_CONTACT_SYNC (S17, prompt) | S04 contacts move; S06-S17 re-bound | each hit lands on its pose; deflect at 2.5 | golden contact times recorded (O23) |
| 07 | none | AIRBORNE_PICKUP (S07 reads S06 support) | S04 b18-b20, S11, S13 re-authored | A lands by the rope dart and the kunai first | A rows 7.5, 8.0 recorded (O18) |
| 08 | causal edge: optional `type`, derived `delay` | delay printed; types checked | S05 output | causes read with their timing | reasons already rewritten |
| 09 | state vocabulary: wounds, costume, exhaustion (logged) | existing replay checks | S06 replays new effects | B's shoulder wound stays; pillar marked | new effects recorded |
| 10 | Contact: `surface`, `verb` (1.4) | CONTACT_VERB (S04), CONTACT_WORLD (S13) | S04, S07, S13 | "DEFLECT: R foot (sole) > kunai blade" | contacts gain verbs |
| 11 | none | AIRBORNE_BALLISTIC (S11) | S11 check | no floating unless declared | A's airborne keys checked |
| 12 | none | BARTENIEFF_POSE (S13) | S13 check reads S12 | claimed patterns show in the pose | may refuse golden keys → owner |
| 13 | segment-length card (logged); motion graph derived points | CONTACT_WORLD, ROTATION_* , FR.4 (S13) | S13 derives FK | foot meets blade; one named turn | flip/cartwheel already fixed (O18) |
| 14 | none | SHAPE_DIRECTION, PHRASING_MISSING, IDLE_FIGHTER (S15) | S15 checks | B acts between hits | B keys added (O27) |
| 15 | camera plan: optional `arc_deg`; camera cards | C10 rules, CAMERA_ARC (S16) | S16 re-authored (~11 shots) | holds with both bodies, crane and orbit | camera rows deviate from the golden's 21 |
| 16 | render schema unchanged | BODY_HOLD_FRAMES, EMPTY_HAND_UNSTATED, ROTATION_ANGLES_PRINTED, HIDDEN_PHRASING, IMPACT_CONTACT_SYNC, LINE_DENSITY | S17 prose only | wording the model follows (probes) | prose changes; render.txt unchanged unless meant |
| 17 | post-gen report schema | pose, object, state, affordance checks | S18 built | none before render | none |
| 18 | none | none | none | none | none |
| 19 | per ruling | none | per ruling | none | none |

Per-gap detail (schema · validator · pipeline · render · golden):

- **GAP-01:** schema adds `parsed.starts {label: {axis: value}}`, `parsed.counts {noun: n}`; S04 gains START_LITERAL
  (refuses a first anchor that disagrees) and COUNT_CONTRADICTION moves upstream; S01 output grows; the opening and
  counts render as written; golden: preface items already recorded (PREFACE_RECOUNTED), the y=10 start becomes another.
- **GAP-03:** S02 writes `/edges/equipment` (layer_order change, logged); S06's first states read it; renders put stowed
  props on the right fighter; no golden change.
- **GAP-04:** constraint items gain `check: {subject, property, value, from, to}` where a rule is checkable (schema);
  CONSTRAINT_BEAT at S04 and S06 (validator); S03 output richer (pipeline); renders hold the rules; golden: its rules
  declared in checkable form, each passing (a failure there is an owner question, not a silent fix).
- **GAP-05:** no schema change; the declared `constraint` validator runs after S04, S06, S07, S11, S13 and applies
  GAP-04's checkable constraints to that layer's output; pipeline calls it per step; render and golden as GAP-04.
- **GAP-06:** no schema change; IMPACT_CONTACT_SYNC; the reference contacts move to their poses (b05 release 2.0, b06
  deflect 2.5, b10 4.0, b12 4.7, b17 6.6, b19 7.5, b21 8.5); every authored step downstream re-binds; golden records the
  contact times (O23).
- **GAP-07:** AIRBORNE_PICKUP at S07; b18-b20 re-authored with grounded keys; S11/S13 keys for crouch-and-reach; golden
  records A's 7.5 and 8.0 rows (O18).
- **GAP-08:** derived delay on causal edges; printed "(+0.40 s)"; no golden change.
- **GAP-09:** kernel vocabulary (logged); reference effects for B's wound and the pillar marks; printed as lasting rules.
- **GAP-10, 13:** Contact 1.4 (`surface`, `verb`); FK at S13 from the 11 joints and segment lengths; CONTACT_WORLD
  refuses a miss over a tolerance; renders get the contact point and the verb; golden contacts gain verbs and pass.
- **GAP-11:** AIRBORNE_BALLISTIC at S11; anime floats only where declared (O34).
- **GAP-12:** BARTENIEFF_POSE at S13 (interpretation, labelled); if it refuses golden keys, the owner rules.
- **GAP-14:** S15 checks; B's active keys authored (O27).
- **GAP-15:** the reference camera re-authored to the D9 shape in V5's wording; C10 codes at S16.
- **GAP-16:** prose wording rules first (they change every prompt); render.txt unchanged.
- **GAP-17:** M7 only.

## Phase 3.5 — Cascade (✓ = must be re-checked or re-bound; – = unaffected)

| Gap | L0.5 | L1.5 | L1.1 | L1.2 | L2.1 | L2.2 | L4a | L4b | L4c | L4d | L5 | L5.5 | L6 | L6.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 03 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 04 | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 05 | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 06 | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 07 | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 08 | – | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 09 | – | – | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 | – | – | ✓ | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 11 | – | – | – | – | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 12 | – | – | – | – | – | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 13 | – | – | – | – | – | – | – | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 14 | – | – | – | – | – | – | – | – | – | – | ✓ | ✓ | ✓ | ✓ |
| 15 | – | – | – | – | – | – | – | – | – | – | – | ✓ | ✓ | ✓ |
| 16 | – | – | – | – | – | – | – | – | – | – | – | – | ✓ | ✓ |
| 17 | – | – | – | – | – | – | – | – | – | – | – | – | – | ✓ |
| 02 | – | – | – | – | – | – | – | – | – | – | – | – | – | – |
| 18 | – | – | – | – | – | – | – | – | – | – | – | – | – | – |
| 19 | – | – | – | – | – | – | – | – | – | – | – | – | – | – |

Cost: every ✓ step that is authored (S04, S11-S13, S15-S17 for anime; `compiler/pipeline.py:37`) re-binds its packet (`python -m compiler.rebind
--write`), and every example recompiles byte for byte. Risk: an upstream mistake (a wrong contact time, a wrong
constraint) is inherited by every later layer, which is why each slice re-runs the whole gate and keeps render.txt
byte-identical unless the slice means to change it.

## Phase 4 — Plan map

| Gap | Plan item (final plan v1.1, section 9) | Status | Action | Dependency | Risk |
|---|---|---|---|---|---|
| 01 | O16 applicability stage (step 16); O21 opening (step 8) | not started | parse literal starts and counts at S01; START_LITERAL at S04 | intent schema change (logged) | the parser misreads prose; evidence spans required |
| 02 | — | owner ruling | none unless ruled | ruling on rule 10 | — |
| 03 | new item (not in the plan) | not started | `/edges/equipment` at S02 | layer_order change (owner) | layer_order is a kernel file: owner approval |
| 04 | new item (not in the plan) | not started | checkable constraint form + check | GAP-05 | rules that are not checkable stay prose |
| 05 | new item (not in the plan) | not started | run declared validators per layer | GAP-04 | slows the gate slightly |
| 06 | F5.3 (step 2) | not started (next) | contacts at poses + IMPACT_CONTACT_SYNC | W rules (step 1) | rebind of every downstream step |
| 07 | F6.3 (step 3) | not started | AIRBORNE_PICKUP + b18-b20 | F5.3 | crouch-and-reach keys must pass joint limits |
| 08 | FP.4 (step 15) | not started | derived delay printed | F5.3 | none |
| 09 | F6.4, FP.9 (step 15) | not started | vocabulary + effects | — | kernel change (logged) |
| 10 | F3.1, F4.1 (steps 6-7), F5.1/F5.2 (step 6) | not started | Contact 1.4 + FK + CONTACT_WORLD | F5.3 | FK tolerance is an interpretation |
| 11 | F9.2 (step 9) | not started | AIRBORNE_BALLISTIC at S11 | — | anime hangs need declared floats |
| 12 | FP.1 (step 15) | not started; **moved to S13** | BARTENIEFF_POSE at S13 | F5.1 FK helps | interpretive rule |
| 13 | F5.1, FR.1/FR.3 (steps 5-6), FR.4 (step 9, **at S13**) | not started | FK, rotation checks | segment-length card | — |
| 14 | F9.1 (step 9), FP.6 (step 15), F4.4 (step 10, **at S15**) | not started | S15 checks | B keys (O27) | thresholds are interpretations |
| 15 | C10 + FR.5 (step 13) | not started | camera re-authored in V5's wording | F5.3 | 21 → about 11 shots changes golden camera rows |
| 16 | W1-W4 (step 1), IMPACT_CONTACT_SYNC (step 2), O19 (step 12) | not started (first) | prose wording rules | — | none |
| 17 | M7 | deferred (O40) | — | model + API authorisation | — |
| 18 | — | owner ruling | none | — | — |
| 19 | — | owner ruling | none | — | — |

## Phase 5 — System simulation (after every gap is closed; the video description is an expectation, renders judge)

1. **L0 S01** reads the query; writes the Intent Document with literal values and evidence, now including starts
   ("falling from y=10"), counts (two fighters, five props) and anchors (pillar 8 m at z=6); flags what is missing.
2. **L0.5 S02** reads the intent and the cards; writes entities (A lean ninja, B broad ninja), props (kunai, rope dart,
   smoke pellet, shuriken volley, substitution post), surfaces (ground, pillar, canopy) and equipment edges (B carries
   kunai and shuriken; A carries rope dart and smoke pellet); validates coherence.
3. **L1.5 S03** reads entities, props and the kernel; writes constraints (kernel invariants, card rules, the fight's
   rules in checkable form) and `constraint_application` edges to their targets.
4. **L1.1 S04** reads entities, props, surfaces and constraints; the authored beats arrive with strikes at their poses,
   grounded pickups, callbacks and first states; writes beats, temporal and beat-constraint edges; refuses teleports,
   bad props kinematics, vanished bodies seen, airborne pickups, starts that disagree with the query, constraint breaks.
5. **L1.2 S05** reads beats; writes causal edges with reasons and delays; refuses placeholders and reactions before
   their cause.
6. **L2.1 S06** replays effects into states (props known from the first beat, wounds, damage, conditions); refuses
   unknown first states and conflicts.
7. **L2.2 S07** reads beats and states; writes contacts with verbs and surfaces and the lifecycle edges; refuses a holder
   without a grip.
8. **L2.5-L2.7** skipped (anime).
9. **L4a S11** reads states and contacts; writes support and cues; refuses an airborne body that floats undeclared.
10. **L4b S12** writes connectivity, patterns, initiation and timed follow-through.
11. **L4c S13** reads S11-S12; writes keys and the derived world points and rotation paths; refuses joint limits, a
    contact whose points do not meet, a named turn not performed, a launch missing before an aerial turn, a Bartenieff
    claim the pose does not show.
12. **L5 S15** reads keys; writes efforts; refuses a Shape or Space direction the motion contradicts and an idle
    fighter.
13. **L5.5 S16** reads keys, efforts (and faces in live action); writes about 11 shots; refuses C10 breaks and a turn
    without its arc.
14. **L6 S17** projects LBN-2.4 (every number) and the prose (wording rules W1-W4, D9 lines, reasons, camera in V5's
    wording); the checklist judges every row; IMPACT_CONTACT_SYNC holds every hit to one time.
15. **L6.5 S18** (M7): after the owner renders, checks pose, objects, state, affordance against the envelope.

**The final video, as the prompt would ask for it:** A falls into frame from above onto the 8 m pillar top (0.6), runs
down its face and kicks off toward B (1.6); B, kunai in the right hand from the first frame, throws it up at A (2.0);
A's right sole taps the blade at 2.5 and the kunai drops and lies by the pillar; A lands squared up, the rope dart in the
left hand (3.0); B charges with a rising palm (3.4); A vanishes in smoke and the post beside A takes the palm (3.7-4.0);
A reappears behind B (4.4) and drives a knee into B's spine (4.7); one backflip about the side-to-side axis (5.1-5.5);
B, recovering in the air, answers with three shuriken (5.5, callback to the kunai throw); A slides under them into the
pillar (5.9); one cartwheel into a rising elbow (6.3); B catches the elbow and throws A at the pillar (6.6); A pushes off
it (7.0, callback to 1.6), lands by the rope dart, retakes it and wraps B's shoulder (7.5, callback to 3.0), pulls B in
on the taut line, lands by the kunai and takes it (8.0), drives B's own kunai into B's shoulder (8.5, callback); both
crash, B stays down (9.0); A holds a crouch over B (9.5, mirror of 0.6). Camera: about 11 shots, each hit held with both
bodies in frame, height or depth changing at least every 2 s. Constraints holding: one kunai, five props tracked, B
never stands after 9.0, nothing visible appears from nowhere. Known model drift (probes): aerial takeoffs may come late.

## Phase 6 — Final report

1. **Verification:** the repo's order is the corrected order (plus L4d facial), enforced in code. My plan did not apply
   it as a trickle-down rule in six placements (FP.1, FR.4, F4.4 misplaced; FP.12, F4.5's check, F9.3/F9.4 unplaced);
   corrected in Phase 1 and Phase 4.
2. **Gaps:** 19. Critical 2 (GAP-06, GAP-16), high 9 (GAP-01, 04, 05, 07, 10, 11, 13, 14, 15), medium 4 (GAP-03, 08,
   09, 12), low 4 (GAP-02, 17, 18, 19).
3. **Impact:** every layer from L1.1 down changes; validators added at S04, S05 (delay), S07, S11, S13, S15, S16, S17;
   the viewer sees hits on their poses, props that never pop, one rotation per turn, a camera that holds hits with both
   bodies. The golden passes after its recorded deviations (O7-O54); whether a golden failure means "fix the check" (rule
   9) or "fix the golden" (O26) is the owner's call.
4. **Plan map:** steps 1-16 cover GAP-01 and 06-16; GAP-03, 04, 05 are new items not in the plan; GAP-17 is M7; GAP-02,
   18, 19 need rulings. Nothing is blocked except by those rulings.
5. **Simulation:** above.
6. **Next actions (critical path):** W wording rules → F5.3 strike timing (GAP-06) → F6.3 pickups (GAP-07) → F2/F6
   props → FR.1/FR.3 → F5.1/F5.2 FK and world contact (GAP-10, 13) → the rest; GAP-04/05 (checkable constraints) can run
   in parallel after F5.3 once the owner approves them.
