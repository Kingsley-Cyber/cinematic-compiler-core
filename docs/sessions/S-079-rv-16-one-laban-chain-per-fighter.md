# S-079 — RV-16: each fighter's laban chain in render.txt lists its own moves

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-16 (PLAN-007); finding F-091; rulings O1

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-079]

## Plan
render.txt's `laban` field (the owner's LBN-2.4 format, O1) chains, for each fighter, the label of every beat it has
a key in, so A's chain carries B's "throw kunai" and B's opens with A's "fall from above" (F-091). The 2.4 source gives
each fighter its own chain. The class: whose action a per-fighter line prints.
1. A fighter's chain lists the beats it acts in (it is the beat's actor), in time order; its Effort chain stays its
   own efforts. A fighter that acts in no beat prints "none".
2. Neighbours: the other per-fighter lines render.txt and the prose print (the tracks, the staff, the guidance) are
   checked for the same mix-up.

Predictions, made before the change (08:14 by the clock):
1. The gate passes before the change: 707 tests (b6534e2, S-078's chained gate).
2. The reference fight's A chain goes from 22 moves to 18 and B's from 20 to 5; in each other example every chain
   shrinks to its fighter's own beats and no chain is empty.
3. Only render.txt changes in each example (its laban field); no prose prompt changes; checklist counts stay.
4. The neighbouring per-fighter lines already print each fighter's own keys: no other line changes.
5. About 708 tests (707 and one).

## Decisions
- D1 — A fighter's own beats are the beats it acts in. The 2.4 source's chains also word a fighter's side of the
  other's beats ("caught by B", "pulled toward pillar"), but no node words that side: the S13 key names follow the
  source's rows, which name the actor's move ("B_throws_kunai" is A's row at 2.0). Level: interpretation (F-053).
- D2 — The tracks keep their rows' names: A's track row at 2.0 is labelled b_throws_kunai because the owner's A row is
  (O1); the chain was the renderer's own construction, the row names are the source's. Level: covered (O1).
- D3 — A fighter that acts in no beat prints "none" for its moves (no example has one). Level: interpretation (F-053).

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | run after the last edit, its output copied below; then the chained gate commits |
| One gap, right layer | PASS | the LBN-2.4 projection (S17's renderer, L6); no graph changed |
| Predictions written first | PASS | the session file was written at 08:14, before any code |
| New behaviour, old behaviour | PASS | the chains: the fight 18 and 5 moves (from 22 and 20), the wizard example 4 and 10 (from 6 and 13), the live-action 2 and 2 (from 4 and 4), the UGC 4 (unchanged); the test: each chain equals its fighter's actor beats, the spinning kick only in the acrobat's |
| Neighbours | PASS | render.txt's other fields compared field by field: only laban differs; the tracks print each fighter's own keys (D2); the prose's staff, guidance and camera lines name each beat's actor |
| The step's instructions teach it | n/a | the renderer is derived, not authored: no instructions |
| Tests changed with their data | PASS | `git diff -- tests`: one new test; nothing removed or loosened |
| Examples | PASS | render.txt and its envelope in three examples; no prose; checklist counts the same |
| Records | PASS | F-091 resolved; F-053; backlog (RV-16 done, RV-35 next); PLAN-007; CHANGELOG; run report |
| Hygiene | see Verification | the scan's count copied below |

## Duration
from 08:14 (the plan) to 08:16 (the record's last edit before the gate; the gate and the commit follow)

## Changes
- renderers/anime_renderer.py (`_laban`; the layout docstring); tests/test_render.py (one test)
- render.txt and the envelope in reference_fight, wizard_vs_acrobat and live_action_standoff; their checklists
- F-091 resolved; F-053; backlog; PLAN-007; CHANGELOG; run report

## Verification
- before: S-078's chained gate at b6534e2: 707 passed
- Prediction 1 held. Prediction 2 held in part: the fight's chains went from 22 and 20 to 18 and 5 (numbers read from
  the beat list before the plan, so known rather than forecast) and no chain is empty, but the UGC's did not shrink:
  its one performer acts in all four beats. Prediction 3 held in part: render.txt changed in three examples, not the
  UGC; no prose; checklist counts the same. Prediction 4 held (only the laban field differs). Prediction 5 held (708).
  Predictions 4 of 5.
- the gate on this record (08:16:39): `scripts/verify.sh` exit 0, 708 passed in 75.60 s, docs plane: PASS, check:
  PASS
- the hygiene scan over the staged diff: 0 hits
