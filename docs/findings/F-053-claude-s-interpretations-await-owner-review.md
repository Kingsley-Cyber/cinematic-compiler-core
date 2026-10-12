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
in force at its start or first set inside it, ignoring one set before the prop's last hold. Added in S-011 (M9-05,
solver/euler_solver.py): a flip or cartwheel's inversion is read on linear Euler interpolation between its keys; O38's
landing key for the wizard's dodge_flip is a new hold beat b14 at 9.80 (land_guard shortened to 9.40-9.80 and
continuing the flip), not the 9.40 apex key turned into a landing. Added in S-013 (M9-07a, library/combat_verbs.yaml
and planner/dynamic_beat_validator.py): strike joins O22's nine verbs; which contact type takes which verb; a throw
leaves its prop moving (so a touch may throw); which of the reference fight's contacts carry a verb. Added in S-015
(M9-08a, planner/dynamic_beat_validator.py): SURFACE_HEIGHT puts the root between a supporting top (less 0.05 m) and
1.2 m above it, and reads a surface's top from its world card's geometry text. Added in S-016 (M9-08b,
renderers/prose_renderer.py): an entrance is a first line in the air and a first foot support on a raised top; V6's
"not visible before 0.20" and "never stands on the ground" are left out.
Added in S-019: rule R-34 scoped to whole-body checks (ADR-O76 keeps the owner's wider sentence). Added in S-020
(solver/shape_direction.py): SHAPE_DIRECTION's thresholds and span; nine rewrites, not twelve (three are flights). Added in S-021
(compiler/passes/derived/p11_kinematic.py): MOMENTUM_MISSING's arc and 0.3 m; the hang said once per span in RULES.
Added in S-022 (solver/euler_solver.py): a turn that stays on the ground (a tip) needs no launch; the takeoff
effects of the wizard's two flips sit on the beats before them (run_in, the slicing bolt).
Added in S-024 (planner/dynamic_beat_validator.py): PROP_SUPPORT reads a top by height alone and a card's worn
state as the wearer's support; the pellet bursts as it lands at 4.0 (the owner's words: fall after bursting).
Added in S-026 (solver/quaternion.py): a face within FACE_LEVEL 0.2 of vertical keeps the summed heading.

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
