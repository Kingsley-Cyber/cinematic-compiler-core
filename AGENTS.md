# AGENTS.md — The Agent Operating Manual

<!-- docs-version: 1.3 -->

> Before every session, read `AGENTS.md` fully — it is the map of this repo, not a suggestion — and follow its
> nine-step session protocol exactly: read the five indexes, run `scripts/verify.sh`, pick one gap, confirm its layer
> from `docs/layer_order.md`, plan the fix, implement it at the correct layer, verify with `scripts/verify.sh` and
> `make golden`, update the plan and changelog, and commit one gap per commit. Never skip the verifier, never work on a
> blocked gap, never edit the layer order or golden by hand, and never paper over a failure — if the verifier fails,
> revert, update the plan with what went wrong, and try again. The repo is the source of truth; the indexes are the
> map; the verifier is the gate; you navigate by them, not by memory, and every session picks up exactly where the
> last one left off.

## 1. The golden rule

The repo is the source of truth. If a fact is not in the repo (an index, a decision, a rule, the code or a log), it
does not exist. Chat memory and summaries are not sources. If you are about to guess, stop: the answer is in the layer
order, the rules or an ADR. If it is not, write the question as a finding (type `question`) and wait for the owner's
ruling.

## 2. What this repo is

`cinematic-compiler-core` compiles a scene request into one validated envelope through 18 ordered steps (S01 intent to
S18 post-generation), then projects it into video-model prompts: LBN-2.4 (`render.txt`) and four structured-prose
modes. The mission (ADR-S3): every emitted prompt provably adheres to the owner's knowledge DAG
(`docs/sources/knowledge_dag_v1.md`, mapped in `kernel/knowledge_map.yaml`), row by row, as a checklist. A green test is
not adherence, and a PASS a render contradicts is NOT CHECKED. The repo is model-agnostic and built for Seedance
(ADR-O49). The owner renders; agents never do (ADR-S2). Plain-English tour: [docs/for_the_owner.md](docs/for_the_owner.md).

## 3. The map: read these first

| Read | What it is |
|---|---|
| [docs/bootstrap/README.md](docs/bootstrap/README.md) | start here after a compaction or in a new session: resume steps, generated state, environment, working agreements, lessons (`/bootstrap`) |
| [docs/index/plans.md](docs/index/plans.md) | every plan, its status, its open findings |
| [docs/index/findings.md](docs/index/findings.md) | every bug, gap, contradiction, drift, question, risk, opportunity |
| [docs/index/decisions.md](docs/index/decisions.md) | every owner ruling (ADR); IDs as the code cites them (O48, Q6) |
| [docs/index/sessions.md](docs/index/sessions.md) | every session, its gap, its commit, what comes next |
| [docs/index/renders.md](docs/index/renders.md) | every render, bound to its prompt hash |
| [docs/plan.md](docs/plan.md) | the build order across plans (from `docs/plans/backlog.yaml`) |
| [docs/layer_order.md](docs/layer_order.md), [docs/rules.md](docs/rules.md) | the layer table; the rulebook |
| [docs/ownership.md](docs/ownership.md), [docs/versioning.md](docs/versioning.md) | who changes what; version bumps |
| [docs/how_to_refactor.md](docs/how_to_refactor.md) | steps, checks and rollback for any refactor |
| [docs/prompts/self_audit.md](docs/prompts/self_audit.md) | the self-audit run before every commit or push (`/self-audit`) |
| [docs/prompts/autopilot.md](docs/prompts/autopilot.md) | the owner-started run that builds slice after slice, every decision logged (`/autopilot`) |
| [docs/reference/](docs/reference/README.md) | generated: every step's inputs and outputs, every schema field, every data file, code imports |
| `kernel/layer_order.yaml` | the machine source of the layer DAG and write ownership |

Indexes first, then only the files the gap needs. Generated files say so in their first lines; never edit them.

## 4. Layer order

<!-- BEGIN GENERATED: layer_order -->
S01 intent (L0) → S02 brief (L0.5) → S03 constraint (L1.5) → S04 temporal (L1.1) → S05 causal (L1.2) → S06 state (L2.1) → S07 contact (L2.2) → S08 hand_role (L2.5) → S09 object_state (L2.6) → S10 affordance (L2.7) → S11 kinematic (L4a) → S12 bartenieff (L4b) → S13 motion (L4c) → S14 facial (L4d) → S15 effort (L5) → S16 camera (L5.5) → S17 render (L6) → S18 post_generation (L6.5)

Full table: [docs/layer_order.md](docs/layer_order.md).
<!-- END GENERATED: layer_order -->

## 5. Rules

<!-- BEGIN GENERATED: rules -->
- **R-01** Read AGENTS.md, the five indexes and docs/plan.md before touching anything; refresh and query graft and graphify before reading files.
- **R-02** One slice per commit, committed only when scripts/verify.sh exits 0.
- **R-03** Nothing is pushed without the owner's word.
- **R-04** Claude never renders and never calls a paid model API; authored steps are written in-session from a sealed packet.
- **R-05** Predict the outcome before each check and report whether it held.
- **R-06** Ask the owner only where the DAG, these rules or the decisions are silent or contradict; write the question as a finding (type question) and wait instead of guessing.
- **R-07** Log every schema, library card, kernel file and frozen doc change in its hash log; a frozen doc change also bumps its docs-version.
- **R-08** Never edit authored data silently: scripts derive and refuse; a content change is an owner-decided, recorded deviation.
- **R-09** Never edit kernel/layer_order.yaml or the golden by hand: a change needs an accepted ADR, its log entry and a version bump; examples are rewritten only by python -m compiler.examples --write.
- **R-10** Place every check at the first step that can see its data (docs/layer_order.md); a fix lives in the layer that owns the data.
- **R-11** Test the uncertain, build the certain: a change gets a render probe only if it is uncertain, visual and not verifiable without a render.
- **R-31** Before asking the owner to commit or push, run the self-audit (docs/prompts/self_audit.md) and report its verdict, evidence table and wrong claims.
- **R-32** Log every decision the plan did not spell out in the session file's Decisions section, with the rule, ruling or DAG row behind it, the alternatives and what it affects; a choice no rule or ruling makes is labelled as an interpretation or proposed as an ADR.
- **R-33** A slice may rewrite the examples so they pass its own new check, as recorded deviations (the golden test and the session file), without a ruling per change.
- **R-34** A check that judges a whole-body quality (direction, lean, height, momentum) reads the root's rotation, the support and every joint it depends on, and skips a span it cannot judge (an airborne turn) instead of reporting it.
- **R-12** Never paper over a failure: when the verifier fails, fix or revert, and record what went wrong in the plan or a finding.
- **R-13** The step IDs carry the build order: a step reads only what earlier steps wrote and writes only its own paths.
- **R-14** Every layer that produces state has nodes and edges; L0, L0.5, L6 and L6.5 have nodes only; L4d facial runs for live action and UGC only.
- **R-15** Contracts are JSON Schemas checked by the in-repo validator; no Pydantic; pyyaml is the only runtime dependency.
- **R-16** The repo is model-agnostic and built for Seedance: no model cards; models arrive later as adapters (M7).
- **R-17** Where the golden contradicts its own words or the DAG, fix the golden as a recorded deviation; where a new check fails on internally consistent golden content, fix the check.
- **R-18** Bodies and props obey the scene's physics: no teleport above 25 m/s except a declared substitution; props follow gravity unless a float is declared (anime only).
- **R-19** A prompt is a deliverable only when every applicable DAG-map row passes on it, shown per prompt; NOT CHECKED is not a pass.
- **R-20** The format comes from the DAG's own instances (D6, D9, D10).
- **R-21** No hold, freeze or pause is written in frames; a hit gets a camera hold with the bodies in frame and no close-up.
- **R-22** A hand that releases a prop and then holds nothing is said to be empty.
- **R-23** A turn is named once by axis, plane and count, with takeoff and landing; no angles at times, no rates, no angles on the lines inside it.
- **R-24** No prop is called hidden or not visible; an object the scene needs later stands in the scene from the start and the prompt says where.
- **R-25** Every causal link prints a reason that states a cause.
- **R-26** Every stated count agrees with the scene.
- **R-27** Effort actions stay Laban (punch = thrust); combat verbs go on contacts.
- **R-28** Only the owner accepts a decision; an agent proposal not objected to is recorded as owner_default.
- **R-29** Only the owner renders and gives render verdicts; verdicts are logged word for word, Claude's frame notes apart.
- **R-30** Only the owner approves a push, a card leaving draft and a change to the layer order or the golden.

With sources and enforcement: [docs/rules.md](docs/rules.md).
<!-- END GENERATED: rules -->

## 6. Current state

<!-- BEGIN GENERATED: state -->
- Layer order 1.7; rules 3.0; backlog 5.
- Last session: S-020 (2026-10-11, applied): M9-09a: SHAPE_DIRECTION refuses a Shape quality the body contradicts (F9.1; O31, O73, O76).
- Next slice: M9-09b F9.2 airborne momentum under gravity (O74) (step kinematic).
- Open findings: 40; decisions: 107 (0 proposed).
<!-- END GENERATED: state -->

The agent updates this section after every session by writing its session file (`docs/sessions/`), updating the
backlog and findings, and running `make docs`; the verifier checks that it matches.

## 7. Open rulings

<!-- BEGIN GENERATED: rulings -->
- F-051 (low): Draft library cards await owner review
- F-052 (low): Kernel scope numbers await owner review
- F-053 (medium): Claude's interpretations await owner review
- F-054 (low): Agent additions await owner review
- F-055 (low): M6 tools are undefined
- F-057 (low): The kernel rule 'substitution log reveals' reads against O48's staging
- F-059 (low): Reference-fight deviations from its own data await review
- F-060 (low): What is a motif?
- F-066 (high): What is a key's root position: the pelvis or the ground point?
- F-069 (medium): Nine airborne spans hang longer than gravity allows
- Backlog M9-03a blocked: GAP-04/05 checkable constraint form and the per-layer constraint run — owner approval of the checkable constraint schema (O61)
<!-- END GENERATED: rulings -->

The owner updates this section by ruling: in chat (the agent writes the ADR) or by writing an ADR from
`docs/decisions/_template.md`. `make docs` regenerates the list; the verifier checks that it matches.

## 8. Session protocol (nine steps)

1. **Read the state.** `docs/bootstrap/` (after a compaction or in a new session), this file, the five indexes,
   `docs/plan.md`. Refresh the graphs (`make graphs`) and navigate
   with graft and graphify before reading source (R-01).
2. **Verify.** Run `scripts/verify.sh`. If it fails before you change anything, the failure is your first gap: record
   it as a finding and fix it, or stop and report.
3. **Pick one gap.** Take the `next` slice in `docs/plan.md`. Never take a `blocked` slice; never take two.
4. **Confirm the layer.** Find the slice's step in `docs/layer_order.md`. The fix lives in the layer that owns the
   data, and a check goes at the first step that can see its data (R-10).
5. **Plan.** Open `docs/sessions/S-NNN-<slug>.md` from the template, with the plan and a prediction of what each
   check will show (R-05).
6. **Implement at that layer.** Schema first (logged), then code, then the check with two or three break tests and a
   should-not-fire run over every prompt. Authored data changes only as recorded, owner-decided deviations (R-08).
7. **Verify.** `scripts/verify.sh` and `make golden`. Say whether each prediction held. If the gate fails, follow
   section 11.
8. **Update.** The backlog status, the findings (resolved, with the code that catches them), `CHANGELOG.md`, the
   session file (commit, verification, next), then `make docs`.
9. **Audit, then commit.** Run the self-audit (`docs/prompts/self_audit.md`; `/self-audit` in Claude Code, rule
   R-31) and give the owner its verdict, evidence table and any wrong claims. One gap per commit, with `[S-NNN]` in
   the message and only after `scripts/verify.sh` exits 0. No push without the owner (R-03).

## 9. Commit protocol

- Run the gate first and keep its exit code: `scripts/verify.sh > gate.log 2>&1 && git commit ...`. Never pipe the
  gate into `tail`, which hides the exit code.
- One slice per commit; the message names the slice, the session (`[S-NNN]`) and the rulings it applies.
- End the message with the co-author line the session's harness requires.
- Never commit generated files you did not regenerate, files of another session (ADR-O52), secrets or personal paths
  (the remote is public).
- The pre-commit hook (`.githooks/pre-commit`, enabled by `make hooks`) runs the gate. Never bypass it with `--no-verify`.

## 10. Rollback protocol

Use the table in [docs/how_to_refactor.md](docs/how_to_refactor.md#rollback): `git restore` for uncommitted work,
`git revert` for a local commit, and a branch from the last `checkpoint-*` tag for anything larger. Never force-push,
never rewrite pushed history, never delete a log line. Record every rollback in the session file (status
`reverted`) and in a finding if it taught something.

## 11. Failure protocol

When `scripts/verify.sh` fails:
1. Read the first failure; don't guess from the last line.
2. If your change caused it, fix it at the layer that owns it, or revert (section 10).
3. If a check fails on internally consistent golden content, fix the check; if the golden contradicts its own words
   or the DAG, fix the golden as a recorded deviation, but only under an owner ruling (R-17, ADR-O59).
4. Never weaken a check, skip a test, edit a log or regenerate a golden to make the gate pass.
5. Write what went wrong into the session file and the plan or a finding, then try again.

## 12. Docs protocol

- Every plan, finding, decision, session and render is one file in its folder, made from the folder's `_template.md`,
  starting `# <ID> — <Title>`. The indexes are generated from those files (`make docs`). The verifier refuses a file
  without its required fields, a value outside its legend, a dangling link and a stale index.
- `docs/layer_order.md`, `docs/rules.md`, `docs/plan.md`, `docs/index/*` and the generated blocks in this file and
  `docs/for_the_owner.md` are generated; `docs/reference/` too (`python -m kernel.build_docs`).
- Frozen docs (this file's hand-written sections, `docs/rules.yaml`, the guides, the templates, CODEOWNERS) change only
  with a version bump and a docs-log entry: `python -m kernel.schema_log --log docs record <file> --change changed
  --reason "..." --decided-by owner|owner_default`.
- Reports (`docs/reports/`) are dated records; their items live as findings.

## 13. Schema protocol

- Every `schemas/**/*.schema.json` change bumps its `$id` version and is logged:
  `python -m kernel.schema_log record <file> --change created|changed --reason "..." --decided-by ...`.
- Library cards: `--log library`; drafts stay `status: draft` until the owner approves. Kernel files: `--log kernel`;
  regenerate the kernel with `python -m kernel_extraction.control_inventory`.
- Contracts are JSON Schemas checked by the in-repo validator; no Pydantic (R-15). Shared definitions live once and
  are referenced (ADR-O65).
- Logs are append-only and hash-chained; a file whose bytes differ from its latest entry fails the gate.

## 14. ADR protocol

- An owner ruling becomes `docs/decisions/ADR-<series><n>-<slug>.md` (new rulings continue the `O` series), with
  status `accepted`, the owner's words in Decision, and Supersedes / Superseded By kept consistent on both files.
- An agent proposal is `proposed` until the owner rules; one the owner saw and did not object to is `accepted`,
  Decided By `owner_default` (ADR-O67).
- A ruling that changes a rule bumps `docs/rules.yaml` and cites the ADR. A ruling that changes the layer order needs
  the kernel log and a layer-order version bump.
- Then `make docs`: section 7 and the decisions index update.

## 15. Render protocol

- The owner renders; agents never render or call a paid model API (R-04).
- Before a probe render, its prompt is saved in `docs/render_tests/` and hashed. After it, log
  `docs/renders/R<n>-<slug>.md` bound to that sha256, with the owner's verdict word for word, Claude's frame notes
  apart, and the findings it raises.
- Test the uncertain, build the certain (R-11).

## 16. Tools and commands

| Need | Command |
|---|---|
| The gate | `scripts/verify.sh` (or `make verify`) |
| Golden check | `make golden` (examples byte for byte, golden tests) |
| Regenerate docs | `make docs` (indexes, canonical docs, reference docs, checklists) |
| Graphs | `make graphs` (graft and graphify into the ignored `.graphs/`); `graft --dir .graphs/graft skeleton <file> .`, `graft --dir .graphs/graft callers <symbol> .` |
| Compile | `cinematic compile "<query>" [--genre G] [--until NODE] [--plans DIR] [--packet-out F]` (exit 3: an authored step needs a document) |
| Rebind | `python -m compiler.rebind --write <example>...` after a prompt, library, schema-id or upstream plan edit |
| Rewrite examples | `python -m compiler.examples --write <example>...` then `python -m validators.checklist --write` |
| Log a change | `python -m kernel.schema_log [--log library|kernel|docs] record <file> --change ... --reason ... --decided-by ...` |
| Setup | `mise exec -- uv sync --locked`; `make hooks` |

## 17. Session checklist

- [ ] Read AGENTS.md, the five indexes and docs/plan.md; graphs refreshed
- [ ] `scripts/verify.sh` passed before any change
- [ ] One `next` slice picked; not blocked; its layer confirmed
- [ ] Session file opened with the plan and predictions
- [ ] Fix at the owning layer; schema and data changes logged; break tests added
- [ ] `scripts/verify.sh` and `make golden` pass; predictions reported
- [ ] Backlog, findings, CHANGELOG and session file updated; `make docs` run
- [ ] Self-audit run (`/self-audit`); its verdict, evidence and wrong claims reported to the owner
- [ ] One commit, `[S-NNN]` in the message; nothing pushed without the owner
