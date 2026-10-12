# S-036 — The finish run: a prompt that works until the repo is done (O101)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog D-11 (added this session); ruling O101

## Layer
docs

## Status
applied

## Commit
the commit whose message names [S-036]

## Plan
The owner asked for a prompt that keeps the work going until the repo is done, answering questions from the plan's own
documents, adding and migrating freely but never taking away from the plan's soul (ADR-O101). docs/prompts/finish.md
builds on the autopilot (O70, O75) with the owner's gate as the definition of done (O98), the principal review every
eight slices (O99), the no-shortcuts principle and the anti-reward-hacking clause (O100), a push per slice, and the
bootstrap's step 6 resuming a running finish run. No code, data or test changes.

Predictions, made before the gate run:
1. The gate passes with 640 tests (S-034/S-035, d463bfe); the docs plane accepts ADR-O101, D-11 and backlog 12.

## Decisions
- D1 — The run pushes each slice that clears the gate, the self-audit and the hygiene scan. Why: the owner's words
  ("working until the repo is done", while away; "commit it, push it" for this turn's work); the autopilot never
  granted a push, so this is stated in the grant table for the owner to strike. Level: covered (O101), flagged.
- D2 — Open questions are answered from the sources in a stated order of authority (the owner's rulings, the DAG, the
  source fights and render verdicts, the plans, the rules, the owner's original documents), each recorded as an ADR
  Decided By owner_default; only renders, verdicts and cards leaving draft wait. Why: O101 ("all questions you have ...
  the original document plan can be used to find the soul"). Level: covered.
- D3 — A test changes only where a ruling or the plan's intent moves the data it pins, recorded as a typed deviation;
  never to make a failing check pass. Why: AGENTS.md section 18 with O101's "you can change things"; F-119 is answered
  by the run itself under section 4. Level: covered (O100, O101).
- D4 — Done includes a new fight scene written from a new query and compiled end to end to deliverable prompts. Why:
  the owner's "nor is it working" and the gate's fight_works (O98). Level: interpretation (what "working" is proved by).
- D5 — The bootstrap README goes 2.0 to 3.0 (its resume protocol changes, +1.0, docs/versioning.md); D-11 joins
  PLAN-005 (backlog 12). Level: covered.

## Duration
about 30 minutes

## Changes
- docs/prompts/finish.md and .claude/commands/finish.md (new; docs log); docs/bootstrap/README.md 3.0 (step 6; docs
  log); ADR-O101; backlog 12 (D-11); CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (d463bfe)
- after: `scripts/verify.sh` exit 0, 640 passed, docs plane PASS; no test, example or code changed
- Prediction 1 held.

## Next
Run `/finish` (or "Read docs/bootstrap/README.md, then run docs/prompts/finish.md until the repo is done."): RV-01 first.
