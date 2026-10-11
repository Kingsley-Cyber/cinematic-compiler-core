# F-061 — A start-of-beat release prints its holder change at the beat's end

<!-- docs-version: 1.0 -->

## Type
drift

## Severity
low

## Layer
L2.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
examples/reference_fight/prose_mixed.txt, kunai state machine ("2.00 released by B R hand" ... "2.50 holder B -> none"); session S-003

## Description
S06 commits a beat's effects at the beat's end. Since M9-02 a throw releases at its pose (`at: start`, O23), so the
kunai's track prints the release at 2.00 and the holder change at 2.50. S07 accepts this (at the beat's first instant
the prop is still in the hand), but the prompt shows the holder half a second after the release.

## Impact
A reader may think B holds the kunai until 2.50; the model saw no render of it yet.

## Proposed Fix
S06 commits a holder change at the time of the contact that causes it (the release), not at the beat's end; a
derivation change at L2.1 with its own break test.

## Owner Ruling
none needed (follows O23)

## Related
- ADR-O23
- backlog M9-02
- PLAN-003

## Resolution
Open.
