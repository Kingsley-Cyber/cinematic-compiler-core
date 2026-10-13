# ADR-O114 — The root is printed as position data; the phrase "root exact" is retired

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
Owner, in chat, 2026-10-13, on the conflict between O3 and O113: "O113 wins for the data. O3 wins for the phrasing.
Print the root as 'position: [x, y, z]', not 'root exact'. Update O3: the root position is printed as data; the rigid
'root exact' phrasing is retired." And: "coordinates printed, rigid language retired."

## Context
O3 kept the kernel rule "<label> root exact" out of the prose. O113 prints every field the graph holds. Before this,
the pure staff printed no root at all and the mixed modes printed it only on strike, first and last lines.

## Consequences
- Every staff and in-between line, in every prose mode, prints its root once: as `position: [x, y, z]`, or inside the
  Root block where the mode prints one. EULER_MODE_MISMATCH refuses a line with neither, with both, or with numbers
  that differ from the S13 key.
- The prose never says "root exact" (ROOT_EXACT_PRESENT unchanged); the rule's line stays out of [RULES].
- LBN-2.4 (render.txt) keeps the kernel rule as it is.

## Alternatives Considered
- Print "root exact" with the numbers: the owner retired the phrasing.

## Supersedes
- ADR-O3 (its clause that leaves the root out of the prose: the phrase stays out, the data is printed)

## Superseded By
—

## Related
- ADR-O3
- ADR-O113
