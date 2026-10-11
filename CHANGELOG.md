# Changelog

All notable changes, newest first. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[docs/versioning.md](docs/versioning.md). Before 2026-10-11 the record is the git history and the checkpoint tags.

## Unreleased

### Changed
- The reference opening follows O21 (M9-08a, S-015): A starts at root y=10 above the frame and lands with the feet
  on the 8 m pillar top, root 8.5 (S04 anchors, S13 roots, the golden test's recorded deviation).
- Laban actions print as qualities (M9-07b, plan F4.2, owner O22, S-014): the implied guidance writes "(thrust
  quality)" for punch and "(press quality)" and so on; S15's data and LBN-2.4 keep the Laban vocabulary.

### Added
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
