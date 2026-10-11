# Layer dependency (L0 → L6.5)

The DAG is data: [`kernel/layer_order.yaml`](../kernel/layer_order.yaml) (version 1.4). The envelope
schema is generated from it, and `tests/test_layer_dependency.py` enforces it. Order is encoded only by
the ordered step IDs (S01–S17); `band` is the owner's band name and carries no order.

## Build order (from `planner/topological_sort.py`)

```
S01 → S02 → S03 → S04 → S05 → S06 → S07 → [S08 → S09 → S10 (UGC)] → S11 → S12 → S13 → S14 → S15 → S16 → S17
```

| Node | step_id / band | Depends on | Writes |
|---|---|---|---|
| intent | S01 / L0 | user query + CLI flags | `/intent` (Intent Document) |
| brief | S02 / L0.5 | intent + ontology, archetypes, worlds | `/scene`, `/nodes/entities`, `/nodes/props`, `/nodes/surfaces` (definitions) |
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
- Every group carries its owner's `band` and `step_id`; an item's optional `band` equals its group's band.
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
| 2026-10-10 | Post-generation stays a validation block (`validation.post_generation`): verdicts, not atoms | owner |
| 2026-10-10 | S01 is pure deterministic Python; gates: schema, determinism, completeness, non-invention | owner |
| 2026-10-10 | S01 writes `/intent`; `/scene` moves to S02 (scene needs genre/world/ax, which S01 may not infer) | owner_default |
| 2026-10-10 | Intent Document adds `flags` and per-value `evidence`; genre uses modality names (`ugc_ad`) | owner_default |
| 2026-10-10 | Keys are `step_id` and `band` everywhere | owner |
| 2026-10-10 | S02 resolves from library cards only (no model); unresolved stays in `scene.missing` | owner |
| 2026-10-10 | Starter cards drafted by Claude (status draft), hash-logged in `library/library_log.jsonl` | owner |
| 2026-10-10 | Scene values nullable with named sources; genre may come from a single-genre world card | owner_default |
| 2026-10-10 | Kernel = controls both LBN-2.3-ADV and LBN-2.4-ADV-LMA state (68 shared items) | owner |
| 2026-10-10 | Per-item kernel scope: kernel 20, per-actor 6, per-prop 5, reference fight 37 (draft) | owner_default |
| 2026-10-10 | One envelope (MGRAPH-1.1) | owner_default |
| 2026-10-10 | Camera node = 13 subdivisions + required `motivation` | owner_default |
| 2026-10-10 | L5 holds LMA Effort (weight, time, space, flow) with Shape and Space as separate fields | owner_default |
| 2026-10-10 | Quadrant scoring gains a separately scored style-density question | owner_default |
| 2026-10-10 | No paid model API or renders; authoring via host callback / IDE; post-generation `null` | owner_default |
| 2026-10-10 | `pyyaml` is the only runtime dependency | owner_default |
| 2026-10-11 | F1: facial step (FACS + valence/arousal) for ugc_ad and live_action only | owner |
| 2026-10-11 | F2: renumber; facial = S14, effort S15, camera S16, render S17, post-generation S18 | owner |
| 2026-10-11 | F3: valence and arousal both on −1…1 | owner |
| 2026-10-11 | F4: the render describes faces in words only (codes stay in the envelope) | owner |

## Open for owner review

1. **Kernel scope (draft).** `kernel/kernel_scope.yaml` tags each of the 68 shared LBN controls. Notable calls:
   "no full circle / no ring / no halo" are kernel (no scene entity named); "no scarf covering head" is reference-only;
   "slerp A joints", "A root exact" and "no cloned A" apply to every actor; "no duplicated kunai" and the five-props
   rule apply to every prop.
2. **Draft cards (11).** Archetypes: wizard, acrobat, ninja, knight, superman_variant. Worlds:
   bamboo_courtyard, medieval_fantasy, modern_ugc. Objects: glasses, coffee_cup, jacket. All `draft`.
3. **Loose world match.** Any setting sharing one match term picks the card, so "stone courtyard" becomes
   `bamboo_courtyard` (the only courtyard card) and brings bamboo surfaces. Add a stone-courtyard card, or
   require more shared terms?
4. **Post-generation block shape.** `validation.post_generation` is `pass`/`fail`/`null` today; your
   object shape (run_at, video_ref, checks, verdict, replan_*) lands with the S17 slice.
5. **Cross-file `$ref`.** Sub-schemas are embedded into the envelope by the generator (document-local refs);
   a cross-file resolver is still not implemented.
