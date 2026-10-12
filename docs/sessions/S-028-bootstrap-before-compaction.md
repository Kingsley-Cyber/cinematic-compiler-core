# S-028 — Bootstrap before a compaction: the owner's review of the miss list (O82, O83)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-10; rulings O81, O82

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-028]

## Plan
The owner reviewed F-070's miss list and said "push it, then calibrate the card and start M9-06b. but after pushing
update bootstrap so i can compact". 7613d2f was pushed. The records make the next steps survive a compaction:
ADR-O82 (the owner's words), ADR-O83 (proposed: M9-06b's three open points), backlog M9-06c (calibrate) before M9-06b,
lesson L-22, and the regenerated state.md.

Prediction: the gate passes (627); state.md lists M9-06c next and ADR-O83 waiting on the owner.

## Decisions
- D1 — Calibration is its own slice (M9-06c) before M9-06b. Why: it changes a library card, the repo-authored roots
  and the miss list; the refusal then judges the calibrated body. Level: covered (O82).
- D2 — M9-06b's three open points are proposed (ADR-O83), not assumed: the owner ruled on the calibration and the
  start, not on what the refusal covers. Level: proposed ADR-O83.

## Duration
about 10 minutes

## Changes
- ADR-O82 (accepted), ADR-O83 (proposed), backlog (version 7: M9-06c, M9-06b ready, D-10), lessons L-22, CHANGELOG,
  state.md (generated)

## Verification
- before: `scripts/verify.sh` exit 0, 627 passed (S-027, 7613d2f; pushed)
- after: `scripts/verify.sh` exit 0, 627 passed; state.md lists M9-06c next and ADR-O83 waiting. The prediction held.

## Next
M9-06c (calibrate library/body_segments.yaml to the source's grounded A rows; re-root; regenerate the miss report),
then M9-06b under ADR-O83 unless the owner rules otherwise.
