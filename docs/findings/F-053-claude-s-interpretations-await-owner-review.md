# F-053 — Claude's interpretations await owner review

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
docs/reports/2026-10-11-renders-and-dag-adherence.md section 6

## Description
Limb levels (mid within 45 degrees), what counts as a strike, 'steps alternating', the Euler blocks per mode, the joint-limit mapping onto Q6 axes and the anime +30 widening, the 2 m prop reach and 0.25 m gravity tolerance, and the substitution exemption are Claude's interpretations, each labelled where it lives. Added in S-009 (M9-04a,
planner/dynamic_beat_validator.py): a free prop moving into a contact must carry a pre/post sample pair there, and the
velocity into a pre sample is held to gravity within 0.25 m/s. Added in S-010 (M9-04b, renderers/prop_samples.py):
the WHERE line is printed in the prose only (LBN-2.4's prop rows unchanged), and a resting span names the S06 location
in force at its start or first set inside it, ignoring one set before the prop's last hold.

## Impact
Waits on the owner.

## Proposed Fix
Owner review of each.

## Owner Ruling
none yet

## Related
- PLAN-001

## Resolution
Open.
