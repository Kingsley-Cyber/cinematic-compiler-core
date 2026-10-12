# S-056 — RV-46: the stale and overclaimed records corrected; the owner's waiting list complete

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-46 (PLAN-007); findings F-130, F-140, F-166, F-154 (the lists), F-015, F-052, F-054; rules R-06, R-12, R-28

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-056]

## Plan
Reviews 2 and 3 found records that say what the repo does not (F-130, F-166) and an owner list that hides the
owner_default ADRs (F-154). Each is corrected at its source, not reworded around:
1. The generated owner lists (AGENTS.md section 7, docs/for_the_owner.md, docs/bootstrap/state.md) name every
   owner_default ADR as awaiting the owner, and the pre-commit hook as a question (a new finding).
2. Overclaims corrected: CHANGELOG (RV-10's hand, RV-42's render.txt row, RV-09's frame), the resolutions of F-084,
   F-144, F-080 and F-083 (what remains, and where), a test docstring ("at any instant").
3. Stale lines: AGENTS.md (F-119), docs/for_the_owner.md (the rule count; forward kinematics), PLAN-007 (RV-33, the
   test rule), ADR-O92 (where HIT_HOLD runs), ADR-O83 (amended by O89, O104), F-148 (RV-53), F-070, F-071, F-124 and the
   exceptions file (O83's words), solver/contact_world.py and validators/contact_world_report.py, MASTER_PLAN (commit
   times); the Duration of S-046 to S-053 by their commit times.
4. Assignments: F-015 to RV-57; F-052 and F-054 to RV-38. F-140: the track test shows a place giving way to a hold
   again, on the reference kunai (at rest 2.72-8.0, then held).

Predictions, made before the change (03:19 by the clock):
1. The gate passes before the change: 664 tests (a14f99a).
2. No prompt, envelope or checklist changes (the exceptions file is not hashed into the kernel and its basis line is
   not in S13's packet).
3. The generated owner lists gain seven owner_default ADRs (O67, O71, O103, O104, O105, O106, O108) and the hook
   question.
4. 664 tests (one re-pointed, one docstring).

## Decisions
- D1 — The owner lists name every accepted owner_default ADR as awaiting the owner (R-28: the agent's proposal the
  owner has not objected to; R-06: the run's answers for him to confirm), generated from the ADRs' own fields, so a new
  one appears without a hand edit. Level: covered (F-154's RV-46 part).
- D2 — A resolved finding whose slice did part of the work keeps its status and gains a dated "Corrected" line naming
  what remains and where, rather than reopening, since the rest has its own finding and slice. Level: covered (S-054
  D4).
- D3 — F-140's test keeps its name and claim on the reference kunai; the glasses' pins moved to their own test
  unchanged. Level: covered (ADR-O102: the plan's intent, the test's own claim).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh` exit 0, 665 passed, check: PASS |
| One gap, right layer | PASS | RV-46 only: records, the owner-list generator (docs plane), one test re-pointed |
| Predictions written first | PASS | written 03:19, before the first edit |
| Examples untouched | PASS | `git status examples`: nothing; `compiler.rebind` exit 0 |
| Tests not weakened | PASS | `git diff -- tests`: one docstring line replaced; the glasses' assertions moved intact |
| The owner list | PASS | for_the_owner.md and AGENTS.md: 6 owner_default lines each, and F-168 |
| Logs and freeze | PASS | AGENTS.md 2.4 and for_the_owner.md 1.1 in the docs log; the exceptions file version 2 in the kernel log; the four logs verify |
| Claims re-derived | PASS | the commit times give 6, 6, 18, 33, 18, 12, 6 and 3 minutes; the kernel log entry is seq 64 (a first draft said 62, corrected before the commit) |
| Hygiene | PASS | the scan before the push |

## Duration
about 6 minutes by the clock (03:19 to 03:24)

## Changes
- kernel/docs_plane.py (the owner lists); AGENTS.md 2.4 and docs/for_the_owner.md 1.1 (docs log); CHANGELOG (three
  entries corrected); kernel/contact_world_exceptions.yaml 2 (kernel log); solver/contact_world.py and
  validators/contact_world_report.py (docstring and report text); ADR-O83 and ADR-O92; docs/plans/MASTER_PLAN.md;
  PLAN-007
- findings: F-070, F-071, F-080, F-083, F-084, F-124, F-144, F-148, F-015, F-052, F-054 amended; F-130, F-140 and F-166
  resolved; F-168 (new); S-046 to S-053's Duration
- tests/test_prop_track.py (the claim on the kunai; the glasses in their own test), tests/test_forward_kinematics.py (a
  docstring)
- backlog (RV-46 done, RV-48 next); CHANGELOG; run report

## Verification
- before: S-055's gate at a14f99a: `scripts/verify.sh` exit 0, 664 passed
- after: `scripts/verify.sh` exit 0, 665 passed, check: PASS
- Prediction 1 held. Prediction 2 held (no prompt, envelope or checklist changed). Prediction 3 held in part: six
  owner_default ADRs, not seven (ADR-O71 is superseded), and the hook. Prediction 4 held in part: 665, since the
  glasses' pins became a test of their own.

## Next
RV-48 (throws and releases at their pose; the 6.6 throw; the S04 instructions).
