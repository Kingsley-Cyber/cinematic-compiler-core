# S-063 — Principal review 4: does the finished work match the plan?

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
docs/prompts/finish.md section 6 (after eight slices: RV-45, RV-46, RV-48a, RV-48b, RV-60, RV-61, RV-62, RV-57);
docs/prompts/principal_review.md (ADR-O99), docs/prompts/no_shortcuts.md; rulings O98, O99, O100, O101

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-063]

## Plan
Five fresh read-only reviewers, one each for layers S01-S09, layers S10-S18, rules and shortcuts, decisions and
findings, and the golden and the fight, follow the review prompt and the no-shortcuts prompt. The builder checks their
heaviest claims against the files, files each gap as a finding with a slice (or answers it from the plan's sources,
or leaves it for the owner), and writes the verdict to docs/reports/2026-10-12-principal-review-4.md.

Predictions, made before the review (04:41 by the clock):
1. The gate passes before the review: 684 tests (5a7664f).
2. Every reviewer's verdict is "partially": the owner's questions stay open, render.txt cannot pass, and bodies may
   still pass through each other between keys.
3. The heaviest gaps named are already filed (F-159 between-key overlaps, F-153 render.txt, F-167 the S04 packet's
   query, F-093 the declared validators); at least one new gap is found in this run's own slices S-055 to S-062.
4. No test tampering is found; at least one reviewer flags an overclaim or a widened reading in S-055 to S-062.
5. Between five and fifteen new findings.

## Decisions
- D1 — The reviewers' heaviest claims were checked against the files before filing (the substitution's two exemptions,
  the instructions' F-077 sentence, the draw's clearance, a thrown blade as a hit, CAUSE_REASON's non-causes, O14's menus,
  the unsliced rows, B's takeoff, the C21 count, R-28's logs, S-055's and S-056's trees re-gated); every one held, and
  one of the builder's own records (S-061's 0.05 m) was wrong. Level: covered (finish.md section 6).
- D2 — From S-063 a partly fixed finding reads open with "Open in part" and names its carrier, as F-166 proposed; ten
  findings reopened; S-056 D2 reversed; the choice is listed for the owner. Level: covered (F-166's proposed fix).
- D3 — F-001 and F-002 stay resolved: the golden's reasons state causes; the looseness of the check that credits them
  is F-185 (RV-75). Level: interpretation (F-053's list carries the reviewers' point as F-185).
- D4 — The backlog (26): RV-66 to RV-84 added, the builder's own shortcuts first; RV-64 split, RV-64b waiting for
  F-133; RV-27 and RV-33 blocked on what they wait for; RV-39 widened to the six conditions; RV-58 back to ready.
  Level: covered (finish.md section 6; PLAN-007).
- D5 — What would set aside an owner ruling waits for the owner (R-06): the decoy's reach beyond O48, O23 read
  literally, O93's single instant, O103 against O88, R-21's reach. RV-66 builds only the literal reading. Level:
  covered (R-06).
- D6 — From S-064 each commit runs through `scripts/verify.sh > gate.log && git commit` (F-181); this one does too.
  Level: covered (R-02, AGENTS.md section 9).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | PASS | `scripts/verify.sh > gate.log && git commit`: the commit exists only if the gate passed after the last edit |
| One gap, right layer | PASS | records only: findings, backlog, PLAN-007, the review and run reports, F-053, S-061's correction; no code or example changed |
| Predictions written first | PASS | the file was created at 04:41:39 (its creation time), before the reviewers were launched, predictions inside |
| Claims checked | PASS | the probes in D1, run in S-063 (the draw: 0.108 m to the axis; the hit probe: False; CAUSE_REASON: [] for both non-causes; the two exported trees: check: PASS) |
| Tests | PASS | `git diff -- tests`: no change |
| Records | PASS | F-169 to F-186 filed; ten findings reopened in part with carriers; F-165 a question; F-117 high; backlog 26; docs plane PASS |
| Hygiene | PASS | the scan over the staged diff before the commit (no home paths, emails or keys) |
Claim corrected before the commit: F-001 and F-002 were first reopened; the docs plane showed the checklist credits
them through CAUSE_REASON, and on reading them again they are resolved for the golden, the gap being the check (F-185).

## Duration
about 41 minutes by the clock (04:40 to 05:21; the reviewers ran about 18 to 26 minutes each)

## Changes
- docs/reports/2026-10-12-principal-review-4.md (new); docs/findings F-169 to F-186 (new); F-084, F-122, F-130, F-136,
  F-137, F-155, F-160, F-161, F-162, F-163 reopened in part; F-001, F-002, F-015, F-016, F-053, F-117, F-138, F-165,
  F-166 noted; S-061's Verification corrected
- docs/plans/backlog.yaml 26 (RV-64b, RV-66 to RV-84; RV-27, RV-33, RV-39, RV-58, RV-64); PLAN-007; CHANGELOG; the run
  report

## Verification
- before: S-062's gate at 5a7664f: `scripts/verify.sh` exit 0, 684 passed
- after: the chained gate and commit (684 tests; no code changed)
- Prediction 1 held. Prediction 2 held in part: four reviewers said partially; the golden reviewer said faithful
  partially, coherent no, fight works no. Prediction 3 held (F-159, F-153, F-167 and F-093 named; new gaps in S-057 to
  S-062: F-169, F-170, F-175, F-176, F-182). Prediction 4 held (no tampering; overclaims flagged, the builder's 0.05 m
  among them). Prediction 5 failed: eighteen new findings, not five to fifteen.
