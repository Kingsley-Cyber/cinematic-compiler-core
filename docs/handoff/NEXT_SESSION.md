# Next session — start here

Written 2026-10-11, before a compaction. Read this after the bootstrap block in [HANDOFF.md](../../HANDOFF.md) and
before touching code. The evidence behind every line is in
[docs/findings/2026-10-11-renders-and-dag-adherence.md](../findings/2026-10-11-renders-and-dag-adherence.md).

## The steering prompt (the owner pastes this)

```text
Resume cinematic-compiler-core (~/Documents/cinematic-compiler-core). Before anything else read HANDOFF.md's
bootstrap block, docs/handoff/NEXT_SESSION.md and docs/findings/2026-10-11-renders-and-dag-adherence.md.

Mission: every prompt the compiler emits must provably adhere to my knowledge DAG
(docs/sources/knowledge_dag_v1.md, mapped row by row in kernel/knowledge_map.yaml), used as a checklist. A prompt
that fails any applicable row, or leaves one unchecked, is not a deliverable. Today only 38 of the 84 checklist rows
are verified, and my five renders (R1-R5) failed for exactly the reasons the unverified rows describe: no real
causes, a camera that is not the DAG's, prose far denser than the DAG's own format, and choreography contradictions
inherited from the golden.

Work in this order, one slice per commit, scripts/check.sh green before each commit:
1. If Q1 (scope: prose only or LBN too) and Q2 (not-applicable rulings) in the findings' section 9 are still open,
   ask me both in one question, and build whatever they do not block.
2. M8.10, the checklist: for every prompt, a table of all 84 checklist rows marked PASS / FAIL / NOT CHECKED with
   evidence, written next to the prompt. The gate refuses any prompt with a FAIL or NOT CHECKED row (after the Q2
   rulings). Expect everything red at first; show me the table.
3. Causes: real reasons for reference_fight and live_action_standoff (build on the DAG's D2 causal graph, section
   3.3, and the golden's own words); print the reasons in the prompts; a CAUSE_REASON check refuses placeholders.
4. Camera the DAG's way (C10, and D9's 11-line camera): hits held with both bodies in frame, no limb close-ups,
   height or depth change every 2 s or less; encode C10's rules and forbidden shots as checks.
5. Body and props: grounded pickups (Q5), props hidden until they are used, a wrapped rope dart written as one line,
   the right owner for every prop at t = 0.
6. Density and format (Q4): D9-style staff lines and adaptive density; then every remaining row until all
   applicable rows are green for every prompt.

Rules: take content and density from the DAG's own instances (D6, D9, D10), never invent a format it does not show.
Never say a prompt adheres without its checklist; the conformance test alone is not proof. Predict the result before
each check. No renders, no paid model API, no push without me. Log every schema, library and kernel change. Ask only
where the DAG or my decisions are silent or contradict each other, in one line. When I send a render, log it in
docs/render_log.md bound to the prompt's sha256: my verdict verbatim, your frame notes separate.

Done means: every prompt in scope is green on every applicable row. Then I render one change at a time with a fixed
model and seed, and each result goes into the render log.
```

## Where things stand

| | |
|---|---|
| Repo | HEAD is local; GitHub `main` at `cda5ffe` (M8.4). Everything after is unpushed until the owner says push |
| Built | S01–S17 (layer DAG); K1 knowledge map (109 rows); M8.1–M8.9: four structured-prose modes beside LBN-2.4, 37 prompt codes, conformance test, joint limits, teleport ban, prop p/v under gravity |
| Truth about adherence | 38/84 checklist rows verified per prompt; 46 unverified (findings §8). The conformance test is green but covers only those 38 |
| Renders | R1–R5 of the reference fight, all poor; LBN `render.txt` (R2) the most cohesive. See `docs/render_log.md` |
| Map honesty | C6 (causal graph) was downgraded to partial after R4; mandatory 16/27, required 10/15 enforced |

## Start-up checklist

```bash
git -C ~/Documents/cinematic-compiler-core status --short
```

```bash
cd ~/Documents/cinematic-compiler-core && scripts/check.sh > gate.log 2>&1; echo "exit=$?"
```

```bash
cd ~/Documents/cinematic-compiler-core && DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore
```

Then read, in order: `HANDOFF.md` bootstrap → this file → the findings → `docs/plans/M8_DAG_PROSE.md` →
`kernel/knowledge_map.yaml` rows marked partial or missing.

## Work queue

| # | Slice | Done when |
|---|---|---|
| 0 | Owner answers Q1 and Q2 | Scope and the not-applicable list recorded in MASTER_PLAN as owner decisions |
| 1 | M8.10 checklist per prompt (`validators/checklist.py` or inside the prompt validator; a file per prompt, e.g. `examples/<name>/checklist_<mode>.md`) | Every prompt in scope has an 84-row table; the gate refuses FAIL and NOT CHECKED; the current red state is shown to the owner |
| 2 | Causes (F1, F2, F3) | reference_fight and live_action_standoff carry real reasons; prompts print them; CAUSE_REASON fires on a placeholder; C6 back to enforced |
| 3 | Camera (F4, F5) | The reference camera plan follows C10 and D9 (about 11 shots, holds on hits with both bodies, no limb inserts); C10's rules are codes; C10, C25 green |
| 4 | Body and props (F7–F12) | No airborne ground pickup without the owner's Q5 ruling; props hidden until used; rope dart as one line; counts held; C5 green |
| 5 | Density and format (F6) | Staff lines follow D9 (owner's Q4); C2 bands checked as ranges; prompt sizes recorded |
| 6 | Remaining rows | Every applicable row green for every prompt in scope |
| 7 | Renders | The owner renders one change at a time with a fixed model and seed; each logged |

## Lessons from 2026-10-11 (do not repeat)

- A green conformance test is not adherence: it only covered what had been built. Report the checklist, not the test.
- Placeholders pass structural checks. Every authored "why", description or label needs a check that it says
  something ("<beat> leads straight into the next exchange" passed for a day).
- Don't invent formats. The 21-shot camera, limb close-ups on hits and every-limb staff lines were not in the DAG,
  and they are what broke the renders.
- Copying the golden copies its contradictions (X1–X17). Check the golden against the DAG audit before building on it.
- The owner's renders are the only judge. Bind each to the prompt bytes; keep the owner's words verbatim; frame notes
  are Claude's reading and are labelled as such.
- Tools: `python -m compiler.rebind` reports plans whose packet moved; `--write NAME` re-binds them. Frames from a
  render: `ffmpeg -i video.mp4 -vf "fps=2,scale=432:-1,tile=4x3" sheet_%d.png`; cuts:
  `ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null -`.

## Open owner decisions

Q1–Q8 are in the findings, section 9: scope (prose only or LBN too), not-applicable rulings, reasons in LBN, D9-style
staff lines, grounded pickups, PRESERVE_AXIS, FINAL's four negatives and saving FINAL, the render model and settings.
