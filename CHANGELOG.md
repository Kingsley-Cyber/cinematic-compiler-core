# Changelog

All notable changes, newest first. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[docs/versioning.md](docs/versioning.md). Before 2026-10-11 the record is the git history and the checkpoint tags.

## Unreleased

### Added
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
