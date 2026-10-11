# S-008 — The autopilot prompt (/autopilot) and the decision log

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-08 (PLAN-005); rulings ADR-O70 (owner) and ADR-O71 (owner_default, by delegation)

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-008]

## Plan
The owner asked for a prompt that has the agent work end to end without stopping, update the statuses and the
bootstrap, test, and log every decision with its reason from AGENTS.md and CLAUDE.md. The owner chose the run length
(until no slice is ready) and delegated the golden-change policy ("can you decide but plan it based on meeting my
intent and downward effects?").

One source of truth, docs/prompts/autopilot.md (frozen, docs log), with a thin `.claude/commands/autopilot.md`.
Decisions get a home: a `## Decisions` section in the session template and rule R-32 (source O70). The bootstrap
README sends a resumed session back into a running autopilot run; the working agreements record the commit grant;
the ownership map gains the missing `docs/prompts/` row.

Predictions, made before the change:
1. The gate passes before the change (582 tests).
2. No code changes: the test count stays 582 and `make golden` shows no output change.
3. The docs log verifies with seven new entries (seq 21 to 27).
4. After `make docs`, AGENTS.md section 6 says decisions 98 (1 proposed) and open findings 36, and section 7 lists
   ADR-O71 as proposed.
5. state.md's next free IDs become ADR-O72, F-064, S-009.
6. The docs plane passes: links resolve, R-32 cites an accepted ADR (O70), D-08 is done with no codes.

## Decisions
- D1 — Version bumps: protocol changes take +1.0 (bootstrap README 2.0, session template 2.0, rules.yaml 2.0); map
  rows take +0.1 (AGENTS.md 1.3, ownership 1.2). Why: docs/versioning.md ("+0.1 for wording; +1.0 for a protocol or
  rule change"). Alternatives: the earlier precedent of +0.1 for protocol changes (O68, O69), rejected because it
  contradicts the written rule; the mismatch is finding F-063. Downstream: none (versions only rise). Level: covered.
- D2 — The golden-change policy (ADR-O71): covered changes go ahead; an uncovered leaf change goes ahead as a
  proposed deviation in its own slice commit, at most three unratified at a time; an uncovered change other slices
  depend on parks the slice. Why: the owner delegated it; it keeps the run moving (the owner's intent) while bounding
  the rework a rejection causes (each leaf change is one `git revert`, and nothing builds on it), and nothing leaves
  the machine before the owner's push review (R-03). Alternatives: park every uncovered change (safe, but a stall);
  make every change and flag it (fast, but a rejection could unwind a chain of slices). Downstream: R-30 is read as
  "approved before it leaves the machine" for these local commits; the owner may overrule. Level: proposed ADR-O71,
  accepted as owner_default when the owner replied "commit it" to the report without objecting.
- D3 — Decision levels (covered, interpretation, owner's call) and their logs (session Decisions; labelled code
  comment plus F-053; proposed ADR plus question finding). Why: AGENTS.md section 14 (agent proposals are proposed
  ADRs), R-06 (questions are findings), F-053 (the existing queue of interpretations), R-28. Alternatives: one
  decisions log file outside the docs plane, rejected (a second source of truth). Downstream: R-32 applies to every
  session, not only autopilot runs. Level: covered by O70 (the owner's request to log every decision and why).
- D4 — A run report per run in `docs/reports/` (status running, finished or stopped). Why: a resumed session must
  know a run is active (bootstrap README), and the owner gets one place to read the run's results; reports are dated
  records (AGENTS.md section 12). Alternatives: state.md only, rejected (it is generated and holds no run state).
  Downstream: the README's resume steps check for a running report. Level: covered by O70.
- D5 — The run's limits: at most three attempts at a red gate per slice, at most two self-audit fix rounds, and a stop
  when two slices in a row park or revert on the same cause. Why: AGENTS.md section 11 ("never paper over a
  failure") and R-12 need a point where the run reverts and records instead of retrying; two failures on one cause
  mean the fault is upstream of the slice, which only the owner can see whole. Alternatives: no limits (a run could
  loop on one slice), a stop on the first failure (the run would stall on what parking handles). Downstream: a
  stubborn slice costs at most three gate runs before it is parked. Level: interpretation (Claude's, for owner
  review; the numbers are not from any rule).

## Duration
about 40 minutes

## Changes
- `docs/prompts/autopilot.md` (new, frozen 1.0) and `.claude/commands/autopilot.md` (new, frozen 1.0)
- `docs/decisions/ADR-O70-autopilot-runs.md` (accepted, owner), `docs/decisions/ADR-O71-golden-changes-in-autopilot.md`
  (proposed), `docs/findings/F-063-version-bumps-disagree-with-versioning.md`
- `docs/sessions/_template.md` 2.0 (Decisions section), `docs/rules.yaml` 2.0 (R-32), `docs/bootstrap/README.md` 2.0
  (step 6 resumes a running run; the commit grant), `docs/ownership.md` 1.2, `AGENTS.md` 1.3 (map row)
- `docs/bootstrap/working_agreements.md`, `docs/plans/backlog.yaml` (D-08), `CHANGELOG.md`, `docs/docs_log.jsonl`
  (seq 21 to 27), generated: `docs/index/*`, `docs/rules.md`, `docs/plan.md`, `docs/bootstrap/state.md`, AGENTS.md
  sections 5 to 7, `docs/for_the_owner.md`

## Verification
- before: `scripts/verify.sh` exit 0, 582 passed (after the compaction, 2026-10-11)
- after: `scripts/verify.sh` exit 0, 582 passed; `make golden`: unchanged (no code or example changed)
- Prediction 1 held (582 before). Prediction 2 held (582 after, no output changed). Prediction 3 held (docs log seq
  21 to 27, verified by the gate). Prediction 4 held (decisions 98 with 1 proposed, open findings 36, ADR-O71 in
  section 7). Prediction 5 held (ADR-O72, F-064, S-009). Prediction 6 held (docs plane PASS).

## Next
The owner replied "commit it, Run the autopilot in docs/prompts/autopilot.md.": ADR-O71 accepted as owner_default and
the prompt's section 5 heading reworded to match (docs-version 1.1). The first autopilot run starts at M9-04.
