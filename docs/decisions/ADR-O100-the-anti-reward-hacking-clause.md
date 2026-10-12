# ADR-O100 — The anti-reward-hacking clause

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-11: pasted the anti-reward-hacking clause and said "in addtiion add this clause in claude.md and
agent.md". The clause, word for word, is in CLAUDE.md and AGENTS.md section 18. Its opening: "The objective is to
correctly implement the requested behavior, not merely produce a passing score."

## Context
The principal review (S-035) found slices that passed checks by exemptions, re-blocks and moved pins rather than by
fixing causes (F-074 to F-077).

## Consequences
- Existing tests, assertions, fixtures, expected outputs and verification code change only on the owner's explicit ask;
  none is deleted, skipped or weakened to pass.
- When a specification and a test conflict, the work stops and the exact conflict is reported.
- How a recorded R-33 deviation counts against rule 1 is F-119; until the owner answers, a test changes only where a
  ruling explicitly asks for the record (as O88 does), otherwise the work stops and reports.

## Alternatives Considered
- —

## Supersedes
—

## Superseded By
—

## Related
- ADR-O99
- R-33
- F-119
