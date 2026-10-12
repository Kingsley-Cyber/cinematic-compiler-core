# F-092 — Two possession models disagree, and two holders of one prop are never refused

<!-- docs-version: 1.0 -->

## Type
bug

## Severity
medium

## Layer
L1.1

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- planner/dynamic_beat_validator.py `holds()` keys a hold by prop and ends it on any release; compiler/passes/mandatory/p07_contact.py `lifecycle` tracks each hand; a simulated handoff and a two-handed hold disagree (the principal review, S-035 (docs/prompts/principal_review.md))
- `holds()` feeds PROP_KINEMATICS, PROP_SUPPORT and the WHERE line (renderers/prop_samples.py)
- PROP_TWO_HOLDERS is the gap on mandatory row C5 with no slice
- RV-10 (S-051): a possess of the kunai by B's torso at 8.5 (the blade lodged) replaced A's open hold in `holds()`
  and dropped A as holder from 8.0, so the lodged blade is a touch plus the embedded state until one model
  holds a prop in a hand and lodged in a body at once

## Description
A disarm, catch or handoff would be judged by the wrong model, and nothing stops a prop being in two hands at once while every prompt says it never is.

## Impact
Latent today; wrong as soon as a scene hands a prop over.

## Proposed Fix
Backlog RV-17: one possession model shared by S04 and S07; PROP_TWO_HOLDERS at S07.

## Owner Ruling
none needed

## Related
- PLAN-007

## Resolution
Open.
