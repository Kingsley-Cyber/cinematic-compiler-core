# cinematic-compiler

Compiles a scene request into a validated movement-graph envelope (MGRAPH-1.1) and then into
video-model prompts, layer by layer (L0 intent → L6.5 post-generation).

- Layer DAG: `kernel/layer_order.yaml`; explanation and open owner decisions: `docs/layer_dependency.md`.
- Envelope schema: `schemas/cinematic_ir.schema.json` (generated; change log `schemas/schema_log.jsonl`).
- Working protocol, schema control and graph navigation: `AGENTS.md`.

```bash
mise exec -- uv sync --locked
mise exec -- uv run --locked pytest -q
mise exec -- uv run --locked python -m kernel.schema_log verify
```

Status: skeleton, DAG check, S01 (intent parser) and S02 (cards-only query expander). Try it:

```bash
mise exec -- uv run --locked python -m planner.intent_parser "10s anime fight, 24fps, moonlit bamboo courtyard"
mise exec -- uv run --locked python -m planner.query_expander "wizard vs superman variant, castle"
```
