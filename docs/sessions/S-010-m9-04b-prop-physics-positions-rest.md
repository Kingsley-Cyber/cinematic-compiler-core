# S-010 — M9-04b: where each prop is, its physics while free and its rest (F2.1, F6.1, F6.2)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-04b (split from M9-04; PLAN-003 F2.1, F6.1 as amended by W4, F6.2); rulings O8, O47, O48 (W4), O61

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-010]

## Plan
The prop state machines print samples and state changes as instants; between them the model is told nothing: how a
free prop moves (F2.1), where a prop is while nobody samples it (F6.1, which W4 turned from a visible/hidden track into
"where each prop is and when it changes hands or state"), and how long a resting prop stays put (F6.2). A derived
track in `renderers/prop_samples.py` cuts 0 to the scene's end at holds and samples and names each span: held by a
hand, carried by its owner, in flight under gravity (or a declared float) from p and v, or at rest at a place. The
prose prints it as a `WHERE:` line in each prop's block. Two prompt codes check it: PROP_PHYSICS_UNSTATED (a free
prop's flight lacks its clause) and PROP_VISIBILITY (the line is missing, leaves a gap, disagrees with the track, or a
span has no place). Map rows C31, C5 (physics) and C5, C23 (visibility), logged.

Predictions, made before the change:
1. The gate passes before the change: 587 tests.
2. The reference fight's WHERE lines: kunai five spans (B's hand, two flights split by the deflect, at rest on the
   ground 2.90-8.00, A's hand); rope dart four (carried by A, A's hand, at rest on the ground, A's hand); smoke pellet
   two (carried by A, then at rest at [0.4, 1.1, 4.7] to the end); shuriken volley three (carried by B, in flight,
   at rest on the wooden pillar); substitution log three (at rest on the ground, falling 4.00-4.40, at rest).
3. The UGC glasses: at rest on the tabletop, then the creator's hand, then at rest to the end.
4. Neither new code fires on the twenty prompts; each fires on its break.
5. render.txt does not change in any example; the prose changes in the reference fight and the UGC demo only.
6. No checklist row changes result (C31 stays PASS on the prose prompts; C5 and C23 keep their reasons).
7. About 591 tests (two breaks, two track tests).

## Decisions
- D1 — The WHERE line goes in the prose prop blocks only; LBN-2.4's prop rows stay as they are. Why: the prompt
  codes read the structured prose (prompt_validator's scope), the W rules that amended F6.1 are prose rules (O47-O49),
  and the LBN is the owner's kernel format (R-20). Alternatives: F6.2 in `motion_words`, shared with the LBN (the plan's
  file list), which would change the LBN rows with no check reading them. Downstream: the LBN keeps "at rest" without
  an end time. Level: interpretation (Claude's, for owner review; added to F-053).
- D2 — Span wording: "held by B R hand", "carried by A", "ballistic under gravity from p[…] v[…]", "stylised float,
  no gravity, from p[…] v[…]", "at rest on the ground at […]", each prefixed by its time range (planned with "in
  flight," before the physics; dropped while building because the falling log is not in flight). Why: F2.1's own words ("ballistic under gravity from p… v…"), F6.2's ("at rest on the ground at […] from 3.40
  until 8.00", written as a range so every span reads alike), the track's existing "held by B R hand" and SCENE's
  "carried by A" (O63). Alternatives: "visible 0.00-10.00 (…)" (F6.1's first wording, replaced by W4). Downstream: the
  prose of two examples. Level: covered (F2.1, F6.1 as amended, F6.2).
- D3 — A resting span names the S06 location in force at its start or first set inside it, ignoring a location set
  before the prop's last hold. Why: S06 commits a location at the end of the beat that changes it (the kunai rests
  from 2.90 but is 'ground' from 3.00), and S06 keeps a held prop's last surface (the kunai stays 'ground' in A's
  hand; the UGC glasses stay 'tabletop' on the creator's face), so the holder decides first and an old surface does
  not outlive a hold. Alternatives: the first location within the span (planned; it printed the worn glasses "on the
  tabletop" at y 1.6, caught before the commit). Downstream: none outside these two examples. Level: interpretation
  (Claude's, for owner review; added to F-053).
- D4 — PROP_PHYSICS_UNSTATED checks the flight spans; PROP_VISIBILITY checks the rest: the line exists, its spans tile
  0 to the end, every other span is printed as derived, and every span has a place. Why: the plan names the two codes;
  splitting by span kind lets each fire alone on its break (test_dag_conformance). Level: covered (plan section 6).
- D5 — Map rows: PROP_PHYSICS_UNSTATED on C31 and C5, PROP_VISIBILITY on C5 and C23 (kernel log). Why: the plan's
  section 6 lists exactly these rows. Level: covered.
- D6 — Row C31 also gains M9-04a's `_contact_pairs` check and a note on the F2.2 pairs, missed in S-009's commit. Why:
  the map lists every check that enforces a row (R-19); the omission was found while editing C31 here. Alternatives: a
  separate records-only commit for S-009 (one line of map, same log entry). Downstream: none. Level: covered.
- D7 — The smoke pellet's rest in mid-air is finding F-065, not a data change. Why: ADR-O71 (fixing it re-authors S04
  and its contacts, S07 and S08: not a small leaf); the WHERE line prints what the data says. Alternatives: hide the
  span (against W4), invent a landing (an uncovered golden change). Level: covered (O71).

## Duration
about 45 minutes

## Changes
- `renderers/prop_samples.py`: `track`, `where_line`, `_place`, `_hand`, `_moving` (labelled interpretation)
- `renderers/prose_renderer.py`: each prop block prints its WHERE line after the state track
- `validators/prompt_validator.py`: PROP_PHYSICS_UNSTATED, PROP_VISIBILITY (`_where_checks`, CODES, READS)
- `kernel/knowledge_map.yaml` (C31, C5, C23; two kernel-log entries), `tests/test_dag_conformance.py` (two breaks),
  `tests/test_prop_track.py` (new, four tests), `tests/test_dynamic_beat_validator.py` (one test also asserts its code)
- outputs: the reference fight's and the UGC demo's four prose prompts; checklists (evidence text only)
- `docs/findings/F-065-*.md` (new), F-053, backlog (M9-04b done, M9-05 next), CHANGELOG, the run report

## Verification
- before: `scripts/verify.sh` exit 0, 587 passed (the pre-commit gate of S-009, 93da7fd)
- after: `scripts/verify.sh` exit 0, 593 passed (the first run failed: test_knowledge_map's locators need a test that
  names its code, lesson L-18; the locators now point at tests/test_prop_track.py); `make golden`: the reference fight's and the UGC demo's prose changed
  on purpose (one WHERE line per prop); every render.txt unchanged
- Prediction 1 held. Prediction 2 held (the five reference spans as listed). Prediction 3 failed at first: the
  glasses' last span read "at rest on the tabletop at [0, 1.6, 0.1]" (S06's stale surface); fixed by D3 before the
  commit, now "at rest at [0, 1.6, 0.1]". Prediction 4 held (no finding on the 16 prose prompts; both breaks fire).
  Prediction 5 held. Prediction 6 held (no row changed result). Prediction 7 failed on the count: 593, not 591 (four track tests).
- Found on the way: F-065 (the smoke pellet rests in mid-air from 3.70 after it bursts).

## Next
M9-05 (FR.1/FR.3 rotation path and checks).
