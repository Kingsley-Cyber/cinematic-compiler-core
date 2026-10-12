# F-053 — Claude's interpretations await owner review

<!-- docs-version: 1.0 -->

## Type
question

## Severity
medium

## Layer
all

## Status
open

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
docs/reports/2026-10-11-renders-and-dag-adherence.md section 6

## Description
Limb levels (mid within 45 degrees), what counts as a strike, 'steps alternating', the Euler blocks per mode, the joint-limit mapping onto Q6 axes and the anime +30 widening, the 2 m prop reach and 0.25 m gravity tolerance, and the substitution exemption are Claude's interpretations, each labelled where it lives. Added in S-009 (M9-04a,
planner/dynamic_beat_validator.py): a free prop moving into a contact must carry a pre/post sample pair there, and the
velocity into a pre sample is held to gravity within 0.25 m/s. Added in S-010 (M9-04b, renderers/prop_samples.py):
the WHERE line is printed in the prose only (LBN-2.4's prop rows unchanged), and a resting span names the S06 location
in force at its start or first set inside it, ignoring one set before the prop's last hold. Added in S-011 (M9-05,
solver/euler_solver.py): a flip or cartwheel's inversion is read on linear Euler interpolation between its keys; O38's
landing key for the wizard's dodge_flip is a new hold beat b14 at 9.80 (land_guard shortened to 9.40-9.80 and
continuing the flip), not the 9.40 apex key turned into a landing. Added in S-013 (M9-07a, library/combat_verbs.yaml
and planner/dynamic_beat_validator.py): strike joins O22's nine verbs; which contact type takes which verb; a throw
leaves its prop moving (so a touch may throw); which of the reference fight's contacts carry a verb. Added in S-015
(M9-08a, planner/dynamic_beat_validator.py): SURFACE_HEIGHT puts the root between a supporting top (less 0.05 m) and
1.2 m above it, and reads a surface's top from its world card's geometry text. Added in S-016 (M9-08b,
renderers/prose_renderer.py): an entrance is a first line in the air and a first foot support on a raised top; V6's
"not visible before 0.20" and "never stands on the ground" are left out.
Added in S-019: rule R-34 scoped to whole-body checks (ADR-O76 keeps the owner's wider sentence). Added in S-020
(solver/shape_direction.py): SHAPE_DIRECTION's thresholds and span; nine rewrites, not twelve (three are flights). Added in S-021
(compiler/passes/derived/p11_kinematic.py): MOMENTUM_MISSING's arc and 0.3 m; the hang said once per span in RULES.
Added in S-022 (solver/euler_solver.py): a turn that stays on the ground (a tip) needs no launch; the takeoff
effects of the wizard's two flips sit on the beats before them (run_in, the slicing bolt).
Added in S-024 (planner/dynamic_beat_validator.py): PROP_SUPPORT reads a top by height alone and a card's worn
state as the wearer's support; the pellet bursts as it lands at 4.0 (the owner's words: fall after bursting).
Added in S-026 (solver/quaternion.py): a face within FACE_LEVEL 0.2 of vertical keeps the summed heading.
Added in S-027 (solver/forward_kinematics.py, library/body_segments.yaml, validators/contact_world_report.py): the
draft segment lengths; where each contact part's point is; the pelvis re-rooting rule; a touch on a non-floor surface
is a face; the miss report's likely causes.
Added in S-029 (M9-06c; solver/forward_kinematics.py, library/body_segments.yaml, planner/dynamic_beat_validator.py,
validators/contact_world_report.py): the hip joints sit on the pelvis while the thighs turn with the trunk (O84 sets
the trunk reading, not where the joint sits); the anime leg is one scale of the adult's (x1.25, rounded to thigh 0.56,
shin 0.56, ankle 0.10) fitted to the 17 grounded source feet other than 3.00's right; SURFACE_HEIGHT's bound is the
body's standing leg, 0.05 m either way; A's rows at 0.6, 7.5 and 8.0 count as repo-authored roots (O21, O18) and
were re-rooted.
Added in S-030 (M9-06b; solver/contact_world.py, compiler/passes/derived/p13_motion.py, the examples): an exception
naming a contact that is not a real miss is refused too; each re-block is the least change of the repo-authored
joints (and root over the ground, both soles kept on it) that brings the point within 0.06 m; the rope dart's sample
is its dart (the weight), so at 8.0 it sits on B while A keeps the rope's end; the UGC glasses sit on the face 0.1 m
in front of the head's centre.
Added in S-031 (M9-06d), superseded in S-033: body_type lived in the per-genre modality schemas; it now lives in the
genre profile cards (`library/genre_profiles/<genre>.yaml`; the folder name is Claude's), whose schema the owner asked
for in O65.
Added in S-032 (M9-09h): B's 8.0 move is 1.0 m along z, about 20 degrees of pull toward the pillar.
Added in the finish run (RV-45, S-055, from the sessions' decisions; several were labelled "covered" though no ruling
made them, F-166): S-034: hands and feet as orientation words at S13; the kinetic chain from the support (or the core
in the air) to the striking limb; the trail limb authored at S12. S-038: the 0.6 hips keep their numbers (ADR-O103); a
hip flipped past the anime limit held at +60. S-039: the deflect pair at A's right foot; the 8.0 tableau moved with the
kunai's landing; B's palm meets the log's own point; the pellet leaves A's right hand and rests beneath it; the volley's
velocity solved to its 5.9 sample; B rises on straighter legs to A's knee; the vault's hand plant as a support at its
first key. S-040: a beat's requirements read before its own effects; each transition's `t`. S-041: the UGC glasses held
from the first frame on the creator's right; the keys by the scratch solver; the put-on's left hand on the left temple.
S-042: the rope dart drops at 2.25 m/s to land at 4.0 (F-164); A reappears on both feet; the 7.5 crouch moves with the
dart; c10 becomes a full shot. S-043: a release is measured, a takeoff is not; B re-staged on A's -Z side (yaw 340,
347, 320); the kunai's 2.0 velocity solved to A's foot. S-044: the bump check's cutoffs; the library log reads
`version`. S-046: "toward X" needs the free flight within 0.3 m of X and 0.1 m nearer (ADR-O108's thresholds); the
contradiction check reads every section. S-048: an effect may take effect at its beat's start; RULES read each
property's last S06 change; same-instant items keep state, contact, sample order. S-049: the capsule radii; BODY_OVERLAP
at shared key instants only, no depth, a body's own segments and props left out (F-159, F-151); body contacts measured
surface to surface (F-152, for the owner); the re-blocks' 0.01 m clearance and B lying 0.18 m aside. S-050: a hit is a
hold on an impact frame (F-155); a camera hold is a static shot on every body present; PLAYBACK_RAMP for every scene;
the hit shots' scales, distances and azimuths; 43.46 mm and 57.09 mm for fov45 and fov35; 9.0-10.0 split at 9.5.
S-051: b17 cut to 6.6-6.8 (F-158); the kunai on B's torso point and its lodging a touch; a touch on another's held
prop is no strike, and any possess counts on an impact frame (F-157). S-052: an excluded row with a code keeps its
verdict; the compiler judges without the render findings (F-156).
Added in S-055 (RV-45, examples/reference_fight/deviations.yaml): the deviation registry's seven types.
Added in S-057 (RV-48a, planner/dynamic_beat_validator.py, compiler/passes/mandatory/p07_contact.py): a release is on
its pose when its actor has a key at that instant (a beat's start that lists it); a contact between two samples
may move a resting prop only by taking hold of it; a substitution swaps a prop it changes into its new place at
its start, with no hand on it, and S07 lets it change that prop without a contact.
Added in S-058 (RV-48b, compiler/passes/derived/p08_hand_role.py, tests/test_instructions.py, docs/plans/backlog.yaml):
a support hand counts as holding when it holds the object at one of the interaction's beat starts or makes any
contact on it in one; S04's instructions answer for S05, S06 and S07's codes too, since those passes read only the
beat plan; RV-20's prompt part needs no layer-order ADR (F-095 names only the layer order as its block), so it became
RV-65.
Added in S-059 (RV-60, validators/prompt_validator.py, library/camera_conventions, library/camera_idioms/ninja.yaml):
the words that make a camera rule ask for slowed playback (slow motion, slowed, ramp, freeze) or a close-up on a hit
(close or insert with blow, hit, impact, strike or contact); a blade landing in a body is one of O92's hits, so the
ninja's insert on it went; the UGC card plays normal only, following PLAYBACK_RAMP's reach to every scene.
Added in S-060 (RV-61, compiler/passes/derived/p09_object_state.py, p10_affordance.py): a change's trigger hand is
judged at the earliest instant among the transition's changes inside the triggering beat; a postcondition is read at
the next state before that state's beat acts, as a precondition is.
Added in S-061 (RV-62, renderers/prose_renderer.py, examples/reference_fight): the vanishing actor's line keeps its
key's support for the instant and ends it there, in words ("then none: A vanishes here until 4.40"); B draws the volley
at 5.1, its key in A's beat, with the repo's 5.1 arm re-posed to the thigh pouch (corrected in S-063: 0.028 m
from the thigh's surface, and the hand's own radius overlaps it by 0.012 m; F-182).
Added in S-062 (RV-57, planner/hits.py): the four kinds of hit, read from F-155's list (a touch on another
performer's body whatever its verb; a striking verb on a prop another holds or threw; a catch of a body; a body touched
by a held prop that affords stab); hits are judged in every genre, as PLAYBACK_RAMP is.
Added in S-063 (review 4), four choices the sessions made without a ruling: S-055 D3 (DEV-18's rulings name ADR-O12,
R-18's source, for RV-49's re-blocks, which had no ruling of their own); S-056 D2 (a partly fixed finding kept
resolved with a "Corrected" line, against F-166's proposed fix; reversed in S-063); S-059 D5 (a camera rule that negates
the struck words is flagged too); S-061 D5 (the volley's card gains flight `drawn`).

## Impact
Waits on the owner.

## Proposed Fix
Owner review of each.

## Owner Ruling
none yet

## Related
- PLAN-001

## Resolution
Open.
