# S-025 — M9-09f: the reference query says A falls from y=10 (F-067, O79)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-09f; finding F-067; ruling O79

## Layer
L0

## Status
applied

## Commit
the commit whose message names [S-025]

## Plan
O79: "O21 wins. A starts at y=10. Update the query to y=10 so the source and the ruling agree. Record the
rewording." The reference example's request reads "falling from y=10"; the golden test records the rewording of
reference item k_preface_04 (START_HEIGHT).

Predictions, made before the change: no packet moves (the query's wording reaches the SCENE line and the LBN preface,
not an authored step's packet); the five reference prompts change in one sentence; the golden test reports
k_preface_04 until the rewording is recorded.

## Decisions
- D1 — The query file changes; the verbatim source `kernel/sources/lbn-2.3-adv.txt` does not. Why: the owner named
  the query; the kernel sources are the owner's verbatim texts (ownership map: nobody edits them), and the golden test
  is where a rewording of the source's items is recorded (L-08). Level: covered (O79, the ownership map).

## Duration
about 10 minutes

## Changes
- `examples/reference_fight/request.json`; outputs regenerated; `tests/test_reference_fight_golden.py` (START_HEIGHT)
- F-067 resolved; backlog; CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 622 passed (S-024, 79bc7b5)
- after: `scripts/verify.sh` exit 0, 622 passed
- The predictions held: no re-bind, five outputs, k_preface_04 until recorded.

## Next
M9-09g (the face's heading through the spine, R-34).
