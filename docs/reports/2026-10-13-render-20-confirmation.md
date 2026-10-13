# Confirmation: the R20 critique checked against the code (2026-10-13)

<!-- docs-version: 1.0 -->

Four read-only checks of the claims in the owner's `confirmation-prompt/docs/state.md`, at b910b95, against the code and
the prompt the owner rendered (docs/render_tests/2026-10-13-author-1/prose_mixed.txt). Result: TRUE GAP (missing),
PARTIAL (some exists), FALSE (the repo has it). State: [state](2026-10-13-render-20-state.md); work:
[next actions](2026-10-13-render-20-next-actions.md).

## 1. The render's failures

| Claim | Evidence | Result |
|---|---|---|
| Hand custody per beat; no "hand empty" | S08/S09 run for `ugc_ad` only (kernel/layer_order.yaml:121,131); S06 `possession` stays `unknown` for both fighters; the prompt never says empty or bare | TRUE GAP |
| No negative prop declaration | "Props at the start: none." plus the kernel's generic "no extra weapons" (kernel/invariants.yaml:551) | PARTIAL |
| Card text invites the weapon | ninja.yaml's invariant, `throw_kunai` and description printed regardless of props (p03_constraint.py:64-69) | TRUE GAP (found by the check) |
| Surfaces have no position | brief_nodes / world_card surface: free-text `ax` only; the pillar has none; S06 pillar pos None | TRUE GAP |
| Strikes are prose, no limb field | contact b04_c1: `body_part: right_hand`, `b.part: torso`, `verb: strike` (beat_plan.schema.json:178-197) | FALSE |
| A part strikes and supports at once | b08_c1 (right foot strikes) and b08_c3 (right foot on the ground) at 5.30; feet land at the hand strike's 2.20 | TRUE GAP (found by the check) |
| Impact lands at the beat's end | `at`: start or end only; p07_contact.py:49 | TRUE GAP |
| No target reaction | only a state effect (`condition: staggered`) at the beat's end | PARTIAL |
| Chain starts at the hand | `initiation` free; no support-first rule (knowledge_map CHAIN_ORDER gap) | PARTIAL |
| No idle / gap ceiling per performer | GAP_S 1.5 adds guidance only; KEY_GAP_UNGUIDED checks the guidance exists | PARTIAL |
| Pillar damage does not persist | S06 `damage: cracked` from 3.8 to the end, printed as a rule | FALSE (it lands at 3.8, not 3.0) |
| Contact source/target parts (fist, chest) | whole segments only | PARTIAL |
| Limb/verb consistency, weapon on a bare-hand strike | none; `strike` names no punch or kick | TRUE GAP |
| One contact policy for every strike | prose_renderer.py:573-576 prints the same line | TRUE GAP |
| Undeclared sword and shield in the prose | knight card has no equipment; "sword drawn back", "shield hand" printed | TRUE GAP (unsure whether any check covers it) |

## 2. Motion, camera and render

| Claim | Evidence | Result |
|---|---|---|
| Hang time is prose | S11 `float` boolean + MOMENTUM_MISSING; no seconds | PARTIAL |
| No support/contact consistency | KINEMATIC_SUPPORT, CONTACT_WORLD, INBETWEEN_SUPPORT | FALSE |
| No limb paths | motion graph: root path and slerp only (PLAN-006 AS-05 open) | TRUE GAP |
| No per-limb world points | 11 points per key in the graph; prose prints contact points only | PARTIAL |
| No lead/trail | implicit lead only (AS-03 open) | PARTIAL |
| No camera position / aim | camera graph `derived.camera_pos`, `aim`; render.txt prints them; prose does not | PARTIAL |
| Camera does not arc with a rotation | `camera_arc_ratio` declared, unused | TRUE GAP |
| Holds without frame counts | `holds {t, frames}` in the graph and render.txt; prose drops frames on purpose (O47) | PARTIAL |
| Smear arc/intensity, speedline count/direction | free-text note only | TRUE GAP |
| Style is words | genre_profile schema declared, values empty (M9-11 blocked) | PARTIAL |
| "back-low" vs "left-back-low" | two 45-degree sectors, a boundary flip (staff_geometry.py:29) | FALSE |
| Airborne lines lack a body | body words printed; the authored pose description is printed on no line | PARTIAL |
| No precedence validator | rule-present check only; one source makes them agree | PARTIAL |

## 3. The "112 missing" inventory

| Group | Exists | Partial | Missing | The missing |
|---|---|---|---|---|
| Validators (30) | 15 | 13 | 2 | IDLE_FIGHTER, CAMERA_ARC |
| Stages (3) | 0 | 2 | 1 | S18 post-generation (declared only) |
| Infrastructure (11) | 4 | 3 | 4 | motion primitives, critic, sampler, speculative execution |
| Docs (13) | 11 | 0 | 2 | SOUL.md, docs/confirmation.md |
| Workflows (6) | 6 | 0 | 0 | — |
| Schemas (8) | 7 | 0 | 1 | style |
| Control (7) | 7 | 0 | 0 | — |
| Genre profiles (12) | 0 | 3 | 9 | every named style profile |
| Verification (5) | 3 | 2 | 0 | — |
| Schema layers (14) | 3 | 8 | 3 | anticipation, sound, line of action |

## 4. Casting and the author

| Claim | Evidence | Result |
|---|---|---|
| Parser and matcher are separate and disagree | S01 PLACE_NOUNS vs S02 `match_terms`; world `names` never matched | TRUE |
| No normalization | case and hyphens yes; punctuation, plurals no | PARTIAL |
| No canonical forms | `card_id` + `names` aliases for performers and props; worlds match a bag of words | PARTIAL |
| No ambiguity resolution | every tie refused by design | TRUE |
| No fallback | none in S01/S02; casting drafts cards in the author path | PARTIAL |
| No model-made cards | casting drafts schema-checked cards (AA-6) | FALSE |
| Retries discard state | cards kept; the previous query is not resent | PARTIAL |
| 15 of 18 steps need a human | 9 authored, all by the model now; 8 computed; S18 unbuilt | FALSE |
| Casting covers every hint | stops at one performer and a place: "ninja versus samurai in a castle" drops the samurai | TRUE GAP |
| Concepts, not strings | casting returns a rewritten string S01/S02 re-parse; cards have no `extends` | PARTIAL |
