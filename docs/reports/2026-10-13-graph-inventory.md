# Graph and field inventory (2026-10-13)

<!-- docs-version: 1.0 -->

Generated from kernel/data_flow.yaml (contract v4, measured on the four examples) and validators/graph_reach.py (what the prose renderer reads). Printed = the prose renderer reads it; S17 also reads fields it does not print (see the data-flow report's dormant column).

## Layers

| Step | Layer | Reads (fields) | Writes (fields) | Passes downstream | Checks |
|---|---|---|---|---|---|
| S01 | intent | 0 | 9 | 3 | schema |
| S02 | brief | 3 | 55 | 45 | schema, coherence |
| S03 | constraint | 6 | 15 | 10 | schema |
| S04 | temporal | 42 | 27 | 27 | schema, invariants, constraint |
| S05 | causal | 38 | 7 | 6 | schema, invariants, constraint |
| S06 | state | 17 | 16 | 14 | schema, invariants, constraint |
| S07 | contact | 16 | 12 | 12 | schema, invariants, constraint |
| S08 | hand_role | 21 | 21 | 15 | schema, invariants, constraint |
| S09 | object_state | 27 | 15 | 13 | schema, invariants, constraint |
| S10 | affordance | 15 | 18 | 14 | schema, invariants, constraint |
| S11 | kinematic | 26 | 21 | 21 | schema, invariants, constraint |
| S12 | bartenieff | 33 | 15 | 15 | schema, invariants, constraint |
| S13 | motion | 57 | 25 | 24 | schema, invariants, constraint |
| S14 | facial | 33 | 24 | 9 | schema, invariants, constraint |
| S15 | effort | 57 | 17 | 17 | schema, invariants, constraint |
| S16 | camera | 53 | 31 | 31 | schema, invariants, constraint, camera_rules |
| S17 | render | 215 | 9 | 9 | schema, invariants, constraint |

## Fields

| Field | Written by | Read by | Printed | Orphaned |
|---|---|---|---|---|
| edges.affordance_dependency.from | S10 | S17 | yes | — |
| edges.affordance_dependency.id | S10 | — | — | — |
| edges.affordance_dependency.relation | S10 | — | — | **yes** |
| edges.affordance_dependency.to | S10 | S17 | yes | — |
| edges.affordance_dependency.via | S10 | S17 | yes | — |
| edges.bartenieff_transition.changes | S12 | S17 | yes | — |
| edges.bartenieff_transition.from | S12 | S17 | yes | — |
| edges.bartenieff_transition.id | S12 | — | — | — |
| edges.bartenieff_transition.to | S12 | S17 | yes | — |
| edges.beat_constraint.from | S04 | S17 | yes | — |
| edges.beat_constraint.id | S04 | — | — | — |
| edges.beat_constraint.to | S04 | S17 | yes | — |
| edges.camera.axis | S16 | S17 | yes | — |
| edges.camera.azimuth_change_deg | S16 | S17 | yes | — |
| edges.camera.from | S16 | S17 | yes | — |
| edges.camera.id | S16 | — | — | — |
| edges.camera.relation | S16 | S17 | yes | — |
| edges.camera.scale_from | S16 | S17 | yes | — |
| edges.camera.scale_to | S16 | S17 | yes | — |
| edges.camera.side_from | S16 | S17 | yes | — |
| edges.camera.side_to | S16 | S17 | yes | — |
| edges.camera.to | S16 | S17 | yes | — |
| edges.camera.transition | S16 | S17 | yes | — |
| edges.causal.causal_strength | S05 | S14, S17 | yes | — |
| edges.causal.from | S05 | S14, S16, S17 | yes | — |
| edges.causal.id | S05 | S14, S16 | — | — |
| edges.causal.relation | S05 | — | — | **yes** |
| edges.causal.to | S05 | S14, S16, S17 | yes | — |
| edges.causal.why | S05 | S14, S17 | yes | — |
| edges.constraint_application.constraint_id | S03 | S04, S17 | yes | — |
| edges.constraint_application.id | S03 | — | — | — |
| edges.constraint_application.target | S03 | S04, S17 | yes | — |
| edges.contact.from | S07 | S17 | yes | — |
| edges.contact.id | S07 | — | — | — |
| edges.contact.relation | S07 | S17 | yes | — |
| edges.contact.to | S07 | S17 | yes | — |
| edges.effort.end | S15 | S17 | yes | — |
| edges.effort.from | S15 | S17 | yes | — |
| edges.effort.id | S15 | — | — | — |
| edges.effort.relation | S15 | S17 | yes | — |
| edges.effort.start | S15 | S17 | yes | — |
| edges.effort.to | S15 | S17 | yes | — |
| edges.facial_transition.from | S14 | — | — | **yes** |
| edges.facial_transition.id | S14 | — | — | — |
| edges.facial_transition.onset | S14 | — | — | **yes** |
| edges.facial_transition.onset_frames | S14 | — | — | **yes** |
| edges.facial_transition.relation | S14 | — | — | **yes** |
| edges.facial_transition.to | S14 | — | — | **yes** |
| edges.facial_transition.trigger | S14 | — | — | **yes** |
| edges.hand_role_transition.agent_hand_changed | S08 | — | — | **yes** |
| edges.hand_role_transition.from | S08 | — | — | **yes** |
| edges.hand_role_transition.gap | S08 | — | — | **yes** |
| edges.hand_role_transition.id | S08 | — | — | — |
| edges.hand_role_transition.relation | S08 | — | — | **yes** |
| edges.hand_role_transition.support_hand_changed | S08 | — | — | **yes** |
| edges.hand_role_transition.to | S08 | — | — | **yes** |
| edges.kinematic_transition.changes | S11 | S17 | yes | — |
| edges.kinematic_transition.from | S11 | S17 | yes | — |
| edges.kinematic_transition.id | S11 | — | — | — |
| edges.kinematic_transition.to | S11 | S17 | yes | — |
| edges.motion.axis_declaration | S13 | S17 | yes | — |
| edges.motion.euler_delta | S13 | S17 | yes | — |
| edges.motion.from | S13 | S17 | yes | — |
| edges.motion.id | S13 | — | — | — |
| edges.motion.inbetweens | S13 | S17 | yes | — |
| edges.motion.interpolation | S13 | S17 | yes | — |
| edges.motion.relation | S13 | — | — | **yes** |
| edges.motion.slerp_angle | S13 | S17 | yes | — |
| edges.motion.to | S13 | S17 | yes | — |
| edges.motion.trajectory | S13 | S17 | yes | — |
| edges.motion.turn | S13 | S17 | yes | — |
| edges.object_state_transition.changes | S09 | S17 | yes | — |
| edges.object_state_transition.from | S09 | — | — | **yes** |
| edges.object_state_transition.id | S09 | — | — | — |
| edges.object_state_transition.interaction | S09 | S17 | yes | — |
| edges.object_state_transition.relation | S09 | — | — | **yes** |
| edges.object_state_transition.to | S09 | S17 | yes | — |
| edges.object_state_transition.trigger_beat | S09 | S17 | yes | — |
| edges.object_state_transition.trigger_contact | S09 | S17 | yes | — |
| edges.state_transition.changes | S06 | S09, S17 | yes | — |
| edges.state_transition.from_state | S06 | S09, S17 | yes | — |
| edges.state_transition.id | S06 | S09 | — | — |
| edges.state_transition.t | S06 | S17 | yes | — |
| edges.state_transition.to_state | S06 | S07, S09, S17 | yes | — |
| edges.state_transition.trigger_event | S06 | S07, S09, S17 | yes | — |
| edges.temporal.duration | S04 | S17 | yes | — |
| edges.temporal.from | S04 | S17 | yes | — |
| edges.temporal.gap | S04 | S17 | yes | — |
| edges.temporal.id | S04 | — | — | — |
| edges.temporal.relation | S04 | S17 | yes | — |
| edges.temporal.to | S04 | S17 | yes | — |
| intent.ambiguous | S01 | — | — | **yes** |
| intent.band | S01 | — | — | **yes** |
| intent.confidence | S01 | — | — | **yes** |
| intent.evidence | S01 | S02, S04 | — | — |
| intent.flags | S01 | — | — | **yes** |
| intent.missing | S01 | — | — | **yes** |
| intent.parsed | S01 | S02, S04 | — | — |
| intent.raw_query | S01 | S02 | — | — |
| intent.step_id | S01 | — | — | **yes** |
| invariants.band | S03 | S17 | yes | — |
| invariants.id | S03 | S17 | yes | — |
| invariants.rule | S03 | S17 | yes | — |
| nodes.affordance.action | S10 | S17 | yes | — |
| nodes.affordance.after | S10 | S17 | yes | — |
| nodes.affordance.agent_grip | S10 | — | — | **yes** |
| nodes.affordance.before | S10 | S17 | yes | — |
| nodes.affordance.duration | S10 | S17 | yes | — |
| nodes.affordance.duration_range | S10 | S17 | yes | — |
| nodes.affordance.id | S10 | S17 | yes | — |
| nodes.affordance.library | S10 | — | — | **yes** |
| nodes.affordance.object | S10 | S17 | yes | — |
| nodes.affordance.postconditions | S10 | S17 | yes | — |
| nodes.affordance.preconditions | S10 | S17 | yes | — |
| nodes.affordance.required_grip | S10 | S17 | yes | — |
| nodes.affordance.satisfied | S10 | — | — | **yes** |
| nodes.bartenieff.beat | S12 | S13, S15 | — | — |
| nodes.bartenieff.body_mode | S12 | S13, S15, S17 | — | — |
| nodes.bartenieff.connectivity | S12 | S13, S15, S17 | — | — |
| nodes.bartenieff.developmental_pattern | S12 | S13, S15, S17 | — | — |
| nodes.bartenieff.entity | S12 | S13, S15 | — | — |
| nodes.bartenieff.extensions | S12 | S13, S15, S17 | — | — |
| nodes.bartenieff.follow_through | S12 | S13, S15, S17 | yes | — |
| nodes.bartenieff.id | S12 | S13, S15, S17 | yes | — |
| nodes.bartenieff.initiation | S12 | S13, S15, S17 | yes | — |
| nodes.bartenieff.intent | S12 | S13, S15, S17 | — | — |
| nodes.bartenieff.t | S12 | S13, S15 | — | — |
| nodes.beats.action | S04 | S08, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.actor | S04 | S05, S07, S08, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.causes | S04 | S05 | — | — |
| nodes.beats.contacts | S04 | S05, S06, S07, S08, S09, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.dur | S04 | S05, S06, S07, S08, S09, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.effects | S04 | S05, S06, S07, S11, S13 | — | — |
| nodes.beats.event_type | S04 | S05, S07, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.facing | S04 | S06, S11, S12, S13, S14, S15, S17 | yes | — |
| nodes.beats.id | S04 | S05, S06, S07, S08, S09, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.label | S04 | S05, S08, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.modes | S04 | S15 | — | — |
| nodes.beats.participants | S04 | S05, S08, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.beats.pos | S04 | S06, S07, S11, S12, S13, S14, S15, S17 | yes | — |
| nodes.beats.prop_samples | S04 | S07, S11, S13, S16, S17 | yes | — |
| nodes.beats.requires | S04 | S05, S06 | — | — |
| nodes.beats.t | S04 | S05, S06, S07, S08, S09, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.camera.angle | S16 | S17 | yes | — |
| nodes.camera.beats | S16 | S17 | yes | — |
| nodes.camera.blur | S16 | S17 | yes | — |
| nodes.camera.composition | S16 | S17 | yes | — |
| nodes.camera.derived | S16 | S17 | yes | — |
| nodes.camera.dur | S16 | S17 | yes | — |
| nodes.camera.editing | S16 | S17 | yes | — |
| nodes.camera.focus | S16 | S17 | yes | — |
| nodes.camera.framing | S16 | S17 | yes | — |
| nodes.camera.id | S16 | S17 | yes | — |
| nodes.camera.intent | S16 | S17 | yes | — |
| nodes.camera.lens | S16 | S17 | yes | — |
| nodes.camera.motivation | S16 | S17 | yes | — |
| nodes.camera.movement | S16 | S17 | yes | — |
| nodes.camera.movement_quality | S16 | S17 | yes | — |
| nodes.camera.playback | S16 | S17 | yes | — |
| nodes.camera.position | S16 | S17 | yes | — |
| nodes.camera.relation_to_action | S16 | S17 | yes | — |
| nodes.camera.support | S16 | S17 | yes | — |
| nodes.camera.t | S16 | S17 | yes | — |
| nodes.constraints.enforcement | S03 | — | — | **yes** |
| nodes.constraints.field | S03 | S17 | yes | — |
| nodes.constraints.id | S03 | S04, S17 | yes | — |
| nodes.constraints.origin | S03 | — | — | **yes** |
| nodes.constraints.reference_labels | S03 | — | — | **yes** |
| nodes.constraints.rule | S03 | S04, S17 | yes | — |
| nodes.constraints.scope | S03 | — | — | **yes** |
| nodes.constraints.source | S03 | S17 | yes | — |
| nodes.constraints.status | S03 | — | — | **yes** |
| nodes.contacts.a | S07 | S08, S11, S13, S16, S17 | yes | — |
| nodes.contacts.b | S07 | S08, S09, S11, S13, S16, S17 | yes | — |
| nodes.contacts.beat | S07 | S08, S09, S11, S16, S17 | yes | — |
| nodes.contacts.body_part | S07 | S08, S09, S13, S16, S17 | yes | — |
| nodes.contacts.contact_type | S07 | S08, S09, S11, S13, S16, S17 | yes | — |
| nodes.contacts.id | S07 | S08, S09, S13, S16, S17 | yes | — |
| nodes.contacts.t | S07 | S08, S09, S11, S13, S16, S17 | yes | — |
| nodes.contacts.verb | S07 | S16, S17 | yes | — |
| nodes.efforts.actor | S15 | S16, S17 | yes | — |
| nodes.efforts.beats | S15 | S17 | — | — |
| nodes.efforts.effort | S15 | S17 | yes | — |
| nodes.efforts.effort_action | S15 | S16, S17 | yes | — |
| nodes.efforts.effort_mode | S15 | S17 | — | — |
| nodes.efforts.end | S15 | S16, S17 | yes | — |
| nodes.efforts.id | S15 | S16, S17 | — | — |
| nodes.efforts.intensity | S15 | S16, S17 | — | — |
| nodes.efforts.shape | S15 | S17 | yes | — |
| nodes.efforts.space | S15 | S17 | yes | — |
| nodes.efforts.t | S15 | S16, S17 | yes | — |
| nodes.entities.capabilities | S02 | S04 | — | — |
| nodes.entities.card_id | S02 | S03, S16 | — | — |
| nodes.entities.card_status | S02 | — | — | **yes** |
| nodes.entities.card_version | S02 | — | — | **yes** |
| nodes.entities.costume | S02 | S17 | yes | — |
| nodes.entities.description | S02 | S04 | — | — |
| nodes.entities.face_profile | S02 | S14 | — | — |
| nodes.entities.hint | S02 | S05 | — | — |
| nodes.entities.hint_evidence | S02 | — | — | **yes** |
| nodes.entities.id | S02 | S03, S04, S05, S06, S08, S11, S12, S14, S16, S17 | yes | — |
| nodes.entities.modes | S02 | S04 | — | — |
| nodes.entities.name | S02 | S04, S05, S14, S17 | yes | — |
| nodes.entities.parts | S02 | S04, S06, S08, S11, S12, S16, S17 | — | — |
| nodes.entities.silhouette | S02 | S17 | yes | — |
| nodes.facial.arousal | S14 | — | — | **yes** |
| nodes.facial.aus | S14 | S16 | — | — |
| nodes.facial.beat | S14 | S16 | — | — |
| nodes.facial.description | S14 | S17 | yes | — |
| nodes.facial.display_rule | S14 | — | — | **yes** |
| nodes.facial.emotion_label | S14 | — | — | **yes** |
| nodes.facial.entity | S14 | S16 | — | — |
| nodes.facial.family | S14 | — | — | **yes** |
| nodes.facial.gaze_target | S14 | S17 | yes | — |
| nodes.facial.id | S14 | S16, S17 | yes | — |
| nodes.facial.inactive_aus | S14 | — | — | **yes** |
| nodes.facial.onset | S14 | — | — | **yes** |
| nodes.facial.onset_frames | S14 | — | — | **yes** |
| nodes.facial.salience | S14 | S16, S17 | yes | — |
| nodes.facial.t | S14 | — | — | **yes** |
| nodes.facial.valence | S14 | — | — | **yes** |
| nodes.facial.words | S14 | S17 | yes | — |
| nodes.hand_role.actor | S08 | S17 | yes | — |
| nodes.hand_role.agent_grip | S08 | S10, S17 | yes | — |
| nodes.hand_role.agent_hand | S08 | S17 | yes | — |
| nodes.hand_role.beats | S08 | S09, S10 | — | — |
| nodes.hand_role.duration | S08 | S10 | — | — |
| nodes.hand_role.end | S08 | S10, S17 | yes | — |
| nodes.hand_role.id | S08 | S09, S10, S17 | yes | — |
| nodes.hand_role.object | S08 | S09, S10, S17 | yes | — |
| nodes.hand_role.role_invariant | S08 | S17 | yes | — |
| nodes.hand_role.role_template | S08 | S17 | yes | — |
| nodes.hand_role.support_grip | S08 | S17 | yes | — |
| nodes.hand_role.support_hand | S08 | S17 | yes | — |
| nodes.hand_role.t | S08 | S10, S17 | yes | — |
| nodes.hand_role.verb | S08 | S10, S17 | yes | — |
| nodes.kinematic.balance | S11 | S12, S13, S15, S17 | — | — |
| nodes.kinematic.beat | S11 | S12, S13, S15 | — | — |
| nodes.kinematic.bracing | S11 | S12, S13, S15, S17 | — | — |
| nodes.kinematic.breathing | S11 | S12, S13, S14, S15, S17 | yes | — |
| nodes.kinematic.entity | S11 | S12, S13, S15 | — | — |
| nodes.kinematic.float | S11 | S12, S13, S15, S17 | yes | — |
| nodes.kinematic.id | S11 | S12, S13, S14, S15, S17 | yes | — |
| nodes.kinematic.loading | S11 | S12, S13, S15, S17 | — | — |
| nodes.kinematic.reads | S11 | S12, S13, S15 | — | — |
| nodes.kinematic.release | S11 | S12, S13, S14, S15, S17 | — | — |
| nodes.kinematic.restraint | S11 | S12, S13, S14, S15, S17 | — | — |
| nodes.kinematic.strain | S11 | S12, S13, S14, S15, S17 | — | — |
| nodes.kinematic.support | S11 | S12, S13, S15, S17 | yes | — |
| nodes.kinematic.t | S11 | S12, S13, S15 | — | — |
| nodes.kinematic.tension | S11 | S12, S13, S14, S15, S17 | yes | — |
| nodes.kinematic.weight_transfer | S11 | S12, S13, S15, S17 | yes | — |
| nodes.kinematic.yielding | S11 | S12, S13, S15, S17 | — | — |
| nodes.motion.axis_declaration | S13 | S15, S17 | — | — |
| nodes.motion.beat | S13 | S15, S17 | — | — |
| nodes.motion.bones | S13 | S14, S15, S16, S17 | yes | — |
| nodes.motion.description | S13 | S15, S16, S17 | yes | — |
| nodes.motion.entity | S13 | S15, S17 | yes | — |
| nodes.motion.heading_basis | S13 | S15, S17 | — | — |
| nodes.motion.id | S13 | S14, S15, S16, S17 | yes | — |
| nodes.motion.name | S13 | S15, S16, S17 | yes | — |
| nodes.motion.points | S13 | S15, S17 | yes | — |
| nodes.motion.pos | S13 | S15, S16, S17 | yes | — |
| nodes.motion.quat | S13 | S15, S17 | — | — |
| nodes.motion.rot | S13 | S14, S15, S16, S17 | yes | — |
| nodes.motion.t | S13 | S15, S17 | yes | — |
| nodes.motion.turn | S13 | S15, S16, S17 | yes | — |
| nodes.object_state.beat | S09 | S10 | — | — |
| nodes.object_state.id | S09 | S17 | yes | — |
| nodes.object_state.interaction | S09 | S17 | yes | — |
| nodes.object_state.object | S09 | S10, S17 | yes | — |
| nodes.object_state.state | S09 | S10 | — | — |
| nodes.object_state.state_name | S09 | S17 | yes | — |
| nodes.object_state.t | S09 | S10, S17 | yes | — |
| nodes.props.affordances | S02 | S04, S08, S16, S17 | yes | — |
| nodes.props.card_id | S02 | S03, S10 | — | — |
| nodes.props.card_status | S02 | — | — | **yes** |
| nodes.props.card_version | S02 | — | — | **yes** |
| nodes.props.carried_by | S02 | S06, S17 | yes | — |
| nodes.props.count | S02 | S17 | yes | — |
| nodes.props.description | S02 | S04 | — | — |
| nodes.props.grips | S02 | S04, S08 | — | — |
| nodes.props.group_name | S02 | S17 | yes | — |
| nodes.props.hint | S02 | S05 | — | — |
| nodes.props.hint_evidence | S02 | — | — | **yes** |
| nodes.props.id | S02 | S03, S04, S05, S06, S08, S09, S10, S14, S16, S17 | yes | — |
| nodes.props.materials | S02 | — | — | **yes** |
| nodes.props.name | S02 | S03, S04, S05, S17 | yes | — |
| nodes.props.parts | S02 | S04 | — | — |
| nodes.props.states | S02 | S04, S06, S09, S17 | yes | — |
| nodes.props.unit_name | S02 | S17 | yes | — |
| nodes.render.coverage | S17 | — | — | — |
| nodes.render.frame_parts | S17 | — | — | — |
| nodes.render.id | S17 | — | — | — |
| nodes.render.labels | S17 | — | — | — |
| nodes.render.prose | S17 | — | — | — |
| nodes.render.sha256 | S17 | — | — | — |
| nodes.render.target | S17 | — | — | — |
| nodes.render.text | S17 | — | — | — |
| nodes.render.variant | S17 | — | — | — |
| nodes.states.beat | S06 | S09, S11 | — | — |
| nodes.states.before_own_effects | S06 | S09 | — | — |
| nodes.states.conditions | S06 | S07, S09, S11, S12, S13, S14, S15, S17 | yes | — |
| nodes.states.facing | S06 | — | — | **yes** |
| nodes.states.hands | S06 | S17 | yes | — |
| nodes.states.id | S06 | S07, S09, S11, S12, S13, S14, S15, S16, S17 | yes | — |
| nodes.states.pos | S06 | S16, S17 | yes | — |
| nodes.states.pos_source | S06 | — | — | **yes** |
| nodes.states.subject | S06 | S07, S09, S11, S17 | yes | — |
| nodes.states.t | S06 | S07, S09, S17 | yes | — |
| nodes.surfaces.ax | S02 | S04, S13, S17 | yes | — |
| nodes.surfaces.boxes | S02 | S04, S13, S17 | yes | — |
| nodes.surfaces.card_status | S02 | — | — | **yes** |
| nodes.surfaces.card_version | S02 | — | — | **yes** |
| nodes.surfaces.description | S02 | S04, S17 | yes | — |
| nodes.surfaces.id | S02 | S04, S05, S06, S13, S16, S17 | yes | — |
| nodes.surfaces.kind | S02 | S04, S05, S13, S17 | yes | — |
| nodes.surfaces.world_card_id | S02 | — | — | **yes** |
| scene.ambiguous | S02 | S04, S05 | — | — |
| scene.ax | S02 | S04, S05, S13, S17 | — | — |
| scene.ax_source | S02 | S04, S05 | — | — |
| scene.chained_from | S02 | S04, S05, S06, S07, S08, S09, S11, S12, S13, S14, S15, S16, S17 | — | — |
| scene.duration_s | S04 | S05, S06, S16, S17 | — | — |
| scene.duration_source | S04 | S05 | — | — |
| scene.fps | S02 | S04, S05, S13, S14, S16, S17 | — | — |
| scene.fps_source | S02 | S04, S05 | — | — |
| scene.genre | S02 | S04, S05, S11, S13, S16, S17 | — | — |
| scene.genre_source | S02 | S04, S05 | — | — |
| scene.missing | S02 | S04, S05 | — | — |
| scene.quadrant | S05 | S06 | — | — |
| scene.setting | S02 | S04, S05, S16, S17 | — | — |
| scene.setting_source | S02 | S04, S05 | — | — |
| scene.style_reference | S02 | S04, S05, S16, S17 | — | — |
| scene.style_reference_source | S02 | S04, S05 | — | — |
| scene.unresolved_hints | S02 | S04, S05 | — | — |
| scene.world | S02 | S03, S04, S05 | — | — |
| scene.world_source | S02 | S04, S05 | — | — |
