# ADR-O89 — A miss at an exact instant is not a measurement artefact

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11, answering the principal review's question 2 (S-035): "A miss at an exact instant is not an artefact. Re-block B's throw, the palm on the log, and the vault hand. Only exempt genuine airborne or prop-moving misses."

## Context
F-075: CONTACT_WORLD exempted any contact whose actor was airborne or turning or whose prop had any velocity, though the key, the sample and the contact share one instant (the agent's definition, S-027 D6, S-030).

## Consequences
- Backlog RV-02: no exemption at an exact instant; B's throw at 5.5, B's palm on the log at 4.0 and the vault hand at 2.0 are re-blocked; the agent reads "genuine" as a contact measured between keys or samples (an interpolated instant), recorded for the owner to confirm.
- The source's exact-instant misses have their repo-authored side moved, or are listed as exceptions with reasons (ADR-O83 point 2). O83 stands; its point 3 now exempts only genuine airborne or prop-moving misses.

## Alternatives Considered
- Keep the instant-based artefacts: not chosen.

## Supersedes
—

## Superseded By
—

## Related
- F-075
- F-076
- ADR-O83
- PLAN-007
