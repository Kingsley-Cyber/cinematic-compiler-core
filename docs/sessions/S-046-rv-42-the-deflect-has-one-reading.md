# S-046 — RV-42: the deflect has one reading; a track says "toward X" only where the path reaches X

<!-- docs-version: 2.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog RV-42 (PLAN-007); finding F-122; rulings O77, O102, O105, O107, O108 (new)

## Layer
L6

## Status
applied

## Commit
the commit whose message names [S-046]

## Plan
F-122: since S-043 every reference prompt prints "2.50 post-contact ... moving down toward B" beside the rule "...NOT
toward B", and S-043's records credit "the source's rule" for "toward B". The source says both: A's 2.5 row, B's track
and the kunai track send it "toward B and ground", the rules and the kunai track say "NOT toward B".
1. Answered from the sources (ADR-O108): the deflected kunai goes down to the ground on B's side and is not aimed at
   B; printed as its direction (along -Z, down), not as a goal.
2. The track renderer (renderers/prop_samples.py) says "toward X" only where the prop's free flight from the sample (to
   its next sample or the ground) passes within 0.3 m of one of X's body points, nearer than it starts; a pre-contact
   sample describes its arrival and names no goal. The old rule named whoever the horizontal velocity pointed at.
3. PROMPT_CONTRADICTION also refuses a prop track that says "toward X" where a RULES clause about that prop says "NOT
   toward X".
4. The records corrected: S-043 (a correction note), F-075, the CHANGELOG, the golden comment.

Predictions, made before the change:
1. The gate passes before the change: 646 tests (e1aa736).
2. With the check alone, the reference prompts are refused (PROMPT_CONTRADICTION, the kunai); after the renderer
   change the kunai's post-contact line reads "moving down along -Z" and the 2.0 throw still "moving up toward A".
3. Only the reference fight's outputs change; no other prop's words move (the volley, the pellet and the dart already
   name no goal; the UGC glasses are held or at rest).
4. 648 tests (a path test and a break); the deflect pair's two pins move with ADR-O108 (ADR-O102).

## Decisions
- D1 — The deflect's reading answered from the sources (ADR-O108): down to the ground on B's side, not at B. Why: the
  source says "toward B and ground" (A's row, B's track, the kunai track) and "NOT toward B" (the rules, the kunai
  track); read together they name a side, not a target. It sets aside no owner ruling (O77 fixes the reversal to -Z), so
  R-06 lets the run answer it. Level: owner_default ADR, for the owner to confirm.
- D2 — "toward X" now means the prop's free flight reaches X: within 0.3 m of one of X's body points at the key nearest
  in time, and nearer than it starts by 0.1 m; a pre-contact sample names no goal. The old rule named whoever the
  horizontal velocity pointed at, whether or not the prop got there. Interpretation (the two distances, for the owner).
  Alternatives: keep the angle rule and special-case the deflect (a patch, not a rule). Level: covered (F-122).
- D3 — PROMPT_CONTRADICTION reads every section's clauses for "NOT toward X" about the prop, since the source's rule is
  printed on A's staff line, not under RULES. Level: covered.
- D4 — The dead `_anchors` helper goes with the old rule. Level: covered.
- D5 — Tests: the deflect pair's two pins move with ADR-O108 (ADR-O102, confirmed by the owner); a path test and a
  contradiction test are new; the contradiction break is its own test, as the conformance test allows one BREAKS entry
  per code. Level: covered.

## Duration
about 40 minutes

## Changes
- renderers/prop_samples.py (`bodies`, `reaches`, `motion_words`), validators/prompt_validator.py (the NOT-toward check)
- examples regenerated (the reference fight's kunai line)
- tests: test_prop_track (two new tests), test_reference_fight_golden and test_dynamic_beat_validator (the pins)
- kernel/knowledge_map.yaml version 3 (locator; kernel log); ADR-O108 (new); F-122 resolved; S-043, F-075 and the
  CHANGELOG corrected; backlog (RV-42 done, RV-43 next)

## Verification
- before: 646 passed at e1aa736 (S-045's gate)
- with the check alone: PROMPT_CONTRADICTION on all four reference prose prompts ("kunai: its track says toward B where
  the prompt says NOT toward B")
- after: `scripts/verify.sh` exit 0, 648 passed; `make golden` passed; `compiler.rebind` silent; only the reference
  fight's outputs changed
- Prediction 1 held. Prediction 2 held (the check fired on the old prompts; the throw still reads "moving up toward A",
  the deflect "moving down along -Z"). Prediction 3 held. Prediction 4 held (648; the two pins moved with ADR-O108).

## Next
RV-43 (CONTACT_WORLD exceptions from an owner-held list).
