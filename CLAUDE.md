# cinematic-compiler: Claude Code context

Read AGENTS.md first; it owns the working protocol, schema control and authority rules.
Then read kernel/layer_order.yaml and docs/layer_dependency.md.

Navigate with graft/graphify before reading files. Log every schema change with
`python -m kernel.schema_log record`. Build one layer per slice, and end each slice with
tests green, the schema log verified and `harness checkpoint`.
