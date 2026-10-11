# Findings — 2026-10-11: five renders, DAG adherence, and what to fix

> Report of 2026-10-11, moved from docs/findings/ (owner O64). Its findings F1-F15 are now docs/findings/F-001 to F-015 ([index](../index/findings.md)); this report keeps the method and the evidence.

Repo HEAD `ebb0cd3` (local). GitHub `main` is at `cda5ffe` (M8.4); everything from M8.5 on is local and unpushed.
Owner renders are the only render evidence; Claude never renders. Details of each render:
[docs/render_log.md](../render_log.md). The DAG: [docs/sources/knowledge_dag_v1.md](../sources/knowledge_dag_v1.md);
its map: [kernel/knowledge_map.yaml](../../kernel/knowledge_map.yaml).

## 1. Bottom line

- The owner rendered five prompts of the reference fight (R1–R5). None is good. The LBN-2.4 `render.txt` (R2) told
  the most cohesive story; the four structured-prose modes were choppy (R1, R3) or cohesive with poor choreography
  (R4, R5).
- **The prompts do not adhere to the DAG map.** Only **38 of the 84 checklist rows** (the 109 rows minus 25 evidence
  rows) are verified for each prompt. The conformance test passed because it checked what had been built, not the
  whole map. Every prompt sent for rendering today was unverified on 46 rows.
- Four root causes, all visible in the renders:
  1. **No causes.** The reference fight's causal graph is a placeholder timeline, and no prompt prints reasons.
  2. **The camera is not the DAG's.** 21 shots in 10 s, written as hard cuts, with every hit as a limb close-up.
  3. **The prose is far denser and longer than the DAG's format.** 38–49 KB, with every limb on every line.
  4. **Choreography contradictions inherited from the golden.** A airborne while picking things up from the
     ground, both hands working in opposite directions, props visible before they are used.

## 2. Render results

The owner's verdicts are verbatim. Cuts were measured by ffmpeg scene detection (> 0.3); frames were sampled at 2 fps.
Model, settings and seed were not stated, so this is not a controlled comparison.

| # | Prompt rendered | Owner verdict | Cuts | Main faults seen |
|---|---|---|---|---|
| R1 | `prose_mixed` (@2e08217) | "hard to even tell whats happening" | 13 (every ~0.3 s mid-fight) | Montage of close-ups; log strike, knee, backflip, slide and cartwheel lost; log on the ground from 0.5 s; A starts on the pillar top |
| R2 | `render.txt`, LBN-2.4 (@2e08217) | "more cohesive story, the hits coulve been better same with the knife kick being a key fraame but the evade of the attacks and the rope swings and dance was legit" | 2 | Hits weak; foot deflect shown as a kunai-only close-up; beats ~0.5–1 s late; log early; A starts on the pillar top |
| R3 | `prose_pure_staff` (@2e08217) | "to many inchoherent scenes in this fight, and the rope was used in both hands but only 1 target. like in two directions like in 6-7sec" | 4 hard, many reframes | Deflect drawn as a hand driving a kunai into the ground; rope pulled two ways at ~7.5 s; the only render that starts with A falling from above |
| R4 | `prose_euler_heavy` (@e500831) | "he substituted but nothing warranted this , and the last attachment scene with ropes didnt make much sense, im starting to see a theme? is their a causal graph?" | 2 | Deflect reads (sole and blade); A holds B's kunai at 0.0; rope in both hands at 2.5; substitution without a threat; rope pull without a purpose |
| R5 | `prose_upgraded_mixed` (@e500831) | "about the same its more cohesive story, but the choreography sucks" | 1 | Set drifts (wooden deck, gate-like crossbeam); muddled 5.0–7.5 s; end appears to show four shuriken (exactly three asked) |

## 3. Findings

| # | Finding | Evidence | DAG rows | Status |
|---|---|---|---|---|
| F1 | **The causal graph gives no causes.** All 22 reference-fight links read "<beat> leads straight into the next exchange" (19 soft, 3 hard): a timeline. Written by Claude on 2026-10-10 when the example was built from the golden, which has no causal graph. `live_action_standoff` also has placeholders ("The stand-off answers itself" ×3); `wizard_vs_acrobat` and `ugc_glasses_demo` have real reasons. | R4 "nothing warranted", R3/R4 rope pull, owner's "is there a causal graph?" | C6, T9, C21, C26, C27; audit X40 | C6 downgraded enforced → partial, gap CAUSE_REASON |
| F2 | **No prompt prints the reasons.** Prose CAUSAL LINKS lists names and arrows only; LBN-2.4 has no causal list (causal edges appear only as camera motivations). | Prompt text | C6, V7, V8 | Open |
| F3 | **The conformance test passed placeholders.** CAUSAL_LIST_MISSING only checks that each link is listed, not that it states a cause. The same pattern runs through the test: it verifies what the renderer writes, not every DAG requirement. | 38/84 rows verified | M4, all partial rows | Open |
| F4 | **The camera plan is not the DAG's.** 21 shots in 10 s (one every ~0.5 s), from the golden's 21 `cam` lines plus Claude's S16 authoring; the prose writes each as "cut to …". The DAG's example camera has 11 lines in 10 s: orbits, a crane rise, a dolly-in, holds of 3–5 frames on hits, and a height/depth change every ≤ 2 s. | R1 13 cuts vs R2 2 cuts from the same plan | C10, C11, C25, V3, V6, E2 | Open (C10 rules not encoded) |
| F5 | **Every hit is a limb close-up.** The 2.5 deflect, 4.7 knee and 8.5 kunai drive are "smash cut to insert" on the striking limb, so the hit shows without its target. The DAG holds on hits with both bodies in frame ("hold 3 frames on kunai/foot impact", "profile kick impact"). | R2 "hits could've been better", "knife kick as a key frame"; R3 deflect drawn as a hand | C10, C12, C25 | Open |
| F6 | **The prose is much denser than the DAG's format.** Staff lines average 386 characters (every limb and fold, every line); the staff alone is 16.6 KB; whole prompts 38–49 KB. The DAG's staff lines (D9) name only the limbs that matter (~120–200 characters), density is adaptive (dense on impacts, sparse on travel), and "never make every frame explicit — it bloats the prompt". The dense lines were Claude's reading of the no-compression rule, which applies to the LBN projection. | R1, R3, R5 | C2, C3, C4, FM6, D4/D9 | Open (owner question Q4) |
| F7 | **Airborne ground pickups split the hands.** Between 7.0 and 8.0 the prompt asks airborne A to snatch the rope dart (left hand), throw it to wrap B, take the kunai from the ground (right hand) and pull B toward the pillar. This is inherited from the golden (audit X2, X3). | R3 rope two ways at ~7.5 s; R4 rope ending | BIO, T7, C5, X2, X3 | Open (owner decision Q5) |
| F8 | **A wrapped rope dart is never one line.** Its track says "8.00 p[0.4, 1.3, 4] held by A" with the dart on B; nothing says it runs from A's left hand to B's shoulder. Also a doubled word: "rope dart dart". | R3, R4 | C5, C7, C31 | Open |
| F9 | **Props are drawn before they are used.** SCENE lists the substitution log with the other props and never says it is hidden until 3.70. | Log on the ground from 0.5–1.5 s in R1–R5 | C5, C23, H3 | Open |
| F10 | **The opening is not followed.** A starts standing or crouched on the pillar top in R1, R2, R4 and R5, instead of falling from above the frame (R3 got it). | R1–R5 | M1, C9 | Open |
| F11 | **Props sometimes cross to the wrong owner.** A holds a kunai at 0.0 (it is B's) in R4. | R4 | C5, C24 | Open |
| F12 | **Counts drift.** R5 appears to show four shuriken in the pillar. | R5 | C5, NEG | Open |
| F13 | **The set drifts.** R5 replaces the courtyard and its single pillar with a wooden deck and a gate-like crossbeam. | R5 | C9, C23 | Open |
| F14 | **Timing slips.** In R2 most beats land 0.5–1 s late. | R2 | C1, C2, E4 | Open |
| F15 | **The foot deflect read only once the wording named the limb with its target in frame.** R4 and R5 (after the insert-wording fix) show sole and blade; R2 and R3 (before) did not. n = 2 each, one variable not isolated. | R2–R5 | C12, C25 | Hypothesis |

## 4. Where the generated prompts diverge from the DAG

| | The DAG | What was generated |
|---|---|---|
| Structure | Master Template [SCENE] … [RULES] (C19), staff FORMAT (L507), tags, implied guidance, prop state machines, causal links, rules, negatives last | Followed |
| Causes | Short cause → effect chains; constraints that enforce causal edges (C6, T9, I2) | Placeholder reasons; reasons not printed |
| Camera | ~11 lines, holds on hits, orbits, crane, dolly; change height/depth every ≤ 2 s (C10) | 21 shots as hard cuts; hits as limb close-ups |
| Staff lines | Only the limbs that matter (D9) | Every limb and fold on every line |
| Density | Adaptive (C2) | Uniform |
| Length | A few KB per instance | 38–49 KB |
| Choreography | The Master Template was shown on the Part 2 stone-wall fight | Applied to the courtyard fight with its own contradictions (X1–X17) |

## 5. Changes made to the golden today (recorded deviations)

All are in `tests/test_reference_fight_golden.py` and the commits named.

| Change | Owner decision | Commit |
|---|---|---|
| 44 negative knee angles made positive (knee flexion = +X under Q6) | O7 | a612ec1 |
| Right hip at 1.1 and 3.0 clamped from +90 to +60 (the anime extension limit) | O10, O11 | a612ec1 |
| FX "pillar-top landing dust ring" and "crash dust ring" became "dust burst" (the kernel negative "no ring" stays) | O10 | 2e08217 |
| Prop positions and velocities solved under gravity (17 samples), not the golden's literal p/v | O8, O10 | 0570db6 |
| Kawarimi beat b09 declared `substitution` | O12 | 3bf35a5 |
| LBN actor rows as named fields {t, label, pos, rot, joints, desc} | O9 | 4115da4 |
| Wizard example: right shoulder adduction 30 → 0 (the owner's table allows none) | O11 | a612ec1 |

## 6. Claude's interpretations awaiting owner review

| Interpretation | Where |
|---|---|
| Limb levels: mid inside ±45°, place within 10° of vertical (from the owner's laban lookup) | `solver/staff_geometry.py` |
| A strike = a touch whose beat holds an S17 impact frame, on anything but a prop the performer holds | `renderers/prose_renderer.py` |
| "Steps alternating" only between two grounded, level lines | same |
| Mixed: root on strike, first and last lines; Upgraded: root + joints on strike and last lines (reading D6/D7/D10) | same |
| Joint-limit mapping onto Q6 axes: NK+HD summed as the neck; hinge stops stay 0 in anime; shoulder adduction min 0 as given | `library/joint_limits.yaml` (draft) |
| Anime widening: each nonzero bound +30° away from neutral | same |
| Prop reach 2 m from the holder's anchor; gravity tolerance 0.25 m | `planner/dynamic_beat_validator.py` |
| Substitution exemption: any prop state change counts as the decoy revealed (the owner's rule names the smoke pellet and the log) | same |

## 7. LBN-2.3-ADV-FINAL (the DAG's D5), measured

Same 24 A keyframes, number for number, as the on-disk 2.3 golden. 48 joint values out of range under O7/O11 (46
knees, 2 hips); no teleport; no ring clash (its fx say "dust"); no prop positions or velocities; 24 of 31 kernel items
(no preface: "Euler degrees XYZ" and "Render spec exactly" are missing); keeps "Root positions are exact"; carries all
17 of the DAG's own audit contradictions (X1–X17). It adds four useful negatives: "no floating limbs", "no inverted
gravity errors", "no scarf physics errors", "no scarf covering head or face". No render evidence exists for it.

## 8. DAG map status today

| Class | Enforced | Partial | Missing | Other |
|---|---|---|---|---|
| Mandatory (27) | 16 | 11 | 0 | |
| Required (15) | 10 | 5 | 0 | |
| Style (22) | 8 | 9 | 5 | |
| Projection (7) | 4 | 1 | 2 | |
| Excluded (13) | | | | 12 excluded, 1 clash (P3.2-6 PRESERVE_AXIS) |
| Evidence (25) | never enforced | 11 | 14 | |

**Not verified on any prompt (46 rows):** LMA, BIO, KC, KF, T3, T4, T5, T6, T7, T10, C5, C6, C8, C10, C11, C18, C20,
C21, C22, C25, C26, V1, V2, V3, V4, V5, V6, V7, V9, V10, V11, V12, V13, and the 13 excluded items (only "root exact" is
checked as absent).

## 9. Open owner decisions

| # | Question |
|---|---|
| Q1 | Must every prompt pass the map, including `render.txt` (LBN-2.4), or only the four prose prompts? (LBN would need causal links, implied guidance and the other DAG sections.) Answered later on 2026-10-11: owner O13, the five are fragments of one complete prompt; the checklist judges all five and their union. |
| Q2 | Rows that cannot be checked on a prompt — C26's 14 unnamed states, T3/T4 (overridden by O4), V4/V5 (menus, not rules): accept "not applicable" with a reason, or must each become a check? Answered later on 2026-10-11: owner O14, N/A only for T3, T4 and C26's 14 unnamed states; V4/V5 checked when selected. |
| Q3 | Print reasons in LBN-2.4 too (a new causal field changes its layout)? Answered: O55, prose only. |
| Q4 | Staff lines in the DAG's brief D9 style (only the limbs that matter), with every number kept in LBN? Answered later on 2026-10-11: owner O19, D9-style lines, every number kept in LBN. |
| Q5 | Ground the pickups at 7.5 and 8.0 (A lands by the rope dart and by the kunai): changes the golden's root positions there. Answered later on 2026-10-11: owner O18, ground the pickups (with the golden's other number fixes). |
| Q6 | P3.2-6 PRESERVE_AXIS: keep or drop S16's 180-degree rule. Answered: O53, keep the rule. |
| Q7 | Add FINAL's four extra negatives to the reference fight (through its cards, not the kernel)? Save FINAL verbatim in `docs/sources/`? Answered: O54, add all four; FINAL saved as docs/sources/lbn-2.3-adv-final.json. |
| Q8 | Which video model and settings were used for R1–R5 (for the render log)? Answered: O56, Seedance 2.0 Mini (from the file names), no fixed seed, 864x496, 24 fps. |

## 10. Proposed plan (not started)

1. **A checklist per prompt.** Next to every prompt file, a table of all 84 checklist rows marked PASS / FAIL /
   NOT CHECKED, each with its evidence. The gate refuses any prompt with a FAIL or a NOT CHECKED row. On day one every
   prompt is refused, and the table says exactly why.
2. **Close rows in the order the renders point to:**
   - causes: real reasons, printed in the prompt, and a check that refuses placeholders (CAUSE_REASON)
   - camera: the DAG's C10 rules, hits held with both bodies in frame, no limb close-ups
   - body and props: grounded pickups, props hidden until used, a wrapped rope written as one line
   - density and format
   - the rest
3. **Definition of done:** a prompt counts as finished only when every applicable row is green. Then the owner renders
   with one fixed model and seed, changing one variable at a time, and each result goes into the render log.

## 11. Today's commits

`19d732b` K1 map · `9de14b0` M8.0 plan · `db40e74` M8.1 staff geometry · `eeb36bf` M8.2 prose · `02764bc` M8.3
sections · `cda5ffe` M8.4 codes + conformance (pushed up to here) · `4115da4` M8.5 named fields · `a612ec1` M8.6 joint
limits · `3bf35a5` M8.7 teleport · `0570db6` M8.8 prop p/v · `2e08217` M8.9 golden passes · `1de4c8e` R1/R2 ·
`e500831` insert wording · `c0a990f` R3 · `a37a276` R4 + C6 downgrade · `ebb0cd3` R5.
