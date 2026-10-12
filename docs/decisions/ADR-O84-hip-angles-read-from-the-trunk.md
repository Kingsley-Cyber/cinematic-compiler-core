# ADR-O84 — Hip angles are read from the trunk, in every key

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-11

## Decided By
owner

## Scope
L4c

## Decision
Owner, in chat, 2026-10-11: "R-20 confirmed. Trunk, everywhere. Forward kinematics reads hip angles from the trunk
(the spine) in every key, in every genre, in every example. Rewrite the 42 repo-authored leaning keys so their hip
numbers read from the trunk. Preserve their bodies — the position doesn't move. The 47 printed leg words that change
are expected. Record each as an R-33 deviation. The authoring rule changes for new keys: all new keys read hip angles
from the trunk. Update AGENTS.md and the authoring guide with the new rule. [...] This gives us one convention, the
source's, for UGC and elite animation consistency."

## Context
M9-06c (S-029): no leg length grounds the source's supported A rows while the legs hang from the root (4 of 17 grounded
feet within 0.15 m at the best scale); hung from the trunk (root, then Sp), one leg scale grounds 14 of 17. The repo's
authoring prompt had put leans in Sp with the legs planted (the pelvis reading).

## Consequences
- `solver/forward_kinematics.py` hangs the legs from the trunk: root -> Sp -> (NK -> HD, LA -> LFA, RA -> RFA,
  LUL -> LL, RUL -> RL).
- The repo-authored keys that lean through Sp have their hip rotations re-expressed (R_hip' = R_Sp^-1 R_hip), so
  every point of their bodies stays where it was; the printed leg words that change are R-33 deviations.
- Rule R-35; `planner/prompts/euler_solving.txt` tells authors to read hip angles from the trunk.

## Alternatives Considered
- The source's rows from the trunk, the repo's keys from the pelvis (two conventions): not chosen.
- The pelvis reading, the source's foot misses kept as exceptions: not chosen.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O7
- ADR-O72
- ADR-O82
- ADR-Q6
- R-20
- R-33
- F-070
