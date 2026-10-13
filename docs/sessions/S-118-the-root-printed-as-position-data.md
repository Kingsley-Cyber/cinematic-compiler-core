# S-118 — The root printed as position data on every line; "root exact" retired (ADR-O114)

<!-- docs-version: 3.0 -->

## Date
2026-10-13

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
ADR-O114 (owner): O113 for the data, O3 for the phrasing: print the root as "position: [x, y, z]"

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-118]

## Plan
1. A staff or in-between line with no Root block prints `position: [x, y, z]` from its S13 key, the pure staff too;
   the movement language explains it.
2. EULER_MODE_MISMATCH refuses a line with neither, with both, or with numbers that differ from the key.
3. "root exact" stays out of the prose (ROOT_EXACT_PRESENT); LBN-2.4 keeps it.

Predictions, made before the change (04:40 by the clock):
1. Only the prose changes; the envelopes' graphs and reach stay the same (the position is already read).
2. One test that compares the pure staff's lines to the other modes' lines breaks.

## Decisions
- D1 — The Root block keeps its name where a mode prints it (the LBN instances' format, ADR-S7); every other line
  prints `position:`, so each line carries the root once. Level: the owner's ruling.
- D2 — The planted break for a missing position is its own test (one break per code in the list). Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| graft used | PASS | graft grep of ROOT_EXACT, omitted and "Root " before the edits |
| Tests | PASS | one line in tests/test_prose_render.py compares lines without the position; two new assertions |

## Duration
from 04:40 to 05:10

## Changes
- renderers/prose_renderer.py; validators/prompt_validator.py; tests/test_prose_render.py,
  tests/test_dag_conformance.py; examples' prompts, envelopes and checklists; ADR-O114, ADR-O3

## Verification
- Prediction 1 held: reach 146, 134, 120, 171 unchanged; no "root exact" in any prose file.
- Prediction 2 held: test_euler_blocks_sit_on_the_lines_each_mode_names (the mixed line no longer starts with the pure
  staff's whole line).
