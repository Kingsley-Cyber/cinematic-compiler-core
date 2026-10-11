# AGENTS.md — cinematic-compiler

Start with `HANDOFF.md` (state, decisions, open questions), then `docs/plans/MASTER_PLAN.md`,
`docs/graph_types.md`, `docs/reference/` (generated: DAG and dependencies, every schema field by field, data files,
code imports) and `kernel/layer_order.yaml` (the layer DAG and write ownership).

## Gate
`scripts/check.sh` must pass before every commit: ruff, pytest, the three hash logs, the two generated files
(`schemas/cinematic_ir.schema.json`, `kernel/invariants.yaml`), the examples (byte-for-byte) and the reference docs.
After changing the DAG, a schema, a library file or imports, regenerate the docs: `python -m kernel.build_docs`.
One commit per step.

## Schema control (owner rule 2026-10-10)
- Every `schemas/**/*.schema.json` change is logged: `python -m kernel.schema_log record <file> --change ... --reason ... --decided-by ...`.
- Library cards (`library/**/*.yaml`): `--log library`; drafts stay `status: draft` until the owner approves.
- Kernel files (`kernel/sources/*.txt`, `kernel/kernel_scope.yaml`, `kernel/invariants.yaml`, `kernel/knowledge_map.yaml`): `--log kernel`;
  regenerate the kernel with `python -m kernel_extraction.control_inventory`.
- Logs are append-only and hash-chained; a file whose bytes differ from its latest entry fails the gate.
- `kernel/layer_order.yaml` is the single source for steps, edges and write ownership. A pass writes only its paths.

## Working rules
- One step per slice. No paid model API and no renders; authored steps are written in-session from a hash-bound packet.
- Ask the owner only where the plan is silent or contradicts itself; name the contradiction in one line.
- Navigate with graft and graphify before reading files (caches in ignored `.graphs/`):
  `DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore`,
  `graft --dir .graphs/graft skeleton <file> .`, `graphify extract . --code-only --no-cluster --out .graphs/graphify`.
- Do not edit `kernel/layer_order.yaml` or a logged file to make work easier; a real conflict goes to the owner.
