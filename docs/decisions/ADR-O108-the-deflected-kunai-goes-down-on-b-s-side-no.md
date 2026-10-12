# ADR-O108 — The deflected kunai goes down to the ground on B's side, not at B

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner_default

## Scope
L6

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-046), for F-122: after A's foot deflects it at 2.5, the kunai
travels down and back along -Z, to the ground on B's side of the fight, and is not aimed at B. The prompts print its
direction ("moving down along -Z") and name no goal; a prop track says "toward X" only where the prop's path reaches X.

## Context
The source (kernel/sources/lbn-2.3-adv.txt) says both: A's 2.5 row, "kunai REVERSES direction from +Z (toward A) to -Z
and downward (toward B and ground)"; B's track, "kunai reverses toward B and ground"; the kunai track, "kunai arcs down
toward B and ground ... this is a foot deflection NOT toward B"; the rules, "FOOT DEFLECT KINDS: kunai REVERSES from +Z
to -Z and downward at 2.5,kunai STAYS IN FRAME,NOT toward B". Read together: toward B's side and the ground, not at B. Since
S-043 the prompts printed "moving down toward B" beside "NOT toward B" (F-122); ADR-O77 fixes the reversal to -Z.

## Consequences
- renderers/prop_samples.py names a goal only where the prop's free flight passes within 0.3 m of that performer's body
  and closes on it; PROMPT_CONTRADICTION refuses a track that says "toward X" where the prompt says "NOT toward X".
- S-043's, F-075's and the CHANGELOG's "as the source's rule says" are corrected.

## Alternatives Considered
- "toward B" (the B and kunai tracks' first half): against the rule's "NOT toward B" printed in the same prompt.
- Re-aim the deflect away from B's side: against "toward B and ground" and O77's v_post.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O77
- ADR-O105
- F-122
