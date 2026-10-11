# Environment

Facts about the machine and the repo setup that no other file records. Update it when the setup changes.

## Repository and folders

- **Remote:** github.com/Kingsley-Cyber/cinematic-compiler-core, public (MIT). Every push is public: run the
  self-audit's hygiene step (no secrets, no absolute home paths, no email, no third-party text) before pushing.
- **Worktree (all work):** `~/Documents/ccc-m810`, branch `m8.12-harden`. GitHub `main` is fast-forwarded from it:
  `git push origin m8.12-harden:main`, after `git merge-base --is-ancestor origin/main HEAD` confirms a fast-forward.
- **Main folder (do not touch):** `~/Documents/cinematic-compiler-core`, branch `main`. Its local `main` ref stays
  behind GitHub because another session's uncommitted files sit there (its `scripts/check.sh` among them), so it cannot
  be fast-forwarded. Never edit, commit or check out anything there (ADR-O52, finding F-056).
- **Scratch:** temporary files go in the session's scratchpad, never in the repo.

## Tools

- **Python environment:** mise pins Python 3.12.14 (`mise.toml`); uv 0.11.12 runs the locked environment
  (`uv.lock`): `mise exec -- uv run --locked <command>`. `scripts/verify.sh` and the Makefile pick mise when present,
  plain uv otherwise.
- **Gate:** `scripts/verify.sh` (`make verify`); `scripts/check.sh` only calls it.
- **Graphs:** graft at `.graphs/graft` and graphify at `.graphs/graphify` (both ignored); `make graphs` rebuilds.
  `graft --dir .graphs/graft skeleton <file> .`, `graft --dir .graphs/graft callers <symbol> .`,
  `graft --dir .graphs/graft grep <text> .`.
- **CI:** six GitHub workflows (verify, tests, golden, schemas, docs on every push; nightly regenerates the docs and
  opens a PR when they are stale). They build the Dockerfile on GitHub's machines; the owner does not use Docker
  locally. `gh run list --limit 6` shows the last results.
- **Renders:** the owner renders on Seedance 2.0 Mini (O56) and sends the mp4. Read frames with ffmpeg
  (`-vf fps=N,scale=…,tile=…`); this ffmpeg has no `drawtext` filter.

## Shell

zsh: an unquoted variable does not split into words (`for f in $FILES` runs once), while an unquoted `$(...)` does.
Use Python for anything that loops over file lists (lessons L-01).
