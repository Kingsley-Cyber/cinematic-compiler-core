# PLAN-007 — The principal review of 2026-10-11: every gap named, the owner's rulings, the gate

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
| ADR-O89 | An exact-instant miss is not an artefact; re-block B's throw, the palm on the log, the vault hand | RV-02 |
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

The builder reads O89's "genuine airborne or prop-moving misses" as contacts measured between keys or samples (an
interpolated instant); RV-02 carries that reading for the owner to confirm.

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| RV-01 | L6 | high | open | C12 off CONTACT_WORLD (F-074) |
| RV-02 | L4c | high | open | CONTACT_WORLD per O89; releases measured; the vault's hand plant; test hygiene (F-075, F-076, F-079) |
| RV-03 | L1.1 | medium | open | the UGC pickup and poses (F-077) |
| RV-04 | docs | medium | open | records: versions, logs, hook, stale docs and findings (F-078) |
| RV-05 | L4c | high | open | A's words follow the source (F-080) |
| RV-06 | L1.1 | high | open | the vanish (F-081) |
| RV-07, RV-08 | L1.1, L2.1 | high | open | the smoke at 3.7 after commits at the contact's instant (F-082, F-061) |
| RV-09 | L5.5 | high | open | hits as camera holds (F-083, F-005) |
| RV-10 | L1.1 | high | open | the kunai drive and the catch (F-084) |
| RV-11 | L6 | high | open | compile refuses non-deliverables; excluded rows N/A (F-085) |
| RV-12 | L6 | medium | open | the cartwheel's words (F-087) |
| RV-13, RV-13b | L6 | high | open | prompt length (F-088) |
| RV-14 | L4c | high | open | every-key body checks (F-089, F-062) |
| RV-15 | L5.5 | high | open | the camera's aim and vertical framing (F-090) |
| RV-16 | L6 | high | open | one laban chain per fighter (F-091) |
| RV-17 | L2.2 | medium | open | one possession model; PROP_TWO_HOLDERS (F-092) |
| RV-18 to RV-41 | various | medium-low | open | F-093 to F-116 and F-016, one slice each (docs/plans/backlog.yaml) |

## Dependencies
- RV-07 after RV-08; RV-13b after RV-13 and F-088; RV-21 after RV-01; RV-22 after RV-14; RV-35 after RV-02; RV-39
  after RV-11. PLAN-006's AS-01 and AS-07 follow RV-37 (one strike definition at S04).

## Owner Rulings Needed
- F-088: the caps (which prompts carry them, what a capped prompt drops, whether O97 amends R-16)
- F-099: A's backflip at 5.1 launched from the air (O80's "prior beat")
- F-101: which anime spans keep a declared hang and which are re-timed
- F-108: which of B's two kunai releases is real
- F-111: the frame limb and head words are read in
- F-114: whether R-21, R-23 and R-25 bind render.txt
- F-116: whether a moved packet forces re-authoring
- F-117: how F-013 and F-014 close without a fixed seed
- F-118: O37's split cards or the one genre profile (blocks M9-11)
- F-119: how the anti-reward-hacking clause meets R-33 (decides how step 3 treats every test pin)
- RV-20: an ADR for the layer-order edit; RV-38: the owner's review of draft values and F-053

## Critical Path
1. Step 3, the builder's own shortcuts first (only on the owner's "go"): RV-01, RV-02, RV-03, RV-04
2. The owner's rulings: RV-05, RV-06, RV-08, RV-07, RV-09, RV-10, RV-11, RV-12, RV-13
3. The fight-breakers that need no ruling: RV-14, RV-15, RV-16, RV-17, RV-37, RV-35, RV-22
4. The rest in backlog order: RV-18, RV-19, RV-21, RV-23, RV-25, RV-27 to RV-32, RV-34, RV-39, RV-41
5. Then PLAN-006 (AS-01 to AS-07) and PLAN-003's remaining M9 slices
6. Waiting on the owner: RV-13b, RV-20, RV-24, RV-26, RV-33, RV-36, RV-40; the owner's own: RV-38

## Verification
- Each slice: `scripts/verify.sh` and `make golden`, its predictions reported, the self-audit; tests change only on the
  owner's explicit ask (AGENTS.md section 18, F-119); a second principal review before the next release (O98's
  soul_check_passes).

## Changelog
- 2026-10-11 — Created from the first principal review (S-035) and the owner's rulings O88 to O100.
