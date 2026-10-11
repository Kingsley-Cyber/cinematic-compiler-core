# S-003 — M9-02: strike, throw and release contacts at their pose (IMPACT_CONTACT_SYNC)

<!-- docs-version: 1.0 -->

## Date
2026-10-11

## Agent
Claude Code (Opus 5.5)

## Gap
Backlog M9-02; findings F-021 (GAP-06), F-031 (GAP-16); ruling ADR-O23

## Layer
L1.1

## Status
applied

## Commit
the commit whose message names [S-003] (approved by the owner after the diff review)

## Plan
One time per hit (O23). Data at S04 (the layer that owns contact times): the reference fight's strike, throw and
release contacts move to their key pose with `at: start` (b05 throw 2.0, b06 deflect 2.5, b10 palm 4.0, b12 knee 4.7,
b14 shuriken 5.5, b17 catch 6.6, b21 kunai drive 8.5); prop samples follow so the kunai flies 2.0-2.5 and the log
falls 4.0-4.4 under gravity. Check at S17, the first step that sees both contacts and impact frames:
IMPACT_CONTACT_SYNC refuses an impact frame with no touch or support onset on it, and a strike touch off every impact
frame; the same code reads the prompt. A support onset counts as an impact's contact (a body hitting a surface: the
9.0 crash, the wizard's 5.2 slam); that reading is an interpretation. The strike definition moves into one helper
shared by the renderer and the check. The prose adds V1b's tested words to each strike's recovery line: "one instant
contact, the limb does not stay on the target" (R16).

Predictions, made before the change:
1. The strike helper refactor leaves all 20 prompts byte-identical.
2. Before the data change, IMPACT_CONTACT_SYNC fires on the reference fight only: impacts 2.5, 4.7, 5.5, 6.6 and 8.5
   with no contact on them, and strikes at 3.00, 5.10, 5.90 and 7.00 (twice) off every impact; the 9.0 impact passes
   on its support onsets and the 9.00 kunai touch sits on it. Wizard, live action and UGC stay silent.
3. After the data change the compile may refuse at S06/S07 (the kunai's holder B while its possess ends at 2.0) and
   at S04 (PROP_KINEMATICS: the kunai needs a release sample at 2.0, the log falls 4.0-4.4 with no contact at 4.4).
4. Only the reference render.txt changes (contact times, prop tracks); the other three examples stay byte-identical.

## Duration
about 1.5 hours

## Changes
- `examples/reference_fight/plans/temporal.json`: `at: start` on b05 (throw 2.0), b06 (deflect 2.5), b10 (palm 4.0),
  b12 (knee 4.7), b14 (shuriken 5.5), b17 (catch 6.6, both hands), b21 (kunai drive 8.5); kunai samples 2.0 / 2.5 / 2.9,
  the 3.0 sample removed; the log falls from 4.0 (v [0, -0.29, 0])
- `examples/reference_fight/plans/camera.json`: c10, c12, c14, c17 motivated by their own beat (their cut no longer
  sits on a contact); c20's insert shows B's torso, where the kunai lands (coupling)
- `compiler/passes/derived/p17_render.py`: `impact_sync` (IMPACT_CONTACT_SYNC); `renderers/prose_renderer.py`:
  `strike_contacts` shared by the staff and the check, V1b's words on each strike's recovery line
- `compiler/passes/mandatory/p07_contact.py`: a release at its own beat's start still holds at that instant
- `validators/prompt_validator.py`: IMPACT_CONTACT_SYNC on the prompt; `kernel/knowledge_map.yaml` C21 (logged)
- tests: S07 boundary both ways, S17 break, conformance break, golden CONTACTS_AT_POSE; three tests pinned to the old
  late times updated; `kernel/docs_plane.py` code links follow the tree being checked
- findings F-021 resolved, F-031 progress, F-061 new (holder change prints at the beat's end)

## Verification
- `scripts/verify.sh` before the change: pass; after: pass (579 tests)
- Predictions: (1) the strike helper left all 16 prose prompts byte-identical: held. (2) Before the data change the
  check fired on the reference fight only, on exactly the 5 impact frames and 5 strikes named: held. (3) S07 refused
  with HOLDER_CONTACT on kunai@b05: held (fixed at S07, see Changes); S16 also refused (four cut motivations, one
  coupling), which I had not predicted. (4) Only the reference render.txt changed: held.
- `make golden`: render.txt changed on purpose for the reference fight only (contact times, three prop tracks, five
  camera rows; A's roots and joints unchanged); checklists: no row moved to PASS; C21's LBN cell went NOT CHECKED to
  FAIL in all four examples (LBN has no staff section for the new code to read)

## Next
M9-03 (F6.3 grounded pickups).
