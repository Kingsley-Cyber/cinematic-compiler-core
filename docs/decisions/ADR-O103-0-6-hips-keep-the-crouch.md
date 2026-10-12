# ADR-O103 — At 0.6 A's hips keep the crouch: O88's flip there would break its own row

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
Answered from the sources under ADR-O101 (finish run 1, S-038): of O88's 21 limb flips, the two at 0.6 (both hips,
the source's "leg back mid") are not made. Their numbers (-135, a deep hip flexion under Q6 and O7) stay; the other 19
flips and all 13 head flips are made.

## Context
The source's 0.6 row says both "L: ... leg back mid bent7 ... R: ... leg back mid bent7" and "LANDING ON PILLAR TOP,
both feet on pillar top y=7.2, deep compressed crouch" (kernel/sources/lbn-2.3-adv.txt). Flipping both hips to "back"
(+60 at the anime limit, O11) under the trunk reading (O84) points the thighs up: forward kinematics puts the soles at
y 9.27, 1.27 m over the pillar's top (y 8) and above the pelvis (8.71). The row's own words then contradict each other
and the landing (CONTACT_WORLD on b01_c1, b01_c2) fails. The finish run's order of sources (docs/prompts/finish.md
section 2): the owner's newest words (O88: "Follow the source's words") apply to every word of the row, and these two
pull apart; the fight working (a landing crouch on the pillar top) and the row's support words decide.

## Consequences
- A's 0.6 legs still print "forward-high", against the source's "leg back mid": the two disagreements left out of 88.
- The golden test records the 19 flips and these two exceptions with O88 and this ADR.

## Alternatives Considered
- Flip them anyway: the soles leave the pillar top and the thighs point up.
- Print the source's word over numbers that say otherwise: a prompt that contradicts its own pose.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O88
- ADR-O101
- F-080
