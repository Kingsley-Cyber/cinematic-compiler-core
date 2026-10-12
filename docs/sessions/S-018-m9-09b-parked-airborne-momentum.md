# S-018 — M9-09b parked: the examples' airborne spans leave the gravity arc

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-09b (PLAN-003 F9.2); finding F-026

## Layer
L4a

## Status
not started

## Commit
the commit whose message names [S-018]

## Plan
MOMENTUM_MISSING (F9.2) refuses an airborne span that rises or hangs against gravity without a declared float
(anime) or a push contact. A prototype before any code: each airborne root against the arc through its span's
takeoff and landing roots. Nine spans in the four examples leave it, and no field declares a body float, so the
check cannot land without content choices per span (float or retime) that no ruling covers: parked (ADR-O71 rule 3:
not small, though a leaf) with a proposed ADR and a question finding. This is the second slice in a row parked for
the same cause (S-017), so the run stops (docs/prompts/autopilot.md section 7).

Predictions, made before the prototype: the reference fight's long aerial spans (A 1.10-3.00) would leave the arc;
the wizard's would mostly fit. Half held: the wizard's three spans leave it too.

## Decisions
- D1 — The arc through the takeoff and landing roots, 0.3 m tolerance, as the measure. Why: F9.2's "rises or hangs
  against gravity" with only key positions known (no velocities); the tolerance matches the prop tolerance. Level:
  interpretation (recorded in ADR-O74).
- D2 — Park, not build. Why: the fix is a new schema field plus a float-or-retime choice per span (not small, ADR-O71
  rule 3). Level: proposed ADR-O74.
- D3 — Stop the run after this park. Why: S-017 parked for the same cause (a new check refuses example data authored
  before it; landing it needs content rulings), which the autopilot's section 7 reads as something upstream: the
  owner's policy for re-authoring examples to new checks. Level: covered (docs/prompts/autopilot.md section 7).

## Duration
about 20 minutes

## Changes
- `docs/decisions/ADR-O74-*.md` (proposed), `docs/findings/F-069-*.md` (question), backlog (M9-09b blocked), the run
  report

## Verification
- before: `scripts/verify.sh` exit 0, 609 passed (the pre-commit gate of S-017, 5469821)
- after: `scripts/verify.sh` exit 0 on the records (no code, no example changed)

## Next
The owner rules on ADR-O72, ADR-O73 and ADR-O74 (and the policy behind them); a new run then resumes at M9-09c or
the first unblocked slice.
