# Self-audit: check your own work before the owner commits or pushes

<!-- docs-version: 1.0 -->

Invoke at the end of a slice or session, before any commit or push:
- in Claude Code: `/self-audit` (optionally `/self-audit S-004` or `/self-audit M9-03`);
- in any agent: "Run the self-audit in docs/prompts/self_audit.md on this session's work."

## Stance

Audit your own work as if someone else wrote it and you expect to find mistakes. The repo is the evidence. Your memory,
your session file, your commit messages and your last report to the owner are claims to test, not facts.

- **Read-only.** Change nothing in the working tree while auditing. A throwaway worktree for an old commit is allowed
  (`git worktree add <scratch>/audit <sha>`, removed afterwards). List fixes; apply them only after the owner says so,
  each as its own slice.
- **Evidence or nothing.** A row is PASS only with evidence produced in this audit: a command and its key output, or a
  `file:line`. Without evidence the row is NOT CHECKED, never PASS. "I did this earlier" is not evidence.
- **Report failures plainly**, including predictions that failed and claims that were wrong. Do not soften or omit.
- Navigate with graft and graphify first (`make graphs`); read only the line ranges you need.

## 0. Scope

1. The sessions: the one named in the argument; otherwise every `docs/sessions/` file with Status `in progress`, plus
   the last `applied` one.
2. The work: `git log --oneline origin/main..HEAD` (unpushed commits), `git status --short` and `git diff --stat`
   (uncommitted). The base is `origin/main` unless the argument names a commit.
3. The claims: each session file's Plan, Predictions, Changes and Verification; the commit messages; your last report
   to the owner. Write them down as a numbered list before checking anything.

## 1. The gate, fresh

- `scripts/verify.sh > gate.log 2>&1; echo "exit=$?"`: exit 0 and the last line `check: PASS`. Compare the test count
  with what you reported.
- If it fails, run the parts one by one to find the first failure: `ruff check .`, `pytest -q`,
  `python -m kernel.schema_log --log <schemas|library|kernel|docs> verify`, `python -m kernel.build_ir_schema --check`,
  `python -m kernel.shared_schemas --check`, `python -m kernel_extraction.control_inventory --check`,
  `python -m compiler.examples`, `python -m kernel.build_docs --check`, `python -m kernel.docs_plane`.

## 2. Protocol (AGENTS.md section 8), per session

| Step | Evidence to produce |
|---|---|
| Read the state | the session file names its backlog slice, findings and ruling |
| Verify before | the session's Verification records the pre-change gate result |
| One gap | `git show --stat <sha>` for each commit: one backlog slice per commit, `[S-NNN]` in the message |
| Right layer | for each new check: the data it reads, the step that writes each item (`docs/layer_order.md`), and the step it lives in; it must be the first step that can see all of it (rule R-10) |
| Plan and predictions | the session file has numbered predictions; Verification says for each one whether it held, with what happened |
| Implement | schema or card changes logged before the code that uses them |
| Verify after | section 1 above; `make golden` matches what the session says changed |
| Update | the backlog status matches the code (`python -m kernel.docs_plane`); each resolved finding names the code that catches it; a CHANGELOG line under Unreleased; AGENTS.md sections 6 and 7 regenerated |
| Commit | nothing pushed that the owner did not approve: compare `git log origin/main` with the owner's words in the conversation |

## 3. Every claim, re-derived

For each numbered claim from section 0, re-run what proves it and mark it **VERIFIED**, **WRONG** (give the correct
statement) or **UNVERIFIABLE** (say why):
- counts ("579 tests", "10 findings", "16 prompts byte-identical"): run the command again;
- "only X changed": `git diff --stat <base> -- <paths>`;
- "prediction held": re-run the check that proves it, on the commit before the change in a throwaway worktree if needed;
- "no checklist row moved to PASS": `git diff <base> -- examples/*/checklist.md`;
- "the gate passed": section 1.

## 4. Every new or changed check is real

For each code added or changed (`git diff <base> -- compiler validators renderers planner solver | grep '"[A-Z_]\{6,\}"'`):
- **Wired:** `graft --dir .graphs/graft callers <function> .` shows the pass, validator or test that runs it in the
  gate.
- **Fires:** a test breaks one thing and asserts the code (`grep -n <CODE> tests/`), and it passes.
- **Silent where it should be:** it reports nothing on the four examples and their 20 prompts.
- **Registered:** prompt codes in `prompt_validator.CODES` and `READS`; a `BREAKS` entry in
  `tests/test_dag_conformance.py`; the DAG-map row's `codes` and `enforced_by` in `kernel/knowledge_map.yaml`, logged.
- **Not weakened elsewhere:** `git diff <base> -- tests/` lists every changed assertion or expected value. Each change
  must follow from the slice's intended change (data moved on purpose), never from making a test pass. No new
  `skip`, `xfail` or deleted test.

## 5. Data and the golden

- `git diff <base> -- examples/*/plans`: list every authored change and map it to a ruling (ADR) and the session
  plan. Authored data changes only under a ruling, as a recorded deviation (rule R-08).
- `python -m compiler.rebind` (report mode, no `--write`): reports no moved packet.
- `git diff --stat <base> -- examples/*/render.txt examples/*/prose_*.txt`: only the examples the slice meant to change.
- Each golden change is recorded in `tests/test_reference_fight_golden.py` with its ruling.
- Hand-picked numbers (positions, angles, velocities): list each one and how it was justified (a check that passed, a
  search, a source).

## 6. Logs and the freeze

- `python -m kernel.schema_log --log <log> verify` for schemas, library, kernel and docs.
- `git diff <base> -- '*_log.jsonl'` only adds lines, and each new entry's reason cites a ruling.
- Every changed frozen doc bumped its docs-version, and the bump matches the change (0.1 for wording, 1.0 for a
  protocol or rule change; `docs/versioning.md`).

## 7. The docs plane

- `python -m kernel.docs_plane`: PASS.
- Each session file has Status, Commit, Verification and Next filled in.
- Anything discovered but not fixed is a finding, not a sentence in chat.
- `docs/plan.md` shows the right `next` slice.

## 8. Rules (docs/rules.md)

Go through R-01 to R-30 and state compliance, with evidence, for every rule this session touched. Always check:
no render and no paid model API call by the agent (R-04); no push without the owner (R-03); no hand edit of
`kernel/layer_order.yaml` or the golden outputs without a ruling and a log entry (R-09); no failure papered over (R-12).

## 9. Interpretations and silent choices

`git diff <base> | grep -in "interpretation"` plus your own list: every choice the plan or rulings did not make for
you. Each needs a labelled docstring, an ADR, or a finding of type `question`. List the ones that need the owner.

## 10. Public-repo hygiene (before a push)

Over `git diff origin/main..HEAD` and the uncommitted diff: no secrets (keys, tokens, passwords), no absolute home
paths (`/Users/...`), no email addresses, no third-party copyrighted text.

## 11. Report to the owner (plain English, answer first)

1. **Verdict, one line:** READY TO COMMIT, READY TO PUSH, or NOT READY, and why.
2. **Table:** Check | Result (PASS / FAIL / NOT CHECKED) | Evidence (the command and its key output, or `file:line`).
3. **Claims that were wrong or unverifiable**, each with the correct statement.
4. **Fixes proposed**, split into mechanical fixes and fixes that need a ruling. None applied yet.
5. **Questions for the owner**, one line each.

Keep evidence short: the deciding line of output, not file dumps.
