# ADR-O115 — The graphs turn as one wheel: data-flow contract, cross-graph consistency, end-to-end tracer

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-13

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-13: "The graphs need to be a cog wheel, and right now there's no validation that they turn."
Three checks: a data-flow contract per layer (reads, writes, validates, passes_downstream; "the validator confirms the
layer reads what it says it reads and writes what it says it writes"); cross-graph consistency ("every beat references
an entity that exists, every contact references a body part declared in the beat, every constraint binds a beat that
exists"); an end-to-end tracer (lost, invented and orphaned fields). Run on the R20 envelope first; fix the phantom
inputs first ("those are where the renderer guesses"); "a layer that fails the data-flow contract fails the gate."

## Context
The checks measured each graph alone. Nothing proved that what one layer writes is what the next reads.

## Consequences
- kernel/data_flow.yaml declares each layer's flow; validators/data_flow.py measures it by re-running every layer on
  the envelope before it with every key it touches tracked, and tests/test_data_flow.py fails the gate on any
  difference, on a phantom read, or on a layer that does not reproduce its own output from its own input.
- validators/cross_graph.py checks every reference between graphs (GRAPH_REFERENCE), in the gate on every example.
- A change to what a layer reads or writes regenerates the contract (`python -m validators.data_flow
  --write-contract`) and logs it in kernel/kernel_log.jsonl, so the change is deliberate and recorded.

## Alternatives Considered
- Declaring the reads by hand: they would drift from the code; measured and then held, they cannot.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O113
- docs/reports/2026-10-13-data-flow.md
