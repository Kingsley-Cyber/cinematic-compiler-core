# ADR-O104 — "Genuine airborne or prop-moving misses" are contacts measured between keys or samples

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner_default

## Scope
L4c

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-039): CONTACT_WORLD exempts a miss only when the contact's
instant falls between the actor's keys or between the prop's samples, so that the measured point is interpolated, and
the actor is airborne or the prop is moving there. A contact measured at an exact instant (a key, and a sample, at the
contact's own time) is never exempt, airborne, turning or moving; a turn alone never exempts.

## Context
ADR-O89 (owner): "A miss at an exact instant is not an artefact. Re-block B's throw, the palm on the log, and the vault
hand. Only exempt genuine airborne or prop-moving misses." Every contact CONTACT_WORLD measures today has a key and a
sample at its instant (solver/contact_world.py), so none is exempt until contacts between keys are measured (RV-14).

## Consequences
- solver/contact_world.py `artefact` reads an `interpolated` flag; every measured miss today is either met, re-blocked
  on its repo-authored side, or listed with its reason when both sides are the owner's source (ADR-O83 point 2).

## Alternatives Considered
- Keep exempting airborne or moving contacts at exact instants: what O89 rules out.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O89
- ADR-O83
- F-075
