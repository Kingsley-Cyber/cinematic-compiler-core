# S-035 — The first principal review, and its gaps filed: rulings O88-O100, findings F-074-F-119, PLAN-007

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), with five independent read-only reviewers

## Gap
Backlog RV-01 to RV-41 (added this session; PLAN-007); rulings O88 to O100; findings F-074 to F-119

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-035]

## Plan
The owner pasted a principal-review prompt and the no-shortcuts principle (ADR-O99). The review ran read-only and
reported (verdict: partially). The owner answered its ten questions (O88 to O97), added the gate to CLAUDE.md (O98) and
the anti-reward-hacking clause to CLAUDE.md and AGENTS.md (O100), and said: "File it. Steps 1 and 2 only — no fixes
yet." Step 1: freeze new features and do not commit PLAN-006 as written (it is corrected in place, S-034 D7). Step 2:
name every gap the review found as a finding with a backlog slice, or as a question for the owner. No code, data or test
changes; then wait for the owner's "go".

Predictions, made before the gate run:
1. The gate passed before the filing: 640 tests (S-033, 50e20f5).
2. After the filing the gate passes with the same 640 tests; the docs plane accepts ADR-O88 to O100, F-074 to F-119,
   PLAN-007 and backlog 11; `docs/bootstrap/state.md` names RV-01 next.
3. No test, fixture, expected output or example changes (AGENTS.md section 18).

## Decisions
- D1 — The review ran with five fresh read-only reviewers (layers S01-S09, S10-S18, rules and shortcuts, decisions and
  findings, the golden and the soul), none with access to the builder's reasoning, because the builder wrote much of the
  work; the builder then checked the heaviest claims against the files (fourteen held, among them four of the builder's
  own shortcuts). Why: the review prompt ("You are not the builder"). Level: covered (O99).
- D2 — One finding per unrecorded gap, grouped by cause (F-074 to F-118), each with a slice or written as a question;
  F-119 asks how the new clause meets R-33. Why: O99 ("THERE IS NO OPTION D"). Level: covered.
- D3 — O89's "genuine airborne or prop-moving misses" is read as contacts measured between keys or samples (an
  interpolated instant), recorded in ADR-O89 and RV-02 for the owner to confirm. Level: interpretation.
- D4 — O97 meets the owner invariant no_render_compression and R-16: F-088 asks which prompts carry the cap, what a
  capped prompt drops and whether R-16 is amended; RV-13 (the check) is ready, RV-13b (fitting) blocked. Level:
  question (option C).
- D5 — The order: the builder's own shortcuts (RV-01 to RV-04), then the owner's rulings, then the fight-breakers, then
  the rest, then PLAN-006 and PLAN-003; RV-01 is next. Why: the owner's step 3 and the review's ranking by harm. Level:
  interpretation (the owner can reorder).
- D6 — The owner's three pasted texts are kept word for word in the repo (docs/prompts/principal_review.md,
  docs/prompts/no_shortcuts.md, AGENTS.md section 18 and CLAUDE.md; the gate in CLAUDE.md). Why: AGENTS.md section 1,
  the repo is the source of truth. Level: covered (O98, O99, O100).
- D7 — AGENTS.md goes from 1.3 to 2.3: a protocol change, +1.0 (docs/versioning.md; F-063 still asks which reading).
  Level: covered.
- D8 — Where the clause's rule 1 (tests immutable without the owner's ask) meets R-33 (slices record deviations in the
  golden test), the conflict is asked (F-119), not settled in AGENTS.md. Why: the clause's rule 5. Level: question.
- D9 — The owner's original documents in the main checkout were read only to compare (O52): the deconfliction plan and
  the probes README in the worktree are newer, and the render log lives as docs/renders/R1-R19 and
  docs/reports/2026-10-11-render-log.md, which the reviewers read. Level: covered.

## Duration
about 3 hours (the review, its verification and the filing)

## Changes
- docs/prompts/principal_review.md, docs/prompts/no_shortcuts.md (new, the owner's words; docs log)
- CLAUDE.md (the gate; the anti-reward-hacking clause); AGENTS.md 2.3 (section 18; docs log)
- ADR-O88 to ADR-O100 (new); F-074 to F-119 (new); docs/plans/007-principal-review.md (new, PLAN-007)
- docs/plans/backlog.yaml 11: RV-01 to RV-41 and RV-13b (new), AS-07 (new), AS-01, AS-04, M9-10, M9-11, M9-14b amended,
  RV-01 next
- docs/plans/006-ten-asymmetric-things.md and S-034 corrected (step 1); CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (S-033, 50e20f5)
- after: `scripts/verify.sh` exit 0, 640 passed, docs plane PASS; `git diff --stat -- tests examples` empty;
  docs/bootstrap/state.md names RV-01 next and lists the owner's open questions (F-088, F-108, F-111, F-114, F-116 to
  F-119) and the blocked slices
- Prediction 1 held. Prediction 2 held. Prediction 3 held.

## Next
Wait for the owner's "go" before step 3 (RV-01). The owner has a next topic ready: the render feedback loop.
