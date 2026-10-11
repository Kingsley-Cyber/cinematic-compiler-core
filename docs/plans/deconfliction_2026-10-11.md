# Deconfliction: the owner's cinematic_beat_v2 plan (parts 1-3) against the repo (2026-10-11)

Status: **FINAL, v1.1 (2026-10-11).** Every recommendation accepted (O22-O44); the probe results amend the printed
wording (O47, O48); the repo stays model-agnostic, built for Seedance with no model cards, adapters later (O49). Open:
nothing. Q-G is answered (O50: five callbacks), probe V6 is rendered by the owner before the opening slice (O51), and
Q3, Q6, Q7, Q8 are closed (O53-O56). The build order is in section 9. Repo at local `main` `7e962cc` (553 tests, 44 prompt
codes, gate green). Every repo claim below was checked against the code on disk; `file:line` points at it.

## 1. Executive summary

The plan's diagnoses are real symptoms, but several causes differ here: B already carries every layer A does, "punch"
is Laban's effort action rather than a fist, a backflip in this repo's frame turns about the lateral X axis, Bartenieff
and staging already exist (part 3), and the larger fault is that every strike's contact lands 0.4-0.5 s after the pose
that shows it. Every remaining gap closes additively inside S01-S17, the JSON Schema contracts, the plans and the
validators, as checks or as values derived from authored data (strike timing, world contact points, a printed physics
and rotation path, Laban and Bartenieff agreement with the pose, momentum, money-shot frame parts, per-genre cards);
the part-3 scripts that would edit authored beats (resolve, integrate, apply, update) become derivations and checks,
and the render scripts wait for M7. There is no rewrite, no Pydantic and no new dependency, and twenty-four one-line
questions settle the conflicts.

## 2. Plan inventory (what the plan contains)

| ID | Kind | Item |
|---|---|---|
| L1-L16 | Beat schema `cinematic_beat_v2` | 1 identity · 2 world position · 3 anticipation · 4 momentum · 5 body · 6 effort (+ combat verbs in `action`) · 7 shape · 8 space · 9 kinematics · 10 support (+ com_height) · 11 contact (world points, surface, force, timing) · 12 impact · 13 reaction · 14 environment · 15 causal · 16 continuity; plus `symmetry` and per-limb fields |
| E1-E6 | Enforcement | E1 schema types (Pydantic) · E2 Laban direction (rising +Y, advancing toward target, plane axes, sudden = high acceleration, bound flow at impact) · E3 limb completeness (11 joints, L/R pairs) · E4 momentum continuity (no teleport, no float) · E5 contact in world space · E6 golden gate ("when the golden contradicts a code, the code is wrong") |
| S-fixes | Stage fixes (plan numbering) | S02 prop physics (ballistic interpolation, pre/post contact keyframes) · S03 body geometry (foot orientation, symmetry flag, anime ROM) · S04 beat declaration (B's LMA, combat action vocabulary, timed kinetic chain, callbacks) · S05 contact (world positions) · S06 prop carry (visibility track, rest state) · S08 anime FX (force, hold frames, shake, freeze, per-limb smear and speedlines) |
| N1-N7 | Naruto signatures | weighted impact · kinetic chain · extreme asymmetry · Euler exaggeration · contact frames · selective smear · choreographic callbacks |
| D1-D5 | Diagnoses | D1 kunai skips (no ballistic interpolation) · D2 kunai pops (no visibility track) · D3 B doesn't fight (no LMA for B) · D4 kick-to-kunai fails (no world positions, no `deflect`, no foot orientation, no instantaneous velocity flip) · D5 LMA direction can go weird (no direction validator) |
| P1-P6 | Principles | props need physics contracts · secondary fighters get the primary's encoding · contact needs world positions · the world is stateful · every beat needs anticipation + momentum + continuity · the golden is the source of truth |
| W1-W12 | Weaknesses (Part 2) | prop physics · B second-class · contact from joint angles · thin action vocabulary · no world state · no reaction model · no anticipation · no momentum carry · no environment interaction · no causality visualisation · no failure recovery · no cross-beat continuity |
| V1-V9 | World-view layers (Part 3) | world state track · contact contract · anticipation · momentum · reaction · environment · causal overlay · continuity contract · failure recovery |
| R1-R6 | Money-shot requirements (part 2) | rotation axis, degrees, direction, plane · at least 3 rotation keyframes · inversion frame (time, head below hips) · per-limb paths (crescent, tuck, reach, counterbalance) · launch and land times · linear and angular velocity |
| MV1-MV6 | Rotation validators (part 2) | ROTATION_INCOMPLETE · ROTATION_NOT_MONOTONIC · INVERSION_FRAME_MISSING · AIRBORNE_WITHOUT_LAUNCH · ROTATION_WITHOUT_ANGULAR_MOMENTUM · BODY_SMEAR_FORBIDDEN |
| MC, MS1-MS5 | Money-shot camera and signatures (part 2) | camera arcs with the rotation (arc = 0.5 × rotation in anime, 0.1 × in realism; tilt follows) · inverted hold 2-3 frames at slow 0.25 · limb crescent · smear trail · impact frame 3-4 · camera arc |
| G1-G2 | Genre profiles (part 2) | anime_sakuga vs realism: gravity override, rotation speed ×1.5, airtime ×0.7, inverted hold 3/1, apex slow 0.25/1, limb extension ×1.3 (max 150/120), smear selective/none, speedlines radial/none, impact hold 4/1, camera arc 0.5/0.1, dust on landing, shake 2.0/0.5; six shared physics laws; genre-aware thresholds |
| M1-M20 | Missing domains (part 3) | Bartenieff · world motion · non-ballistic physics · causal delay · acceleration and jerk · Laban phrasing and drives · contact materials · environment depth · renderer hints · per-frame continuity · interpolation curves · sound · character state · perspective · line of action · silhouette · staging · anticipation curves · follow-through · secondary-motion parameters; priority tiers 1-4 |
| SC1-SC24 | Fire-off scripts (part 3, conceptual) | compile · validate laban, bartenieff, limbs, momentum, contact world, rotation · solve prop physics, body kinematics · resolve contacts · integrate momentum · apply follow-through, secondary motion, world motion · update environment, character state · drive camera · trigger fx, sound · dispatch renderer · validate render · retry · assemble · verify golden |
| T1-T8 | Python tasks | `schema.py` (Pydantic) · `validators/contact_world.py` · `validators/prop_physics.py` · `validators/prop_visibility.py` · `validators/b_active.py` · `compile/prose.py` · `render/session.py` (retry) · `tests/test_golden_conformance.py` |

## 3. Codebase audit (what the repo actually has)

**Topology (macro).** One envelope (MGRAPH-1.1) built by 17 steps in `kernel/layer_order.yaml`: S01 intent, S02 brief,
S03 constraint, S04 temporal (authored beats), S05 causal, S06 state, S07 contact, S08 hand role (UGC), S09 object
state, S10 affordance, S11 kinematic, S12 Bartenieff, S13 motion (Euler keys), S14 facial, S15 effort (LMA), S16
camera, S17 render. Entry points: `cinematic compile` (`cli/main.py`), `compiler/pipeline.run`,
`python -m compiler.examples`. Authored steps take sealed, hash-bound packets (`compiler/authoring.py`); contracts are
JSON Schema 2020-12 (own subset validator `validators/schema_validator.py`, no third-party); schema, library and
kernel changes are hash-logged; the only runtime dependency is `pyyaml` (`pyproject.toml:6`). Outputs: LBN-2.4
`render.txt` plus four structured-prose modes (`renderers/prose_renderer.py`), 44 prompt codes
(`validators/prompt_validator.py:20`), the per-prompt DAG checklist (`validators/checklist.py`).

**The plan's stage numbers are not the repo's.** Mapped without renumbering (layer_order stays):

| Plan stage | Repo step(s) and code |
|---|---|
| S02 prop kinematics | S04 prop samples + PROP_KINEMATICS (`planner/dynamic_beat_validator.py:184`), printed by `renderers/prop_samples.py:54` |
| S03 body geometry | S11 support (`compiler/passes/derived/p11_kinematic.py:29`), S13 Euler keys + JOINT_LIMIT (`solver/euler_solver.py:41,97`) |
| S04 beat declaration | S04 beats (`schemas/graphs/beat_plan.schema.json`), S12 Bartenieff (`p12_bartenieff.py:21`), S15 effort/shape/space (`p15_effort.py:23,68`) |
| S05 contact | S07 contact events (`compiler/passes/mandatory/p07_contact.py:32,42`) |
| S06 prop carry | S06 state replay (`p06_state.py:20`, `validators/continuity_validator.py:40`) + S07 possess/release |
| S07 camera | S16 camera (`compiler/passes/derived/p16_camera.py`, `validators/camera_validator.py:197`) |
| S08 anime FX | S17 render frame parts (`compiler/passes/derived/p17_render.py:59`) |
| S09 negative filter | S03 negatives + NEGATIVES section (NEGATIVES_MISSING, COUNT_CONTRADICTION) |
| S10 render compile | S17 (`renderers/anime_renderer.py`, `renderers/prose_renderer.py`) |

**Facts that correct the plan (verified on the reference fight):**
- **B is fully encoded.** B has 20 keys; each has S11 kinematics (the same ten cues as A), S12 Bartenieff, S13 Euler
  with all 11 joints, and an S15 effort interval. What is thin is B's *choreography*: 5 of B's 20 keys are B's own
  actions (throw kunai, rising palm, palm hits log, shuriken volley, catch-and-throw), and B's effort action is `none`
  over most of 4.0-9.5 (D3 is a content and quality gap, not a missing encoding).
- **"punch" is Laban, not a fist.** S15 derives the effort action from weight × time × space, Laban's eight basic
  actions (`p15_effort.py:23`; `library/laban_vocabulary.yaml:5`: "punch is also called thrust"). The foot deflect is
  correctly strong + sudden + direct = punch/thrust. Adding `deflect` to effort actions would break that definition
  (the laban-notation law: keep LMA quality words distinct from action verbs). The renderer misreading "punch" is a
  real risk; the word is on 11 lines of the reference fight's `prose_mixed.txt`.
- **Contact timing is the bigger fault.** Contacts happen at their beat's end (`p07_contact.py:42`), poses and impact
  frames at its start. On the reference fight every strike lands 0.4-0.5 s after its pose: deflect pose 2.5, contact
  3.0; knee 4.7 → 5.1; palm on log 4.0 → 4.4; catch 6.6 → 7.0; rope wrap 7.5 → 8.0; kunai drive 8.5 → 9.0, while the
  impact frames sit at 2.5, 4.7, 5.5, 6.6, 8.5, 9.0. At 2.5 the kunai has only just left B's hand (`2.50 released by B R
  hand`), so the foot cannot meet it there. The golden (DAG D5) has B throw at 2.0 and A deflect at 2.5. This explains
  D4's "never meet", and plausibly F14 (R2's beats 0.5-1 s late) and F5 (weak hits).
- **No forward kinematics exists** (no segment lengths in any card; `solver/quaternion.py` has rotation maths only),
  so no world point of a hand or foot is known anywhere. D4's "the renderer must FK the leg" is accurate.
- **Props already have a physics check, but no printed contract.** S04 refuses a free prop that leaves gravity by more
  than 0.25 m between samples, a held prop more than 2 m from its holder, and a resting prop that moves without a
  contact; floats are anime-only (`dynamic_beat_validator.py:184`, owner O8). The prompt prints each sample (`p`, `v`,
  "at rest"), but no "ballistic between samples" contract and no pre/post-contact pair at the same instant.
- **Visibility is partly there.** Every prop's first state is known and printed (M8.12b: "kunai (held by B R hand …)",
  "substitution log (deployment hidden until 4.00)"); hidden/holstered/sealed are card states. There is no per-segment
  visible/hidden track, and "at rest" is printed once, not "until 8.00".
- **The world is stateful in the engine, unused in this fight.** Surfaces have damage states (none, marked, scorched,
  cracked, cut; `kernel/state_vocabulary.yaml:16`), carried across chained clips; the wizard example uses them. The
  reference fight never sets one (ground, pillar, canopy end `unknown`), though shuriken and a kunai embed in things.
- **Already done, beyond the plan's picture:** limb completeness (MOTION_JOINTS: exactly the 11 kernel joints, so L/R
  pairs always present); anime ROM +30 on spine, neck, shoulders, hips, knees (`library/joint_limits.yaml`, O11);
  per-limb smear (FRAME_SMEAR: one subject, one part); hold frames (`holds: {t, frames}`); typed negatives; causal
  reasons printed and checked (CAUSE_REASON); prop first states; vanished body (X9); named turns (X5/X6); counts;
  the golden gate (`tests/test_reference_fight_golden.py`, `tests/test_dag_conformance.py`, the checklist).
- **Plan numbers are stale:** 553 tests and 44 codes today (the plan says 520 and 37). `compile/prose.py` exists as
  `renderers/prose_renderer.py`; `tests/test_golden_conformance.py` exists as the two golden tests plus the checklist.

**Part 2 facts (rotation, money shots, genres):**
- **Axes.** The repo's frame is Y up, +Z forward, +X the performer's left (owner Q6). Turns are declared as flip about
  X, spin about Y, cartwheel about Z (`planner/prompts/euler_solving.txt`; MOTION_AXIS in `euler_solver._turn_findings`;
  TURN_LABEL at `euler_solver.py:140`). The MovementXML thesis defines somersault on the lateral axis and cartwheel on
  the sagittal axis (Hatol 2006, §3.7.2, pp. 24-25). The plan's backflip "axis [0, 1, 0]" and "angular [0, 6.28, 0]"
  are a spin in this frame.
- **The reference backflip (M8.12f)** is a declared flip about X of -360 from 5.1 to 5.5: 0.4 s, 900 degrees per
  second, the plan's own anime figure, interpolated about that axis (`p13_motion.py:91`, `euler_axis`). The staff prints
  "flip sign (lateral axis, backward, 360)". It has two keys only: no 5.2/5.3/5.4 angles, no printed inversion time, no
  hold at the apex (holds at 4.7 and 5.9), and no smear on the kicking left leg during 5.1-5.5 (the left-leg smear runs
  4.7-5.1). The 6.3 cartwheel is -360 about Z with +90 of yaw in 0.3 s (the plan's two-axis flying cartwheel).
- **Launch and landing.** A is airborne from 4.7 to 5.9 (no support at b12-b14; landing in the 5.9 slide), so the
  flip starts mid-air; the plan's "launch at 5.1 from both feet" does not fit this fight. AIRBORNE_UNBOOKENDED already
  requires a takeoff and a landing line for every airborne span (prompt level only).
- **Completion.** A turn of 90 degrees or more must be declared and its axis must dominate (MOTION_AXIS); a named
  flip or cartwheel must be declared (TURN_LABEL). A full 360 is not enforced: the wizard's dodge_flip turns 180 to an
  inverted apex and lands inside the unkeyed final hold.
- **Smear per limb** is DONE (FRAME_SMEAR, `p17_render.py:79`; the ink rule "body does NOT smear").
- **Camera.** S16 has orbit, crane and tracking moves and slow/ramp/freeze playback (`library/camera_grammar.yaml:35-54`)
  and per-genre cards (`library/camera_conventions/{anime,live_action,ugc_ad}.yaml`); no rule ties an arc to a
  rotation (the DAG's C10 "orbit on spins" is not encoded).
- **Genres.** The repo's genres are media (anime, live_action, ugc_ad), each with its own camera card, effort modes and
  joint limits (anime +30 degrees, O11); props may float only in anime (O8). The live-action example authors no smear,
  speedline or impact frame. There is no single profile and no multipliers for rotation speed, airtime, slow motion or
  extension. The plan's "realism" is the repo's live_action.
- **Law 1's anime numbers** (launch v_y 4.5 m/s, 0.4 s airtime) cannot both hold under gravity (ballistic airtime would
  be 0.92 s): they describe stylised timing, i.e. a hang or float the genre allows.

**Part 3 facts (domains and scripts):**
- **Bartenieff exists** (S12, `compiler/passes/derived/p12_bartenieff.py`): per slot the connectivity pattern (breath,
  core-distal, head-tail, upper-lower, body-half, cross-lateral, and `cpcs:spiral` as a labelled extension, because
  spiral is not one of the six Patterns of Total Body Connectivity; `library/bartenieff_vocabulary.yaml:2,10`), the
  developmental pattern, initiation, follow-through and body mode. S12 checks vocabulary, slot coverage, own parts and
  body-mode coherence (:55-67), not agreement with the pose (the plan is right about that half).
- **Breath** is an S11 cue (steady, held, exhale, gasp; `library/kinematic_cues.yaml:17`).
- **Staging exists** in S16: subject placement in the frame, focus target, depth anchor, negative space.
- **Persistence exists**: lasting effects print as time-bounded rules (CAUSAL_RULE_MISSING); smoke has card states
  (sealed, burst, dissipating, gone); the rope dart's line has coiled, thrown, wrapped and taut; surfaces have damage.
- **Secondary motion and follow-through exist as words**: a lag line per performer's loose costume parts and a
  recovery line after every strike (IMPLIED_GUIDANCE_MISSING); no numbers.
- **Interpolation is declared** for joints (slerp, or about a declared turn's axis) and camera easing exists
  (`movement_quality`); no body ease curves.
- **The repo derives and refuses, it never edits authored data**: "A mismatch is a finding (the step fails and is
  re-authored); nothing is corrected silently" (`solver/euler_solver.py` docstring). Scripts that resolve, integrate,
  apply or update beats would break that rule.
- **Per-frame work is planned for M7**: post-generation validation (S18, already in `kernel/layer_order.yaml`, unbuilt),
  conditioning emitters (pose, depth, flow, hand-object), a per-model renderer (`docs/plans/MASTER_PLAN.md:498-501`).
  No renders and no paid API until the owner picks a model and authorises it (open Q8).
- **No CI service**: the gate is `scripts/check.sh` locally (no `.github/`).

**The 16 layers against the repo:**

| # | Layer | Repo | Status |
|---|---|---|---|
| 1 | Identity | S04 beat id, t, dur, label, actor, participants; a slot = one fighter's key (`entity@beat`) | DONE (beats are scene events, slots are per-fighter beats) |
| 2 | World position | S04 pos + facing (authoritative, Q2), S13 root rot | DONE |
| 3 | Anticipation | S11 `loading`, S17 anticipation holds possible, implied guidance; gap ANTICIPATION_MISSING (KF) | PARTIAL |
| 4 | Momentum | TELEPORT (25 m/s), prop velocities, the printed law "Momentum is conserved"; gap MOMENTUM_MISSING (T10, C22); no body velocity, no airborne ballistic check | MISSING |
| 5 | Body | S12: connectivity, developmental pattern, initiation, follow-through (ordered), body mode, intent; KINETIC_CHAIN_MISSING; gap CHAIN_ORDER | DONE (untimed chain) |
| 6 | Effort | S15: weight, time, space, flow, action (Laban 8), intensity, mode | DONE; combat verbs CONFLICT |
| 7 | Shape | S15 quality, mode | DONE |
| 8 | Space | S15 kinesphere, pathway, plane | DONE |
| 9 | Kinematics | S11 the same ten cues | DONE |
| 10 | Support | S11 support parts, S07 support contacts on named surfaces, S06 posture; no com_height | DONE (com_height from posture) |
| 11 | Contact | S07 events: type (touch/possess/support/release), part, target part, time, `at: start` | PARTIAL: no world points, surface, force or verb; strike timing off by a beat |
| 12 | Impact | S17 impact times, holds (frames), fx text; S16 shake-like camera texture | PARTIAL: no force, shake, freeze or contact frame number |
| 13 | Reaction | target's S11 cues (balance off, yielding) and pose; gap POST_CONTACT_MISSING (C21) | PARTIAL |
| 14 | Environment | surface damage states (engine), smoke card states | PARTIAL (unused in the fight; no debris) |
| 15 | Causal | S05 edges, hard/soft, printed reasons; linear only (owner) | DONE (one child per beat, by owner decision) |
| 16 | Continuity | S06 replay snapshots + transitions + triggers, continuity checks, M5.5 chaining, MOTION_POS | DONE (no momentum match) |

## 4. Gap table

Status: DONE · PARTIAL · MISSING · CONFLICTS. "Fix" names the enhancement in section 5.

| Plan item | Status | Evidence | Fix |
|---|---|---|---|
| D1 / S02 ballistic interpolation | PARTIAL | `dynamic_beat_validator.py:184` checks gravity; `prop_samples.py:25,54` print p/v, no contract | F2.1 |
| D4 / S02 pre/post-contact keyframes | MISSING | `beat_plan.schema.json:322` PropSample has no phase; one sample per (prop, t) | F2.2 |
| D2 / S06 visibility track | PARTIAL | first states printed (`prose_renderer.py:307`); no visible/hidden segments | F6.1 |
| S06 rest-state persistence | PARTIAL | "at rest" printed once (`prop_samples.py:25`) | F6.2 |
| D2 kunai appears in A's hand at 8.0 | CONFLICTS with data (airborne pickup, audit X2) | A support `[]` at b20; `8.00 holder none -> A` | F6.3 (= O18 item 1) |
| D3 / S04 B's LMA encoding | DONE (encoding) / PARTIAL (choreography) | 20 B keys with S11/S12/S13/S15; 5 actor beats; effort `none` 4.0-9.5 | F4.3 (content), F4.4 (check) |
| D4 / S04 action = deflect | CONFLICTS (Laban) | `p15_effort.py:23` effort action = weight × time × space | F4.1 (verb on contact) + F4.2 (wording) |
| W4 combat vocabulary | MISSING | contact types only touch/possess/support/release (`beat_plan.schema.json:110`) | F4.1 |
| D4 / S05 contact world positions | MISSING | no FK, no segment lengths anywhere | F5.1, F5.2 |
| Strike contact timing (found in audit) | CONTRADICTION in data | contact = beat end (`p07_contact.py:42`) vs pose/impact at beat start; +0.4-0.5 s on every strike | F5.3 |
| D4 / S03 foot orientation, contact surface | MISSING | 11-joint kernel skeleton has no feet; contact parts are limbs | F3.1 |
| N3 / S03 symmetry flag, per-limb fields | PARTIAL | per-side Euler on every key (S13), staff names L and R; no flag | F3.2 |
| N4 / S03 anime ROM | DONE | `library/joint_limits.yaml` (O11), JOINT_LIMIT (`euler_solver.py:41`) | trigger is genre, not `style_era` |
| N2 / S04 timed kinetic chain | PARTIAL | `p12_bartenieff.py:21` follow_through ordered, untimed; gap CHAIN_ORDER | F4.5 |
| N7 / S04 callbacks | MISSING | no field; the fight's 'regrapple' is a callback with no source (audit X4) | F4.6 |
| N1, N5 / S08 force, shake, freeze, contact frame | PARTIAL | `p17_render.py:59` impact times + holds{frames}; S16 `movement_quality` texture | F8.1, F8.2 |
| N6 / S08 per-limb smear, speedlines | DONE / PARTIAL | smear has `part`; speedlines only `subject` | F8.3 |
| E1 schema types | DONE (JSON Schema) / CONFLICTS (Pydantic) | `validators/schema_validator.py`, logged schemas | keep JSON Schema (section 6) |
| E2 / D5 Laban direction | MISSING | S15 checks vocabulary and factor combinations only | F9.1 |
| E3 limb completeness | DONE | MOTION_JOINTS (`euler_solver.py:97`) | — |
| E4 momentum continuity | PARTIAL | TELEPORT (`dynamic_beat_validator.py:27,114`), props only under gravity | F9.2 |
| E5 contact world space | MISSING | — | F5.2 |
| E6 golden gate | DONE / CONFLICTS (precedence) | golden tests + checklist; O7, O10, O17, O18, O21 fixed the golden where it contradicts its words or the DAG | Q-E |
| L3 anticipation | PARTIAL | gap ANTICIPATION_MISSING | F9.3 |
| L4 momentum | MISSING | gap MOMENTUM_MISSING | F9.2 |
| L13 reaction | PARTIAL | gap POST_CONTACT_MISSING | F9.4 |
| L14 / W5 / W9 environment | PARTIAL | `kernel/state_vocabulary.yaml:16` used by the wizard, not the fight | F6.4 |
| L15 causal type `enables`/`blocks` | PARTIAL | S05 `causes` + hard/soft; S10 `enables` (UGC); linear only | keep (owner linear rule) |
| W10 causal overlay | CONFLICTS (format) | the DAG prints causes as CAUSAL LINKS text; arrows on screen would be drawn by the model | Q-I |
| L16 / W12 continuity contract | DONE | S06 replay + continuity checks + chaining | momentum part in F9.2 |
| W11 / V9 / T7 retry loop | CONFLICTS (standing rule) | no renders, no paid API; post-generation is M7 | defer to M7 (Q-J) |
| T1 `schema.py` Pydantic | CONFLICTS | adds a dependency and a second contract system | Q-J |
| T6 `compile/prose.py` | DONE | `renderers/prose_renderer.py` | — |
| T8 golden conformance test | DONE | `tests/test_dag_conformance.py`, `tests/test_reference_fight_golden.py`, `validators/checklist.py` | — |
| R1 rotation axis | DONE (convention) / CONFLICTS (plan's Y for backflips) | `euler_solving.txt`, MOTION_AXIS, TURN_LABEL `euler_solver.py:140` | Q-L |
| R2 at least 3 rotation keyframes | MISSING (printed) | two keys per turn, `euler_axis` edge `p13_motion.py:91` | FR.1 |
| R3 inversion frame | PARTIAL | posture `inverted` exists (MOTION_POSTURE); no apex time printed | FR.1, FR.3 |
| R4 per-limb paths during a turn | MISSING | keys only at beat starts; "LEFT LEG crescent" only in the action text | FR.2 |
| R5 launch and land | PARTIAL | AIRBORNE_UNBOOKENDED (prompt), no graph twin | FR.4 |
| R6 / MV5 angular velocity | MISSING | gap MOMENTUM_MISSING | FR.1 (derived), F9.2 |
| MV1 rotation completes | PARTIAL | declared, 360 not enforced | FR.3, Q-R |
| MV2 monotonic | DONE by construction (continuous angles; one turn per span) | `euler_solver.py:97` | FR.3 covers multi-key runs |
| MV3 inversion occurs | MISSING | — | FR.3 |
| MV6 no body smear | DONE | FRAME_SMEAR `p17_render.py:79` | — |
| MC / MS5 camera arcs with the rotation | MISSING | orbit exists in `camera_grammar.yaml:39-42`; no rule | FR.5, Q-P |
| MS1 inverted hold + apex slow motion | PARTIAL | holds{frames}, playback slow exist; none at 5.3 | FR.6 |
| MS2 limb crescent | MISSING | action text only | FR.2 |
| MS3 smear trail on the kicking leg | PARTIAL (content) | no left-leg smear 5.1-5.5 | FR.6 |
| G1-G2 genre profiles | PARTIAL | per-genre cards exist; no multipliers | FR.7, Q-Q |
| Law 1 anime gravity override | CONFLICTS (O8, F9.2) | props float only where declared | Q-N |
| Limb extension ×1.3, max 150 | CONFLICTS (O11: +30 degrees absolute) | `library/joint_limits.yaml` | Q-O |
| I Bartenieff | PARTIAL (exists; agreement with the pose unchecked) | S12 `p12_bartenieff.py:55-67`, `bartenieff_vocabulary.yaml:10` | FP.1 |
| II World motion | PARTIAL | smoke and line card states; no ambient or reactive parameters | FP.2, Q-V |
| III Non-ballistic physics | PARTIAL | rope line states; no tension curve, friction, restitution | FP.3 |
| IV Causal delay | PARTIAL (derivable) | S05 timing rules `p05_causal.py:36` | FP.4 |
| V Acceleration, jerk | MISSING | no body velocity at all | FP.5 |
| VI Laban phrasing, drives | PARTIAL | LBN `laban` phrase chain; gap PHRASING_MISSING | FP.6, Q-W |
| VII Contact materials | PARTIAL | card `materials` (kunai steel), costume text | FP.7 |
| VIII Environment depth | PARTIAL | damage states, lasting rules | F6.4, FP.2 |
| IX Renderer hints per model | MISSING (planned M7) | `MASTER_PLAN.md:501` | Q-T |
| X Per-frame continuity, rollback | CONFLICTS now (no renders); planned M7 / S18 | `MASTER_PLAN.md:498`, `kernel/layer_order.yaml` S18 | Q-T |
| XI Interpolation curves | PARTIAL | joint slerp / turn axis, camera easing | FP.8, Q-V |
| XII Sound | MISSING | — | Q-U |
| XIII Character state | PARTIAL | S06 condition (ok, staggered, stunned, down); embedded kunai state | FP.9, Q-X |
| XIV Perspective, scale | PARTIAL | `solver/camera_geometry.py` (position, lens, frame height); metric world | FP.10 |
| XV Line of action | MISSING (derivable from S13) | — | FP.11 |
| XVI Silhouette | MISSING (needs FK and projection) | — | FP.12 |
| XVII Staging | DONE (depth layers PARTIAL) | S16 composition | small check with C10 |
| XVIII Anticipation curves | MISSING | gap ANTICIPATION_MISSING | F9.3, FP.8 |
| XIX Follow-through | PARTIAL | S12 follow-through, recovery lines | FP.8 |
| XX Secondary-motion parameters | PARTIAL | lag lines from the costume | FP.8, Q-V |
| P5 "every beat, all 16 layers" | CONFLICTS (density) | DAG C2 "never make every frame explicit", owner O19 (D9 lines) | Q-D |

### Part 3 scripts against the repo

| Script | Repo counterpart | Status |
|---|---|---|
| 1 compile | `compiler/pipeline.run`, `cinematic compile`, `compiler/examples.py` | DONE |
| 2 validate_laban | S15 `p15_effort.check` (:68) + F9.1 | PARTIAL |
| 3 validate_bartenieff | S12 `p12_bartenieff` + FP.1 | PARTIAL |
| 4 validate_limbs | MOTION_JOINTS in `euler_solver.check` (:97) | DONE |
| 5 validate_momentum | TELEPORT (`dynamic_beat_validator.py:114`) + F9.2 | PARTIAL |
| 6 validate_contact_world | F5.2 | MISSING |
| 7 validate_rotation | MOTION_AXIS, TURN_LABEL + FR.3 | PARTIAL |
| 8 solve_prop_physics | PROP_KINEMATICS (check) + F2.1 (derived segments); a per-frame track is M7 conditioning | PARTIAL |
| 9 solve_body_kinematics | F5.1 (`solver/forward_kinematics.py`, new); per frame is M7 | MISSING |
| 10 resolve_contacts | F5.2 refuses a miss; moving bodies to meet would edit authored data | CONFLICTS as written |
| 11 integrate_momentum | F9.2 checks; updating beats would edit authored data | CONFLICTS as written |
| 12 apply_follow_through | FP.8 derives and prints; adding overshoot keys would edit poses | CONFLICTS as written |
| 13 apply_secondary_motion | implied guidance; FP.8 | PARTIAL |
| 14 apply_world_motion | states and lasting rules, FP.2; per frame is M7 | PARTIAL |
| 15 update_environment | S06 replays authored surface effects; FP.2 can refuse an impact on a surface with no effect | PARTIAL |
| 16 update_character_state | S06 condition; FP.9 | PARTIAL |
| 17 drive_camera | S16 authored shots + `solver/camera_geometry.py` (per shot); per frame is M7 | DONE per shot |
| 18 trigger_fx | S17 frame parts (`p17_render.py:59`) | DONE |
| 19 trigger_sound | — | MISSING (Q-U) |
| 20 dispatch_renderer | — | CONFLICTS (no renders, no paid API) → M7 + Q8 |
| 21 validate_render | S18 post-generation (in layer order, unbuilt) | PLANNED M7 |
| 22 retry_on_failure | — | PLANNED M7 |
| 23 assemble_output | — | out of scope (the owner renders) |
| 24 verify_golden | `scripts/check.sh` + the golden tests + `validators/checklist.py` | DONE locally (no CI service) |

## 5. Surgical flow enhancements (grouped by the plan's stages)

### W. Wording rules from the owner's probes (O47-O49): the first slice

The probes (R10-R18, `docs/render_tests/2026-10-11-m9-probes/`) showed which wordings Seedance follows. They become
default rules of `renderers/prose_renderer.py` for every prompt, each with a prompt code in
`validators/prompt_validator.py` (and a break test), with no model card (O49):

| Rule | Evidence | Renderer change | Check |
|---|---|---|---|
| W1 Never print a body hold or freeze in frames; camera holds on a hit use V5's wording ("hold with BOTH bodies in frame, no close-up") | stretched 0.85-1.75 s in R10, R11, R14; gone in R16; V5 passed (R15) | holds stay in the graph and LBN; the prose prints camera holds only | BODY_HOLD_FRAMES |
| W2 After every release, state the releasing hand is empty | R11 kept a second kunai in B's hand; R16 with the line held one | a release line ends "<label>'s <side> hand is empty from <t>" | EMPTY_HAND_UNSTATED |
| W3 Print a turn as "ONE <turn> about the <axis> axis (<plane>)" with takeoff and landing; never print quarter-turn angles or degrees per second | the angle list gave two flips (R13); plain wording one (R18) | the derived angles stay in the graph (narrows O33) | ROTATION_ANGLES_PRINTED |
| W4 An object the scene needs later is placed in the scene from the start, with where it stands; never "hidden" or "not visible before" | the log was drawn from 0.00 when named hidden (R12) and when unnamed (R17), as in R1-R5 | M8.12b's "deployment hidden until 4.00" goes; the reference log becomes a post beside A from 0.00 (O48, golden deviation) | HIDDEN_PHRASING |

Timing: aerial takeoffs rendered 0.75-1.6 s late in every probe, strikes within about 0.2 s. Times stay in the prompt;
renders are judged with that drift in mind.


Each fix is additive: a field in an existing schema (version bump, logged), a function in an existing module, a new
prompt code with its break, or plan content recorded as a golden deviation. "Rows" are knowledge-map rows it closes.

### Plan S02 (repo S04 prop samples)

**F2.1 Printed prop-physics contract** · Priority P0 · Depends on: —
- File/Module: `renderers/prop_samples.py` (`motion_words` :25, `rows` :54); `renderers/prose_renderer.py` `_props`
  (:441); `validators/prompt_validator.py`.
- Current: each sample prints `p`, `v` and "moving up toward A" / "held by B" / "at rest"; S04 already enforces gravity.
- Gap: the model is never told how to move the prop between samples, so it skips.
- Enhancement: derive per segment `physics: held | ballistic | rest | float` (from `holds`, the samples' `v` and
  `float`, all already in S04) and print one clause per segment: "2.50-3.00 ballistic under gravity from p… v…".
  New prompt code PROP_PHYSICS_UNSTATED.
- Why: the physics contract already exists in S04 (O8); this only projects it. No schema change.

**F2.2 Pre/post-contact sample pair** · P0 · Depends on: F5.3
- File/Module: `schemas/graphs/beat_plan.schema.json` PropSample (:322) and `temporal_graph` (1.4); PROP_KINEMATICS
  (`dynamic_beat_validator.py:184`).
- Current: one sample per prop and time; a deflect's velocity flip is spread over the gap to the next sample.
- Gap: a deflect is an instantaneous velocity change.
- Enhancement: optional `phase: pre | post` on PropSample; two samples may share a time if one is pre and one post and
  a contact on that prop happens at that instant; gravity is checked into `pre` and out of `post`. The track prints
  "2.50 pre-contact v[…] · 2.50 post-contact v[…]".
- Why: extends the existing sample contract; the gravity check gains one rule.

### Plan S03 (repo S13 keys, S07 contact parts)

**F3.1 Contact surface (sole, heel, knuckles, palm, blade…)** · P1 · Depends on: F4.1
- File/Module: Contact in `beat_plan.schema.json` (:110) and `temporal_graph.schema.json`; staff bow text in
  `prose_renderer.staff_lines` (:148).
- Current: a contact names a limb (`right_foot`) and the target part (`kunai.blade`); the golden's "sole" lives only in
  the beat's action text.
- Gap: the striking surface is not structured, so the model draws a generic foot.
- Enhancement: optional `surface` enum on the contact's `a` side; the bow prints "R foot (sole) > kunai blade".
  Foot orientation (plantar flexion) stays out of the joints: the kernel skeleton has 11 joints and no feet (owner
  kernel decision); the surface plus the world point (F5.1) tells the model which face meets the target.
- Why: one optional field, no skeleton change.

**F3.2 Derived symmetry flag** · P2 · Depends on: —
- File/Module: `solver/staff_geometry.py`, `prose_renderer.staff_lines`.
- Current: every key has per-side Euler (asymmetry is in the data); the staff names L and R.
- Gap: nothing says "mirror" or "do not mirror".
- Enhancement: compute per key `symmetric` (L/R joint pairs within a tolerance after mirroring) and print "asymmetric:
  R leg leads" or "symmetric"; under O19's D9 style, an asymmetric line always names both sides. No authored field.
- Why: derived from S13, so it can never disagree with the pose.

### Plan S04 (repo S04 beats, S12, S15)

**F4.1 Combat verb on contacts** · P1 · Depends on: Q-A
- File/Module: Contact (`beat_plan.schema.json:110`), S04 validator (`dynamic_beat_validator.py`), staff and prop text.
- Current: contact types touch/possess/support/release; the verb lives in labels ("foot_deflect_kunai").
- Gap: no structured strike/deflect/parry/catch/redirect/trap/bind/disarm/throw/grapple vocabulary.
- Enhancement: optional `verb` on touch contacts from a closed list (new library card, logged); the staff prints
  "DEFLECT: R foot (sole) > kunai blade"; S04 refuses a verb that disagrees with the contact (e.g. `catch` must be
  followed by a possess, `throw` by a release).
- Why: keeps Laban effort pure and gives the model the action word.

**F4.2 Unambiguous effort wording** · P1 · Depends on: Q-A
- File/Module: `prose_renderer` implied guidance and staff (effort text), `anime_renderer` desc (LBN unchanged unless
  Q3).
- Current: "strong sudden direct bound punch".
- Gap: the model reads "punch" as a fist.
- Enhancement: print Laban actions as qualities: "thrust quality (strong, sudden, direct)"; same for slash, press etc.
- Why: projection-only wording; S15 data unchanged.

**F4.3 B's active keys (content)** · P2 · Depends on: Q-F
- File/Module: `examples/reference_fight/plans/*.json` (S04, S11-S15, S16).
- Current: B tracks A at 1.6, watches the kunai at 2.5, braces at 3.0; effort `none` from 4.0.
- Gap: the plan's tracking / recovering / charging / reacting keys for B.
- Enhancement: re-author B's participant keys (and, where the plan asks, new B beats) with active efforts; record as
  golden deviations.
- Why: content inside existing plans; no code.

**F4.4 Idle-fighter check** · P2 · Depends on: Q-F
- File/Module: `planner/dynamic_beat_validator.py` or S15 `p15_effort.check` (:68); prompt code.
- Gap: nothing flags a fighter left without an active key while the other fights.
- Enhancement: IDLE_FIGHTER: a fighter whose effort action is `none` and whose root and joints barely change for longer
  than an owner-set span while another fighter acts. Threshold is the owner's (Q-F).

**F4.5 Timed kinetic chain** · P3 · Depends on: —
- File/Module: S12 `p12_bartenieff.py` (:21 `follow_through`), schema `bartenieff_plan`; gap CHAIN_ORDER.
- Enhancement: optional offsets per follow-through link (fractions of the beat); CHAIN_ORDER checks proximal to distal;
  the staff prints "chain R foot 0.0 > R leg 0.1 > torso 0.2".

**F4.6 Choreographic callbacks** · P3 · Depends on: Q-G
- File/Module: Beat (`beat_plan.schema.json`), S04 validator, causal/staff text.
- Enhancement: optional `callback: {references, type: mirror|variant|escalation, note}`; S04 refuses a reference to a
  later or missing beat; the prose prints "echoes 2.50 foot deflect, inverted". Also catches audit X4 ('regrapple' with
  no earlier grapple).

### Plan S05 (repo S07 contact, S13 keys)

**F5.1 World contact points from the pose** · P1 · Depends on: Q-C, F5.3
- File/Module: new `solver/forward_kinematics.py` (uses `solver/quaternion.matrix` :29); new library card of segment
  lengths per archetype or body mode (logged); S13 `p13_motion.py` derives `contact_points` into `/nodes/motion` or a
  derived contact field.
- Current: no point of a hand or foot is known.
- Gap: source_world / target_world.
- Enhancement: FK from root pos + rot + the 11 joint Eulers (the Q6 convention already declared) gives each limb end at
  each key; for every touch contact, `source_world` = that limb end at the contact time and `target_world` = the prop
  sample or the other body's point; the staff prints "R foot sole at [x, y, z] meets kunai blade at [x, y, z]".
- Why: one new solver module beside the existing ones; the numbers are computed, so they cannot contradict the pose
  (authored world points, as the plan sketches, could).

**F5.2 CONTACT_WORLD check (E5)** · P1 · Depends on: F5.1
- File/Module: S13 check (`solver/euler_solver.check` :97 or `p13_motion.py`); prompt code CONTACT_WORLD.
- Enhancement: refuse a touch whose source and target points are farther apart than a tolerance (owner value) at the
  contact time; the prompt must print both points.
- Why: catches "the foot and the kunai never meet" before any render.

**F5.3 Strike contacts at the pose** · P0 · Depends on: Q-B
- File/Module: reference plans (S04 contacts `at: start`, b05 release at 2.0, deflect at 2.5 …); new check
  IMPACT_CONTACT_SYNC in S17 `p17_render.check` (:59) and the prompt.
- Current: every strike lands 0.4-0.5 s after its pose and its impact frame.
- Gap: one time per hit.
- Enhancement: strike and release contacts happen at the key pose (`at: start`, which exists since M8.12b), so throws
  release at 2.0 and the deflect lands at 2.5 as the golden says; IMPACT_CONTACT_SYNC refuses an impact frame without a
  touch at the same frame, and a strike touch without an impact frame.
- Why: uses the existing `at` field; only plan content and one check change.

### Plan S06 (repo S06 state, S07 possess/release)

**F6.1 Visibility track** · P1 · Depends on: —
- File/Module: `prose_renderer.first_states` (:307) and `_props` (:441); prompt code PROP_VISIBILITY.
- Enhancement: derive visible/hidden segments per prop (hidden while a card state is hidden/holstered/sealed or while
  stowed; visible otherwise) and print "kunai visible 0.00-10.00 (in B's hand, in flight, on the ground at […] 3.40-8.00,
  in A's hand)"; "substitution log hidden until 4.00".
- Why: derived from S06/S07; no new state.
- **Amended by W4 (O47, O48):** no "hidden" segment is printed. A prop that appears later is in the scene from the start
  (the reference log stands beside A as a post); the track prints where each prop is and when it changes hands or state.

**F6.2 Rest persistence** · P1 · Depends on: F6.1
- File/Module: `prop_samples.motion_words` (:25).
- Enhancement: print "at rest on the ground at [0.3, 0, 5.3] from 3.40 until 8.00" (until the next contact on it).

**F6.3 Grounded pickups (X2/X3)** · P0 · Depends on: O18 (approved)
- Already approved and specified in NEXT_SESSION item 1: AIRBORNE_PICKUP, A lands by the rope dart and the kunai.
  Fixes D2's "kunai appears in A's hand at 8.0".

**F6.4 World state used** · P2 · Depends on: Q-H
- File/Module: reference plans (effects on `wooden_pillar.damage`, `ground.damage`); prose RULES lasting effects.
- Enhancement: shuriken and kunai mark the pillar, the crash cracks the ground (`marked`, `cracked` exist in the
  vocabulary); debris and ember counts would need new values (logged kernel change) and are left to Q-H.

### Plan S08 (repo S17 frame parts, S16 camera)

**F8.1 Impact force, shake, freeze** · P2 · Depends on: F5.3
- File/Module: S17 plan schema `schemas/graphs/frame_parts_plan.schema.json`, `p17_render.check` (:59), `_genre_block`
  (`prose_renderer.py:539`).
- Enhancement: optional per impact `force` (0-1), `freeze` (bool), `shake` (camera, 0-3); anime card ranges; checks:
  freeze implies a hold, shake only on an impact.
- **Amended by W1 (O47):** freezes and holds stay in the graph and LBN; the prose prints only camera holds on a hit, in
  V5's wording.

**F8.2 Contact frame numbers** · P2 · Depends on: F5.3
- Enhancement: print each impact as "frame 60 (2.50 s at 24 fps), hold 3 frames, reaction from frame 63"; derived.
- **Amended by W1 (O47):** the prose prints the impact time only ("impact at 2.50"), no frame counts.

**F8.3 Per-limb speedlines** · P3 · Depends on: —
- Enhancement: optional `part` on speedlines, checked like smear (FRAME_SMEAR's rule).

### Money shots and genre profiles (part 2: plan S03, S04, S05, S07, S08)

**FR.1 Derived rotation path** · P1 · Depends on: Q-L, Q-M
- File/Module: `solver/euler_solver.py` (from the declared turn and the next key), `renderers/prose_renderer.staff_lines`
  (:148); prompt code ROTATION_PATH_UNSTATED.
- Current: a declared turn prints "flip sign (lateral axis, backward, 360)" on its start line.
- Gap: quarter-turn angles, the inversion time and the angular speed are never stated, so the model holds one pose.
- Enhancement: derive, per turn run, the angle at each quarter turn with its time, the inversion time (180 degrees for
  flips and cartwheels) and degrees per second, and print "5.10-5.50 backflip about the lateral axis: 0 at 5.10, -90 at
  5.20, -180 at 5.30 (inverted, head below hips), -270 at 5.40, -360 at 5.50; 900 degrees per second". Time spacing is
  linear between the keys (interpretation; easing from the Effort could follow).
- Why: computed from the keys, so it cannot disagree with them; no authored data, no new key.
- **Amended by W3 (O47, probes R13 and R18):** the quarter-turn angles, the inversion time and the degrees per second
  are derived and checked but not printed; the prose prints "ONE backflip about the side-to-side axis (sagittal plane),
  takeoff 5.10, landing 5.50". ROTATION_PATH_UNSTATED checks those words.

**FR.2 Limb paths during a turn** · P2 · Depends on: FR.1
- File/Module: `schemas/graphs/motion_plan.schema.json` (optional `limb_paths` on a turning key), `p13_motion.py`, the
  staff text.
- Enhancement: `limb_paths: {left_leg: crescent, right_leg: tuck, left_arm: reach, right_arm: counterbalance}` from a
  closed list; S13 checks that each named limb exists and that a crescent or tuck agrees with the hip and knee change to
  the next key; the reference 5.1 key takes the golden's own words (left leg crescent, right leg tucked).

**FR.3 Rotation checks** · P1 · Depends on: FR.1, Q-R
- File/Module: `solver/euler_solver.py` beside `named_turn_findings` (:140).
- Enhancement: ROTATION_INCOMPLETE (a named flip or cartwheel's turn run reaches its full turn, 360 unless declared
  otherwise), ROTATION_NOT_MONOTONIC (one sign across a multi-key run, e.g. the wizard's vault 0 → 90 → 180 → 360),
  INVERSION_MISSING (a flip or cartwheel run that passes 180 has its inversion printed). AIRBORNE_WITHOUT_LAUNCH is FR.4.

**FR.4 Launch before an aerial turn** · P2 · Depends on: —
- File/Module: S11 `p11_kinematic.check` (:29) or S13.
- Enhancement: the graph twin of AIRBORNE_UNBOOKENDED: a flip or cartwheel key without support lies inside an airborne
  span that has a takeoff (support to none) and a landing or the clip's end state. The fight passes (takeoff after
  4.4, landing 5.9).

**FR.5 Camera arc with the rotation** · P3 · Depends on: Q-P, camera slice (C10)
- File/Module: `schemas/graphs/camera_plan.schema.json` (optional `movement.arc_deg`), `validators/camera_validator.py`, the genre
  camera cards.
- Enhancement: a shot covering a declared flip, cartwheel or spin uses an orbit, crane or arc move whose arc lies at the
  card's ratio of the rotation (anime 0.5, live action 0.1, within 10 degrees) and tilts with it (C10 "orbit on spins").

**FR.6 Money-shot frame parts** · P2 · Depends on: FR.1
- File/Module: the S17 plan (`schemas/graphs/frame_parts_plan.schema.json`), `p17_render.check` (:59); the reference
  render plan (content).
- Enhancement: in anime, a flip or cartwheel gets a hold at its derived inversion time (2-3 frames) inside a shot played
  slow, and a smear on the kicking limb during the turn; check MONEY_SHOT reads the genre card. Reference content:
  hold at 5.30, left-leg smear 5.1-5.5, cartwheel inversion hold at 6.45.
- **Amended by W1 (O47):** the apex hold stays in the graph; the prose prints the smear on the kicking limb and, if any,
  a camera hold in V5's wording, never a body freeze in frames (R14 froze 0.85 s for "3 frames").

**FR.7 Genre values in the existing cards** · P2 · Depends on: Q-Q, Q-N, Q-O
- File/Module: `library/camera_conventions/<genre>.yaml` (arc ratio, apex slow motion), `library/joint_limits.yaml`
  (only if Q-O changes it), a new `library/fx_profiles/<genre>.yaml` (inverted hold, impact hold, smear and speedline
  policy, dust on landing, shake), all logged; checks read the scene genre's card.
- Why: the repo already keys behaviour by genre card; one more card per genre keeps that pattern. Realism = live_action.

### Part 3 additions (all derive or check; none edits authored data)

| Fix | File/Module | Current | Gap | Enhancement | Why | Priority | Depends on |
|---|---|---|---|---|---|---|---|
| FP.1 Bartenieff agrees with the pose | S12 check (`p12_bartenieff.py`) reading S13 keys | vocabulary + body-mode coherence | a claimed pattern the pose does not show | BARTENIEFF_POSE: body-half → one side leads the change, cross-lateral → a diagonal arm-leg pair moves together, head-tail → spine, neck and head engaged, upper-lower → arms and legs move together, breath → torso change with little limb change (interpretation, labelled) | uses existing S12 and S13 data | P2 | — |
| FP.2 World motion as states | reference plans (smoke `dissipating`/`gone` times), world card ambient line in SCENE, impact fx on surfaces | smoke bursts, never shown dissipating | curves for smoke, sway, shake | print each persistent state's span ("smoke dissipating 4.50-6.00, gone from 6.00"); ambient words from the world card; reactive shake as an S17 fx at a surface impact | existing card states and fx channel | P3 | Q-V |
| FP.3 Line tension | prose `line_links` (F8), rope states | wrapped/taut states | tension curve, anchor | "taut from 8.50, anchored at B torso, pulled by A L hand" from the line states and contacts; friction and restitution only as card values if asked | extends M8.12c | P3 | — |
| FP.4 Causal delay | prose `_causal` | reasons printed | delay between cause and effect | "→ (+0.40 s)" from the beats and contact times; REACTION_WITHOUT_CAUSE already refuses a negative delay | derived | P2 | F5.3 |
| FP.5 Body velocity and acceleration | `solver/` (finite differences of S04 anchors), strike lines | none | velocity, acceleration | printed on strike and landing lines; jerk is not meaningful from sparse keys and is stated as such | derived | P3 | F9.2 |
| FP.6 Phrasing and drives | S15 derived fields, prose | LBN phrase chain | phrasing, drive | drive from which Effort factor is latent (action: flow latent; passion: space latent; vision: weight latent; spell: time latent), phrasing from the intensity profile over an interval run (impulsive = accent first, impactive = accent last, swing = middle); PHRASING_MISSING | derived from S15 | P3 | Q-W |
| FP.7 Contact materials | contact bow text | limb > target part | materials | from cards: prop `materials` (kunai steel), costume (B's armour) → "R foot sole (flesh) > kunai blade (steel)" | existing card data | P3 | F3.1 |
| FP.8 Curves: interpolation, anticipation, follow-through, secondary motion | IMPLIED GUIDANCE (`prose_renderer._implied` :362) | qualitative lines | curves and parameters | curve words per segment from Effort time and flow (sudden → snap in, sustained → ease in-out, bound → stop short, free → overshoot and settle); numbers kept in the graph unless Q-V says print | follows the DAG's implied-guidance format (C4, K-Btw) | P2 | Q-V |
| FP.9 Character state | `kernel/state_vocabulary.yaml` (logged), reference plans | condition only | wounds, costume damage, exhaustion | new actor properties set by effects (B's shoulder wound at 9.00), printed as lasting rules | existing state machine | P3 | Q-X |
| FP.10 Scale and perspective | S16 shot text from `camera_geometry` | lens, position | scale anchors | print camera height and the frame's scale anchor (pillar 8 m) per shot; consistency checked with C10 | derived | P4 | camera slice |
| FP.11 Line of action | S13-derived, strike lines | none | curve of the body | C, S, straight or spiral from the spine and lead limb angles | derived | P3 | — |
| FP.12 Silhouette | FK (F5.1) + camera projection | none | readability | flag a strike whose striking limb overlaps the torso from the shot's view | derived | P4 | F5.1, camera slice |

### Cross-cutting validators (the plan's E2, E4)

**F9.1 Laban direction (E2, D5)** · P2 · Depends on: Q-K
- File/Module: S15 `p15_effort.check` (:68) with S04 positions and S13 keys; prompt code SHAPE_DIRECTION.
- Enhancement: per interval, compare the declared Shape quality and Space plane with the measured root and torso
  motion (rising: up; sinking: down; advancing/retreating: toward/away from the target; spreading/enclosing: limbs
  away from/toward the centre; plane: the dominant axes); Effort time against measured speed (sudden = fast).
  Interpretation labelled: Laban Shape qualities describe the body's form change; the root-trajectory reading is the
  plan's (Q-K).

**F9.2 Momentum (E4, L4)** · P2 · Depends on: —
- File/Module: S11 or S13 check (support per slot is known there); prose MOTION CONTROL; gap MOMENTUM_MISSING.
- Enhancement: derive each body's root velocity between keys; refuse an airborne span (no support at both ends) whose
  root rises or hangs against gravity without a declared float (anime) or a push contact; print velocity on strike
  lines.

**F9.3 Anticipation (L3)** · P3 · Depends on: Q-H
- Enhancement: ANTICIPATION_MISSING: every strike has a preceding key or implied-guidance line with loading/coiled
  intent within a span (DAG K-Ant: "strong actions have clear preparation").

**F9.4 Reaction (L13)** · P3 · Depends on: F5.3
- Enhancement: POST_CONTACT_MISSING: every strike's target has a key at or just after the contact with yielding /
  off-balance cues and a pose change; optional `reaction` words (deformation, head snap) printed from S11.

## 6. Dependency and contract updates

- **No new packages.** Keep JSON Schema 2020-12 with the in-repo validator (`validators/schema_validator.py`); no
  Pydantic (T1). The only runtime dependency stays `pyyaml`.
- **Schemas (each version bump logged in `schemas/schema_log.jsonl`):** `beat_plan` and `temporal_graph` 1.3 → 1.4
  (Contact.surface, Contact.verb, PropSample.phase, Beat.callback); `bartenieff_plan` (optional link offsets); the
  `frame_parts_plan` (impact force, freeze, shake; speedlines part); the motion graph (derived limb-end points).
- **Library (logged):** a combat-verb card; a segment-lengths card for FK; `library/fx_profiles/<genre>.yaml`
  (part 2); camera-card values for arc ratio and apex slow motion (part 2).
- **Part 3 (logged, only on the owner's yes):** actor properties for wounds, costume damage and exhaustion in
  `kernel/state_vocabulary.yaml` (Q-X); friction and restitution as card values if asked; no per-frame stores before M7.
- **Part 2 schemas (logged):** `motion_plan.schema.json` (optional `limb_paths`), `camera_plan.schema.json` (optional `movement.arc_deg`).
- **Kernel (logged):** none required; debris/ember states only if Q-H says so.
- **Map (`kernel/knowledge_map.yaml`, logged):** new codes on rows: PROP_PHYSICS_UNSTATED (C31, C5), PROP_VISIBILITY
  (C5, C23), CONTACT_WORLD (C21, C12), IMPACT_CONTACT_SYNC (C12, C25, STY), SHAPE_DIRECTION (LMA, T6), the momentum code
  (T10, C22, BIO), IDLE_FIGHTER (to place), CHAIN_ORDER (KC), ANTICIPATION_MISSING (KF), POST_CONTACT_MISSING (C21).
- **Prompt codes:** each new code gets a break in `tests/test_dag_conformance.py` and a READS entry.
- **Owner decisions to add:** answers to Q-A … Q-K as O22+.

## 7. Verification checklist

For every fix:
1. Predict, then run `scripts/check.sh > gate.log 2>&1` (exit 0) in the worktree.
2. The new code fires on its break test, and on the old prompt the render saw (the finding it closes is "caught" in
   `validators/checklist.py` FINDINGS).
3. `python -m compiler.rebind --write <examples>`; `python -m compiler.examples --write`; compare `render.txt`
   byte-for-byte before and after: unchanged unless the fix is meant to change LBN, and then the diff is limited to the
   fields it names.
4. `python -m validators.checklist --write`: no row goes from PASS to anything else; the rows the fix names go from
   NOT CHECKED to PASS (or to FAIL with an owner question).
5. Golden: `tests/test_reference_fight_golden.py` passes, every change to the golden's numbers recorded beside the
   existing deviations (HIP_CLAMPS, VANISHED, ROOT_TURNS, PREFACE_RECOUNTED …) with its owner decision.
6. Logs: every schema, library and kernel change has its entry; `python -m kernel.build_docs --check` passes.

For the golden as a whole: every prompt code returns no finding on all four prose prompts (`KNOWN` stays empty), and
its checklist shows no FAIL.

For the money shots (part 2): the golden test asserts the 5.1 flip (about X, -360 in 0.4 s, inversion printed at
5.30, hold there, left-leg smear) and the 6.3 cartwheel (about Z, -360, inversion at 6.45); a unit test runs the same
turn under the anime and the live-action cards and gets the two genres' thresholds.

For part 3: every derived track is a pure function of the envelope (a determinism test compiles twice and compares),
and compiling never changes an authored plan (a test hashes `plans/*.json` before and after).

For the 16 layers: add a coverage report (part of the applicability stage, O16) that lists, for every slot of every
example, which of the 16 layers the envelope carries and which the prompt prints; a layer that applies but is absent
is a NOT CHECKED row, never a silent pass.

## 8. Open questions (one line each)

- **Q-A** Combat verbs: keep `effort.action` as Laban (punch = thrust quality) and add `verb` on contacts (F4.1), instead of putting deflect/parry/... into `effort.action` as the plan says?
- **Q-B** Strike timing: move every strike, throw and release contact to its key pose (`at: start`), so the deflect lands at 2.5 as the golden says (the golden's contact times become recorded deviations)?
- **Q-C** World contact points: compute them from the pose by forward kinematics with a new segment-length card and check them (F5.1-F5.2), rather than author them as numbers?
- **Q-D** "Every beat, all 16 layers, no exceptions": keep all 16 in the graph and print them selectively (strike and support-change lines, DAG C2 and O19), or print every layer on every line?
- **Q-E** The plan says a code that contradicts the golden is wrong; O7, O10, O17, O18 and O21 changed the golden where it contradicted its own words or the DAG. Do those decisions stand?
- **Q-F** B's active keys: add them to the reference fight (new B keys and beats, recorded deviations), and what idle span should IDLE_FIGHTER allow (e.g. 0.8 s without an active key while A acts)?
- **Q-G** Callbacks: the plan's example (a kawarimi at 7.5 mirroring 3.7) is not in the fight (7.5 is the rope-dart regrapple); which beats are callbacks of which?
- **Q-H** World state: mark the pillar (shuriken, kunai) and crack the ground at the crash with the existing damage values, and add debris/embers as new states, or the first only?
- **Q-I** Causal overlay: show causes only through existing FX (impact flash, speedlines) and the printed reasons, never as drawn arrows or markers?
- **Q-J** Out of scope until M7: the per-frame retry loop (`render/session.py`) under "never render, no paid API"; and no Pydantic `schema.py` (JSON Schema stays). Agreed?
- **Q-K** Laban direction: check Shape qualities against the root trajectory (the plan's reading), the torso and limb spread (Laban's form-change reading), or both?

- **Q-L** Axes: keep the repo's frame (flip or somersault about the lateral X axis, spin about Y, cartwheel about the sagittal Z axis, as MovementXML defines them) instead of the plan's backflip about Y?
- **Q-M** Rotation keyframes: derive the quarter-turn angles, inversion time and angular speed from the declared turn and print them, instead of authoring 5.2/5.3/5.4 keys?
- **Q-N** Anime gravity: exempt a body from the airborne gravity check only where a hang or float is declared (as props are, O8), instead of ignoring gravity after every anime launch?
- **Q-O** Limb extension: keep O11 (anime +30 degrees per joint over the human table) or switch to ×1.3 with a 150-degree cap?
- **Q-P** Camera arc: adopt arc = 0.5 × rotation for anime and 0.1 × for live action (within 10 degrees) as camera-card values? (The DAG's C10 says only "orbit on spins".)
- **Q-Q** Genre profile: extend the existing per-genre cards (camera, joint limits, a new FX card per genre) instead of one combined profile file, with "realism" = live_action?
- **Q-R** Completion: must a named flip finish its full turn inside the clip? (The wizard's dodge_flip ends at 180, inverted; yes means adding its landing key.)

- **Q-S** Keep the repo's rule that scripts derive and refuse but never edit authored beats, so resolve_contacts, integrate_momentum and apply_follow_through become checks and derived guidance?
- **Q-T** Rendering scripts (dispatch, validate render, retry, assemble) and per-model hints wait for M7, after you pick the model and settings (Q8) and authorise API use?
- **Q-U** Sound: add a SOUND section now, printed from the contacts, impacts and materials the graph already has, or leave sound until the model is chosen?
- **Q-V** Numbers for curves, secondary motion and world motion: keep them in the graph and print words (the DAG's implied-guidance format), or print the numbers too?
- **Q-W** Phrasing: use the plan's list (impulsive, impactive, swing, sustained) with drives derived from the latent Effort factor; "remote" is a Laban state, not a phrasing, so drop it?
- **Q-X** Character state: add wounds, costume damage and exhaustion as new states (kernel change) and set them in the fight (B's shoulder wound at 9.00)?

Proposed order once answered (merges both parts with NEXT_SESSION's queue): F5.3 strike timing → F6.3 grounded
pickups → F2.1/F2.2 prop physics → F6.1/F6.2 visibility → FR.1/FR.3 rotation path and checks → F5.1/F5.2 world
contact → F4.1/F4.2 verbs → O21 opening → F9.1 Laban direction → F9.2 momentum with FR.4 → F4.3/F4.4 B active →
FR.7 genre cards → FR.6/FR.2 money-shot frame parts and limb paths → O19 D9 lines → camera C10 with FR.5 and
F8.1-F8.3 → F4.5, F4.6, F9.3, F9.4 → F6.4 → part 3 in tiers: FP.1, FP.4, FP.8 → FP.2, FP.3, FP.5, FP.6, FP.7, FP.9,
FP.11 → FP.10, FP.12 → applicability stage (O16) with the 16-layer coverage report. Deferred to M7: per-frame tracks,
rendering, validation and retry, per-model hints.

## Answers (owner, 2026-10-11)

"All recommended": Q-A → O22, Q-B → O23, Q-C → O24, Q-D → O25, Q-E → O26, Q-F → O27 (idle span 0.8 s), Q-H → O28
(existing damage values first), Q-I → O29, Q-J → O30, Q-K → O31 (both), Q-L → O32, Q-M → O33 (derive), Q-N → O34,
Q-O → O35 (keep +30 degrees), Q-P → O36, Q-Q → O37, Q-R → O38, Q-S → O39, Q-T → O40, Q-U → O41 (sound waits), Q-V → O42
(words), Q-W → O43, Q-X → O44. Q-G had no recommendation and stays open: which beats are callbacks of which.

The owner's Seedance axis tests (R6-R10, `docs/render_tests/2026-10-11-seedance-axis/`) support O32 (the axis and plane
words were followed in all five) and add evidence for FR.1, FR.5 and FR.6 (timing, rotation counts, holds and the
camera arc were not followed).

## 9. Final build order (v1.0)

1. **W wording rules** (W1-W4: BODY_HOLD_FRAMES, EMPTY_HAND_UNSTATED, ROTATION_ANGLES_PRINTED, HIDDEN_PHRASING; O48's
   post) and O54's four negatives in the reference fight's cards.
2. F5.3 strike timing (IMPACT_CONTACT_SYNC) with V1b's deflect wording.
3. F6.3 grounded pickups (AIRBORNE_PICKUP).
4. F2.1/F2.2 prop physics, F6.1/F6.2 positions and rest (as amended by W4).
5. FR.1/FR.3 rotation path and checks (as amended by W3).
6. F5.1/F5.2 world contact points (CONTACT_WORLD).
7. F4.1/F4.2 verbs and Laban wording.
8. O21 opening (wording from the owner's V6 render, O51; SURFACE_HEIGHT).
9. F9.1 Laban direction, F9.2 momentum, FR.4 launch.
10. F4.3/F4.4 B's active keys (IDLE_FIGHTER).
11. FR.7 genre cards; FR.6/FR.2 money-shot frame parts and limb paths (as amended by W1).
12. O19 D9 lines (LINE_DENSITY).
13. C10 camera in V5's wording, FR.5, F8.1-F8.3 (as amended by W1).
14. F4.5 chain timing, F4.6 callbacks (O50's five), F9.3 anticipation, F9.4 reaction.
15. F6.4 world state; part 3: FP.1, FP.4, FP.8, then FP.2, FP.3, FP.5-FP.7, FP.9, FP.11, then FP.10, FP.12.
16. The applicability stage (O16) with the 16-layer coverage report.
17. One full-fight render by the owner (D9 lines, camera, part 3 words), logged.

Checks planned: 43 new codes (the 39 of the earlier count plus W1-W4). Deferred to M7: per-frame tracks, rendering,
render validation, retry, model adapters (O49), sound (O41).

## Closing answers (owner, 2026-10-11, before the push)

Q-G → O50 (all five callbacks) · V6 → O51 (the owner renders it before the opening slice) · the other session's work →
O52 (untouched) · Q6 → O53 (keep the 180-degree rule) · Q7 → O54 (four negatives added, FINAL saved) · Q3 → O55 (no
reasons in LBN) · verdicts and Q8 → O56.
