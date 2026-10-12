# F-168 — The pre-commit gate waits for the owner's `make hooks`

<!-- docs-version: 1.0 -->

## Type
question

## Severity
low

## Layer
docs

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- RV-04 (S-044 D8): `make hooks` writes core.hooksPath into the repository config the worktree shares with the owner's
  main checkout, which O52 keeps the agent from editing; the run report lists it for the owner
- review 3 (S-054): the generated owner lists did not show it (F-154)

## Description
The pre-commit hook that runs the gate is not turned on; only the owner can run `make hooks`.

## Impact
A commit can land without the gate unless the agent runs it by hand.

## Proposed Fix
The owner runs `make hooks` in the worktree, or rules that the agent may.

## Owner Ruling
the question open

## Related
- F-078
- PLAN-007

## Resolution
Open.
