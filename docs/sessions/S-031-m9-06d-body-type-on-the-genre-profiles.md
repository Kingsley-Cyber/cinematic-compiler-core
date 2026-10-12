# S-031 — M9-06d: the genre profiles name each genre's body type; the card holds two bodies (O85 as clarified)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-06d (added this session); ruling O85 as the owner clarified it; F-053

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-031]

## Plan
The owner, 2026-10-11, after S-030: "Schema change: body_segments has two entries (adult, anime). Genre profiles gain a
body_type field. The FK solver reads body_type from the genre profile. No per-key flag. No per-performer frame. Update
the card, the schema, and the genre profiles."

S-029 put the choice in the card (each body listed its genres, with a default body). Now: the card holds two bodies keyed
by type (schema 3.0, card 3, logged); each genre profile, the per-genre modality schema that already carries the
genre's fps and duration defaults (`schemas/modality/<genre>.schema.json`, ADR-O37: no new combined profile file), gains
`scene.body_type` (const and default; 1.1, logged); `planner/modality.body_type(genre)` reads it and
`solver/forward_kinematics.segments(genre)` takes that body from the card. The lengths do not change.

Predictions, made before the change:
1. The gate passes before the change: 639 tests.
2. No packet moves and every output is byte-identical (S13's packet carries the same metres, S04's the same standing
   leg): `make golden` unchanged, `compiler.rebind` silent.
3. About 640 tests (one profile test).

## Decisions
- D1 — The genre profiles are the per-genre modality schemas (`schemas/modality/<genre>.schema.json`): they already
  hold each genre's fps and duration defaults and are read through `planner/modality.py`. `scene.body_type` is a const
  with the same default, so a scene can never claim another body. Why: the owner's words ("Genre profiles gain a
  body_type field"), ADR-O37 (genre values go in the existing per-genre cards, no combined profile file). Alternatives:
  a new `library/genre_profiles/<genre>.yaml` card (a combined profile O37 turned down); the camera cards (a camera
  layer). Level: covered (O85, O37); the choice of file is an interpretation (F-053).
- D2 — The card's bodies are keyed by type and carry no genre list or default; a genre with no body_type fails to load.
  Why: "The FK solver reads body_type from the genre profile"; one place decides. Level: covered (O85).
- D3 — Backlog 8: M9-06d (this, done) and M9-09h (F-071's ruling, next); M9-10 back to ready. Level: covered.

## Duration
about 25 minutes

## Changes
- `schemas/cards/body_segments.schema.json` 3.0, `library/body_segments.yaml` 3 (two bodies keyed by type);
  `schemas/modality/{anime,live_action,ugc_ad}.schema.json` 1.1 (`scene.body_type`); all logged
- `planner/modality.py` (`body_type`), `solver/forward_kinematics.py` (`segments` reads the profile)
- `tests/test_forward_kinematics.py` (the profile test); ADR-O85 (the owner's clarification); F-053; backlog 8;
  CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 639 passed (S-030, e5c1682)
- after: `scripts/verify.sh` exit 0, 639 passed (the first run failed only the docs plane, before the backlog row
  existed); `python -m compiler.rebind` silent; `python -m compiler.examples` exit 0 (every output byte-identical)
- Prediction 1 held. Prediction 2 held (no packet moved, nothing changed in the outputs). Prediction 3 failed on the
  count: 639, not about 640 (the existing body test was rewritten, not added to).

## Next
M9-09h (F-071: B moves to A's far side at 8.0, the owner's ruling).
