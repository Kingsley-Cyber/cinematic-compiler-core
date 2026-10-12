# S-048 — RV-07: the smoke bursts at 3.7 at A's body; an effect can take effect at its beat's start

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-07 (PLAN-007); findings F-082, F-132, F-146 (e, f); rulings O91, O78, O48, O102, O107

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-048]

## Plan
O91 (owner): "Smoke bursts at 3.7 at A's body. The spent pellet falls and rests." S06 commits every effect but a change
of hands at its beat's end, so the smoke (b09, 3.7-4.0) bursts at 4.0 and the log is deployed at 4.0, though the source
does both at 3.7 ("A deploys smoke pellet ... SMOKE BURST", "A deploys substitution log at A former position").
1. A beat's effect may say `at: start` (schemas/beat.schema.json 1.3: an Effect, a Fact with that one field; embedded
   into beat_plan 1.6 and temporal_graph 1.6); S06 commits it at its beat's start; S04's fact times read it too.
2. b09's smoke burst and the log's deployment take effect at its start, 3.7; the pellet still leaves A's hand at 3.7 and
   comes to rest on the ground at 4.0 (O91's "falls and rests"), where its location becomes the ground.
3. F-132: each change in an S06 transition carries its own instant (state_graph 1.2), and RULES' "From t to the end"
   lines read it, in the renderer and in its check, instead of the beat's end.

Predictions, made before the change:
1. The gate passes before the change: 648 tests (1f9fedf).
2. After it the reference prompts print the smoke's burst and the log's deployment at 3.70 (no longer 4.00) and the
   pellet's rest on the ground at 4.00; no other example's text changes.
3. The golden's SUBSTITUTION_POST pin ("4 deployment standing->deployed") moves to 3.7 and PELLET's comment is
   corrected (ADR-O102 with O91); a test of `at: start` effects is added: about 649 tests.
4. S08/S09 (object state) and S07 accept the earlier change: the touch b09_c1 at 3.7 is in the same beat.

## Decisions
- D1 — A beat effect may say `at: start` (beat 1.3: an Effect is a Fact with that one field), as a contact may, and S06
  commits it at its beat's start; a change of hands keeps its possess or release instant (F-061). Why: O91 and the
  source's 3.7 rows ("3.7 A deploys smoke pellet ... SMOKE BURST", "3.7 A deploys substitution log at A former
  position"), while b09 runs 3.7-4.0. Alternatives: split b09 at 3.7 (a new beat the camera and the causes would have
  to follow); move the burst into b08 (B's palm, not A's act). Level: covered (O91).
- D2 — The pellet's location stays at b09's end: it leaves A's right hand at 3.7 and lies on the ground from 4.0, its
  two samples unchanged. Why: O91 ("the spent pellet falls and rests"), O78 (PROP_SUPPORT). Level: covered.
- D3 — S05 compares what an effect sets (subject, property, value), not when it sets it: b09's hard cause to b10 needs
  the log deployed. Level: covered (a hard cause is an effect that satisfies a requirement).
- D4 — F-132: each change in an S06 transition carries its own instant (state_graph 1.2); the "From t to the end" rules
  and their check read each property's last S06 change, not the last beat effect (measured first: on all four examples
  the two readings print the same lines), each with its own code, so the check does not run the renderer's; the prop
  tracks, first states and render.txt rows give each change its own instant; S09 copies a change's property, from and
  to, so its schema is unchanged. Level: covered (F-132's proposed fix, ADR-O107).
- D5 — The golden test's records change with O91 (ADR-O102): the log's deployment pin moves from 4 to 3.7 and the test
  also pins the source's 3.7 row; PELLET's comment and test name say the smoke bursts at A's body at 3.7 and the pellet
  rests from 4.0, and the test pins both state rows in render.txt (F-146's two items). HIDDEN_PHRASING's break in
  tests/test_dag_conformance.py edits the log's first state, which now reads "deployment standing until 3.70" (it read
  4.00), so its text follows. Level: covered.
- D6 — Same-instant items in a prop track keep their order (state changes, contacts, samples), so the track reads
  "3.70 smoke sealed -> burst · 3.70 touched by A R hand", as the kunai's reads "2.00 holder B -> none · 2.00 released
  by B R hand". Level: covered (no change).

## Duration
about 50 minutes

## Changes
- schemas/beat.schema.json 1.3 (Effect), embedded in beat_plan 1.6 and temporal_graph 1.6 (kernel/shared_schemas.py,
  planner/beat_planner.py SCHEMA_ID); schemas/graphs/state_graph.schema.json 1.2 (a change's `t`); schemas log
- solver/prop_state_machine.py (`commit_time`, each change's instant); compiler/passes/mandatory/p05_causal.py;
  compiler/passes/derived/p09_object_state.py; planner/dynamic_beat_validator.py (PROP_SUPPORT reads `at: start`)
- renderers/prose_renderer.py (`last_changes`, the rules, prop tracks and first states), renderers/anime_renderer.py,
  validators/prompt_validator.py (the rules' check reads S06)
- examples/reference_fight/plans/temporal.json (b09's smoke burst and log deployment `at: start`); every example
  re-bound; outputs and checklists regenerated
- tests/test_reference_fight_golden.py (the log at 3.7, PELLET), tests/test_dag_conformance.py (HIDDEN_PHRASING's
  break text), tests/test_state_pass.py and tests/test_causal_pass.py (one test each)
- F-082 and F-132 resolved; F-146 noted; backlog 21 (RV-49 next); CHANGELOG; docs/reports/2026-10-11-finish-1.md

## Verification
- before: pytest on an archive of 1f9fedf (HEAD, unchanged since S-047's gate): 648 passed
- after: `scripts/verify.sh` exit 0, 650 passed, check: PASS; `make golden` 26 passed; `compiler.rebind --write`
  re-bound the four temporal plans and nothing else moved
- Prediction 1 held. Prediction 2 held: the reference prompts print "smoke sealed until 3.70", "3.70 smoke sealed ->
  burst", "3.70 deployment standing -> deployed", "4.00 location unknown -> ground" and "From 3.70 to the end, smoke
  pellet keeps smoke burst"; the other examples' texts did not change (their envelopes and plans did: packet hashes,
  schema ids, each change's instant). Prediction 3 held in part: the pins moved as predicted, but two tests were added
  (S06 and S05), 650, not about 649, and HIDDEN_PHRASING's break text moved too (not predicted). Prediction 4 held: S07, S08 and S09 accepted the change; S09 needed one line (it
  copied S06's changes whole, and its schema has no `t`), found by the compile, not predicted.

## Next
RV-49 (no body through another).
