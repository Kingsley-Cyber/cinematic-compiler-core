# Layer dependency (L0 → L6.5)

The DAG is data: [`kernel/layer_order.yaml`](../kernel/layer_order.yaml). The envelope schema is generated
from it, and `tests/test_layer_dependency.py` enforces it. Layer labels are the owner's names; the build
order comes from the edges, not from the numbers.

## Build order (from `planner/topological_sort.py`)

| Modality | Order |
|---|---|
| anime, live_action | intent → brief → temporal → causal → state → contact → constraint → kinematic → bartenieff → motion → effort → camera → render → post_generation |
| ugc_ad | … contact → constraint → hand_role → object_state → affordance → kinematic → … (rest as above) |

| Node | Layer | Depends on | Writes |
|---|---|---|---|
| intent | L0 | user query | `/scene` |
| brief | L0.5 | intent + ontology, archetypes, worlds | `/nodes/actors`, `/nodes/props`, `/nodes/surfaces` |
| temporal | L1 | brief | `/nodes/beats`, `/edges/temporal` |
| causal | L1 | temporal | `/edges/causal` |
| state | L2 | temporal, causal | `/nodes/states`, `/edges/state_transition` |
| contact | L2 | temporal, causal, state | `/nodes/contacts`, `/edges/contact` |
| hand_role (UGC) | L2.5 | contact + ontology | `/nodes/hand_role`, `/edges/hand_role_transition` |
| object_state (UGC) | L2.6 | contact + ontology, affordances | `/nodes/object_state`, `/edges/object_state_transition` |
| affordance (UGC) | L2.7 | hand_role, object_state | `/nodes/affordance`, `/edges/affordance_dependency` |
| constraint | L3a | brief + kernel invariants | `/nodes/constraints`, `/edges/constraint`, `/invariants` |
| kinematic | L4a | state, contact, UGC layers, constraint | `/nodes/kinematic`, `/edges/kinematic_transition` |
| bartenieff | L4b | kinematic | `/nodes/bartenieff`, `/edges/bartenieff_transition` |
| motion | L4c | kinematic, bartenieff | `/nodes/motion`, `/edges/motion` |
| effort | L5 | motion | `/nodes/efforts`, `/edges/effort` |
| camera | L4.5 | state, contact, kinematic, motion, effort | `/nodes/camera`, `/edges/camera` |
| render | L6 | all graphs | (prompt output, not the envelope) |
| post_generation | L6.5 | render + generated video | `/validation/post_generation` |

Pipeline-owned: `/graph_version`, `/derived_from`, `/provenance`, and the other `/validation/*` fields.

## Rules the code enforces

- Every envelope path has one owner, and paths never nest.
- The DAG is acyclic for every modality, and the order is deterministic (ties follow file order).
- A node validated by `constraint` runs after the constraint graph.
- A pass may change only the paths its node owns (`check_pass_writes`), so no pass mutates an earlier graph.
- Group `layer` tags match the owning node. Layers inactive for the modality hold no items.
- The envelope schema equals its generation from the YAML. Each schema's bytes equal its latest entry in
  `schemas/schema_log.jsonl`, and the log is append-only and hash-chained.

## Decision log

| Date | Decision | By |
|---|---|---|
| 2026-10-10 | Fresh repo from the owner's plan; local only; port proven parts from ai-video-compiler | owner |
| 2026-10-10 | Effort (L5) before camera (L4.5); effort may motivate a camera beat | owner |
| 2026-10-10 | One envelope (MGRAPH-1.1), with per-group schemas to come in each layer slice | owner_default |
| 2026-10-10 | Camera node = 13 subdivisions + required `motivation` | owner_default |
| 2026-10-10 | L5 holds LMA Effort (weight, time, space, flow) with Shape and Space as separate fields | owner_default |
| 2026-10-10 | Quadrant scoring gains a separately scored style-density question | owner_default |
| 2026-10-10 | No paid model API or renders; authoring via host callback / IDE; post-generation `null` | owner_default |
| 2026-10-10 | `pyyaml` is the only runtime dependency | owner_default |

## Open for owner review

1. **Entity groups tagged L0.5.** Your envelope tags actors, props and surfaces as L2, but grounding happens
   at L0.5 and L2 needs the entities. They are owned by `brief` (L0.5) here.
2. **Two L1s and two L2s.** DAG nodes are named by graph (temporal, causal, state, contact), with your layer
   label kept on each.
3. **Constraint before the UGC layers.** L2.5–L2.7 are validated by constraint, so the constraint graph
   (which needs only brief + kernel) is built before them, not where the drawing places it.
4. **Label numbers vs order.** Effort (L5) now runs before camera (L4.5). Renumber them, or keep the labels?
5. **Per-graph schemas.** Items need only `id` until each layer slice fixes its graph schema. The ported
   checker supports document-local `$ref` only; cross-file refs arrive with the first `schemas/graphs/` file.
