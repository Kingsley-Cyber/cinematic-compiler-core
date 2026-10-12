# ADR-O107 — O102 confirmed; the finish run pushes each slice and continues

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-12, while the second principal review (S-045) was reporting: "O102 confirmed, keep pushing,
continue the finish run".

## Context
The second principal review found that finish run 1 changed tests under ADR-O102, its own owner_default answer to
F-119, though ADR-O100's interim rule had left that answer to the owner, and that it pushed each slice while R-03 and
R-30 still read "no push without the owner" (the rules-and-shortcuts and the decisions-and-findings reviewers).

## Consequences
- ADR-O102 is the owner's ruling from 2026-10-12: a test or expected output changes where a ruling or the plan's intent
  moves the data it pins, each change a recorded deviation citing it. F-119 is resolved and ADR-O100's interim rule
  (its third consequence) is superseded.
- A finish run (ADR-O101) pushes each slice that clears its gate, its self-audit and the hygiene scan; R-03, R-06 and
  R-30 say so in rules 5.0, R-06 with one limit: a question whose answer would set aside an owner ruling or an owner
  invariant waits for the owner.
- The run continues. Its answers taken under finish.md section 4 stay owner_default ADRs for the owner to confirm; the
  owner saw ADR-O102 to O106 listed for confirmation and objected to none.

## Alternatives Considered
- Narrow O102 to "only where an owner ruling asks for the record" (the reviewers' option): not chosen by the owner.
- Stop the run until the owner answers each review question: not chosen.

## Supersedes
- ADR-O100 (its third consequence, the interim rule)

## Superseded By
—

## Related
- ADR-O100
- ADR-O101
- ADR-O102
- F-119
- PLAN-007
