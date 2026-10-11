# cinematic-compiler: Claude Code context

Read HANDOFF.md first (its "Bootstrap after compaction" block), then AGENTS.md. Navigate with graft/graphify before
reading files. Log every schema, card and kernel change with `python -m kernel.schema_log`. Build one step per slice
and commit only when `scripts/check.sh` exits 0 (never through a pipe that hides its exit code).

Current mission (2026-10-11): every emitted prompt must provably adhere to the owner's knowledge DAG, row by row, as a
checklist (`python -m validators.checklist`). Next phase: deconflict the owner's plan against this repo first (protocol
in docs/handoff/NEXT_SESSION.md); never call a prompt done without its checklist.
