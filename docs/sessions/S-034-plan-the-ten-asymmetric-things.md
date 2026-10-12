# S-034 — The owner's ten asymmetric things per beat: ADR-O87, the map against the repo, PLAN-006 and its slices

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog AS-01 to AS-06 (added this session; PLAN-006); ruling O87; findings F-025, F-072, F-073

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-034]

## Plan
Record the owner's directive (ADR-O87, in the owner's words, with the owner's table), map each of the ten things
against the repo (read-only: a mapping agent, its key locators re-checked by hand), and turn the gaps into PLAN-006 and
backlog slices in build order. No code changes.

Predictions, made before the change:
1. The gate passes before the change: 640 tests (S-033, 50e20f5).
2. After the docs: the gate passes with the same 640 tests; the docs plane accepts PLAN-006, ADR-O87, F-072, F-073 and
   backlog 10; state.md names AS-01 as the next slice.

## The map (key locators)

Re-checked by hand: PLAN-003 F3.1, F3.2, F4.5, F9.4 (docs/plans/deconfliction_2026-10-11.md, sections 3, 4 and 5); the
DAG's KC, T11, C21, C12 and B-4 rows (docs/sources/knowledge_dag_v1.md lines 1616, 1618, 1620, 1634, 107); FRAME_SMEAR
(compiler/passes/derived/p17_render.py, the smear and speedlines loop); `speedlines[]` without a part
(schemas/graphs/frame_parts_plan.schema.json). From the mapping agent, not re-checked line by line: the S13 `bones`
and MOTION_JOINTS (solver/euler_solver.py), the S12 `initiation` and `follow_through` (schemas/graphs/bartenieff_plan
.schema.json; library/bartenieff_vocabulary.yaml: "The order in which the rest of the body follows"), the contact's
`a.part` and `b.part` (schemas/contact.schema.json), the joint-limits card's unused wrist, ankle and foot and its
forearm twist (library/joint_limits.yaml), the kunai card's grips (library/ontology/objects/kunai.yaml).

| # | Status | Notes |
|---|---|---|
| 1 per-limb poses | exists | S13 bones per side, never mirrored |
| 2 asymmetry flag | missing | F3.2 (derived) has no slice until now |
| 3 kinetic chain | partial | S12 chain ordered, untimed, unchecked (M9-14a) |
| 4 limb path | missing | FR.2 covered turning keys only (M9-11) |
| 5 lead and trail | missing | lead implicit, trail absent (DAG B-4, gap OPPOSITION) |
| 6 contact point per limb | exists; surface missing | F3.1 had no slice (F-025) |
| 7 smear per limb | exists | FRAME_SMEAR looser than DAG C12 (F-073) |
| 8 speedlines per limb | missing | F8.3 sat in the camera slice M9-13 |
| 9 hand and foot orientation | missing | no wrist or ankle joint; the forearm twist exists unused (F-072) |
| 10 follow-through per limb | missing | C21 post_contact; the S12 `follow_through` is the chain order |

## Decisions
- D1 — Hands and feet as orientation words at S13 (hand shape, foot set; the palm's facing derived from the forearm's
  twist), not new joints. Why: O87's concept map ("add a field"), the notations already name foot parts and hand
  facings (the laban-notation skill's lookups: MovementXML foot parts, Labanotation hooks and facing), and a wrist or
  ankle joint would change the 11-joint kernel from the LBN key line and the golden (O1, R-30). The plan's own F3.1
  line ("the kernel skeleton has 11 joints and no feet (owner kernel decision)") has no ADR behind it; it is not
  relied on. Level: interpretation, listed in PLAN-006 for the owner to veto.
- D2 — The kinetic chain runs from the support, or the core when airborne, to the striking limb. Why: the owner's "the
  force travels through a chain, the lead limb strikes", the DAG's KC ("order of force propagation ... extends the
  support chain feet → hips → spine → head"). The repo-authored chains that run from the striking end inward are
  rewritten when CHAIN_ORDER lands (R-33). Level: interpretation, listed for veto.
- D3 — Existing fields keep their names under the concept (smear `part`; the contact's `a.part` and `b.part`; S12
  `follow_through` is the chain's order), and item 10 lives in the DAG's own C21 `post_contact`. Why: O87 ("the schema
  is a concept map"), R-20 (the format comes from the DAG's instances). Level: covered.
- D4 — FR.2 leaves M9-11 (render) for AS-05 (motion) and F8.3 leaves M9-13 (camera) for AS-06 (render): their data is
  S13's and S17's. Why: R-10. Level: covered.
- D5 — AS-01 is next and M9-10 goes back to ready. Why: the owner's newest directive ("must"); AS-01 (F3.1) is P1 in
  PLAN-003 and unblocks F-025 and AS-02. Alternatives: finish M9-10 first. Level: interpretation (the order), the
  owner can reorder.
- D6 — The trail limb is authored at S12 (`counterbalance`), where the body's organisation is authored, and checked at
  S13 against the pose. Why: DAG B-4 (Bartenieff opposition), R-10. Level: interpretation.
- D7 — Corrected before its first commit, after the principal review (S-035): item 1's "never mirrored" was false
  (18 of 73 keys mirror within 5 degrees, F-086), so it now counts them and AS-04 gains MIRRORED_ACTION (O95); item 10
  moves from M9-14b (effort) to AS-07 (set at S04, checked at S13, R-10); AS-02 uses the grips S08 already has; AS-01
  waits for one strike definition at S04 (RV-37, F-112); AS-03's layer reads L4c, as its backlog step. The owner
  vetoed none of D1, D2, D5 and D6 (ADR-O95), so they stand as the owner's. Level: covered (O95, the review).

## Duration
about 40 minutes

## Changes
- ADR-O87 (new); `docs/plans/006-ten-asymmetric-things.md` (new, PLAN-006); F-072, F-073 (new)
- `docs/plans/backlog.yaml` 10: AS-01 to AS-06 (new), M9-11, M9-13, M9-14a and M9-14b amended, AS-01 next
- CHANGELOG

## Verification
- before: `scripts/verify.sh` exit 0, 640 passed (S-033, 50e20f5)
- after: `scripts/verify.sh` exit 0, 640 passed; the docs plane PASS; `docs/bootstrap/state.md` names AS-01 next
- Prediction 1 held. Prediction 2 held.

## Next
AS-01 (the striking surface on contacts), unless the owner reorders or vetoes D1 or D2.
