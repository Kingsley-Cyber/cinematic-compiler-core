# F-151 — No check keeps a body out of a prop: props have no extent

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L4c

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- RV-49 (S-049) checks bodies against bodies only (solver/body_overlap.py); a prop is a point (its samples), with no
  length or radius in its card
- F-144's second item: about 4.19 s, B's legs cross the falling substitution log's line 0.07 m off its centre, between
  B's keys and the log's samples

## Description
A body may pass through a prop, and a point between keys or samples is not checked at all.

## Impact
The model may be told to draw a leg through the falling log.

## Proposed Fix
Backlog RV-54: each prop card gives the prop an extent (a capsule: the log's length and radius, a blade's), S13 refuses
a body's capsule through a prop at each sample instant, and with RV-47 between samples; the poses that fail re-blocked.

## Owner Ruling
none needed (R-18)

## Related
- PLAN-007
- F-144
- F-131

## Resolution
Open.
