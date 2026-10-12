# S-033 — M9-06e: body_type lives in the genre profile cards (schemas/genre_profile.schema.json), not the modality schemas

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-06e (added this session); rulings O85 (as clarified), O65, O37; S-031

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-033]

## Plan
The owner: "Genre profiles gain a body_type field. The FK solver reads body_type from the genre profile." The repo
already has the genre profile's contract, `schemas/genre_profile.schema.json` (DRAFT 0.1, owner O65: FR.7's per-genre
values, O36, O37; "no data file uses it yet"). S-031 missed it and put `scene.body_type` in the per-genre modality
schemas. This slice puts it where the owner named it: the genre profile schema gains a required `body_type` (0.2,
logged); one genre profile card per genre, `library/genre_profiles/{anime,live_action,ugc_ad}.yaml` (draft, logged),
carries it (anime: anime; live action, UGC: adult); `planner/genre_profile.py` loads and validates a genre's card;
`solver/forward_kinematics.segments` reads its body_type; the modality schemas drop `body_type` (1.2, logged) and
`planner/modality.body_type` goes, so one place decides.

Predictions, made before the change:
1. The gate passes before the change: 640 tests.
2. No packet moves and every output is byte-identical (the same metres reach S13 and S04).
3. 641 tests (one test that each genre profile card validates and names a body the segment card has).

## Decisions
- D1 — The genre profile is the owner's own contract, `schemas/genre_profile.schema.json` (O65), with one card per
  genre in `library/genre_profiles/` (the folder name is Claude's, beside `library/camera_conventions/`); body_type is
  required there. Why: the owner's words ("Genre profiles gain a body_type field") and O65; S-031 had used the
  modality schemas because a truncated search hid this schema (lesson L-25). Level: covered (O85, O65).
- D2 — The modality schemas drop body_type (1.2) and `planner/modality.body_type` goes. Why: one place decides (the
  owner: "The FK solver reads body_type from the genre profile"). Level: covered.
- D3 — The cards carry only the required fields and body_type; FR.7's rendering values (arc ratio, holds, smear and
  speedline policy, dust, shake, float) wait on M9-11. Why: no ruling sets those values yet. Level: covered.

## Duration
about 25 minutes

## Changes
- `schemas/genre_profile.schema.json` 0.2 (body_type, required); `library/genre_profiles/{anime,live_action,ugc_ad}.yaml`
  (new, draft); `schemas/modality/*.schema.json` 1.2 (body_type removed); `library/body_segments.yaml` 4 (comment); all
  logged
- `planner/genre_profile.py` (new), `planner/modality.py`, `solver/forward_kinematics.py`
- `tests/test_forward_kinematics.py`; ADR-O85; F-053; lesson L-25; backlog 9 (M9-06e); CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (S-032, 553b302)
- after: `scripts/verify.sh` exit 0, 640 passed (the first run failed one long line); `python -m compiler.rebind`
  silent; `python -m compiler.examples` exit 0 (every output byte-identical)
- Prediction 1 held. Prediction 2 held. Prediction 3 failed on the count: 640, not 641 (the body test was extended,
  not added).

## Next
The owner's ten asymmetric things per beat (ADR-O87, a plan and its slices).
