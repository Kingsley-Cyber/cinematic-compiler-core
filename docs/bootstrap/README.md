# Bootstrap: resume work on this repo

<!-- docs-version: 1.0 -->

Read this first after a context compaction, in a new session, or whenever you are unsure where the work stands. It
holds no state of its own: [state.md](state.md) is generated from the repo, and everything else points at the repo's
own records (owner O69). In Claude Code, `/bootstrap` opens it.

## 1. Resume in six steps

1. **Work in the right folder.** All work happens in the worktree `~/Documents/ccc-m810` (branch `m8.12-harden`).
   The main folder `~/Documents/cinematic-compiler-core` holds another session's uncommitted files: never edit,
   commit or fast-forward it ([environment.md](environment.md), ADR-O52).
2. **Read the git state** (it is not in any file):
   `git -C ~/Documents/ccc-m810 status --short`, then
   `git -C ~/Documents/ccc-m810 log --oneline origin/main..HEAD` (unpushed commits), then
   `git -C ~/Documents/ccc-m810 fetch -q origin` and `git -C ~/Documents/ccc-m810 rev-parse --short origin/main`.
   Uncommitted work belongs to the session whose file says `in progress`; finish it or ask the owner before starting
   anything new.
3. **Read where the work stands:** [state.md](state.md) (generated), then [../../AGENTS.md](../../AGENTS.md) in full
   (the operating manual and its nine-step protocol), then the five indexes it lists and [../plan.md](../plan.md).
4. **Read how to work with the owner:** [working_agreements.md](working_agreements.md) and
   [lessons.md](lessons.md) (gotchas already paid for once).
5. **Run the gate and keep its exit code:** `rm -f gate.log; scripts/verify.sh > gate.log 2>&1; echo "exit=$?"`. A
   `gate.log` you did not just write is not evidence (lessons L-02).
6. **Refresh the graphs** (`make graphs`), take the `next` slice in [../plan.md](../plan.md), open its session file
   from [../sessions/_template.md](../sessions/_template.md) with your predictions, and build it (AGENTS.md section 8).

## 2. Ending a slice

1. `scripts/verify.sh` green; `make docs` run; backlog, findings, CHANGELOG and the session file updated.
2. Run the self-audit ([../prompts/self_audit.md](../prompts/self_audit.md), `/self-audit`) and report its verdict,
   evidence and wrong claims with the diff.
3. Commit only when the owner says so ("commit it"); push only when the owner says so ("push it"), with
   `git push origin m8.12-harden:main` after checking it is a fast-forward.
4. Add any new gotcha to [lessons.md](lessons.md).

## 3. Before a compaction

Everything that matters must already be in files: the session file (Status, Commit, Verification, Next), the
backlog, the findings, [lessons.md](lessons.md), and a short note in the agent's own memory pointing here. Then tell
the owner it is safe to compact.

## 4. Files here

| File | What it holds | Who writes it |
|---|---|---|
| [state.md](state.md) | versions, last sessions, next slices, slices left, open rulings, serious findings, next free IDs | generated (`make docs`) |
| [environment.md](environment.md) | folders, branches, push command, tools, CI, the shell | agent, when the setup changes |
| [working_agreements.md](working_agreements.md) | how the owner wants to work | agent, from the owner's words |
| [lessons.md](lessons.md) | gotchas already paid for, one per line, append-only | agent, after each slice |
