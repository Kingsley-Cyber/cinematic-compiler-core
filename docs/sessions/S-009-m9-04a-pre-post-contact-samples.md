# S-009 — M9-04a: pre- and post-contact prop samples (F2.2)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-04a (split from M9-04; PLAN-003 F2.2); rulings O8 (prop samples), O61 (the approved build order)

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-009]

## Plan
F2.2 of the deconfliction plan: a deflect is an instantaneous velocity change, but S04 keeps one sample per prop and
time, so the kunai's flip at 2.50 has only its post-contact velocity. Add an optional `phase: pre | post` to
PropSample (beat 1.1, embedded in beat_plan 1.4 and temporal_graph 1.4, logged); PROP_KINEMATICS gains the pair
rules: two samples of a prop share a time only as a pre and a post on a contact at that instant, at one position;
gravity is checked into the pre sample (position and velocity) and out of the post sample; a free prop moving into a
contact needs the pair. The reference fight's kunai gets its pre sample at 2.50 (the slice text prints exactly this
pair); `prop_samples.rows` labels the two rows.

Predictions, made before the change:
1. The gate passes before the change: 582 tests.
2. Before the kunai's pair is authored, the new rule fires once on the four examples: the reference fight's kunai at
   2.50 (a free prop moving into A's foot); nothing fires on the other three.
3. The existing flight test with a contact at the second sample returns two PROP_KINEMATICS findings (gravity and the
   missing pair) instead of one.
4. The authored pre velocity [-1.4, -3.46, 0.2] passes the velocity check (gravity gives -3.455 for v_y).
5. `python -m compiler.rebind --write` re-seals the reference fight's later steps with no refusal; the other examples'
   packets move only if the schema id is part of their packet.
6. Outputs: the reference fight's render.txt and four prose prompts each gain one row (the pre sample) and two labels;
   the other examples' outputs do not change.
7. About 589 tests (seven new); no checklist row moves (no new prompt code).

## Decisions
- D1 — Split M9-04 into M9-04a (S04: F2.2) and M9-04b (render: F2.1, F6.1, F6.2, the two prompt codes); backlog
  version 2. Why: the backlog's own rule ("multi-step slices are split per step") and R-13 (the earlier step first, so
  M9-04b prints segments that already know the contact pairs). Alternatives: one slice across two steps (against the
  backlog rule). Downstream: M9-04b depends on M9-04a; nothing else depended on M9-04. Level: covered.
- D2 — F-062 (a held prop up to 2 m from its holder) stays with M9-06, not M9-04. Why: F-062's own proposed fix names
  the hand's world position by forward kinematics (M9-06, which lists F-062); the anchors of standing bodies are on the
  ground (B at y 0, the UGC creator at y 0), and correct held samples sit 1.16 to 1.71 m from them, so an arm's-reach
  radius on the anchor would refuse valid poses (measured on the four envelopes). Alternatives: tighten REACH_M now
  (refuses the kunai at 0.6 and the glasses at 3.5). Downstream: F-062 stays open until M9-06. Level: covered (F-062).
- D3 — The pair is required wherever a free prop moving into a contact meets it (not only allowed). Why: F2.2's gap
  ("a deflect is an instantaneous velocity change"); an optional field nothing requires leaves the ambiguity in place.
  Alternatives: optional pairs only (the kunai could keep one ambiguous sample). Downstream: fires only on the kunai
  at 2.50 in the four examples (prediction 2). Level: interpretation (Claude's, for owner review; added to F-053).
- D4 — Into a pre sample, velocity follows gravity within 0.25 m/s. Why: F2.2 ("gravity is checked into pre"); the
  tolerance matches the existing 0.25 m position tolerance. Alternatives: position only (the pre velocity would go
  unchecked). Downstream: authored pre samples must carry the gravity-consistent velocity. Level: interpretation
  (Claude's, for owner review; added to F-053).
- D5 — A pair shares its position within 0.25 m, and a pre sample's holder is read just before the contact (a pre
  sample at a catch is still in flight). Why: F2.2 calls the contact instantaneous, so nothing moves between pre and
  post. Alternatives: none that keep the contact instantaneous. Downstream: none in current data. Level: covered (F2.2).
- D6 — Author the kunai's pre sample at 2.50 in b05 ([0.5, 1.0, 4.6], v [-1.4, -3.46, 0.2]) and mark b06's 2.50
  sample `post`; recorded in the golden test. Why: the approved slice text prints this exact pair ("2.50 pre-contact
  v[…] · 2.50 post-contact v[…]"), so ADR-O71 rule 1 (covered) applies; the velocity is the 2.00 sample's under
  gravity for 0.5 s. Alternatives: leave the data (the new rule would refuse the plan). Downstream: render.txt and the
  four prose prompts gain the row (prediction 6). Level: covered (O61, F2.2, O71).
- D7 — `prop_samples.rows` prints the phase before the position ("2.50 pre-contact p[…] v[…] moving …"), pre before
  post. Why: F2.2's printed form; before p so the existing PROP_TRACK_MISSING prefix match keeps working. Alternatives:
  after the motion words (breaks the prefix match). Downstream: LBN and prose rows. Level: covered (F2.2).
- D8 — Schema versions: beat 1.0 to 1.1, beat_plan and temporal_graph 1.3 to 1.4. Why: docs/versioning.md (minor for
  an additive field) and the plan's section 6 (1.3 to 1.4). Level: covered.
- D9 — Record the kunai's +Z deflect against the golden's "+Z to -Z" as finding F-064 and leave the data. Why: ADR-O71
  (an uncovered golden change goes ahead only as a small leaf; re-aiming the deflect moves the rest point, A's grounded
  pickup at 8.0 and the shots on it, S11 and S16); AGENTS.md section 1 (a discovered gap is a finding). Alternatives:
  re-author the post velocity now (a cascade no ruling covers), reword the rule (the golden's words, R-17 needs the
  owner). Downstream: the prompts keep printing both until the owner rules. Level: covered (O71, R-17).

## Duration
about 50 minutes (with a pause while the harness's permission check was down)

## Changes
- `schemas/beat.schema.json` 1.1 (PropSample.phase), embedded in `schemas/graphs/beat_plan.schema.json` and
  `schemas/graphs/temporal_graph.schema.json` 1.4 (`kernel.shared_schemas`); three schema-log entries
- `planner/dynamic_beat_validator.py`: `_contact_pairs`, velocity into a pre sample, a pre sample's holder read before
  its contact (labelled interpretations)
- `renderers/prop_samples.py`: rows sorted pre, plain, post and labelled "pre-contact" / "post-contact"
- `examples/reference_fight/plans/temporal.json`: b05 gains the kunai's pre sample at 2.5, b06's marked post; outputs
  and checklist regenerated (`compiler.examples --write`, `validators.checklist --write`)
- `tests/test_dynamic_beat_validator.py` (four tests; one expectation now two findings), `tests/test_reference_fight_golden.py`
  (DEFLECT_PAIR)
- `docs/findings/F-064-*.md` (new), F-053 (two interpretations), backlog (M9-04 split; version 2), CHANGELOG, lessons
  L-16 and L-17, the run report

## Verification
- before: `scripts/verify.sh` exit 0, 582 passed (the pre-commit gate of S-008, 7393f7f)
- after: `scripts/verify.sh` exit 0, 587 passed; `make golden`: the reference fight's render.txt and four prose prompts
  changed on purpose (the pre row and the two labels); the other examples unchanged
- Prediction 1 held. Prediction 2 held (one finding, the kunai at 2.5; none elsewhere). Prediction 3 held (two
  findings). Prediction 4 held. Prediction 5 failed, harmlessly: no packet moved at all (no later step's packet holds
  prop samples, and the schema id is not in the S04 packet), so nothing was re-sealed. Prediction 6 held. Prediction 7
  failed on the count: 587, not 589 (five new tests, not seven); no checklist row moved, as predicted.
- Found on the way: F-064 (the deflect keeps +Z against the golden's "+Z to -Z"); not fixed (not a leaf, ADR-O71).

## Next
M9-04b (F2.1/F6.1/F6.2 at the render step).
