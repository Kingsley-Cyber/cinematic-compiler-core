# S-013 — M9-07a: combat verbs on contacts (F4.1, O22)

<!-- docs-version: 2.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5), autopilot run 1 (docs/reports/2026-10-11-autopilot-1.md)

## Gap
Backlog M9-07a (split from M9-07; PLAN-003 F4.1); ruling O22 (effort stays Laban; combat verbs go on contacts)

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-013]

## Plan
The action word lives only in beat labels ("foot_deflect_kunai"), and the Laban effort carries none (O22: punch =
thrust). Contacts gain an optional `verb` from a closed list (contact 1.1, embedded in beat 1.2, beat_plan and
temporal_graph 1.5; contact_graph 1.1 for the S07 nodes; all logged). A draft vocabulary card
(`library/combat_verbs.yaml`, library log) lists which verbs each contact type takes; S04 receives it in its packet and
refuses a verb its contact type does not take, a throw, catch or disarm that names no prop, and a throw whose prop is
not moving at that instant (CONTACT_VERB). S07 carries the verb into its contact nodes, and the staff prints it in
capitals before the bow ("DEFLECT [DOUBLE BOW + accent: R foot > kunai blade]"), with a legend line when a prompt has
one. The reference fight's five contacts its own words name get their verbs.

Predictions, made before the change:
1. The gate passes before the change: 598 tests.
2. The S04 packet changes (the card), so `compiler.rebind --write` re-seals all four examples' S04 plans and nothing
   after them moves; no example refuses.
3. CONTACT_VERB fires on no example with the five verbs authored, and on each break.
4. The reference fight's five prompts gain THROW at 2.00 and 5.50, DEFLECT at 2.50, STRIKE at 4.00 and 4.70, and one
   legend line; the other examples' outputs do not change.
5. No checklist row changes result (no prompt code).
6. About 602 tests.

## Decisions
- D1 — Split M9-07 into M9-07a (F4.1 at S04, with its own print) and M9-07b (F4.2 at the render step); backlog 3.
  Why: the backlog's rule (split per step); F4.2 is wording only. Alternatives: one slice (two steps). Level: covered.
- D2 — The verb list is the plan's F4.1 list: strike, deflect, parry, catch, redirect, trap, bind, disarm, throw,
  grapple. Why: O22 names nine and leaves out strike, which the plan's list has and the golden's own words use
  ("knee_strike_spine"); the plan was approved with O22 ("all recommended"). Alternatives: O22's nine only (no verb for
  the fight's two strikes). Level: interpretation (Claude's, for owner review; added to F-053).
- D3 — Which contact type takes which verb (the card): touch takes strike, deflect, parry, redirect, trap, bind,
  disarm, grapple, throw; possess takes catch, trap, bind, disarm, grapple; release takes throw. A throw names a prop
  that is moving at that instant (a sample with velocity there, the post one of a pair); catch and disarm name a prop.
  Why: F4.1 ("catch must be followed by a possess, throw by a release"); the fight throws the shuriken volley with a
  touch, not a release, so a throw is read physically (the prop leaves moving). Alternatives: throw on releases only
  (the volley's throw could not carry its verb). Level: interpretation (Claude's, for owner review; added to F-053).
- D4 — Verbs go only where the golden's words name one on that contact: b05 throw, b06 deflect, b10 strike ("palm
  hits"), b12 strike, b14 throw; recorded in the golden test. Why: O22 and the slice text cover adding the verb;
  ADR-O71 rule 1. B's "catch_elbow_throw" on A's arm (a catch of a body, which the card keeps for props) and the
  contacts whose subject is the body being hit (b19, b21) stay without one. Alternatives: grapple on b17 (a word the
  golden does not use). Level: covered (O22, F4.1, O71); the choice per contact is Claude's, added to F-053.
- D5 — The staff prints the verb in capitals before the contact's bow or bracket, and the legend gains one line only
  in prompts that have a verb. Why: F4.1's printed form ("DEFLECT: R foot (sole) > kunai blade"), placed outside the
  brackets the existing checks parse; a conditional legend keeps the other examples unchanged. Level: covered (F4.1).
- D6 — IMPACT_CONTACT_SYNC's reader strips a leading capitalised verb before it reads a bow (VERB_MARK). Why: the
  verb before "[DOUBLE BOW" hid the strikes from the check (twelve findings on the reference prompts, C21 to FAIL);
  the reader must read the new form, and the check itself is unchanged. Alternatives: print the verb after the
  bracket (a second place every reader would need to learn). Level: covered (R-17's "fix the check" side: the content
  is right, the reader was not).
- D7 — S04's packet now names beat_plan 1.5 (it named 1.3 after S-009 bumped the file to 1.4), and a new test ties
  every packet's pinned schema id to the file on disk. Why: the packet must say which contract the author writes to;
  S-009 missed the constant (lesson L-21). Level: covered.
- D8 — R-27's enforcement lists CONTACT_VERB and the planned M9-07b (rules 2.1, enforcement only, +0.1). Why: R-27's
  source is O22 and its enforcement read "planned: backlog M9-07". Level: covered.

## Duration
about 60 minutes

## Changes
- schemas: `contact` 1.1 (verb), `beat` 1.2, `graphs/beat_plan` and `graphs/temporal_graph` 1.5 (embedded),
  `graphs/contact_graph` 1.1; five schema-log entries
- `library/combat_verbs.yaml` (new, draft; library log); `planner/beat_planner.py` (packet `combat_verbs`, SCHEMA_ID
  1.5); `planner/prompts/beat_planning.txt` (the verb line); `planner/dynamic_beat_validator.py` (CONTACT_VERB,
  `_thrown`); `compiler/passes/mandatory/p07_contact.py` (the verb reaches the contact nodes)
- `renderers/prose_renderer.py` (the verb before the bow; the legend line); `validators/prompt_validator.py`
  (VERB_MARK)
- `examples/reference_fight/plans/temporal.json` (five verbs); every example's S04 plan re-bound; outputs and
  checklists regenerated
- tests: three breaks and a throw test (test_dynamic_beat_validator), CONTACT_VERBS (golden), test_packet_schema_ids
  (new); `kernel/knowledge_map.yaml` C21 (kernel log); `docs/rules.yaml` 2.1 (docs log)
- F-053, backlog (M9-07 split, version 3; M9-07a done, M9-07b next), CHANGELOG, lessons L-21, the run report

## Verification
- before: `scripts/verify.sh` exit 0, 598 passed (the pre-commit gate of S-012, ef63600)
- after: `scripts/verify.sh` exit 0, 604 passed; `make golden`: the reference fight's four prose prompts
  changed on purpose (five verbs, one legend line); render.txt and the other examples' prompts unchanged
- Prediction 1 held. Prediction 2 held (the four S04 plans re-bound, nothing after them). Prediction 3 held.
  Prediction 4 held for the four prose prompts; render.txt did not change (the LBN does not print verbs), so four
  prompts, not five. Prediction 5 failed first: the verb hid the strikes from IMPACT_CONTACT_SYNC (C21 FAIL on four
  prompts) until D6; then no row changed result. Prediction 6: 604, not about 602.

## Next
M9-07b (F4.2 Laban actions printed as qualities).
