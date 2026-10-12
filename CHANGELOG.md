# Changelog

All notable changes, newest first. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[docs/versioning.md](docs/versioning.md). Before 2026-10-11 the record is the git history and the checkpoint tags.

## Unreleased

### Changed
- Hits come from the contacts (RV-57, F-155, S-062): a touch on another performer's body, a strike or deflect on a prop
  another holds or threw, a catch of a body, or a body touched by another's held blade owes a static camera hold on
  every body present, checked at S16 (new), at S17 and in the prompt, whatever S17's frame parts hold (owner O92). The
  examples' hits already were holds; no prompt changed.
- Two contradictions in the reference prose gone (RV-62, F-163, F-105, S-061): A's 3.70 line ends its support as A
  vanishes and no longer walks A to 4.40 (owner O90), which the prompt's VANISHED_BODY now checks; B draws the shuriken
  volley from the thigh pouch at 5.1 and lets it go with the 5.5 throw, so B no longer throws from an empty hand (the
  volley's card gains flight `drawn`; deviations DEV-30, DEV-31).
- "Before a beat" is read one way (RV-61, F-161, S-060): a beat's state snapshot keeps the values its own at-start
  effects replaced (`before_own_effects`, state_graph 1.4), which S10 reads for preconditions and postconditions as
  S06 reads requirements; S09 carries each change's instant (object_state_graph 1.2) and credits only a hand on the
  object by then. No prompt changes.
- The camera cards follow O92 (RV-60, F-160, S-059): no close-up after a blow, no insert on a landing blade and no
  slowed playback in the draft cards (every convention card plays normal only); the prompt's printed camera rules are
  checked for both (HIT_HOLD, PLAYBACK_RAMP), so twelve prose prompts lose one sentence each.
- The authoring instructions follow the code (RV-48b, F-135, F-137, F-162, S-058): the S04 instructions teach the rules
  S04 to S07 apply to a beat plan today, each by its code, and the S08 ones S08's; a test fails when a step's
  instructions miss one of its codes. S08 refuses a named support hand that neither holds nor touches its object.
  RV-20's prompt part for S11 to S17 is RV-65.
- S04's latent checks (RV-48a, O23, F-135, F-136, F-138, F-139, F-158, S-057): a throw or release happens on its
  actor's key (RELEASE_AT_POSE), so B throws A at 6.6, on the catch's pose, as the source flashes it; nobody touches a
  vanished body and a touched body is in its beat; a contact between two samples moves a resting prop only by taking
  hold of it, and a substitution swaps its decoy into its new place, so the log takes A's former place at 3.7 with no
  hand on it; a free prop starts somewhere.
- The records corrected (RV-46, F-130, F-140, F-166, S-056): the owner lists name every owner_default ADR awaiting
  confirmation and the pre-commit hook (F-168); overclaims and stale lines corrected at their files (this CHANGELOG's
  RV-09, RV-10 and RV-42 lines among them); the sessions' Duration by the commit times; the track test shows its claim
  again.
- Each slice's records (RV-45, F-128, S-055): from S-055 an applied session records its self-audit or the docs plane
  refuses it; the session template (3.0) asks for the predictions' clock time and labels choices no ruling makes as
  interpretations, which F-053 lists; the golden's records are typed deviations DEV-01 to DEV-28, each with its ADRs
  (examples/reference_fight/deviations.yaml), and a test refuses one without.
- Principal review 3 (S-054, finish.md section 6): five read-only reviewers, verdict "partially"; their gaps filed as
  F-152 to F-167 with slices RV-55 to RV-64 (three wait for the owner). The records come first (RV-45, RV-46).
- The 6.3 cartwheel is a full turn in the words too (RV-12, O96, F-087, S-053): A's 6.3 row says "one full turn", as its
  keys roll it; a recorded rewording.
- `cinematic compile` refuses a prompt that is not a deliverable (RV-11, O94, F-085, S-052): it runs the prompt checks
  and the checklist on every prompt it emits and exits 5, writing nothing, unless all five are deliverables; a row the
  DAG excludes is N/A unless a code checks it. R-19 says so (rules 7.0). No prompt is a deliverable yet.
- The kunai drive and the catch (RV-10, O93, F-084, S-051): from 8.5 the kunai is embedded in B's shoulder to the end,
  its samples on B's torso point (the shoulder has no part of its own; F-165), while A stays its holder, though A's
  right hand is 0.66-0.87 m off it under the source's own arm numbers (F-148); B's hands take A's left arm at 6.6 and
  throw A at 6.8, off its pose against O23 (F-158; corrected in RV-48).
  Neither prints as an instant strike: a body struck by a blade another holds is not striking, and a catch's hold
  counts as the contact on its impact frame (IMPACT_CONTACT_SYNC at S17 and in the prompt). CONTACT_VERB lets a catch
  and a throw name a body (combat verbs 2).
- Hits are camera holds (RV-09, O92, F-083, F-005, S-050): the hits at 2.5, 4.7 and 8.5 are static holds with both
  fighters named in frame at 35 mm (checked across the frame only: the camera aims above them, F-090, RV-15; and only
  where S17 placed a hold, F-155), no insert, no slow motion; no shot changes playback speed. S16 refuses a slowed shot
  (PLAYBACK_RAMP), S17 a hit that is no camera hold on the bodies (HIT_HOLD), and the prompt checks both. The camera
  grammar's impact intent follows O92 (2); R-21 adds it (rules 6.0). The source's lenses are kept (fov45 at 0; the push
  in at fov35 from 9.5, its own shot). The wizard example's kick and landing are holds too.
- No body through another (RV-49, F-144, R-18, S-049): each segment is a capsule with a draft radius from the body card
  (library/body_segments.yaml 5, schema 3.1); S13 refuses two bodies that overlap at an instant both have a key
  (BODY_OVERLAP), and CONTACT_WORLD measures a contact between two bodies from surface to surface. B re-blocked at
  3.4, 3.7, 4.4, 4.7, 6.6, 8.5, 9.0 and 9.5 and the acrobat's kick at 3.6; shot c08 steps back to 2.1 m. A body
  through a prop is not yet checked (F-151, RV-54).
- The smoke bursts at 3.7 at A's body (RV-07, O91, F-082, F-132, S-048): a beat effect may say `at: start` (beat 1.3,
  embedded in beat_plan and temporal_graph 1.6) and S06 commits it at its beat's start; b09's smoke burst and the log's
  deployment take effect at 3.7, as the source says, and the spent pellet rests on the ground from 4.0. Each change in
  an S06 transition carries its own instant (state_graph 1.2), and the prompts' "From t to the end" rules, their check,
  the prop tracks and the first states read it. Every example re-bound.
- CONTACT_WORLD exceptions are the owner's alone (RV-43, F-123, S-047): kernel/contact_world_exceptions.yaml (kernel
  log) holds them by the scene's query hash; S13 reads them through its packet; the motion plan loses its
  `contact_world_exceptions` field (motion_plan 2.0), so an authored exception fails the schema. Every example re-bound.
- The deflect has one reading (RV-42, ADR-O108, F-122, S-046): the deflected kunai goes down to the ground on B's
  side, not at B; a prop track names a goal only where the prop's path reaches that performer; PROMPT_CONTRADICTION
  refuses "toward X" in a prop's track where the prompt says "NOT toward X" (render.txt's A row at 2.5 still keeps the
  source's "(toward B and ground)", F-166). S-043's records corrected.
- Principal review 2 (S-045, finish.md section 6): five read-only reviewers, verdict "partially"; their gaps filed as
  F-120 to F-150 with slices RV-42 to RV-53. The owner confirmed ADR-O102 and per-slice pushes (ADR-O107); rules 5.0
  (R-03, R-06, R-30) and finish.md 2.0 record it, and a question that would set aside an owner ruling or invariant now
  waits for the owner.
- The records agree with the repo (RV-04, F-078, ADR-O106, S-044): rules 4.0; the gate refuses an unbumped change in the
  schemas, library and kernel logs from now on; the library log reads `version` where a file has no `card_version`; the
  kernel log covers kernel/layer_order.yaml; the knowledge map is version 2; README points to docs/layer_order.md; stale
  ADR texts and answered findings (F-066, F-028, F-063) closed; F-015 stays open (no code catches it yet). The pre-commit hook waits on the owner (O52).
- CONTACT_WORLD measures a prop's release (RV-02b, ADR-O105, F-075, S-043): a thrown or dropped prop leaves the hand
  where the hand is. F-108 answered: B's kunai leaves the hand once, at the 2.0 throw. B throws from A's -Z side, so
  the kunai rises toward A, arrives along +Z and is deflected back down on B's side (corrected in S-046: the
  source's rule says "NOT toward B"; ADR-O108). Every S13
  packet carries the releases (the examples re-bound).
- The vanish lets go (RV-06, O90, F-081, S-042): at the substitution A's feet and left hand let go; the rope dart drops
  and lies on the ground until A takes it at 7.5 (the 5.9 release goes); A reappears on both feet at 4.4; VANISHED_BODY
  refuses a vanished body's open supports and holds; A's rows 4.4-6.3 and the slide's rule stop holding the dart
  (recorded deviations); the 7.5 crouch and B's 7.5 anchor move with the dart; shot c10 frames A's feet.
- The UGC creator takes the glasses on the table at the first frame (RV-03, F-077, S-041): the query's "Creator
  holding the glasses"; they rest on the creator's right, where the right hand reaches them; PROP_KINEMATICS keeps a
  resting prop where it rests when a contact takes it; the UGC keys follow their words (both hands at the glasses,
  elbows out; the index finger at the frame); the put-on's left hand takes the left temple; shot c02 is motivated by
  its unfold beat.
- A change of hands takes effect at its contact (RV-08, F-061, S-040): S06 commits a holder change at its possess or
  release, not the beat's end; each state transition records its instant `t` (state_graph 1.1) and the renderers print
  it, so the kunai is free at 2.00 with its release; S07 drops its special case. RV-03 now depends on RV-08 (the UGC
  creator takes the glasses at the first frame).
- CONTACT_WORLD per O89 (RV-02a, ADR-O104, S-039): only a point interpolated between keys or samples, with the actor
  airborne or the prop moving, is an artefact; no exact-instant miss is exempt and a turn alone never is. The repo side
  of each such miss is re-blocked: the kunai is deflected at A's right foot and lands at [1.4, 0, 3.77] (O77's
  v_post), and A's 8.0 crouch, B's 8.0 anchor and the dart move with it; the pellet leaves A's hand at 3.7; the volley
  leaves B's hand at 5.5; B's palm reaches the log at 4.0; B rises to A's knee at 4.7; the wizard's vault plants the
  right hand at its first key and the launch check accepts a hand launch (F-076). The source's slide at 5.9 is listed
  (ADR-O83 point 2). F-076 and F-079 resolved; F-075 open for RV-02b (releases; B's throw re-staged).
- A's limb and head words follow the source's words (RV-05, O88, S-038): 19 limb and 13 head flips in A's rows, each a
  recorded deviation; the hips at 0.6 keep their crouch (ADR-O103); A's 3.0 right foot now meets the ground, so
  CONTACT_WORLD needs no exception; B's catch at 6.6 re-blocked to A's moved elbow. RV-02 split into RV-02a and
  RV-02b, after RV-05 (backlog 13).
- C12 (Stylization layer) loses CONTACT_WORLD and reads NOT CHECKED until AS-06 (RV-01, F-074, S-037): its PASS on twelve
  prose prompts rested on a check of printed points. F-119 answered (ADR-O102: a test changes only where a ruling or
  the plan's intent moves the data it pins). Finish run 1 started.
- The finish run (owner O101, S-036): docs/prompts/finish.md and `/finish` work slice after slice, each committed and
  pushed, until the gate's six conditions hold; open questions are answered from the plan's own sources; the
  bootstrap (3.0) resumes a running finish run after a compaction.
- The first principal review (S-035, owner O99): the work matches the plan only partially. Its gaps are filed as
  F-074 to F-119 with PLAN-007 (slices RV-01 to RV-41); the owner's answers are ADR-O88 to O97; the gate's six
  conditions are in CLAUDE.md (O98); the anti-reward-hacking clause is in CLAUDE.md and AGENTS.md section 18 (O100,
  AGENTS.md 2.3); the owner's review prompt and no-shortcuts principle are kept in docs/prompts/. PLAN-006 corrected
  before its first commit. No code, data or test changes.
- The owner's ten asymmetric things per beat (ADR-O87, S-034): mapped against the repo and planned as PLAN-006
  (slices AS-01 to AS-06, with M9-14a and M9-14b amended); findings F-072 and F-073. No code changes.
- body_type lives in the genre profile cards (M9-06e, owner O85 as clarified, O65, S-033): one card per genre,
  `library/genre_profiles/<genre>.yaml` (draft), on `schemas/genre_profile.schema.json` 0.2 (body_type required);
  `planner/genre_profile.py` loads them and forward kinematics reads them; the modality schemas drop the field
  they gained in S-031 (1.2). No output changes.
- At 8.0 B stands on A's far side from the pillar (M9-09h, owner O86, S-032): B's anchor and key move along z to
  [1.4, 1.18, 3.7] with the dart on its torso, so the rope dart's pull and B's drag run toward the pillar as the
  source says. F-071 resolved.
- The genre profiles name the body type (M9-06d, owner O85 as clarified, S-031): `schemas/modality/<genre>.schema.json`
  1.1 gain `scene.body_type` (anime: anime; live action and UGC: adult); the segment card holds two bodies keyed by
  type (card 3, schema 3.0); forward kinematics reads the genre's body_type. No output changes.
- CONTACT_WORLD (M9-06b, plan F5.2, ADR-O83 accepted, S-030): S13 refuses a touch, hold or support whose two world
  points lie over 0.15 m apart, except an artefact (the actor airborne or turning, the prop moving: reported) and a
  source row the motion plan lists with its reason (motion_plan schema 1.1); the prompt prints both points. Seven
  repo-authored keys and four prop samples re-blocked (R-33); 24 of 33 contacts meet, one source miss excepted, eight
  artefacts reported. Rows C21 and C12. F-070 resolved.
- Hip angles are read from the trunk in every key (M9-06c, owner O84, rule R-35, S-029): the source's crouches put
  their soles on the ground only that way. The 43 repo-authored keys that lean through the spine have their hips
  re-expressed so no point of a body moves; 47 printed leg words change (R-33 deviations,
  tests/test_leg_frame_rewrites.py). The authoring prompt says so. Rules 3.1.
- The segment card holds two bodies (owner O85, schema 2.0, card version 2): anime bodies get the leg fitted to the
  source's grounded A rows (x1.25, standing pelvis 1.22 m); live action and UGC keep the 0.98 m adult. The anime
  examples' repo-authored roots re-rooted (+0.14 to +0.26 m), A's three repo-authored roots too; SURFACE_HEIGHT's
  bound is the body's standing leg. The miss list (F-070): 13 of 33 within 0.15 m, from 9. ADR-O83 accepted.
- The owner reviewed the contact-miss list (ADR-O82): calibrate the segment card first (backlog M9-06c), then
  CONTACT_WORLD (M9-06b, scope proposed in ADR-O83). Lesson L-22.
- The face's heading reads the whole chain, root, spine, neck and head (M9-09g, owner O76, rule R-34, S-026); a face
  near vertical keeps the old reading. No example output changes (no spine twists in the live-action and UGC keys).
- The reference query says A falls from y=10 (M9-09f, owner O79, S-025); the golden test records the rewording of
  k_preface_04. F-067 resolved.
- The kunai reverses to -Z at the deflect (M9-09d, owner O77, S-023): the source's v_post [0.5, -4.0, -3.0]; it lands
  at 2.7 on [0.6, 0, 4.0], where A takes it at 8.0. F-064 resolved.
- The owner's rulings (S-019): ADR-O72 (the root is the pelvis; contacts within 0.15 m), O73 (SHAPE_DIRECTION refuses
  contradictions only), O74 (anime declares hang time), O75 (slices rewrite the examples for their own checks, rule
  R-33; supersedes O71), O76 (whole-body checks read the whole body, rule R-34), O77-O80 (the kunai reverses to -Z,
  a resting prop has support, the query says y=10, a launch needs grounded support); rules 3.0; autopilot 2.0.
- The reference opening follows O21 (M9-08a, S-015): A starts at root y=10 above the frame and lands with the feet
  on the 8 m pillar top, root 8.5 (S04 anchors, S13 roots, the golden test's recorded deviation).
- Laban actions print as qualities (M9-07b, plan F4.2, owner O22, S-014): the implied guidance writes "(thrust
  quality)" for punch and "(press quality)" and so on; S15's data and LBN-2.4 keep the Laban vocabulary.

### Added
- Forward kinematics (M9-06a, plan F5.1, owners O24, O72, O81, S-027): `solver/forward_kinematics.py` and a draft
  `library/body_segments.yaml` (logged, schema `cards/body_segments`); S13 writes each key's world points (motion graph
  1.1); the repo-authored roots stand at the pelvis (the source's A rows unchanged); each touch prints its two points;
  `solver/contact_world.py` and `validators/contact_world_report.py` produce the miss report (F-070). CONTACT_WORLD
  does not refuse yet (M9-06b). SURFACE_HEIGHT judges a landing only on a pose at its instant.
- PROP_SUPPORT (M9-09e, owner O78, S-024): S04 refuses a free prop resting with nothing under it (a top within
  0.1 m, or a location or worn fact since its last hold); the smoke pellet is thrown down at 3.7 and bursts on the
  ground at 4.0. F-065 resolved.
- AIRBORNE_WITHOUT_LAUNCH (M9-09c, plan FR.4, owner O80, S-022): S13 refuses an airborne flip or cartwheel that
  starts turning on the ground or has no grounded support before it; the wizard's vault and dodge flip take off at
  1.20 and 8.60 (R-33); hang lines start at the first airborne key. F-058 resolved.
- MOMENTUM_MISSING (M9-09b, plan F9.2, owner O74, S-021): S11 holds an airborne span to the gravity arc through its
  takeoff and landing roots unless, in anime, its keys declare hang time (`float`; kinematic_plan and kinematic_graph
  1.1); the prompts say each hang once in RULES; the eight anime spans that hung declare it (R-33).
- SHAPE_DIRECTION (M9-09a, plan F9.1, owners O31, O73, O76, S-020): S15 and the prompt refuse a Shape quality the
  body's path and form contradict (`solver/shape_direction.py`; airborne turns are not judged); nine intervals across
  the four examples rewritten (R-33); the single-joint audit finds one defect, the face's heading (M9-09g).
- ENTRANCE_UNSTATED (M9-08b, probe V6, owner O51, S-016): a performer who starts in the air above a raised top gets
  V6's rule (its feet touch the top at the landing, not earlier) and negative (not standing on it at the start); F10
  is caught.
- SURFACE_HEIGHT (M9-08a, owner O21, S-015): at a foot support's onset on a surface with a known top (the world
  card's geometry text, or the ground), S04 refuses a root below the top or over 1.2 m above it; S04's packet carries
  each surface's geometry. F-067 found (the query's "falling from y=8").
- Combat verbs on contacts (M9-07a, plan F4.1, owner O22, S-013): Contact gains `verb` (contact 1.1, beat 1.2,
  beat_plan and temporal_graph 1.5, contact_graph 1.1); a draft card `library/combat_verbs.yaml` says which contact
  type takes which verb; S04 refuses a mismatch, a throw, catch or disarm naming no prop, and a throw whose prop is not
  moving (CONTACT_VERB); the staff prints THROW, DEFLECT, STRIKE before the bow; the reference fight's five named
  contacts carry their verbs. S04's packet named beat_plan 1.3 since S-009; a test now ties every packet's schema id
  to the file.
- Rotation runs (M9-05, plan FR.1 as amended by W3 and FR.3, owner O38, S-011): S13 refuses a run of keys that turns
  both ways (ROTATION_NOT_MONOTONIC), a named flip or cartwheel that ends off a whole turn or after the clip
  (ROTATION_INCOMPLETE), and one that is not upside down where it passes 180 degrees (INVERSION_MISSING); the prompt's
  ROTATION_PATH_UNSTATED reads every turn run, spins too. The wizard's dodge_flip completes: land_guard continues the
  flip to a landing key on a new hold beat b14 at 9.80 (O38).
- PROP_PHYSICS_UNSTATED and PROP_VISIBILITY (M9-04b, plan F2.1, F6.1 as amended by W4, F6.2, S-010): each prose prop
  block gains a WHERE line that tiles the scene with where the prop is (held by a hand, carried by its owner,
  ballistic under gravity from p and v, at rest at a place until the next event), derived in
  `renderers/prop_samples.track`; map rows C31, C5, C23 (kernel log). F-065 found.
- Pre- and post-contact prop samples (M9-04a, plan F2.2, S-009): PropSample gains `phase: pre | post` (beat 1.1,
  beat_plan and temporal_graph 1.4); PROP_KINEMATICS takes two samples at one time only as a pair on a contact at one
  position, checks gravity into the pre sample in velocity too, and needs the pair where a free prop moves into a
  contact; the reference fight's kunai deflect at 2.5 is a pair (recorded in the golden test); the rows print
  "pre-contact" and "post-contact". M9-04 split by step into M9-04a and M9-04b (backlog 2). F-064 found.
- The autopilot (owner O70, S-008): `docs/prompts/autopilot.md` and `/autopilot` build slice after slice without
  stopping until no slice is ready, committing each locally after the gate and the self-audit (never pushing); every
  decision goes in the session's new Decisions section (rule R-32, rules 2.0, session template 2.0); golden changes
  follow ADR-O71 (owner_default); the bootstrap README (2.0) resumes a running run; F-063 (version-bump drift).
- The bootstrap directory (owner O69, S-007): `docs/bootstrap/` with the resume steps, a generated `state.md`,
  the environment, the working agreements and the lessons learned; AGENTS.md (1.2) and CLAUDE.md point to it;
  `/bootstrap` opens it.
- The self-audit (owner O68, S-005): `docs/prompts/self_audit.md` and the `/self-audit` command check the agent's
  own work against the repo, read-only, before a commit or push; AGENTS.md step 9 and rule R-31.
- AIRBORNE_PICKUP (S11 and the prompt): a prop resting on a surface is taken only by a body with support, within
  reach; F7 is caught.
- IMPACT_CONTACT_SYNC (S17 and the prompt): every impact frame has a touch or support onset on it, every strike
  lands on an impact frame; S07 counts a release at its own beat's start as still holding at that instant.
- The docs plane (owner O64-O67, session S-002): AGENTS.md as a 17-section operating manual; five generated indexes
  (`docs/index/`); one file per plan, finding, decision, session and render, each with a template; generated
  `docs/layer_order.md`, `docs/rules.md` and `docs/plan.md`; `docs/for_the_owner.md`, `docs/how_to_refactor.md`,
  `docs/ownership.md`, `docs/versioning.md`; `scripts/verify.sh` as the single gate (`scripts/check.sh` calls it);
  a docs hash log freezing the hand-written docs; `make verify`, `make golden`, `make docs`.
- Seven schemas (O65): `layer_order` and `rules` validate kernel/layer_order.yaml and docs/rules.yaml; `beat`,
  `contact` and `rotation` hold the shared definitions, embedded where used by `kernel/shared_schemas.py` (checked by
  the gate); `genre_profile` and `motif` are drafts.
- Repeatability: exact dependency pins in pyproject.toml (pyyaml 6.0.3; pytest 9.1.1, ruff 0.17.0) and uv.lock; a
  Dockerfile (Python 3.12.14, uv 0.11.12) whose default command is the gate.
- CI: six workflows (verify, tests, golden, schemas, docs, nightly), each running inside the pinned image; the
  nightly job regenerates the generated docs and opens a pull request when they are stale. Not active until pushed.
- Prompt codes BODY_HOLD_FRAMES, EMPTY_HAND_UNSTATED, ROTATION_ANGLES_PRINTED, HIDDEN_PHRASING (M9 step 1, S-001).

### Changed
- Each prop records who carries it (M9-03b, owner O63, S-006): `carried_by` on prop nodes at S02 (brief_nodes 1.1),
  from the archetype cards' equipment; the prose says "carried by A" for the rope dart and smoke pellet and "carried
  by B" for the shuriken volley.
- Grounded pickups (M9-03, owner O18, S-004): A pushes off the pillar at 7.0, lands crouched by the rope dart and
  takes it at 7.5, runs to the kunai and takes it crouched at 8.0, then leaps at 8.5; c18 and c19 re-aimed (azimuth
  28 and 10) so both bodies stay framed on their sides; two golden rules reworded (k_rules_18, k_rules_27).
- One time per hit (M9-02, owner O23, S-003): the reference fight's strike, throw and release contacts happen at
  their pose (throw 2.0, deflect 2.5, palm 4.0, knee 4.7, shuriken 5.5, catch 6.6, kunai drive 8.5); the kunai and
  log fly and fall under gravity; four camera cuts are motivated by their own beat and the 8.5 insert shows B's torso;
  each strike's recovery line says "one instant contact, the limb does not stay on the target" (R16).
- The prose prints camera holds on hits instead of body holds in frames, the empty hand after a release, each turn
  once by axis, plane and count, and no hidden props (W1-W4, owner O47-O49).
- The reference fight's substitution log stands beside A from 0.00 (O48); FINAL's four negatives are added through
  the fighters' cards (O54).
- Decisions, renders and findings moved out of MASTER_PLAN.md, render_log.md and the two findings reports into one
  file each (O64); the reports live in `docs/reports/`.

## checkpoint-2026-10-11-m9-plan (8125483)

- M9 plan FINAL v1.1: the owner's cinematic_beat_v2 plan deconflicted against the repo, decisions O22-O56, the probe
  wording rules, renders R6-R18 logged.

## checkpoint-2026-10-11-m8.9 (16ff68c)

- M8: structured-prose prompts in four modes beside LBN-2.4, the DAG conformance check and the per-prompt checklist;
  the compiler.rebind tool.

## checkpoint-2026-10-11-m3.5 (9c9fd98)

- S01-S17 built (M1-M5.5, M3.5 face layer): four examples compile byte for byte; schema, library and kernel hash logs.
