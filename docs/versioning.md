# Version bump rules

<!-- docs-version: 1.0 -->

Every versioned thing, what its version means and when it moves. A change without its bump fails the gate where a
log guards the file.

| What | Where | Bump | Guard |
|---|---|---|---|
| Package | `pyproject.toml` `version` (semver) | MAJOR: the envelope contract or the layer order breaks old envelopes. MINOR: a milestone ends (new steps or checks). PATCH: a fix release. | CHANGELOG heading; tag `checkpoint-<date>-<slug>` |
| Layer order | `kernel/layer_order.yaml` `version` | +0.1 for any change; only with an accepted ADR | kernel log; every envelope records it |
| Envelope | `kernel/layer_order.yaml` `envelope` (MGRAPH-x.y) | with the IR schema's major change | `kernel.build_ir_schema --check` |
| Schema | the `$id` version of each `schemas/**/*.schema.json` | minor: additive field; major: a field removed or its meaning changed | schema log |
| Library card | `card_version` (+1 on a content change); `status` draft → approved only by the owner | | library log |
| Kernel files | `version` in each kernel YAML | +1 or +0.1 on a change | kernel log |
| Frozen docs | `docs-version` marker (Markdown), `version` (docs/rules.yaml) | +0.1 for wording; +1.0 for a protocol or rule change | docs log: the gate refuses a changed file whose log entry repeats the previous version |
| Backlog | `docs/plans/backlog.yaml` `version` | +1 when the build order changes (not for status changes) | docs plane |
| Artifacts | none; each plan, finding, ADR, session or render file carries its own status and dates | | docs plane |

## CHANGELOG

Every commit that changes behaviour, a contract or a frozen doc adds a line under **Unreleased** in
[CHANGELOG.md](../CHANGELOG.md). When a milestone ends, **Unreleased** becomes a version heading (the package version)
and the commit is tagged `checkpoint-<date>-<slug>`.
