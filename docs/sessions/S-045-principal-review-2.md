# S-045 — Principal review 2: five read-only reviewers, their gaps filed, the owner's ruling O107 recorded

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
finish.md section 6 (a review after eight slices); rulings O99, O101, O107 (new); findings F-120 to F-150 (new)

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-045]

## Plan
Run docs/prompts/principal_review.md with five fresh, read-only reviewers who did not build the work (layers S01-S09,
layers S10-S18, rules and shortcuts, decisions and findings, the golden and the fight); check their heaviest claims
against the files; file every gap as a finding with a slice, or answer it; write the verdict
(docs/reports/2026-10-12-principal-review-2.md); continue.

Predictions, made before the review:
1. The verdict stays "partially": the first review's gaps RV-07 to RV-41 are mostly open.
2. The reviewers find something in this run's own slices the builder missed.
3. No code or data changes in this session; the gate stays green with 646 tests.

## Decisions
- D1 — The heaviest claims checked before filing: the S13 exception door, the RULES lines' end time, S03's
  scene_reference targets, S07's contact order, the deflect contradiction, and the Euler convention (the 3.0 root's up
  axis and the 5.1 flip's direction computed with solver/quaternion.py). Each held. Level: covered (finish.md section 6).
- D2 — The two reviewers who ranked the run's test changes under ADR-O102 as its first shortcut were right that O100 had
  left F-119 to the owner. The builder prepared to stop the run and report; the owner ruled first: "O102 confirmed, keep
  pushing, continue the finish run" (ADR-O107). Rules 5.0 records it in R-03, R-06 and R-30, and finish.md 2.0 with it;
  R-06 keeps for the owner any question whose answer would set aside an owner ruling or invariant, which takes F-088
  off the run's list. Level: owner (ADR-O107); the R-06 limit is the builder's, narrowing its own grant.
- D3 — Questions that set aside an owner ruling or the source's own numbers wait (F-143 ADR-Q6, F-148, F-149, F-099 with
  F-125, F-088); the rest are answered in their slices (finish.md section 4). Level: covered (R-06 as amended).
- D4 — Gaps already named keep their findings; the review's evidence widens their slices (RV-07, RV-09, RV-15, RV-17,
  RV-18, RV-21, RV-24, RV-33, RV-35, RV-36, RV-38, M9-03a). New gaps are F-122 to F-150 with slices RV-42 to RV-53;
  RV-42 (the deflect's contradiction, in every prompt) is next, then RV-43, RV-07 and RV-49, as finish.md section 5 puts
  what a rendered fight shows first. Level: covered.
- D5 — F-120 and F-121 are filed resolved, so the record keeps what the review found and how the owner answered it.
  Level: covered.

## Duration
about 2 hours (the reviewers' reading included)

## Changes
- docs/reports/2026-10-12-principal-review-2.md (new); F-120 to F-150 (new); ADR-O107 (new); ADR-O100 (superseded by
  O107), ADR-O102 (Decided By owner); F-119 resolved
- docs/rules.yaml 5.0 (R-03, R-06, R-30); docs/prompts/finish.md 2.0 (docs log)
- backlog 20 (RV-42 to RV-53; twelve slices widened); PLAN-007; the run report; CHANGELOG

## Verification
- before: 646 passed at 68ab1f9 (S-044's gate)
- after: `scripts/verify.sh` exit 0, 646 passed, docs plane PASS; no code, data or test file changed
- Prediction 1 held (all five reviewers: partially). Prediction 2 held: the deflect contradiction S-043 put in every
  prompt, the exception door, the test-change grant, the Euler convention. Prediction 3 held.

## Next
RV-42 (the deflect's one reading).
