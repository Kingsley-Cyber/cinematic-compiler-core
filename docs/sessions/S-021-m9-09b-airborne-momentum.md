# S-021 — M9-09b: airborne spans follow the gravity arc; anime declares hang time (F9.2, O74)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09b (PLAN-003 F9.2); findings F-069, F-026; rulings O74, O75 (R-33)

## Layer
L4a

## Status
applied

## Commit
the commit whose message names [S-021]

## Plan
O74: anime declares hang time per span; live action and UGC follow the gravity arc. The kinematic plan's node gains
an optional `float` (anime only, airborne only; kinematic_plan and kinematic_graph 1.1, logged). S11 checks
MOMENTUM_MISSING: a span of airborne keys between a takeoff key and a landing key keeps each root within 0.3 m of the
arc through the takeoff and landing roots, unless a key of the span floats; a float outside anime or on a supported
key is refused. The prose's RULES say each float span hangs ("stylised anime hang time"), and the prompt code reads
that line. The examples' off-arc spans (all anime) declare their hang time (R-33).

Predictions, made before the change:
1. MOMENTUM_MISSING fires on eight spans before the floats: the reference fight's five (A 1.10-3.00, 4.40-5.90,
   5.90-7.50, 8.00-9.00; B 4.70-6.30) and the wizard's three (1.20-2.60, 3.60-5.20, 8.60-9.80); A's opening fall (no
   takeoff key) is not judged.
2. With floats on those spans' airborne keys, every example compiles after re-binding S11 onward.
3. The reference fight's and the wizard's prompts gain one RULES line per float span; the other examples are
   unchanged; render.txt unchanged.
4. No checklist row changes result (BIO, T10, C22 gain the prompt code).
5. About 620 tests.

## Decisions
- D1 — The arc through the takeoff and landing roots, 0.3 m, as the measure (ADR-O74's proposal, accepted); a span
  with no takeoff or no landing key is not judged. Level: interpretation (F-053).
- D2 — The float goes on every airborne key of a hanging span, and one floating key makes the span stylised. Why:
  O74 ("per span"); a span is the unit the arc judges. Level: covered (O74).
- D3 — The prose says the hang in RULES, not on each staff line: "<A> hangs in the air <t0>-<t1>, longer than a
  real jump (stylised anime hang time)". Why: the staff's SUPPORT column is checked against S11 (STAFF_FORMAT,
  SUPPORT_MISMATCH); one RULES line per span reads once, like the entrance rule. Level: interpretation (F-053).
- D4 — MOMENTUM_MISSING on BIO, T10 and C22 (the plan's section 6). Level: covered.

## Duration
about 45 minutes

## Changes
- schemas: `graphs/kinematic_plan` and `graphs/kinematic_graph` 1.1 (`float`), logged; the S11 packet's pinned id
- `compiler/passes/derived/p11_kinematic.py` (`float_spans`, `momentum_findings`; labelled interpretation);
  `renderers/prose_renderer.py` (`hang_rules`); `validators/prompt_validator.py` (MOMENTUM_MISSING)
- `examples/reference_fight/plans/kinematic.json` (13 floating keys) and the wizard's (4); every S11 plan re-bound and
  the later plans of the two anime examples; outputs and checklists regenerated
- tests: two breaks and a hang test (test_kinematic_solver; the support-change test drops b03's float with its
  support), a prompt break (test_dag_conformance), HANG_SPANS (golden)
- `kernel/knowledge_map.yaml` BIO, T10, C22 (MOMENTUM_MISSING leaves two gap lists; kernel log); F-069 and F-026
  resolved; F-053; backlog; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 614 passed (S-020, b09ee0c)
- after: `scripts/verify.sh` exit 0, 619 passed
- Prediction 1 held (the eight spans, thirteen and four keys; the opening fall not judged). Prediction 2 held.
  Prediction 3 held (eight prose files, one line per float span). Prediction 4 held (no row changed
  result). Prediction 5 held roughly (619).

## Next
M9-09c (FR.4 launch; F-058, O80).
