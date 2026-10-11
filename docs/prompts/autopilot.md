# Autopilot: work the backlog end to end without stopping

<!-- docs-version: 1.1 -->

Invoke when the owner wants the agent to build slice after slice without waiting between them (owner ADR-O70):
- in Claude Code, in a session opened in the repo folder: `/autopilot`;
- in any agent: "Run the autopilot in docs/prompts/autopilot.md."

The run follows [AGENTS.md](../../AGENTS.md) (the nine-step protocol, rules R-01 to R-32) and CLAUDE.md for every
slice. This file adds only what changes when nobody is waiting between slices: what the owner grants, how every
decision is logged, when to keep going and when to stop.

## 1. What invoking it grants, and what it does not

| Granted for this run only | Never granted: prepare locally, list in the run report, wait for the owner |
|---|---|
| Take the next slice as soon as the last one is committed, without asking | a push (R-03) |
| Commit each slice locally once it clears section 6 (this is the owner's "commit it" for those commits) | a render or a paid model API call (R-04); a render verdict (R-29) |
| Make the decisions sections 4 and 5 allow, each logged with its reason | a change to `kernel/layer_order.yaml`, `docs/rules.yaml` or a card leaving draft (R-09, R-30) |
| Park a slice that needs the owner and move on to the next one | anything in the main folder `~/Documents/cinematic-compiler-core` (ADR-O52) |
| | force-push, rewritten history, an edited or deleted log line, `--no-verify` |

A grant does not outlive its run. A new run needs a new invocation.

## 2. Start the run (once)

1. Follow the bootstrap's resume steps 1 to 5 ([../bootstrap/README.md](../bootstrap/README.md)): right folder, git
   state, state.md, AGENTS.md, working agreements, lessons, then the gate with its exit code.
2. The tree must be clean and no session file `in progress`. If one is, it is the first thing to finish (it is this
   agent's own unfinished slice) or, if its work is not yours, stop and report (section 7).
3. If the gate is red before any change, that failure is the first slice (AGENTS.md section 8 step 2).
4. Open the run report from section 8: `docs/reports/<date>-autopilot-<n>.md`, Status `running`, the base commit
   (`git rev-parse --short HEAD`). It goes into the first slice's commit.
5. Refresh the graphs (`make graphs`).

## 3. Each slice: pick, plan, build

1. **Pick.** The `next` slice in [../plan.md](../plan.md); if none is `next`, the first `ready` slice in backlog order
   whose `depends_on` are all `done`. Skip `blocked`, `deferred`, the owner's own slices (step `owner`, e.g. the
   render M9-17) and any slice that depends on one of these. Mark it `next` in the backlog. Nothing left to pick:
   finish the run (section 7).
2. **Plan before touching anything.** Open `docs/sessions/S-NNN-<slug>.md` from the template (status `in progress`):
   the gap, its layer (`docs/layer_order.md`), the plan, numbered predictions for every check (test count, which
   codes fire where, which outputs change, which checklist rows move) and the first decision: where each check lives
   (R-10).
3. **Read only what the slice needs.** graft (`skeleton`, `callers`, `grep`) and graphify before any file; the slice's
   findings, its DAG-map rows in `kernel/knowledge_map.yaml`, its rulings.
4. **Build at the owning layer** (AGENTS.md section 8 step 6): schema first and logged, then the code, then the check
   with two or three break tests, a should-not-fire run over the four examples and their prompts, the code in
   `prompt_validator.CODES` and `READS` where it is a prompt code, a `BREAKS` entry in
   `tests/test_dag_conformance.py`, and the DAG-map row's `codes` and `enforced_by` (kernel log). While building, run
   only the tests you touched (seconds); run the full gate once the slice is whole.
5. **A slice that turns out to span two steps** is split in the backlog (`a` and `b`, same place in the order),
   logged as a decision (section 4) and built one part at a time.

## 4. Every decision is logged, with its reason (R-32)

A decision is any choice the plan did not spell out: where a check lives, a threshold, a tolerance, a wording, a test
value, what to do when two rules pull apart. Each gets a line in the session file's **Decisions** section:

`D<n> — <the choice> — Why: <the rule, ruling, DAG row or AGENTS.md / CLAUDE.md section behind it, and the reason>
— Alternatives: <what else, and why not> — Downstream: <slices, outputs or checks it affects> — Level: <level>`

| Level | When | Logged where, besides the Decisions line | Then |
|---|---|---|---|
| covered | a rule, an accepted ADR, the DAG or the approved slice text already decides it | cite the ID in the Why | continue |
| interpretation | inside the slice, and no rule or ruling decides it | a comment `Interpretation (Claude's, for owner review): ...` where it lives, and one line added to finding F-053's Description | continue |
| owner's call | something only the owner decides (R-28, R-30), or the rules and rulings are silent or contradict at the owner's level | a `proposed` ADR (next free O number, from state.md) with Context, Consequences and Alternatives, and a finding of type `question` that links it | section 5 |

A choice missing from Decisions is a failure the self-audit reports (its section 9). Never decide silently, and never
guess where the repo has the answer (AGENTS.md section 1).

## 5. Golden and authored-data changes (ADR-O71)

First apply R-17: if a new check fails on golden content that agrees with its own words and the DAG, fix the check,
not the golden. Otherwise:

1. **Covered** by an accepted ADR or the approved slice text: make the change and record it in
   `tests/test_reference_fight_golden.py` with that ADR.
2. **Not covered, a leaf, small:** no `next` or `ready` slice depends on this one; the change is the smallest that
   makes the golden agree with its own words or the DAG, keeping the golden's words (lessons L-08); and fewer than
   three proposed golden changes from this run are still waiting on the owner. Make it in this slice's commit, with
   a proposed ADR, the golden test recording it, and `[proposed ADR-Onn]` in the commit message.
3. **Anything else (park it):** `git restore` the slice's uncommitted work, then commit the records only: the session
   file (status `not started`, or `reverted` if code was written), the proposed ADR, the question finding, and the
   backlog item `blocked` with `blocked_by: "ADR-Onn (proposed): <the question>"`. Then pick the next slice.

The same park path takes every other owner's call that section 1 never grants: the layer order, the rules, a card
leaving draft, a render verdict.

## 6. Verify, update, audit, commit (every slice)

1. **Gate:** `rm -f gate.log; scripts/verify.sh > gate.log 2>&1; echo "exit=$?"` (lessons L-02); `make golden`;
   `python -m compiler.rebind` reports no moved packet. Say which predictions held and which failed, and why.
2. **A red gate:** AGENTS.md section 11, at most three attempts. Still red: revert (section 10 there), record what went
   wrong in the session file (status `reverted`) and a finding, commit the records only, pick the next slice.
3. **Update:** the backlog (this slice `done`, the next one `next`); findings resolved with the code that catches them;
   a CHANGELOG line under Unreleased; the session file (Status `applied`, Commit `[S-NNN]`, Verification with each
   prediction held or failed, Decisions, Next); a new line in `docs/bootstrap/lessons.md` for any new gotcha;
   `python -m validators.checklist --write` when outputs changed; `make docs` (state.md, indexes, AGENTS.md sections
   6 and 7). Then the gate again.
4. **Self-audit** ([self_audit.md](self_audit.md)) on this slice, read-only. READY TO COMMIT: commit. NOT READY: apply
   the mechanical fixes and audit again, at most twice; a fix that needs the owner takes the park path (section 5).
5. **Commit** one slice: `[S-NNN] <slice id>: <title> (<rulings>)`, a short body, `[proposed ADR-Onn]` if any, the
   co-author line the harness requires. The pre-commit hook runs the gate.
6. **Report the slice** in the run report's table, update your own memory note (last commit, next slice), and send
   the owner one line in chat, then go straight on:
   `M9-04 done · <sha> · gate <n> tests · predictions 5/6 held · decisions 4 (1 proposed) · checklist +3 PASS`.
7. `make graphs` and back to section 3.

## 7. When the run ends

**Finish** when no slice can be picked. Run the gate, then the self-audit over the whole run (scope `origin/main..HEAD`,
including its public-repo hygiene step), set the run report's Status to `finished`, commit it as the run's last
records commit, and report to the owner (section 8's "For the owner" list). Never push.

**Stop at once** (Status `stopped`, with the reason) when:
- the owner sends a message or rejects a tool call: the owner's words win (ask nothing more until they say);
- the gate is red at the start of a slice and this run did not cause it;
- the work would need anything section 1 never grants;
- the tree holds files this run did not write;
- two slices in a row park or revert on the same cause (something upstream is wrong).

**Never stop for** a context compaction (section 9), a question that can be logged and parked, or a failed
prediction (report it and go on).

## 8. The run report

`docs/reports/<date>-autopilot-<n>.md`, updated in every slice's commit:

- Status (`running`, `finished` or `stopped: <reason>`), started, base commit, the slice in progress.
- A table: Slice | Session | Commit | Result (done, parked, reverted) | Predictions held | Decisions (proposed) |
  Checklist change.
- **For the owner**, kept current: (1) proposed ADRs to rule on, oldest first; (2) parked slices and their questions;
  (3) render probes prepared (`docs/render_tests/`, R-11), never rendered; (4) interpretations added to F-053;
  (5) commits ready to push, with the hygiene result.

## 9. After a compaction

The bootstrap README sends a resumed session here when a run report says `running`. Read that report, the session
file `in progress` (if any) and this file, then continue where the report says: finish the open slice or pick the
next one. The report and the session files are the record; the compaction summary is a claim to check.
