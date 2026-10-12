# S-017 — M9-09a parked: Shape qualities contradict the motion in every example

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-09a (PLAN-003 F9.1); finding F-029; ruling O31 (Shape against both the root's path and the form)

## Layer
L5

## Status
not started

## Commit
the commit whose message names [S-017]

## Plan
SHAPE_DIRECTION compares each Effort interval's declared Shape quality with the measured motion (F9.1, O31). Before
building it in S15, a prototype measured the four examples: 24 of 42 intervals show neither reading of their quality
and 12 show the opposite. The check cannot land without re-authoring Effort intervals in every example, which no
ruling covers, and M9-10, M9-14b and M9-15d depend on M9-09a: parked (autopilot section 5, ADR-O71 rule 3) with a
proposed ADR and a question finding. No code was written; the prototype is not in the repo.

Predictions, made before the prototype: under the lenient reading (either the path or the form shows the quality),
at most a few intervals would fail. Failed: 24 of 42 showed neither, 12 the opposite.

## Decisions
- D1 — O31's "both" read as: a quality passes when either the root's path or the body's form shows it. Why: Laban
  Shape can live in the form alone (a rising gesture with the feet planted) or in the path alone; requiring both
  would refuse correct movement. Alternatives: both readings must agree (stricter still). Level: interpretation
  (recorded in ADR-O73 for the owner).
- D2 — Park instead of building a check shaped to pass the data. Why: a measure tuned until the examples pass would
  be a check designed around its golden (AGENTS.md section 11: never weaken a check to make the gate pass); the
  owner decides between re-authoring and a contradiction-only check. Alternatives: build the contradiction-only check
  and re-author the twelve (an uncovered change on a non-leaf slice). Level: proposed ADR-O73.

## Duration
about 25 minutes

## Changes
- `docs/decisions/ADR-O73-*.md` (proposed), `docs/findings/F-068-*.md` (question), backlog (M9-09a blocked, M9-09b
  next), the run report

## Verification
- before: `scripts/verify.sh` exit 0, 609 passed (the pre-commit gate of S-016, 2107c89)
- after: `scripts/verify.sh` exit 0 on the records (no code, no example changed)

## Next
M9-09b (F9.2 airborne momentum under gravity); M9-09a after the owner rules on ADR-O73.
