# PLAN-006 — Ten asymmetric things per beat (owner O87)

<!-- docs-version: 1.0 -->

## Status
not started

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-11

## Intent
Every beat records the ten asymmetric things ADR-O87 names, so the renderer never invents them and the fight never
reads as a mirrored dance. The schema is a concept map (O87): where the repo already holds a concept it keeps its
field under the concept's name; where it does not, the schema grows. A thing that is a choice (which limb trails, how
a hand is shaped, which face strikes) is authored at the step that owns that choice; a thing that follows from the
pose (symmetry, palm facing) is derived, so it can never disagree with the pose (R-08, O39). Each check sits at the
first step that sees its data (R-10); each thing prints in the structured prose as words (O42, O47); LBN-2.4 keeps
its rows (O1), as the combat verbs and world points already do.

## Concept map

The owner's ten, against the repo as it stands after S-033 (mapped read-only for S-034; locators in the session file).

| # | Concept (O87 field) | In the repo today | Status | Where it goes | Slice |
|---|---|---|---|---|---|
| 1 | Per-limb poses (body.left_arm ... right_leg) | S13 `bones`: LA/LFA, RA/RFA, LUL/LL, RUL/RL per key, per-side staff words; world points by forward kinematics (M9-06a). 18 of 73 keys mirror within 5 degrees (11 in the reference fight, 6 of them the source's A rows; 7 in the wizard; F-086) | exists (per-side fields); mirroring unchecked | O95: a strike or action beat is never mirrored, an idle guard may be; A's six symmetric source rows and B's five guards stay | AS-04 |
| 2 | Asymmetry flag (body.symmetry) | nothing; asymmetry only implicit in the per-side bones | missing | derived per key at S13: symmetric or asymmetric after mirroring the L/R joint pairs within a tolerance, and which side leads (a strike's lead, AS-03, else the side that moves more); printed "asymmetric: R leg leads" (PLAN-003 F3.2, no authored field); MIRRORED_ACTION refuses a mirrored key on a strike or action beat (O95) | AS-04 |
| 3 | Kinetic chain order (body.kinetic_chain) | S12 `initiation` + `follow_through` (an ordered list of parts; KINETIC_CHAIN_MISSING prints "chain"); order and timing unchecked (gap CHAIN_ORDER) | partial | F4.5: offsets per link authored at S12, CHAIN_ORDER at S13. The order follows the DAG's KC row: force propagates from the support up (feet, hips, spine) to the striking limb; airborne, from the core out (interpretation). The repo-authored chains that run from the striking end inward (the reference b06: foot > leg > torso) are rewritten under R-33 | M9-14a (amended) |
| 4 | Limb path (limbs.<limb>.path) | the root's path only; FR.2 planned `limb_paths` on turning keys | missing | S13 `limb_paths` on every key where a limb travels, from a closed list (Labanotation's straight and circular path signs; FR.2's crescent, tuck, reach), checked against the joint change to the next key (LIMB_PATH); split from M9-11 | AS-05 |
| 5 | Lead and trail limb (strike.lead, strike.trail) | the lead is implicit (the strike contact's `a.part`, S12 `initiation`); the trail is absent (DAG B-4 "Opposition and counterbalance", gap OPPOSITION) | missing | the lead is the strike contact's striking part (printed); the trail is a new S12 field `counterbalance` (the limb that balances), checked at S13 against the pose (OPPOSITION: the trail moves against the lead between the keys); the strike line prints "lead R foot, trail L arm"; S12 initiation and the contact must agree on the lead (DAG T11) | AS-03 |
| 6 | Contact point per limb (contact.source_part, target_part) | S04 contact `a.part` and `b.part`; world points and CONTACT_WORLD at S13 (M9-06a, M9-06b) | exists; the striking surface is missing (F-025) | F3.1: `surface` on the contact's actor side (sole, heel, ball, toes, knuckles, palm, knife edge, elbow, knee, shin; foot parts from MovementXML's vocabulary), required on a strike (CONTACT_SURFACE), a strike being the S04 contact whose verb is a strike verb (RV-37; today the prose infers strikes from S17's impact frames, F-112); the bow prints "R foot (sole) > kunai blade" | AS-01 |
| 7 | Limb-specific smear (anime.smear[].limb) | S17 `smear[].part` (FRAME_SMEAR) | exists, but FRAME_SMEAR accepts a torso or head smear against DAG C12 ("body does NOT smear"), F-073 | FRAME_SMEAR: a body smear names a limb | AS-06 |
| 8 | Limb-specific speedlines (anime.speedlines[].limb) | S17 `speedlines[]` = window and subject only | missing | F8.3: `part` on speedlines (frame_parts_plan), checked like the smear (a body's speedlines name a limb); the reference fight's speedlines gain their limbs (R-33); split from M9-13 | AS-06 |
| 9 | Hand and foot orientation (body.left_hand, body.right_foot) | no field; the kernel's 11 joints (the LBN key line) have no wrist or ankle; the forearm's twist (LFA/RFA Y, "pronate/supinate") exists but no key uses it | missing | S13 per key: each hand's shape (fist, open, knife hand, grip) and each foot's set (flat, pointed, flexed, on the ball, on the heel, edge), authored words; each palm's facing derived from the arm chain and the forearm's twist. Checks (HAND_FOOT_ORIENTATION): a holding hand grips with one of the prop's grips (the kunai card: reverse, forward), in the grip vocabulary S08 already uses (library/grip_types.yaml; S08's agent and support grips stay authoritative where S08 runs, UGC); a supporting foot's set agrees with its support; a strike's surface (AS-01) agrees with the hand or foot. No kernel joint; LBN-2.4 unchanged | AS-02 |
| 10 | Follow-through per limb (follow_through.<limb>) | one generic recovery line per strike; S12's `follow_through` is the chain order (#3), not this | missing | the DAG's C21 `post_contact` (compress, accelerate, follow_through) on each strike contact: set at S04, where the contact is authored, and checked at S13 against the striking limb's next key (FOLLOW_THROUGH_MISSING, R-10); the target's reaction stays F9.4 (M9-14b) | AS-07 |

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| AS-01 | L1.1 | high | open | the striking surface on contacts (F3.1; F-025) |
| AS-02 | L4c | high | open | hand and foot orientation (F-072) |
| AS-03 | L4c | high | open | the trail limb (authored at S12) checked against the lead at S13 (OPPOSITION) |
| AS-04 | L4c | high | open | the derived asymmetry flag (F3.2) |
| AS-05 | L4c | high | open | a path for every travelling limb (FR.2 widened) |
| AS-06 | L6 | medium | open | smear on limbs only, speedlines per limb (F8.3; F-073) |
| M9-14a | L4c | medium | open | the chain's order and timing, from the support to the striking limb |
| AS-07 | L4c | high | open | the striking limb's post_contact (C21), set at S04, checked at S13 |

## Dependencies
- M9-06a, M9-06b (forward kinematics and the world points the checks read); S-033 (the genre profile cards);
  PLAN-007's RV-37 (one strike definition).

## Owner Rulings Needed
- None. The owner vetoed none of S-034's choices (ADR-O95): hands and feet are orientation words, not new kernel
  joints; the kinetic chain runs from the support, or the core when airborne, to the striking limb (DAG KC); the
  concept keeps the repo's field where it already exists and item 10 lives in C21's `post_contact`; AS-01 comes before
  M9-10; the trail is authored at S12.

## Critical Path
0. After PLAN-007's RV slices (the principal review's gaps come first); AS-01 and AS-07 follow RV-37 (one strike
   definition at S04).
1. AS-01 — the striking surface on contacts (S04; F3.1; F-025)
2. AS-02 — hand and foot orientation (S13; F-072)
3. AS-03 — lead and trail (S12 counterbalance, S13 OPPOSITION)
4. AS-04 — the derived asymmetry flag (S13; F3.2)
5. AS-05 — limb paths on every travelling limb (S13; FR.2 widened, split from M9-11)
6. AS-06 — smear on limbs only, speedlines per limb (S17; F8.3 split from M9-13; F-073)
7. M9-14a — the timed kinetic chain, from the support to the striking limb (amended)
8. AS-07 — the striking limb's post_contact (S04 and S13)

## Verification
- `scripts/verify.sh` and `make golden`; each slice's new code with its break tests and a should-not-fire run over
  every prompt; the checklist per prompt (R-19).

## Changelog
- 2026-10-11 — Created from ADR-O87 and the read-only map of S-034.
- 2026-10-11 — Corrected before its first commit after the principal review (S-035) and ADR-O95: item 1 counts the
  mirrored keys; AS-04 adds MIRRORED_ACTION; item 10 moves to AS-07 (R-10); AS-02 uses S08's grips; AS-01 waits for
  one strike definition (RV-37).
