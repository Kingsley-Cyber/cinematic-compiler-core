# How to refactor

<!-- docs-version: 1.0 -->

A refactor changes how the repo is built without changing what it promises, unless a ruling says otherwise. Every step
below has a check, and every change can be rolled back. If a step's check fails, stop at that step.

## Before you start

1. **Gate green.** Run `scripts/verify.sh`. It must end `check: PASS`. If it doesn't, the last session left drift: fix
   it (or record it as a finding) before you change anything else.
2. **Checkpoint.** Run `git tag checkpoint-<date>-<slug>`, then work on a branch or a worktree. Never refactor on the
   only copy.
3. **Map.** Refresh the graphs: `make graphs`. Use `graft callers <symbol>` and `graft skeleton <file>` to see the
   blast radius before you edit a public symbol.
4. **Ruling.** Check the change against [rules.md](rules.md) and [index/decisions.md](index/decisions.md). If it touches
   the layer order, a schema's meaning, the golden or a frozen doc, find the ADR that allows it. If none does, write a
   finding of type `question`, name the contradiction in one line, and wait.
5. **Plan.** Add the work to [plans/backlog.yaml](plans/backlog.yaml), one slice per step it touches. Then open a
   session file from [sessions/_template.md](sessions/_template.md), with the plan and your prediction.

## One layer at a time

For each slice, in build order ([layer_order.md](layer_order.md)):

| Change | Do | Check |
|---|---|---|
| Schema | Edit `schemas/...`, bump its `$id` version, then `python -m kernel.schema_log record <file> --change changed --reason ... --decided-by ...` | `kernel.schema_log verify`; `kernel.build_ir_schema --check` |
| Library card | Edit, then `python -m kernel.schema_log --log library record <file> ...` | `--log library verify` |
| Kernel file or layer order | Only with an accepted ADR: edit, bump `version`, then `--log kernel record` | `--log kernel verify`; docs/layer_order.md regenerates |
| Code (a pass, solver, validator or renderer) | Change only the layer that owns the data. Add the check plus two or three break tests, and run it over every prompt where it must not fire | `pytest`; graft callers unchanged or updated |
| Authored plan data | Only as an owner-decided recorded deviation; never silently (R-08) | the golden test lists the deviation |
| Packets moved | `python -m compiler.rebind --write <examples>` | `rebind` reports nothing more |
| Outputs meant to change | `python -m compiler.examples --write <examples>`, then `python -m validators.checklist --write` | `make golden` shows only the intended change |
| Frozen doc | Edit, bump its `docs-version`, then `python -m kernel.schema_log --log docs record <file> ...` | `--log docs verify` |
| Anything | `make docs` | `python -m kernel.docs_plane` |

Then run `scripts/verify.sh` and commit one slice per commit, with `[S-NNN]` in the message.

## Rollback

| Situation | Command | Then |
|---|---|---|
| Uncommitted change | `git restore --staged --worktree -- <paths>` | `scripts/verify.sh` |
| Committed, not pushed | `git revert <sha>` (keeps history) | `scripts/verify.sh`; set the session `reverted` |
| Back to a checkpoint | `git switch -c rescue-<date> checkpoint-<date>-<slug>` | `scripts/verify.sh`; a finding says why |
| A rebind or example write went wrong | `git restore -- examples/` | `python -m compiler.examples` |

Never force-push, never rewrite pushed history, and never delete a log line: the logs are append-only and the gate
refuses a gap. Record every rollback in the session file and, if it taught something, in a finding.

## After the refactor

- `scripts/verify.sh` passes and `make golden` shows only the intended change.
- The backlog, findings, session file and CHANGELOG are updated, and `make docs` was run.
- Every claim in the commit message has a check behind it.
