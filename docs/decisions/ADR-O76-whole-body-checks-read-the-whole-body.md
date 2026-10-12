# ADR-O76 — Whole-body checks read the whole motion graph

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c, L5

## Decision
Owner, in chat, 2026-10-11, on the lean reading in ADR-O73's measure: "The lean check must read the full motion
graph: joints, rotation, support, world points. If the body is airborne and rotating (support=none, rotation !=
null), skip the lean check — it's a flight artifact, not a contradiction. Otherwise, measure spine lean relative to
root, not relative to vertical. Add a rule to AGENTS.md: 'Every check reads the full motion graph, not a single
joint.' Verify: flips pass, grounded leans still fail when they should." and "Find every check that reads a single
joint. Fix them all."

## Context
The owner read S-017's prototype (the lean from the spine bone during A's backflip). Agent notes, for owner
review: the prototype already read the lean relative to the root (the spine in the pelvis frame); world points do
not exist until M9-06 (forward kinematics, ADR-O72). Rule R-34 is worded for checks that judge a whole-body
quality, because per-joint checks (JOINT_LIMIT, a knee's fold, a limb's direction word) read one joint by design;
the audit of every single-joint read is in session S-020.

## Consequences
- Rule R-34 (rules 3.0).
- SHAPE_DIRECTION (M9-09a) skips an airborne turn (no support, a declared turn) and reads the root, the support, the
  spine and the limbs.

## Alternatives Considered
- R-34 in the owner's exact words for every check (it would forbid JOINT_LIMIT's per-joint reading).

## Supersedes
—

## Superseded By
—

## Related
- PLAN-003
