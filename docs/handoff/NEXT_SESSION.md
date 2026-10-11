# Next session — start here

Written 2026-10-11 (end of session), before a compaction. Read after the bootstrap block in
[HANDOFF.md](../../HANDOFF.md). Evidence: [the findings](../findings/2026-10-11-renders-and-dag-adherence.md),
[the render log](../render_log.md). Decisions: [MASTER_PLAN](../plans/MASTER_PLAN.md) (O1-O21).

## The steering prompt (the owner pastes this)

```text
Resume cinematic-compiler-core. Work in the worktree ~/Documents/ccc-m810 (the main folder holds another session's
uncommitted files; fast-forward main after each commit). Read HANDOFF.md's bootstrap block, this file,
docs/plans/MASTER_PLAN.md (M9; decisions O22-O46) and docs/plans/deconfliction_2026-10-11.md (fixes F*, FR*, FP* with
files, current behaviour, gap, enhancement, priority, dependencies).

Build M9 by the FINAL plan v1.0 (deconfliction doc, section 9), one slice per commit, scripts/check.sh green before
each: first the W wording rules from the probes (W1-W4, O47-O49; O48's post), then F5.3 strike timing with V1b's
deflect wording (IMPACT_CONTACT_SYNC), then F6.3 grounded pickups, F2/F6 prop physics and positions, FR.1/FR.3, and on.
Model-agnostic, built for Seedance, no model cards (O49). Rule O46: test the uncertain, build the
certain. Build every check and data change now; the printed wording of a fix whose probe (V1-V6) has no result yet
follows the probe's wording, and changes if the owner's render of that probe fails. Each slice: predict, add the check
with two or three breaks plus a should-not-fire run over every prompt, fix content as a recorded golden deviation where
O22-O44 say so, re-bind, rewrite the examples, keep render.txt byte-identical unless the slice is meant to change it,
rewrite the checklists, report the rows that went from NOT CHECKED to PASS. Never edit authored data silently (O39).
F4.6 uses O50's five callbacks; the opening slice uses V6's wording (R19, O51). Place every check at the first step
that can see its data (`docs/findings/2026-10-11-layer-order-verification.md`; plan v1.2). Log the owner's probe renders against the probe sha256 values. No
renders by Claude, no paid API, no push without the owner.
```

## State (exact, 2026-10-11 end)

| | |
|---|---|
| Repo | Local `main` = `fdb29ce`, 9 commits ahead of GitHub `main` (`16ff68c`, tag `checkpoint-2026-10-11-m8.9`). Not pushed |
| Gate | `scripts/check.sh` exit 0, 553 tests (run in the worktree; the main folder's gate also runs the other session's uncommitted `knowledge_dag.json --check`, which is stale) |
| Built this session | M8.10 checklist · M8.11 causes · M8.12a honesty rule · b prop first states · c the rope line · d counts · e X9 vanish · f X5/X6 turns |
| Prompt codes | 44 (`validators/prompt_validator.CODES`), each with a break in `tests/test_dag_conformance.py` |
| Checklist | 0 of 20 prompts deliverable. Reference fight prose: 30 PASS / 0 FAIL / 48 NOT CHECKED / 6 N/A; LBN 3 / 48 / 27 / 6. Other examples' prose 37-38 PASS |
| Reference fight, NOT CHECKED because a render contradicts them | M1 (F10), M4 (F3), C1 (F14), C2 (F6, F14), C3 (F6), C4 (F6), C9 (F10, F13), C23 (F13) |
| Reference fight, NOT CHECKED otherwise | 14 rows with unbuilt gap codes (LMA BIO KC KF T6 T7 T10 C5 C8 C18 C21 C22 C25 V7); 21 with no check (C10 C20 V1 V2 V3 V6 V9-V13, ten excluded rows); STY, C12 (graph only); V4, V5 (menu, nothing selects); P3.2-6 (Q6) |
| Unbuilt gap codes | ANTICIPATION_MISSING, CHAIN_ORDER, MOMENTUM_MISSING, OPPOSITION, PHRASING_MISSING, POST_CONTACT_MISSING, PROP_TWO_HOLDERS, SHOT_TRANSITION_MISSING, WEIGHT_TRAVEL |
| Branches | Worktree `~/Documents/ccc-m810`: `m8.10-checklist`, `m8.11-causes`, `m8.12-harden` (= `main`). Keep working there while the other session's files sit uncommitted in the main folder |

## Commits this session

`78a7e6e` M8.10 checklist · `664cf16` M8.11 causes · `63113ca` M8.12a no PASS a render contradicts, O15/O16 ·
`8d169c5` M8.12b first states · `9204ff5` M8.12c rope line, doubled words · `e194c28` M8.12d counts, O17-O20 ·
`10bb1a5` M8.12e X9 vanish, O21 · `fdb29ce` M8.12f X5/X6 turns.

## Probes waiting for the owner's renders (O46)

Six 5 s prompts in `docs/render_tests/2026-10-11-m9-probes/` (README: question, scorecard, sha256 each): V1 deflect on
time (F5.3, F5.1/F5.2, F4.1/F4.2, F2), V2 hidden log and substitution (F6.1, causes), V3 one backflip (FR.1/FR.3), V4
apex hold (FR.6), V5 hit held with both bodies + crane (C10, F8.1), V6 opening from above (O21). Then one full-fight
render after the build (D9 lines, camera, part 3 words). No fixed seed.

## Incomplete work, with resume steps

The owner's plan was deconflicted on 2026-10-11 (docs/plans/deconfliction_2026-10-11.md, O22-O44): its build order in
MASTER_PLAN M9 supersedes the order below. Item 1 = F6.3, item 2 = the O21 opening, item 3 = O19 D9 lines, item 4 =
camera C10 + FR.5, item 5 = the applicability stage (O16), item 6 = the gap codes inside F9.x and FP.x.

| # | Item | Decision | Remains to do | Check to add | Closes |
|---|---|---|---|---|---|
| 1 | Grounded pickups (audit X2/X3) | O18 (answers Q5) | Reference fight b18-b20: A lands by the rope dart (on the ground at `[0.4, 0, 3.8]` since 5.9) before taking it at 7.5, and by the kunai (`[0.3, 0, 5.3]` since 3.4) before taking it at 8.0. Re-author S04 pos/support, S11 support, S13 crouch-and-reach keys (joint limits), S16 geometry if a check trips, S17 frame parts; reword b17's reason ('snatching up the rope dart on the way down'); record the A rows at 7.5 and 8.0 in the golden test | AIRBORNE_PICKUP (S04 or S07 and a prompt code): a possess contact on a prop resting on a surface needs its holder supported and within reach then | F7 on BIO, T7, C5 |
| 2 | Opening (audit X7) | O21 | Query 'falling from y=10' (request.json; record the preface item 'A starts ABOVE the frame, falling from y=8' in the golden test, like PREFACE_RECOUNTED); b01 A root `[0, 10, 3.5]`; b02 landing root about `[0, 8.5, 5.8]`, feet on the 8 m top; S11/S13 keys; prop samples near A; the first shot must not frame A at 0.00 (goes with the camera, item 4) | A support on a surface puts the feet at its top: needs numeric surface geometry (the world card `bamboo_courtyard_pillar` gives only the text 'pillar at z=6 from y=0 to y=8'; a library change, logged) and/or S01 parsing the query's literal starts (O16) | F10 on M1, C9 |
| 3 | D9 staff lines and density | O19 (answers Q4) | `renderers/prose_renderer.staff_lines`: name only the limbs that move or touch (D9's lines run ~120-200 characters); density adaptive per C2 (dense 0.25-0.4 s on impacts and support changes, medium 0.6-0.9, sparse 0.8-1.5, max gap 1.5); LBN keeps every number | A density/verbosity code measured against D9's own lines | F6 on C2, C3, C4 |
| 4 | Camera the DAG's way | queue item 4 | Reference camera.json from 21 shots to the D9 shape (about 11 lines): holds of 3-5 frames on hits with both bodies in frame, no limb inserts, height or depth change every 2 s or less, orbits/crane/dolly; first shot leaves A above the frame | C10's six rules and three forbidden shots as S16 checks and prompt codes; SHOT_TRANSITION_MISSING | C10, C25, V3, V6; F4, F5, F15 |
| 5 | Applicability stage | O16 | From S01/S02 data: rows that apply and what each demands, the V4/V5 choice, the questions the prompt leaves open, before authoring; never rewrites the owner's words | Checklist splits 'applies, unbuilt' from 'does not apply' | V4, V5 and the menus |
| 6 | Remaining gaps | — | The nine gap codes above; V-rows; checks for the excluded rows; STY and C12 in the prompt text | one code each | the rest |
| 7 | F3 on M4 | to ask | M4 now carries DOUBLED_WORD, COUNT_CONTRADICTION, VANISHED_BODY, TURN_LABEL (the DAG's X-audit classes); after items 1-2, ask the owner whether these catch F3 | — | M4 |
| 8 | F13, F14 | O20 | Stay NOT CHECKED until a fixed-seed render repeats or clears them | — | C9, C23, C1, C2 |

## Deconfliction protocol (the owner's plan against this repo)

1. **Inventory to compare against** (read, don't recall): MASTER_PLAN decisions (Q, A, B, F, O1-O21) and milestones;
   `kernel/knowledge_map.yaml` (status, codes, gaps, not_applicable, applies_when per row); `kernel/layer_order.yaml`
   (S01-S17, reads/writes); `validators/prompt_validator.CODES`; `examples/*/checklist.md`; golden deviations in
   `tests/test_reference_fight_golden.py`; `docs/render_log.md`; the open questions Q3, Q6, Q7, Q8.
2. **Classify each plan item** DONE / PARTIAL / MISSING / CONFLICTS, with evidence a reader can open (file:function,
   commit, test, checklist row). "Done" means a check plus a test that fails when it is broken, not text in a doc.
3. **Precedence:** the owner's newest explicit words > owner decisions O1-O21 (a contradiction becomes a one-line
   question, never a silent override) > the DAG map > existing code.
4. **Never drop built work silently:** if the plan supersedes a check, a renderer or a plan edit, list it as
   "superseded by plan item N" and ask before removing it.
5. **Write** `docs/plans/<date>-plan-deconfliction.md`: item table, merged plan, questions. Commit it as its own slice
   once the gate is green.

## Where the code is

| Concern | File · function |
|---|---|
| Checklist (84 rows × 5 prompts + union, honesty rule) | `validators/checklist.py` · `evaluate`, `judge`, `findings_for`, `contested`, `union`, `FINDINGS` |
| Prompt checks | `validators/prompt_validator.py` · `CODES`, `READS`, `unread`, `check`, `_first_state_checks`, `_line_and_word_checks`, `_count_checks`, `_vanish_checks`, `_turn_checks` |
| Causes | `validators/cause_reason.py`; S05 `p05_causal.reason_findings`; prose `_causal` ('Why each link holds:') |
| First states, contacts at a beat's start | `validators/continuity_validator.first_states`; `p07_contact.contact_time`; `dynamic_beat_validator._at`, `holds`; prose `first_states` |
| Vanish (substitution gap) | `dynamic_beat_validator.vanish_windows`, `_vanished`; prose `vanish_rules`; S13 exemption in `euler_solver.check` |
| Named turns | `euler_solver.named_turn`, `named_turn_findings` |
| Rope line, prop part names | prose `line_links`, `_target` |
| Map fields | `kernel/knowledge_map.yaml` (`not_applicable`, `applies_when`); guarded by `tests/test_knowledge_map.py` |

## Start-up

```bash
git -C ~/Documents/cinematic-compiler-core status --short
```

```bash
cd ~/Documents/ccc-m810 && scripts/check.sh > gate.log 2>&1; echo "exit=$?"
```

```bash
cd ~/Documents/cinematic-compiler-core && DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore
```

```bash
cd ~/Documents/cinematic-compiler-core && graphify update .
```

```bash
cd ~/Documents/ccc-m810 && mise exec -- uv run --locked python -m validators.checklist
```

## Lessons from 2026-10-11 (do not repeat)

- A green conformance test is not adherence; report the checklist. A PASS a render contradicts is NOT CHECKED until a
  code catches what the render saw.
- Silence is not a pass: a code that reads a section fails when the prompt lacks that section.
- Placeholders pass structural checks. Every authored 'why', label or description needs a check that it says
  something (CAUSE_REASON caught 25 placeholder reasons).
- Run a new check on every prompt before wiring it: the first count regex fired on times ('2.50 kunai') and a legend
  ('one performer').
- Don't invent formats; take content and density from the DAG's instances (D6, D9, D10). Where the DAG is silent and
  the owner's instruction needs a format, ask in one line (O15: the 'Why each link holds:' lines).
- The kernel quotes the golden. Change the scene through recorded deviations in the golden test, never the kernel file.
- A fix in one plan can trip a later step's check (the camera framing a vanished body): fix it there and re-bind.
- Copying the golden copies its contradictions; check it against the DAG's audit (X1-X41) first.
- Parallel sessions share the folder: work in a worktree, fast-forward `main`, never touch their files.
- The owner's renders are the only judge: bind each to the prompt's sha256, keep the verdict verbatim, frame notes apart.

## Open owner questions

Q3 (print reasons in LBN-2.4), Q6 (P3.2-6 PRESERVE_AXIS), Q7 (FINAL's four negatives; save FINAL verbatim), Q8 (the
render model and settings). F3's status on M4 after items 1-2.
