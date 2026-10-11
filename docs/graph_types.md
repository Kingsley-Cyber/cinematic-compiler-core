# Graph types

Owner catalog (2026-10-10): every graph carries one kind of information the next layer needs; none is redundant.
Kinds: **parse, ground, constrain** (set-up), **structure** (what exists, how it relates), **expression** (how it
is presented), **project, verify** (output). Build status and deltas: [MASTER_PLAN.md](plans/MASTER_PLAN.md).

| Step | Graph | Intent (owner) | Node groups | Edge groups | Reads | Read by | Kind | Status |
|---|---|---|---|---|---|---|---|---|
| S01 | Intent Document | Isolate the literal query from anything inferred | — (`/intent`) | — | query | S02 | parse | built |
| S02 | Query Expansion Brief | Ground the query in the card library | entities, props, surfaces | — | S01, cards | S03, S04 | ground | built |
| S03 | Constraint | Declare the rules before the scene exists; every later layer validates against them | constraints | constraint_application | S02, kernel, world, archetypes | all later | constrain | built |
| S04 | Temporal | Define the timeline every graph attaches to | beats | temporal | S02, S03, beat planner | S05–S07, S11, S15–S17 | structure | built |
| S05 | Causal | Explain the narrative logic (cause vs coincidence) | beats (shared) | causal | S04 | S06, S11, S17 | structure | built |
| S06 | State | Track entity continuity: no teleporting, cloning, disappearing | states | state_transition | S04, S05, S03 | S07, S11, S15, S17 | structure | built |
| S07 | Contact | Track physical interaction; every prop state change is triggered by a contact | contacts | contact | S06, S04, S03 | S08, S09, S11, S17 | structure | built |
| S08 | Hand role (UGC) | Lock handedness for an interaction | hand_role | hand_role_transition | S07, ontology | S09–S11, S13 | structure | built |
| S09 | Object state (UGC) | Track object internals (zipper closed → open) | object_state | object_state_transition | S07, ontology, S08 | S10, S11, S17 | structure | built |
| S10 | Affordance (UGC) | Prove every functional verb works | affordance | affordance_dependency | S08, S09, affordance library | S11, S17 | structure | built |
| S11 | Kinematic | Describe what the audience sees in the body (support, balance, loading, tension…) | kinematic | kinematic_transition | S06, S07 (+UGC) | S12–S17 | expression | built |
| S12 | Bartenieff | Describe the body's internal coordination (pattern, initiation, follow-through) | bartenieff | bartenieff_transition | S11 | S13, S17 | expression | built |
| S13 | Motion | Provide the explicit key poses the renderer interpolates | motion | motion | S11, S12 | S15–S17 | expression | built |
| S14 | Facial (live action, UGC) | FACS action units, valence and arousal per entity per beat; the face the camera must show | facial | facial_transition | S02, S05, S11, S13, FACS library | S16, S17 | expression | M3.5 (planned) |
| S15 | Effort | Describe the qualitative feel of motion (LMA) | efforts | effort | S13 | S16, S17 | expression | built |
| S16 | Camera | Present the scene deliberately; every move motivated | camera | camera | S11, S13, S15 | S17 | expression | built |
| S17 | Render | Project the envelope into the target model's format | render | — | all | video model, S18 | project | built |
| S18 | Post-generation | Verify the generated video; trigger replan on failure | — (`validation.post_generation`) | — | video, S17, all | replan trigger | verify | M7 |

## Repo notes per graph

- **S02** — the catalog adds surface geometry, position and material, and archetype idioms and forbidden beats.
  Cards do not carry these yet; they are added (draft) to the world and archetype card schemas with M1.
- **S04** — catalog beat = "timestamped event with an actor, a name and a description" → repo fields `t`, `actor`,
  `label`, `action` (+ `participants`, `dur`, `event_type`, archetype `mode`, authoritative root `pos`/`facing`).
  S04 also writes `edges.beat_constraint` (beats → constraints).
- **S05** — writes `scene.quadrant` (scene metadata, not a graph), including `linear`.
- **S05** — catalog "cause label" → repo `why`; `causal_strength` as in the graph table.
- **S07** — contact types touch/possess/support/release; "every prop state transition is triggered by a contact"
  is an S07 check against S06.
- **S08 / S10** — catalog adds `agent_grip`, `support_grip`, `duration` (S08) and `required_grip`, `duration` (S10).
- **S12** — catalog adds `initiation point` and `follow-through`.
- **S15** — LMA kept distinct (Effort = weight, time, space, flow; Shape and Space separate), as in the plan.
- **S16** — catalog confirms 14 required fields = 13 subdivisions + `motivation`.
- **S17** — `nodes.render` is a projection group (`projection: true`), not a graph; no edges.
