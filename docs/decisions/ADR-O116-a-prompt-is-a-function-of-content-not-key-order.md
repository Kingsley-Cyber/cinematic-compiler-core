# ADR-O116 — A prompt is a function of its envelope's content, not its key order; a control layer of six checks

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
Owner, in chat, 2026-10-13, on the joint-order bug S-119 found: declare the canonical joint order in the schema; every
writer writes it and every reader reads it; a validator JOINTS_IN_CANONICAL_ORDER; a test that "the same scene renders
identically whether loaded from disk or held in memory", run on R20 ("the hashes must match"). And a control layer at
tests/test_control_validation.py: schema alignment, transition validity, interdependency integrity, canonical order,
determinism, graph conformance, on every commit.

## Context
The stored envelope sorts every key (kernel/canonical.py); the pipeline's own envelope keeps the order each layer wrote.
S17's LBN prompt took the joint order from the dict, so the same envelope gave one prompt from memory and another from
disk (R20: b1dd621f in memory, 2a666b26 from disk before S-119).

## Consequences
- The canonical joint order is the kernel skeleton key; the motion_graph schema (1.4) declares it; S13 writes it; the
  renderers share one constant, held equal to the kernel's.
- The serializer keeps sorting keys alphabetically: every hash (envelopes, packets, the authored documents bound to
  them, the hash logs) is taken over that form. Order-free reading is enforced instead: DETERMINISM renders every
  example with every object's key order reversed, and from memory against from disk, and requires the same bytes.
- tests/test_control_validation.py runs the six checks in the gate.

## Alternatives Considered
- A serializer that writes canonical joint order: it would re-hash every envelope and packet and orphan every committed
  authored document, and would still leave every other object's order to chance; a reader that never takes order from
  a dict fixes the class.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O115
