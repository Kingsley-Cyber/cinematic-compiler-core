# PLAN-008 — The automatic author: an idea in, a prompt out

<!-- docs-version: 1.0 -->

## Status
in progress

## Owner
owner (ADR-O112)

## Created
2026-10-12

## Updated
2026-10-12

## Intent
Turn the compiler from a checker into a generator. `cinematic author "<idea>"` runs the pipeline; at each authored step
it hands the step's sealed packet to a model, binds the returned document to the packet, runs the step's checks, and
on a refusal sends the findings back for another attempt (three at most). Every call is logged with its step, backend,
model, tokens, cost, time, attempt and result. When every step passes it writes the prompts; when a step fails three
times it stops and shows the owner the step and its findings. One call per authored layer; the packet is the prompt.

How the owner's design note maps onto the code:
| Layer | Today | The author |
|---|---|---|
| S01-S03, S05-S07, S09, S10 | automatic | unchanged |
| S04 beats, S16 camera, S15 effort | authored | a frontier model |
| S08 hand roles, S11 kinematic, S12 Bartenieff, S14 facial, S17 render plan | authored | a cheaper model |
| S13 motion keys | authored | a frontier model writes the poses; the re-block solver repairs overlap, floor and contact refusals before a retry (AA-4) |
| S17 projection | automatic | unchanged |

## Gaps
| Gap | Layer | Severity | Status | Fix |
|-----|-------|----------|--------|-----|
| No step writes itself: a new idea takes hours in session | all | critical | open | AA-1 to AA-4 |

## Dependencies
- ADR-O112; the authored steps' packets and instructions (planner/prompts/*.txt)

## Owner Rulings Needed
- The live backend: the Claude subscription through `claude -p` (no per-call bill), or a paid API with a budget per idea.

## Critical Path
1. AA-1: the loop, the call log and `cinematic author`, proven offline by a replay backend that re-authors the four
   examples from their committed plans byte for byte.
2. AA-2: the subscription backend (`claude -p`, isolated, schema-bound output), after the owner's choice.
3. AA-3: the first live idea end to end; its calls, retries and cost reported.
4. AA-4: S13's refusals repaired by the re-block solver before the model retries.
5. AA-5: a paid API backend, if the owner wants one.
6. AA-6: the author casts any idea. S02 only knows its eight archetype cards, its three worlds and the "X versus
   Y" phrasing; a free idea ("a kunoichi ... on a moonlit rooftop") casts nobody, so S04 has no actor (S-108's first
   live run).

## Verification
- `scripts/verify.sh`; AA-1's replay test; AA-3's run log and prompts, judged by the owner's eyes (R-29)

## Changelog
- 2026-10-12 — Created (S-106, ADR-O112).
- 2026-10-12 — AA-1 done (S-107): compiler/author.py and `cinematic author`; the replay backend re-authors the four
  examples byte for byte; a refusal goes back with its findings; the third refusal stops the run.
- 2026-10-12 — AA-2 done (S-108): the owner chose the Claude subscription; `--backend claude-cli`. Live runs: "a
  kunoichi ... on a moonlit rooftop" cast nobody at S02 (AA-6); "ninja versus knight in a moonlit bamboo courtyard"
  passed S04, S11 and S12 (one retry) and stopped at S13 after three attempts, its overlaps 7, then two contact
  misses, then 2 (the knight's forearm 0.045 m into the ninja's trunk): 7 calls, 910 s, $2.53 at list price on the
  subscription. AA-4 next.
