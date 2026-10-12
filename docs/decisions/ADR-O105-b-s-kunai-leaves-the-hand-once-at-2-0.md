# ADR-O105 — B's kunai leaves the hand once, at the 2.0 throw

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner_default

## Scope
L1.1

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-043), for F-108: B's kunai leaves B's hand once, at 2.0, the
throw at A in mid-descent. The source's 0.5 line ("releases kunai toward A,right arm extends forward") reads as the arm
extending in the windup; the kunai stays in B's right hand until 2.0, as the repo has held it since O23.

## Context
The source (kernel/sources/lbn-2.3-adv.txt, line 1, B track and kunai track) gives one kunai two releases: "0.5
releases kunai toward A,right arm extends forward" with "0.5 B hand->air toward A p[0,1.5,4.3] v[0,0.4,-4.5] moving
toward A along -Z", and "2.0 throws kunai upward at A mid-descent". Everything else names one throw, at 2.0: the rules
("B THROWS KUNAI at 2.0 toward A"), the camera ("2.0 tracking kunai thrown upward by B toward A"), A's own 2.0 row ("B
throws kunai upward at A mid-descent, kunai arrives from below at A"), and B's Laban line ("wait with kunai,throw
kunai,brace,..."). The 0.5 velocity runs along -Z, away from the pillar where A stands at 0.5, so a kunai released then
could not reach A; the source's own negative says "no duplicated kunai". ADR-O23 already puts the throw at its pose,
2.0.

## Consequences
- The kunai's release is measured at B's right hand at 2.0 (RV-02b); B's 0.5 line stays a windup in B's track.
- F-108's question is answered, so RV-33 (B's track follows the source) is unblocked.

## Alternatives Considered
- A release at 0.5 and a second kunai at 2.0: against "no duplicated kunai" and the single throw every other line names.
- A release at 0.5 caught back before 2.0: no line says so.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O23
- ADR-O77
- F-108
- PLAN-007
