# S-047 — RV-43: CONTACT_WORLD exceptions come only from an owner-held, logged list

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-43 (PLAN-007); finding F-123; rulings O83, O89, O102, O107

## Layer
L4c

## Status
applied

## Commit
the commit whose message names [S-047]

## Plan
F-123: S13 reads its exceptions from the authored motion plan, so any compile can exempt its own misses; ADR-O83 point 2
keeps exceptions to the owner's source rows. The fix moves them out of the author's reach:
1. kernel/contact_world_exceptions.yaml (kernel log): each entry names a scene by its query's sha256, a contact, the
   ruling that keeps it and the reason; today the reference fight's slide (b14_c2, b14_c3; ADR-O83 point 2 and the
   owner's M9-06b words "keep the source misses as exceptions").
2. S13's packet carries the entries for its scene's query; CONTACT_WORLD reads only those. The motion plan loses its
   `contact_world_exceptions` field (schema 2.0, a field removed), so an authored exception fails the schema.
3. Every reader of the old field (the golden test, the forward-kinematics tests, the motion tests, the contact-world
   report) reads the kernel list.

Predictions, made before the change:
1. The gate passes before the change: 648 tests (18aed87).
2. After it every example compiles; the reference fight's two exceptions come from the kernel list; a motion plan that
   lists an exception is refused at S13 (schema).
3. No prompt text changes; every example's envelope changes (S13's packet carries the list; the schema id moves).
4. About 649 tests: an authored-exception refusal is new; the tests that set the old field move to the packet's list
   (ADR-O102).

## Decisions
- D1 — The owner's exceptions live in the kernel (kernel/contact_world_exceptions.yaml, kernel log), keyed by the
  sha256 of the scene's query, each entry naming the ruling. Why: the kernel holds the owner's data; a query hash names
  a scene without the compiler knowing example names, and a changed query stops matching, so its misses are refused
  rather than silently kept. Alternatives: an ADR list read from docs/decisions (couples the compiler to the docs plane);
  keep the plan's field and refuse it there (the field would invite the door back). Level: covered (ADR-O83 point 2,
  F-123's fix).
- D2 — The motion plan's field is removed (schema 2.0, a field removed is a major bump; the packet's pinned id moves
  with it, L-21), so an authored exception fails S13's schema before any check runs. Level: covered.
- D3 — Tests: the golden, the forward-kinematics and the motion tests read the owner's list; the motion BREAKS entry for a
  stale exception becomes part of a new test that also proves an authored exception is refused (moved, not dropped).
  Level: covered (ADR-O102).
- D4 — Every example re-bound: S13's packet now carries the list (empty outside the reference fight). Level: covered.

## Duration
about 6 minutes by the commit times (01:02 to 01:07); it read "about 40 minutes" until RV-46
(S-056) corrected it (F-166)

## Changes
- kernel/contact_world_exceptions.yaml (new; kernel log); kernel/schema_log.py (the kernel log covers it)
- solver/contact_world.py (`owner_exceptions`, the packet view, docstring and message); compiler/passes/derived/p13_motion.py
  (reads the packet's list; schema 2.0); schemas/graphs/motion_plan.schema.json 2.0 (schemas log);
  validators/contact_world_report.py
- examples/reference_fight/plans/motion.json (the field removed); every example re-bound and regenerated
- tests: test_motion_solver (new test; the kick test reads the packet), test_reference_fight_golden,
  test_forward_kinematics
- kernel/knowledge_map.yaml version 4 (note, locator; kernel log); F-123 resolved; backlog (RV-43 done, RV-07 next);
  CHANGELOG

## Verification
- before: 648 passed at 18aed87 (S-046's gate)
- after: `scripts/verify.sh` exit 0, 648 passed (one parametrized break moved into the new test: net zero); `make golden` passed; `compiler.rebind` silent; no prompt text changed;
  the reference fight's exceptions are b14_c2 and b14_c3, from the kernel list; no refusal in any example
- Prediction 1 held. Prediction 2 held. Prediction 3 held (every envelope changed, no prompt text). Prediction 4 held
  in part: 648, not about 649 (the moved break).

## Next
RV-07 (the smoke bursts at 3.7, O91).
