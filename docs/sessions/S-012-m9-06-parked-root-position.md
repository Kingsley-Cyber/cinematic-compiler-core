# S-012 — M9-06 parked: the root position and the contact tolerance are the owner's

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-06 (PLAN-003 F5.1/F5.2); findings F-025, F-028, F-062; ruling O24

## Layer
L4c

## Status
not started

## Commit
the commit whose message names [S-012]

## Plan
M9-06 computes each hand and foot from the root and the joint angles (forward kinematics, O24) and refuses a touch
whose two points miss (CONTACT_WORLD). Reading the convention and the data before any code: the root position has no
defined meaning and the data uses two (the owner's A rows at pelvis height, the repo's B rows on the ground), and the
plan reserves the contact tolerance for the owner. Both are the owner's calls, and M9-14a depends on M9-06, so the
slice is parked (docs/prompts/autopilot.md section 5, ADR-O71 rule 3) with a proposed ADR and a question finding. No
code was written.

Predictions, made before reading the data: forward kinematics on the reference fight would place hands and feet
within a few centimetres of the contacts. Not tested: the data showed the root has two meanings first.

## Decisions
- D1 — Park M9-06 rather than build part of it. Why: the root's meaning decides every point forward kinematics
  produces, so no part of F5.1 can be built correctly without it; the tolerance is named an owner value in the
  approved plan (F5.2); M9-14a depends on M9-06, so it is not a leaf (ADR-O71 rule 3; autopilot section 5).
  Alternatives: assume the pelvis and re-author B (an uncovered change across four examples), assume the ground
  point (moves the owner's own rows), split off F5.1 (still needs the root). Downstream: M9-06 blocked; M9-14a waits;
  the run goes on with M9-07. Level: proposed ADR-O72.
- D2 — Recommend the pelvis and 0.15 m in ADR-O72. Why: the owner's source writes A's root at pelvis height on both
  feet; 0.15 m is about a hand's width (tighter than the 0.25 m prop tolerance because limb ends are computed, not
  authored). Alternatives: listed in ADR-O72. Level: proposed ADR-O72.

## Duration
about 15 minutes

## Changes
- `docs/decisions/ADR-O72-*.md` (proposed), `docs/findings/F-066-*.md` (question), backlog (M9-06 blocked, M9-07
  next), the run report

## Verification
- before: `scripts/verify.sh` exit 0, 598 passed (the pre-commit gate of S-011, dfce20a)
- after: `scripts/verify.sh` exit 0 on the records (no code, no example changed)

## Next
M9-07 (F4.1/F4.2 combat verbs on contacts and Laban wording); M9-06 after the owner rules on ADR-O72.
