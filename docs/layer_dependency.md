# Layer dependency (L0 → L6.5)

The DAG is data: [`kernel/layer_order.yaml`](../kernel/layer_order.yaml) (version 1.1). The envelope
schema is generated from it, and `tests/test_layer_dependency.py` enforces it. `layer` is the owner's
band label; `step` orders graphs inside a band.

## Build order (from `planner/topological_sort.py`)

```
L0 → L0.5 → L1.5 → L1.1 → L1.2 → L2.1 → L2.2 → [L2.5 → L2.6 → L2.7 (UGC)] → L4a → L4b → L4c → L5 → L5.5 → L6 → L6.5
```

| Node | Band / step | Depends on | Writes |
|---|---|---|---|
| intent | L0 | user query | `/scene` |
| brief | L0.5 | intent + ontology, archetypes, worlds | `/nodes/entities`, `/nodes/props`, `/nodes/surfaces` (definitions) |
| constraint | L1.5 | brief + kernel invariants | `/nodes/constraints`, `/edges/constraint`, `/invariants` |
| temporal | L1 / L1.1 | brief (checked against constraint) | `/nodes/beats`, `/edges/temporal` |
| causal | L1 / L1.2 | temporal | `/edges/causal` |
| state | L2 / L2.1 | temporal, causal | `/nodes/states`, `/edges/state_transition` (state tracks) |
| contact | L2 / L2.2 | temporal, causal, state | `/nodes/contacts`, `/edges/contact` |
| hand_role (UGC) | L2.5 | contact + ontology | `/nodes/hand_role`, `/edges/hand_role_transition` |
| object_state (UGC) | L2.6 | contact + ontology, affordances | `/nodes/object_state`, `/edges/object_state_transition` |
| affordance (UGC) | L2.7 | hand_role, object_state | `/nodes/affordance`, `/edges/affordance_dependency` |
| kinematic | L4a | state, contact, UGC layers, constraint | `/nodes/kinematic`, `/edges/kinematic_transition` |
| bartenieff | L4b | kinematic | `/nodes/bartenieff`, `/edges/bartenieff_transition` |
| motion | L4c | kinematic, bartenieff | `/nodes/motion`, `/edges/motion` |
| effort | L5 | motion | `/nodes/efforts`, `/edges/effort` |
| camera | L5.5 | state, contact, kinematic, motion, effort | `/nodes/camera`, `/edges/camera` |
| render | L6 | all graphs | (prompt output, not the envelope) |
| post_generation | L6.5 | render + generated video | `/validation/post_generation` |

Every layer from L1 onward is validated against the constraint graph. Pipeline-owned: `/graph_version`,
`/derived_from`, `/provenance`, and the other `/validation/*` fields.

## Rules the code enforces

- Every envelope path has one owner, and paths never nest.
- The DAG is acyclic for every modality, and the order is deterministic (ties follow file order).
- A node validated by `constraint` runs after the constraint graph.
- Steps read `<band>.<n>`, are unique, cover their whole band and follow the build order.
- A pass may change only the paths its node owns (`check_pass_writes`), so no pass mutates an earlier graph.
- Group `layer`/`step` tags match the owning node; an item's optional `layer` equals its group's band.
  Layers inactive for the modality hold no items.
- The envelope schema equals its generation from the YAML. Each schema's bytes equal its latest entry in
  `schemas/schema_log.jsonl`, and the log is append-only and hash-chained.

## Decision log

| Date | Decision | By |
|---|---|---|
| 2026-10-10 | Fresh repo from the owner's plan; local only; port proven parts from ai-video-compiler | owner |
| 2026-10-10 | Effort (L5) before camera; effort may motivate a camera beat | owner |
| 2026-10-10 | Entity definitions (entities, props, surfaces) are L0.5; state tracks (states, contacts) are L2 | owner |
| 2026-10-10 | Bands with steps: L1.1 temporal, L1.2 causal, L2.1 state, L2.2 contact | owner |
| 2026-10-10 | Constraint is L1.5, built after L0.5 and before the event graphs, checked at every later layer | owner |
| 2026-10-10 | Camera renumbered L5.5 | owner |
| 2026-10-10 | Incremental schemas: items need `id` (+ optional `layer`) now; full schema per slice; composite at the end | owner |
| 2026-10-10 | One envelope (MGRAPH-1.1) | owner_default |
| 2026-10-10 | Camera node = 13 subdivisions + required `motivation` | owner_default |
| 2026-10-10 | L5 holds LMA Effort (weight, time, space, flow) with Shape and Space as separate fields | owner_default |
| 2026-10-10 | Quadrant scoring gains a separately scored style-density question | owner_default |
| 2026-10-10 | No paid model API or renders; authoring via host callback / IDE; post-generation `null` | owner_default |
| 2026-10-10 | `pyyaml` is the only runtime dependency | owner_default |

## Open for owner review

1. **Beats vs `temporal`/`causal` node groups.** The 2026-10-10 summary lists `temporal` and `causal` as
   node groups and no `beats`. The envelope keeps `nodes.beats` plus `edges.temporal` (L1.1) and
   `edges.causal` (L1.2), because the renderer loop reads `nodes.beats`.
2. **L1.5 runs before L1.1.** Like the old L4.5/L5 case, the number and the order differ. Keep L1.5,
   or relabel (for example L0.8)?
3. **Cross-file `$ref`.** The ported checker supports document-local `$ref` only; cross-file refs are
   added with the first `schemas/graphs/` file.
