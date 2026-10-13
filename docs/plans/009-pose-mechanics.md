# PLAN-009 — Pose mechanics: the eight principles that make a pose read, computed and printed

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
owner

## Created
2026-10-13

## Updated
2026-10-13

## Intent
Every pose the compiler writes carries, as numbers it computed, what makes a fight pose read: its line of action, its
counterbalance, its ground contacts, its weight over its feet, its extension at the strike, and, once the camera is
set, its silhouette, its overlap and its composition. The owner's four reference frames (clash, flying_kick,
takedown, multiplier) are the target. Nothing is authored: every value is computed from the pose S13 already writes,
so the layer costs no model call and no minutes per idea. The values are measured and printed first; only
WEIGHT_DISTRIBUTION refuses (owner, 2026-10-13), the rest refuse later, per genre, once renders show they matter.

## 1. What the repo already has (search, 2026-10-13)

| Mechanic | Today | Where | This plan |
|---|---|---|---|
| Line of action | The spine's lean only (a trunk word, "forward-high (30 lean)"); no curve | solver/shape_direction.py `form`; solver/staff_geometry.py `body_word` | new: a curve through head, chest, pelvis and the leading limb; the lean stays |
| Counterbalance | An authored word (`balance: stable`), never checked | library/kinematic_cues.yaml; S11 | new, computed; checks the word (via 6) |
| Ground contacts | Points and distances per support (CONTACT_WORLD), surfaces' faces since S-124; no angle | solver/contact_world.py; S11 `support` | extend: each support's point (from CONTACT_WORLD) and its angle; the support list stays |
| Silhouette | Visible parts inside the frame (VERTICAL_FRAMING); the face's occlusion; `silhouette` is costume text | validators/camera_validator.py; validators/facial_validator.py | new at S16: limbs projected, clear or hidden |
| Composition | Placement (thirds) checked; negative space printed, unchecked; depth anchor resolved | camera_graph `composition`; CAMERA_COMPOSITION | extend at S16: the bodies' screen boxes, focal point, depth order |
| Weight distribution | Authored directions (`loading`, `weight_transfer`); no share, no centre of mass | library/kinematic_cues.yaml; S11 | new: centre of mass, share per support, margin; checks S11's words |
| Overlap avoidance | Body against body in 3D (BODY_OVERLAP); a body's own limbs, and screen space, unchecked | solver/body_overlap.py | new at S16: limb pairs in screen space; BODY_OVERLAP stays |
| Full extension | Joint limits (JOINT_LIMIT); "straight" under 15 degrees | library/joint_limits.yaml; solver/staff_geometry.py | extend: each limb's extension ratio against its range; the limits stay |

No mechanic is duplicated: four are new, four extend a field that stays.

## 2. Shape of each value (asymmetry)

| Mechanic | Per | Shape |
|---|---|---|
| Line of action | fighter, key | {shape: c, s, straight, reverse_c; direction [x, y, z]; apex: head, chest, pelvis or a limb; tension: deviation over chord} |
| Counterbalance | fighter, key, limb pair | {extended: [limbs], counter: [limbs], com_offset_m} (left and right apart) |
| Ground contacts | support part | [{part, surface, point, angle_deg}] |
| Weight distribution | support part | {com: [x, y, z], share: {part: 0..1}, margin_m (inside the support base +, outside -)} |
| Full extension | limb | {limb: ratio 0..1}; the striking limb named at a strike |
| Silhouette | shot, limb | {clear: [limbs], hidden: [[limb, behind]]} |
| Composition | shot, body | {boxes: {body: screen box}, focal: [x, y], depth: [bodies near to far], negative_space: share of frame} |
| Overlap | shot, limb pair | [{a, b, overlap_share}], min_separation (screen) |

## 3. Skeleton (joint count)

One skeleton for every genre: 11 joints and the root (Sp, LUL, RUL, LL, RL, LA, RA, LFA, RFA, HD, NK; the root is the
pelvis), no wrists, ankles or fingers (library/joint_limits.yaml `unused`). The genre changes the segment lengths only
(anime legs x1.25, library/body_segments.yaml). Forward kinematics gives 21 joint positions and the 11 printed points.
Every mechanic reads those points and the capsules, so it runs for anime, live action and UGC alike; each declares the
points it needs, and one that is missing (a finger, if a later skeleton adds hands) leaves that value out and says so.

## 4. Data flow

| Mechanic | Reads | From | Writes | Read by |
|---|---|---|---|---|
| Line of action | the key's world points | S13 (motion `points`) | pose.line_of_action | S16 (silhouette), S17 |
| Counterbalance | points, segment masses | S13; library/body_segments.yaml (masses, new) | pose.counterbalance | S17 |
| Ground contacts | support parts, contact rows | S11 `support`; CONTACT_WORLD (S13) | pose.ground_contacts | S17 |
| Weight distribution | points, masses, support points | S13, S11, masses | pose.weight | WEIGHT_DISTRIBUTION, S17 |
| Full extension | joint angles, ranges | S13 `bones`; library/joint_limits.yaml | pose.extension | S17 |
| Silhouette | points, capsules, camera | S13; S16 `derived` | camera.derived.silhouette | S17 |
| Composition | points, camera | S13; S16 | camera.derived.composition | S17 |
| Overlap | capsules, camera | S13; S16 | camera.derived.overlap | S17 |

The one missing input: segment masses. Source: Dempster (1955), as tabulated by Winter, Biomechanics and Motor
Control of Human Movement (public): fraction of body mass and centre of mass from the proximal end:

| Segment (the repo's) | Mass | Centre of mass |
|---|---|---|
| trunk (pelvis to shoulders) | 0.497 | 0.50 |
| head and neck | 0.081 | at the head point |
| upper arm (each) | 0.028 | 0.436 |
| forearm and hand (each) | 0.022 | 0.682 |
| thigh (each) | 0.100 | 0.433 |
| shank (each) | 0.0465 | 0.433 |
| foot (each) | 0.0145 | 0.50 |

They sum to 1.000. The anime body keeps these fractions on its longer legs (an interpretation, for the owner).
Outputs with no reader: none; every value is printed.

## 5. The layer

A computed step after S13 (motion) and before facial: it reads only S13's keys and in-betweens, S11's supports and
the contact rows, and writes the pose graph. It does not read facial (S14) or effort (S15), so it runs before both.
The three camera mechanics are computed inside S16's `derived` block, which already holds the camera's position, aim
and screen x, once each shot is set.

Naming (owner ruling needed, see below): step IDs read `S` and two digits (schemas/layer_order.schema.json,
validators/layer_dependency_validator.py STEP_ID). Two ways:
- A. The new step is S14 ("13.5" in place) and every later step moves up one: facial S15, effort S16, camera S17,
  render S18, post-generation S19 (the F2 renumber of 2026-10-11 is the precedent). Code and tests: 175 references in
  44 files; history (sessions, findings, decisions) keeps the numbers it was written with, and an ADR maps old to new.
- B. The step is S13.5 and nothing else moves: the step-ID pattern becomes `S[0-9]{2}(\.5)?`.

Recommended: A. One pattern for every step, and the owner's "renumber later steps".

## 6. Schema

- schemas/graphs/pose_graph.schema.json (new): nodes `pose`, one per S13 key and in-between (id = the key's id);
  edges `pose_transition` between a fighter's consecutive poses: the centre of mass's travel and its speed (what the
  next key inherits). Fields as in section 2.
- camera_graph `derived` gains silhouette, composition (extending the existing `composition`) and overlap.
- library/body_segments.yaml gains `mass` (section 4).
- What each layer computes, reads and feeds is declared once, in kernel/data_flow.yaml (measured, gate-held, S-119):
  the schema descriptions point there instead of a second `computed/depends_on` block that could drift.

## 7. Validators

| Code | Layer | Measures | From the start |
|---|---|---|---|
| WEIGHT_DISTRIBUTION | S14 (new) | S11's `balance` and `weight_transfer` agree with the computed centre of mass: `stable` inside the support base, `precarious`/`off_balance` at or outside its edge, the transfer's direction the way the centre of mass moves | refuses; routes to S13 (the pose must reproduce S11's intent, owner Q2) |
| LINE_OF_ACTION | S14 | a strike or a landing key has a curved line (tension over a genre floor) | printed |
| COUNTERBALANCE | S14 | an extended limb has a counter-limb or the centre of mass stays over the base | printed |
| GROUND_CONTACT | S14 | each support has its point within CONTACT_WORLD's 0.15 m and an angle | printed (the point is already refused by CONTACT_WORLD) |
| FULL_EXTENSION | S14 | the striking limb's ratio at the impact | printed |
| SILHOUETTE_READABLE | S16 | the striking limb is clear of the bodies on screen | printed |
| OVERLAP_AVOIDANCE | S16 | no limb pair overlaps over a share on screen | printed |
| COMPOSITION | S16 | the impact point and the bodies' boxes against the shot's placement | printed (CAMERA_COMPOSITION stays) |

## 8. Genre weights

library/genre_profiles/<genre>.yaml gains, per mechanic, `weight` (how strongly the prose states it) and `required`
(whether its check refuses). Proposed starting values, the owner's to change:

| Mechanic | anime | live_action | ugc_ad |
|---|---|---|---|
| Line of action | 1.0, printed | 0.6, printed | 0.2, printed |
| Counterbalance | 0.8 | 0.8 | 0.2 |
| Ground contacts | 1.0 | 1.0 | 0.4 |
| Weight distribution | 1.0, required, the centre of mass may leave the base by 0.15 m (owner) | 1.0, required, 0.05 m (owner) | 0.6, required, 0.10 m (owner) |
| Full extension | 1.0 (target 0.95 at the strike) | 0.8 (0.85) | 0.2 |
| Silhouette | 1.0 | 0.8 | 1.0 (the hands and the product) |
| Composition | 0.8 | 0.8 | 1.0 |
| Overlap | 0.8 | 0.6 | 1.0 (no hand over the product's face) |

## 9. Tests

- Each mechanic on hand-built poses (a straight stand, a lunge, an inverted kick) with known answers.
- The reference image test: the owner's four frames, each as a pose fixture of numbers (no image in the repo), with
  the classification the frame shows:
  - clash: two opposing C lines meeting at the head; Naruto's wide base, his weight forward (about 60/40 onto the front
    foot), the punching arm extended (ratio over 0.9), the counter arm back; Sasuke compressed over his feet;
  - flying_kick: Sasuke's line one long diagonal from the hands down to the kicking foot, the kicking leg extended
    (ratio about 1.0), no support on the ground at the impact, the leg clear of both bodies on screen;
  - takedown: both bodies inverted on the ground, weight on the shoulders and back, a reversed C, the bodies
    overlapping on screen by design (overlap printed, not refused);
  - multiplier: one fighter at the centre, opponents flung outward along lines from him, several contacts at one
    instant, the bodies spread in depth; composition reads radial.
- The R20 envelope end to end: the layer re-run on its stored poses (it is computed, so it runs without the
  authored documents); WEIGHT_DISTRIBUTION's verdict reported.
- The control layer (tests/test_control_validation.py): the new graph in the data-flow contract, the graph map and
  the cross-graph references (every pose names a key that exists).

## 10. Risks

- Thresholds (tension floor, extension target, the anime allowance) are interpretations until the owner rules.
- WEIGHT_DISTRIBUTION refusing adds author retries to S13 (time, cost); the four examples may fail it and need their
  S11 words or S13 poses re-authored.
- The renumber (A) touches 44 files; a missed reference is caught by the gate, a missed doc link by the docs plane.
- The anime body's mass fractions are the adult's on longer legs.
- The reference frames are the owner's copyrighted stills: the public repo keeps numbers and words, never the images.
- Screen-space capsules are new geometry (camera_geometry projects points today).

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| No centre of mass or weight share | S14 (new) | high | open | PM-1, PM-2 |
| S11's balance words unchecked | S11/S14 | high | open | PM-2 |
| No line of action, extension ratio | S14 (new) | medium | open | PM-3 |
| No screen-space silhouette or overlap | S16 | medium | open | PM-4 |

## Dependencies
- S-124 (surfaces' faces measured): ground contacts read CONTACT_WORLD's rows.

## Owner Rulings Needed
- Ruled 2026-10-13: naming A, the new step is S14 and the later steps renumber; WEIGHT_DISTRIBUTION refuses to S13
  (the pose follows S11's intent); the centre of mass may leave the support base by 0.15 m (anime), 0.05 m
  (live_action) and 0.10 m (ugc_ad).
- Order ruled: line of action, counterbalance, weight distribution, silhouette (at the camera step, which runs after
  S14), each its own slice.
- Open: the other weights and thresholds of section 8.

## Critical Path
1. PM-0: the renumber (if A) and the empty step, the gate green.
2. PM-1: masses (Dempster) and the centre of mass; the pose graph with weight and ground contacts; printed.
3. PM-2: WEIGHT_DISTRIBUTION refusing, routed; the four examples brought through it.
4. PM-3: line of action, counterbalance, extension; printed.
5. PM-4: S16's silhouette, composition and overlap; printed.
6. PM-5: genre weights; the reference image fixtures; R20 end to end.

## Verification
- `scripts/verify.sh`; tests/test_control_validation.py; the reference image fixtures; the R20 report.

## Changelog
- 2026-10-13 — Created from the owner's primer and adjustments (S13.5, Dempster, measure first, WEIGHT_DISTRIBUTION
  refusing early, the four reference frames).
- 2026-10-13 — Owner rulings: naming A (S14, renumber), WEIGHT_DISTRIBUTION to S13, the three allowances; the order
  line of action, counterbalance, weight distribution, silhouette.
