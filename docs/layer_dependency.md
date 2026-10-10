# Layer dependency (L0 → L6.5)

The DAG is data: [`kernel/layer_order.yaml`](../kernel/layer_order.yaml) (version 1.2). The envelope
schema is generated from it, and `tests/test_layer_dependency.py` enforces it. Order is encoded only by
the ordered step IDs (S01–S17); `layer` is the owner's band name and carries no order.

## Build order (from `planner/topological_sort.py`)

```
S01 → S02 → S03 → S04 → S05 → S06 → S07 → [S08 → S09 → S10 (UGC)] → S11 → S12 → S13 → S14 → S15 → S16 → S17
```

| Node | Step / layer name | Depends on | Writes |
|---|---|---|---|
| intent | S01 / L0 | user query | `/scene` |
| brief | S02 / L0.5 | intent + ontology, archetypes, worlds | `/nodes/entities`, `/nodes/props`, `/nodes/surfaces` (definitions) |
| constraint | S03 / constraint | brief + kernel invariants | `/nodes/constraints`, `/edges/constraint_application`, `/invariants` |
| temporal | S04 / L1 | brief (checked against constraint) | `/nodes/beats`, `/edges/temporal` |
| causal | S05 / L1 | temporal | `/edges/causal` |
| state | S06 / L2 | temporal, causal | `/nodes/states`, `/edges/state_transition` (state tracks) |
| contact | S07 / L2 | temporal, causal, state | `/nodes/contacts`, `/edges/contact` |
| hand_role (UGC) | S08 / L2.5 | contact + ontology | `/nodes/hand_role`, `/edges/hand_role_transition` |
| object_state (UGC) | S09 / L2.6 | contact + ontology, affordances | `/nodes/object_state`, `/edges/object_state_transition` |
| affordance (UGC) | S10 / L2.7 | hand_role, object_state | `/nodes/affordance`, `/edges/affordance_dependency` |
| kinematic | S11 / L4a | state, contact, UGC layers, constraint | `/nodes/kinematic`, `/edges/kinematic_transition` |
| bartenieff | S12 / L4b | kinematic | `/nodes/bartenieff`, `/edges/bartenieff_transition` |
| motion | S13 / L4c | kinematic, bartenieff | `/nodes/motion`, `/edges/motion` |
| effort | S14 / L5 | motion | `/nodes/efforts`, `/edges/effort` |
| camera | S15 / L5.5 | state, contact, kinematic, motion, effort | `/nodes/camera`, `/edges/camera` |
| render | S16 / L6 | all graphs | `/nodes/render` |
| post_generation | S17 / L6.5 | render + generated video | `/validation/post_generation` |

Every graph from S04 onward is validated against the constraint graph. Pipeline-owned: `/graph_version`,
`/derived_from`, `/provenance`, and the other `/validation/*` fields.

## Rules the code enforces

- Every envelope path has one owner, and paths never nest.
- The DAG is acyclic for every modality, and the order is deterministic (ties follow file order).
- A node validated by `constraint` runs after the constraint graph.
- Step IDs read `S01`, `S02` …, are unique and rise along every modality's build order.
- A pass may change only the paths its node owns (`check_pass_writes`), so no pass mutates an earlier graph.
- Every group carries its owner's `layer` and `step`; an item's optional `layer` equals its group's band.
  Layers inactive for the modality hold no items.
- The envelope schema equals its generation from the YAML. Each schema's bytes equal its latest entry in
  `schemas/schema_log.jsonl`, and the log is append-only and hash-chained.

## Decision log

| Date | Decision | By |
|---|---|---|
| 2026-10-10 | Fresh repo from the owner's plan; local only; port proven parts from ai-video-compiler | owner |
| 2026-10-10 | Effort (L5) before camera; effort may motivate a camera beat | owner |
| 2026-10-10 | Entity definitions (entities, props, surfaces) are L0.5; state tracks (states, contacts) are L2 | owner |
| 2026-10-10 | Bands: temporal and causal share L1; state and contact share L2 | owner |
| 2026-10-10 | Constraint built after L0.5 and before the event graphs, checked at every later layer | owner |
| 2026-10-10 | Camera renumbered L5.5 | owner |
| 2026-10-10 | Order lives in ordered step IDs S01–S17, not fractional numbers; L labels are names only; constraint has no L number | owner |
| 2026-10-10 | L1 = nodes.beats + edges temporal/causal; constraint edges = constraint_application; L6 writes nodes.render | owner |
| 2026-10-10 | Incremental schemas: items need `id` (+ optional `layer`) now; full schema per slice; composite at the end | owner |
| 2026-10-10 | One envelope (MGRAPH-1.1) | owner_default |
| 2026-10-10 | Camera node = 13 subdivisions + required `motivation` | owner_default |
| 2026-10-10 | L5 holds LMA Effort (weight, time, space, flow) with Shape and Space as separate fields | owner_default |
| 2026-10-10 | Quadrant scoring gains a separately scored style-density question | owner_default |
| 2026-10-10 | No paid model API or renders; authoring via host callback / IDE; post-generation `null` | owner_default |
| 2026-10-10 | `pyyaml` is the only runtime dependency | owner_default |

## Open for owner review

1. **L6.5 output.** Your diagram shows `nodes: (report)` for post-generation. It writes
   `/validation/post_generation` (from your envelope's validation block). Say if it should be a node group.
2. **Cross-file `$ref`.** The ported checker supports document-local `$ref` only; cross-file refs are
   added with the first `schemas/graphs/` file.
