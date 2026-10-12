# ADR-O102 — When a test may change: only where a ruling or the plan's intent moves the data it pins

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner_default

## Scope
all

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-037), answering F-119:
1. A test, fixture or expected output changes only where an owner ruling or the plan's intent moves the data it pins,
   and each such change is a typed, recorded deviation (in the golden test or the session file) that cites the ruling.
2. A test never changes so that a failing check passes, and none is deleted, skipped or weakened (AGENTS.md section 18,
   rules 1-3); a failing test is diagnosed and the implementation fixed.
3. A ruling that asks for its changes to be recorded as R-33 deviations (as O88 does) is the owner's explicit ask; a pin
   holding data a ruling moves (a root height the ruling raised) changes with that ruling, recorded.
4. R-33 stands inside this bound: a slice whose own new check fails on the examples rewrites the examples, never the
   check, each rewrite recorded.

## Context
The sources: ADR-O100's clause, rule 1 ("Treat existing tests ... as immutable unless the user explicitly asks to
change them") and rule 5 ("If the specification and tests conflict, stop and report the exact conflict"); ADR-O101
(the owner: "you can change things but you are working to intentioally implement fully the soul of the plan and ensure
it works, fully implementation and migrations"); ADR-O75 / R-33 ("A slice may rewrite the examples so they pass its own
new check, as recorded deviations (the golden test and the session file)"); docs/prompts/finish.md section 3.

## Consequences
- F-119 resolved. Every slice of this run records each test change with its ruling in the session file's Decisions.

## Alternatives Considered
- Stop and report every pin a ruling moves: against O101's standing instruction to finish the repo.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O100
- ADR-O101
- ADR-O75
- F-119
