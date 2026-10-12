# PLAN-007 — The principal review of 2026-10-11: every gap named, the owner's rulings, the gate

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-12

## Intent
Close what the first principal review (docs/prompts/principal_review.md, S-035) found, under the no-shortcuts principle
(docs/prompts/no_shortcuts.md) and the anti-reward-hacking clause (AGENTS.md section 18): each gap is fixed at its cause,
named here with a slice, or asked of the owner. The review's verdict: the work matches the plan only partially. The
skeleton is real (layer order, write scopes, sealed authoring, hash logs, recorded rulings), but no prompt is a
deliverable, prompt checks never run at compile, and recent checks passed by exemptions and re-blocks that broke the
moves they measured, several of them the builder's own (F-074 to F-077). The gate is the owner's six conditions (ADR-O98,
CLAUDE.md).

## The owner's rulings (2026-10-11)

| Ruling | In short | Slice |
|---|---|---|
| ADR-O88 | A's limb and head words follow the source's words; each flip a recorded deviation | RV-05 |
| ADR-O89 | An exact-instant miss is not an artefact; re-block B's throw, the palm on the log, the vault hand | RV-02a, RV-02b |
| ADR-O90 | A's supports and holds end at 3.7; the rope dart rests on the ground until 7.5 | RV-06 |
| ADR-O91 | The smoke bursts at 3.7 at A's body; the spent pellet falls and rests | RV-07 |
| ADR-O92 | Hits are camera holds framing both bodies; no playback ramps; no inserts | RV-09 |
| ADR-O93 | The kunai drive holds the kunai in B's shoulder; the catch is a grasp plus a throw | RV-10 |
| ADR-O94 | DAG-excluded rows are N/A; `cinematic compile` refuses a non-deliverable prompt | RV-11 |
| ADR-O95 | "Never mirrored" binds strikes and action beats, not idle guards; no veto of S-034's choices | AS-04 |
| ADR-O96 | The 6.3 cartwheel is a full turn | RV-12 |
| ADR-O97 | Prompts capped at 3,500 characters (Runway) and 1,000 words (BytePlus) | RV-13, RV-13b |
| ADR-O98 | The gate's six conditions | RV-39 |
| ADR-O99 | The principal review and the no-shortcuts principle | this plan |
| ADR-O100 | The anti-reward-hacking clause | F-119 |
| ADR-O107 | O102 confirmed; the finish run pushes each slice and continues | S-045 |

The builder reads O89's "genuine airborne or prop-moving misses" as contacts measured between keys or samples (an
interpolated instant): ADR-O104 (RV-02a), for the owner to confirm.

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| RV-01 | L6 | high | done (S-037) | C12 off CONTACT_WORLD (F-074) |
| RV-02a, RV-02b | L4c | high | done (S-039, S-043) | CONTACT_WORLD per O89 (re-blocks, the vault's hand plant, test hygiene), then releases measured (F-075, F-076, F-079) |
| RV-03 | L1.1 | medium | done (S-041) | the UGC pickup and poses (F-077) |
| RV-04 | docs | medium | done (S-044; the hook is the owner's) | records: versions, logs, hook, stale docs and findings (F-078) |
| RV-05 | L4c | high | done (S-038) | A's words follow the source (F-080) |
| RV-06 | L1.1 | high | done (S-042) | the vanish (F-081) |
| RV-07, RV-08 | L1.1, L2.1 | high | done (S-040, S-048) | the smoke at 3.7 after commits at the contact's instant (F-082, F-061) |
| RV-09 | L5.5 | high | done (S-050) | hits as camera holds (F-083, F-005) |
| RV-10 | L1.1 | high | done (S-051) | the kunai drive and the catch (F-084) |
| RV-11 | L6 | high | done (S-052) | compile refuses non-deliverables; excluded rows N/A (F-085) |
| RV-12 | L6 | medium | done (S-053) | the cartwheel's words (F-087) |
| RV-13, RV-13b | L6 | high | open | prompt length (F-088) |
| RV-14 | L4c | high | open | every-key body checks (F-089, F-062) |
| RV-15 | L5.5 | high | open | the camera's aim and vertical framing (F-090) |
| RV-16 | L6 | high | open | one laban chain per fighter (F-091) |
| RV-17 | L2.2 | medium | open | one possession model; PROP_TWO_HOLDERS (F-092) |
| RV-18 to RV-41 | various | medium-low | open | F-093 to F-116 and F-016, one slice each (docs/plans/backlog.yaml) |
| RV-42 to RV-54 | various | high-low | RV-42, RV-43, RV-49, RV-45, RV-46, RV-48a, RV-48b done (S-046, S-047, S-049, S-055 to S-058); the rest open | the second review's gaps, F-122 to F-150 (docs/reports/2026-10-12-principal-review-2.md), and F-151 (a body through a prop, RV-54) |
| RV-55 to RV-65 | various | high-medium | RV-57, RV-60, RV-61, RV-62 done (S-059 to S-062); the rest open (RV-55, RV-56, RV-63, RV-64b wait for the owner) | the third review's gaps, F-152 to F-167 (docs/reports/2026-10-12-principal-review-3.md), and RV-65 (RV-20's prompt part) |
| RV-66 to RV-84 | various | high-medium | open | the fourth review's gaps, F-169 to F-186 (docs/reports/2026-10-12-principal-review-4.md) |

## Dependencies
- RV-02a after RV-05 (A's final poses); RV-02b after RV-02a, RV-03 and RV-06; RV-07 after RV-08; RV-13b after RV-13 and
  F-088; RV-21 after RV-01; RV-22 after RV-14; RV-35 after RV-02a; RV-39
  after RV-11. PLAN-006's AS-01 and AS-07 follow RV-37 (one strike definition at S04).

## Owner Rulings Needed
- F-088: the caps (which prompts carry them, what a capped prompt drops, whether O97 amends R-16)
- F-099: A's backflip at 5.1 launched from the air (O80's "prior beat")
- F-101: which anime spans keep a declared hang and which are re-timed
- F-108: which of B's two kunai releases is real (answered: ADR-O105, the 2.0 throw)
- F-111: the frame limb and head words are read in
- F-114: whether R-21, R-23 and R-25 bind render.txt
- F-116: whether a moved packet forces re-authoring
- F-117: how F-013 and F-014 close without a fixed seed
- F-118: O37's split cards or the one genre profile (blocks M9-11)
- F-119: how the anti-reward-hacking clause meets R-33 (answered: the owner confirmed ADR-O102, ADR-O107)
- F-143: ADR-Q6's label or its meaning (the source's turned leans and its backflip)
- F-148: the source rows whose numbers contradict their words; F-149: O95 against O88 on two action keys
- F-152: O72's measure for body contacts; F-153: render.txt's deliverability under O1 and O94; F-154: owner_default
  ADRs as rulings (confirm or strike O103 to O106 and O108); F-164: O90's timing; F-165: the pellet's point
- F-055, F-057 and F-060: open since before the run
- From review 4 (S-063): whether a substitution may move or change props other than its decoy without a hand (F-169); what counts as a hit beyond a thrown or held blade (F-175); whether a smash cut, a whip onto the impact frame or a shaky handheld shot is a camera hold (F-177); which checklist rows must pass for a deliverable (F-178, with F-153 and F-117); a declared turn plane against the 180-degree side (F-184); O23's `at: start` read literally or as any key of the actor; O93's grasp and throw on one instant at 6.6; whether the source counts as a ruling under R-06 (O105, O108); whether a deviation's ruling must be an owner ADR in force; R-21's reach to every genre; partly fixed findings reopened (S-063) or kept resolved (S-056 D2); `decided_by: owner` (R-28); O103 sets aside two of O88's flips, which R-06 now leaves to the owner
- F-124 (the 5.9 slide's exception) and F-133 (the scene_reference rules; RV-64b waits for it)
- RV-20: an ADR for the layer-order edit; RV-38: the owner's review of draft values and F-053

## Critical Path
1. Step 3, the builder's own shortcuts first (only on the owner's "go"): RV-01, then RV-05 (O88 moves A's arms that
   RV-02a's re-blocks aim at), RV-02a, RV-03, RV-06, RV-02b, RV-04
2. The owner's rulings: RV-05, RV-06, RV-08, RV-07, RV-09, RV-10, RV-11, RV-12, RV-13
3. The fight-breakers that need no ruling: RV-14, RV-15, RV-16, RV-17, RV-37, RV-35, RV-22
4. The rest in backlog order: RV-18, RV-19, RV-21, RV-23, RV-25, RV-27 to RV-32, RV-34, RV-39, RV-41
5. Then PLAN-006 (AS-01 to AS-07) and PLAN-003's remaining M9 slices
After review 3 (S-054): RV-45 and RV-46 (the records) first, then RV-48a, RV-48b, RV-60, RV-61, RV-62, RV-57, RV-58, RV-18,
RV-64 and RV-13, then the rest in backlog order.
After review 4 (S-063): the builder's own shortcuts and overclaims first, RV-66, RV-67, RV-68, RV-69, RV-70, RV-71,
RV-72, RV-73, RV-74, RV-75, RV-76, RV-77; then RV-58, RV-18, RV-64, RV-13; then the fight-breakers RV-15, RV-14,
RV-16, RV-37, RV-35, RV-59, RV-22; then RV-78 to RV-84 and the rest in backlog order.
6. Waiting on the owner: RV-13b, RV-20, RV-24, RV-26, RV-36, RV-40, RV-52, RV-53, RV-55, RV-56, RV-63 (and RV-33, which
   follows RV-52); the owner's own: RV-38

## Verification
- Each slice: `scripts/verify.sh` and `make golden`, its predictions reported, the self-audit recorded (RV-45); tests
  change only where a ruling or the plan's intent moves the data they pin, each change recorded (ADR-O102, confirmed
  in ADR-O107); a principal review every eight slices and before the next release (O98's soul_check_passes).

## Changelog
- 2026-10-11 — Created from the first principal review (S-035) and the owner's rulings O88 to O100.
- 2026-10-11 — RV-02 split into RV-02a and RV-02b; RV-05 moved ahead of them (S-038).
- 2026-10-11 — RV-01, RV-05 and RV-02a done (S-037 to S-039); ADR-O104 answers O89's "genuine"; RV-02b also re-stages
  B's kunai throw (S-039).
- 2026-10-12 — RV-08, RV-03, RV-06 and RV-02b done (S-040 to S-043); ADR-O105 answers F-108.
- 2026-10-12 — RV-04 done (S-044); the second principal review (S-045): F-120 to F-150, RV-42 to RV-53; ADR-O107.
- 2026-10-12 — RV-42, RV-43, RV-07 and RV-49 done (S-046 to S-049); F-151 and RV-54 (a body through a prop) filed.
- 2026-10-12 — RV-09 done (S-050): hits are camera holds, no playback ramps.
- 2026-10-12 — RV-10 done (S-051): the kunai drive holds the kunai in B; the catch grasps then throws.
- 2026-10-12 — RV-11 done (S-052): excluded rows N/A; cinematic compile refuses non-deliverables.
- 2026-10-12 — RV-12 done (S-053): the cartwheel is a full turn in the words.
- 2026-10-12 — Principal review 3 (S-054): verdict partially; F-152 to F-167, RV-55 to RV-64.
- 2026-10-12 — RV-45 done (S-055): self-audit sections enforced; typed deviations DEV-01 to DEV-28.
- 2026-10-12 — RV-46 done (S-056): the stale and overclaimed records corrected.
- 2026-10-12 — RV-48 split; RV-48a done (S-057): S04's latent checks; the 6.6 throw on its pose; the log's swap.
- 2026-10-12 — RV-48b done (S-058): S08's support hand; the S04 and S08 instructions name every rule their plans
  must meet (tests/test_instructions.py); RV-20 split: its prompt part for S11 to S17 is RV-65.
- 2026-10-12 — RV-60 done (S-059): the camera cards follow O92; the printed camera rules are checked.
- 2026-10-12 — RV-61 done (S-060): "before a beat" read one way by S06, S09 and S10; S09 carries instants.
- 2026-10-12 — RV-62 done (S-061): the vanish line ends A's support; B draws the volley at 5.1.
- 2026-10-12 — RV-57 done (S-062): hits come from the contacts; S16 holds the camera on each.
- 2026-10-12 — Review 4 (S-063): verdict partially; F-169 to F-186 filed with RV-66 to RV-84; RV-27, RV-33 blocked; RV-64 split.
- 2026-10-12 — RV-66 done (S-064): a substitution exempts only its decoy, the prop at its actor's anchor.
- 2026-10-12 — RV-67 done (S-065): the S04 instructions and the validator teach F-077's rule and O48's log.
