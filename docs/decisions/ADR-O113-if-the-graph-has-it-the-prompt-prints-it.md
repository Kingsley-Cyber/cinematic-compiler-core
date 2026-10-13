# ADR-O113 — If the graph has it, the prompt prints it

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
Owner, in chat, 2026-10-13, on the finding that the graphs know more than the prompt says: "The rule: if the graph has
it, the prompt prints it. No exceptions. Every dropped field is a place the renderer guesses. Every guess is a render
failure." Fix it at S17: print every edge graph that reaches the render (temporal, contact, kinematic transitions,
Bartenieff transitions, beat-constraint links); stop thinning the data (camera world position and aim, hold frame
counts: "O47 was a probe artifact", per-limb world points on each key, each pose's description on its line); map and
migrate the graphs to their schemas first ("Map first. Migrate second. Check third."); use graft and graphify for code
navigation.

## Context
R20 failed where the prompt said less than the graphs: measured on its envelope, the prose renderer reads 77 of the
209 fields the graphs hold (validators/graph_reach.py). The graph map (validators/graph_map.py, docs/graph_map.md)
found the graphs conform to their schemas: 33 groups, every schema section closed, one optional field never filled.

## Consequences
- S17 prints every graph field in the Master Template's own sections (STACKED_GRAPHS refuses any other section);
  validators/graph_reach.py measures it and the gate holds the count so it only rises.
- O47's "body holds are never printed in frames" is superseded: the prose prints hold frame counts. O47's other
  clause, the quarter-turn angles kept out of a turn's lines (probes R13 against R18: an angle list rendered two
  flips), is a render result, not a probe artifact; it stands until the owner rules on it.
- A card's text that names a prop (capabilities, description) is printed only with the hands each beat declares
  (next actions 1, R20's kunai).

## Alternatives Considered
- Print only what a renderer is known to use: the owner's rule is the opposite.

## Supersedes
- ADR-O47 (its clause on frame counts)

## Superseded By
—

## Related
- ADR-O47
- docs/reports/2026-10-13-render-20-next-actions.md
