# Ownership map

<!-- docs-version: 1.1 -->

Who decides, who edits and what checks each part of the repo. "Owner" is Kingsley; "agent" is any coding agent
following AGENTS.md; "generator" means a command writes the file and nobody edits it by hand.

| Path | Decides | Edits | Checked by |
|---|---|---|---|
| `AGENTS.md` (hand-written sections) | owner | agent, with a docs-version bump | docs log (`--log docs`) |
| `AGENTS.md` and `docs/for_the_owner.md` generated blocks | — | generator (`make docs`) | `python -m kernel.docs_plane` |
| `docs/rules.yaml` | owner (each rule cites an accepted ADR) | agent, with a version bump | docs log; docs plane (rule sources) |
| `docs/decisions/` | owner (`accepted` only by the owner; `owner_default` when a proposal is not objected to) | agent writes the file | docs plane (fields, chains) |
| `docs/findings/`, `docs/sessions/` | agent | agent | docs plane (fields, links, F1-F15 vs the checklist) |
| `docs/renders/` | owner (verdict, word for word) | agent logs it | docs plane (fields) |
| `docs/plans/*.md`, `docs/plans/backlog.yaml` | owner (order and approvals) | agent | docs plane (backlog codes vs the code) |
| `docs/index/`, `docs/layer_order.md`, `docs/rules.md`, `docs/plan.md` | — | generator (`make docs`) | docs plane (staleness) |
| `docs/reference/` | — | generator (`python -m kernel.build_docs`) | `kernel.build_docs --check` |
| `docs/*/_template.md`, `docs/how_to_refactor.md`, `docs/ownership.md`, `docs/versioning.md`, `docs/for_the_owner.md` | owner | agent, with a docs-version bump | docs log |
| `docs/sources/` | owner (verbatim sources) | nobody | review |
| `docs/render_tests/` | owner (probe prompts bound by sha256) | agent writes before the render; nobody after | sha256 in each render file |
| `docs/bootstrap/README.md` | owner | agent, with a docs-version bump | docs log |
| `docs/bootstrap/state.md` | — | generator (`make docs`) | docs plane (staleness) |
| `docs/bootstrap/environment.md`, `working_agreements.md`, `lessons.md` | owner (agreements) | agent; lessons append-only | docs plane (links) |
| `docs/reports/` | — | records; not edited after the day they describe | review |
| `kernel/layer_order.yaml`, `kernel/*.yaml`, `kernel/sources/` | owner (ADR) | agent, with a version bump | kernel log (`--log kernel`) |
| `schemas/` | owner decisions | agent, `$id` version bump | schema log; `kernel.build_ir_schema --check` |
| `library/` | owner (draft to approved) | agent drafts | library log |
| `examples/*/plans/` | owner (deviations) | agent, in-session from a sealed packet | packet hashes (`compiler.rebind`); golden test |
| `examples/*` outputs (`envelope.json`, `render.txt`, `prose_*.txt`, `checklist.md`) | — | generator (`compiler.examples --write`, `validators.checklist --write`) | byte check in the gate |
| `compiler/`, `planner/`, `solver/`, `validators/`, `renderers/`, `kernel/*.py`, `cli/` | agent (within the rules) | agent | ruff, pytest, the gate |
| `tests/` | agent; golden deviation constants need an owner ADR | agent | pytest |
| `scripts/`, `Makefile`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `.githooks/` | owner approves changes to the gate | agent | the gate itself |
| `.github/` (workflows, CODEOWNERS) | owner | agent | CI; CODEOWNERS review on GitHub |
| `~/Documents/cinematic-compiler-core` uncommitted files of another session | owner | nobody (O52) | finding F-056 |

A change outside this map is a finding of type `question` first.
