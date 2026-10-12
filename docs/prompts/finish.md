# Finish the repo: work until the plan's soul is built and the fight works

<!-- docs-version: 1.0 -->

Invoke (owner ADR-O101):
- in Claude Code, in a session opened in the repo folder: `/finish`;
- anywhere else: "Read docs/bootstrap/README.md, then run docs/prompts/finish.md until the repo is done."

The owner's words that start this run: "i need a prompt that will essentially have you working until the repo is done.
ive genuiinely provided you enough information to relay the goal and intent of the repo, and all questions you have can
the original document plan can be used to find the soul of the repo. as of now the repo is not complete nor is it
working, at the end of the day you can add to this repo but you cant take away from the soul and intent of the plan.
you can change things but you are working to intentioally implement fully the soul of the plan and ensure it works,
fully implementation and migrations".

Everything in [AGENTS.md](../../AGENTS.md) (the nine-step protocol, the rules, section 18's anti-reward-hacking
clause), [CLAUDE.md](../../CLAUDE.md) (the gate) and [no_shortcuts.md](no_shortcuts.md) binds this run. This file adds
what changes when the goal is the finished repo and nobody waits between slices.

## 1. What done means: the owner's gate (ADR-O98)

| Gate condition | Proved by |
|---|---|
| layer_order_matches_plan | every step S01-S18 does what docs/layer_order.md, kernel/layer_order.yaml and the plans say; reads and writes checked (R-13), nodes and edges checked (R-14); every declared validator runs and the envelope records it |
| rules_match_dag | every rule R-01 onward enforced in code where code can enforce it, the rest by protocol with evidence; every mandatory DAG-map row's codes cover the whole row (no PASS on a partial check) |
| golden_passes | the reference fight agrees with the owner's source (kernel/sources/lbn-2.3-adv.txt) and its own words; every deviation has a ruling and a record; `scripts/verify.sh` and `make golden` green |
| no_shortcuts_survive | a fresh principal review (section 6) finds no shortcut of the ten types |
| soul_check_passes | the latest principal review's verdict is "matches" |
| fight_works | every emitted prompt is a deliverable (R-19) inside the length caps (O97); `cinematic compile` refuses any prompt that is not; a new fight scene, written from a new query, compiles end to end (its authored steps written in-session) to deliverable prompts; render probes are prepared for the owner, whose verdicts close this condition (R-29) |

The repo is done when every condition holds except the owner's render verdicts, and the run report lists the probes the
owner must render.

## 2. Where the intent lives, in order of authority

1. The owner's rulings (`docs/decisions/`; the owner's words are quoted in each); a newer ruling wins over an older one.
2. The knowledge DAG (`docs/sources/knowledge_dag_v1.md`) and its map (`kernel/knowledge_map.yaml`).
3. The owner's source fights (`kernel/sources/lbn-2.3-adv.txt`, `kernel/sources/lbn-2.4-adv-lma.txt`) and the owner's
   render verdicts (`docs/renders/`, `docs/reports/2026-10-11-render-log.md`).
4. The plans: PLAN-003 (`docs/plans/deconfliction_2026-10-11.md`), PLAN-001 (`docs/plans/MASTER_PLAN.md`), PLAN-002,
   PLAN-004, PLAN-005, PLAN-006, PLAN-007, and `docs/plans/backlog.yaml`.
5. The rules (`docs/rules.yaml`), AGENTS.md, CLAUDE.md, `docs/prompts/no_shortcuts.md`, the findings.
6. The owner's original documents in `~/Documents/cinematic-compiler-core`: read them freely, never edit there (O52).

The soul, in the owner's terms: elite Naruto-style choreography that renders as a fight, not a dance (ten asymmetric
things per beat, O87); every prompt provably follows the DAG row by row; the layer order is the skeleton, the rules the
contract, the golden the source of truth, the plan the map, the verifier the gate, the indexes the record.

## 3. What this run grants, and what it never does

| Granted until the repo is done | Never granted |
|---|---|
| Take slice after slice without asking | Removing or weakening anything the plan intends; a capability may only be replaced by one that does at least as much |
| Commit each slice that clears section 5, and push it to GitHub main after the gate, the self-audit and the hygiene scan pass (`git push origin m8.12-harden:main`, fast-forward only) | A render, a paid model API call (R-04), a render verdict (R-29) |
| Answer open questions from the sources (section 4), each recorded as an ADR | A library card or the knowledge map leaving draft (R-30): prepare the evidence instead |
| Change schemas, data, the examples, modules, the layer order and the rules when the plan's intent needs it: each with its ADR, log entry and version bump (R-07, R-09) | Editing anything in `~/Documents/cinematic-compiler-core` |
| Add checks, fields, steps, prompt modes and examples; migrate every consumer and all examples in the same slice | Force-push, rewritten pushed history, an edited or deleted log line, `--no-verify` |
| Change a test or expected output only where a ruling or the plan's intent moves the data it pins, each change a typed, recorded deviation (the golden test or the session file) citing that ruling: the owner's explicit ask under AGENTS.md section 18 for this case (F-119) | Skipping, deleting or weakening a test, or changing one so a failing check passes |

## 4. Questions: answer them from the sources, never stall

For each open question (the findings typed `question`, every `blocked_by`, the interpretations listed in F-053, and any
new one):
1. Find what the sources (section 2) say and quote the lines, with file and line.
2. Choose the reading that serves the soul best: the fight works, nothing the plan intends is lost, the owner's newest
   words win, the DAG over a plan, the source fight over a repo-authored value.
3. Record an ADR (next free O number; Status accepted; Decided By `owner_default`; the quoted lines in Context; the
   alternatives), resolve or update the finding, unblock the slice.
4. Where the sources cannot decide and the choice is visual and uncertain, prepare a render probe in
   `docs/render_tests/` (R-11) and go on with the reading the DAG favours, labelled.

Only renders, render verdicts and cards leaving draft wait for the owner, and they never block other work.

Open at the start of this run: F-088 (the length caps against `no_render_compression` and R-16), F-099, F-101, F-108,
F-111, F-114, F-116, F-117, F-118, F-119, ADR-O89's "genuine" reading, RV-20's layer-order ADR, and RV-38 (prepare the
owner's review pack of draft values and F-053; do not approve).

## 5. Each slice

1. **Pick** the `next` slice in `docs/plan.md`, else the first `ready` slice in backlog order whose `depends_on` are
   done. A `blocked` slice is unblocked by answering its question (section 4) first. Order: PLAN-007's RV slices, then
   PLAN-006, then PLAN-003's remaining M9 slices, then what the reviews add; within that, whatever changes what a
   rendered fight shows comes before bookkeeping.
2. **Plan** in `docs/sessions/S-NNN-<slug>.md` (status `in progress`): the gap, its layer, the plan, numbered
   predictions, and before every decision the no-shortcuts questions (a fix or a workaround; the owning layer; tightens
   or widens; a named slice; a ruling; a latent bug; a typed deviation).
3. **Build** at the owning layer (AGENTS.md section 8): schema first and logged, then code, then each check with two or
   three break tests and a should-not-fire run over every example and prompt; prompt codes in `prompt_validator.CODES`
   and `READS`, a `BREAKS` entry, the DAG-map row's `codes` and `enforced_by` (kernel log). A failing test: diagnose
   the cause and fix the implementation (AGENTS.md section 18).
4. **Log every decision** (R-32; docs/prompts/autopilot.md section 4's format and levels).
5. **Verify:** `rm -f gate.log; scripts/verify.sh > gate.log 2>&1; echo "exit=$?"`, `make golden`,
   `python -m compiler.rebind`; say which predictions held. Red after three honest attempts: revert, record the cause
   as a finding with a slice, go on.
6. **Update** the backlog, findings, CHANGELOG, session file, lessons, checklists (`python -m validators.checklist
   --write`), `make docs`; the gate again.
7. **Self-audit** (`docs/prompts/self_audit.md`) read-only; fix what it finds, at most twice.
8. **Commit** (`[S-NNN] <slice id>: <title> (<rulings>)` and the co-author line), run the hygiene scan over
   `origin/main..HEAD` (no secrets, home paths, emails or keys), **push**, then one line in the run report and in chat:
   `RV-02 done · <sha> · gate <n> tests · predictions 5/6 · decisions 4 · checklist +3 PASS`.

## 6. The review loop

After every eight slices, when a plan's last slice lands, and before declaring the repo done: run
[principal_review.md](principal_review.md) with fresh read-only reviewers who did not build the work (one each for
layers S01-S09, layers S10-S18, rules and shortcuts, decisions and findings, the golden and the fight). Check their
heaviest claims against the files; file every gap as a finding with a slice, or answer it (section 4); write the
verdict to `docs/reports/<date>-principal-review-<n>.md` (soul_check_passes reads the latest); continue.

## 7. When to stop

- **Done** (section 1): run a last review; its verdict "matches"; Status `finished`; the final report (section 9).
- **Stop at once** (Status `stopped`, with the reason) only when the owner sends a message (the owner's words win), the
  gate is red at a slice's start and this run did not cause it, or the tree holds files this run did not write.
- **Never stop** for a compaction, a question, a failed prediction or a reverted slice. Two reverts on the same cause:
  run a review (section 6), re-plan, go on.

## 8. Records, and after a compaction

- The run report `docs/reports/<date>-finish-<n>.md`: Status (`running`, `finished`, `stopped: <reason>`), base commit,
  the slice in progress, a table (Slice | Session | Commit | Result | Predictions held | Decisions | Checklist change),
  and **For the owner**: probes to render, drafts to approve, ADRs taken under ADR-O101 for the owner to confirm.
- Update your memory note every slice (last commit, next slice, the run report's path).
- After a compaction, the bootstrap README's step 6 sends a resumed session here: read the run report and any session
  file `in progress`, then continue. The report and the session files are the record; a summary is a claim to check.

## 9. The final report

Plain English, answer first: the gate's six conditions, each with its evidence; the deliverable prompts and their
lengths; the new fight compiled end to end; the probes the owner must render; the drafts awaiting approval; the ADRs
this run took for the owner to confirm; anything that remains, each with its slice.
