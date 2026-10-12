# F-122 — The prompt contradicts itself at the deflect, and S-043's records mis-cite the source

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L6

## Status
resolved

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the second principal review, S-045 (docs/reports/2026-10-12-principal-review-2.md)
- examples/reference_fight/prose_mixed.txt: the kunai track prints "2.50 post-contact ... moving down toward B" (line 124) beside the RULES line "...kunai STAYS IN FRAME,NOT toward B" (line 30); the phrase appears in none of the prompts at 4232a0c
- kernel/sources/lbn-2.3-adv.txt: the rules say "NOT toward B"; A's 2.5 row says "(toward B and ground)"; B's track "kunai reverses toward B and ground"; the kunai track says both "arcs down toward B and ground" and "NOT toward B"
- S-043 D3, F-075's resolution, the CHANGELOG and the DEFLECT_PAIR comment in tests/test_reference_fight_golden.py credit "the source's rule" for "toward B"; PROMPT_CONTRADICTION (M4) passes it

## Description
Since S-043 put B on A's -Z side, the track renderer names B as the deflected kunai's goal, beside the rule that says it is not. The source says both: down toward B's side and the ground, not at B. S-043's records name the wrong part of it.

## Impact
All five prompts carry a reader contradiction at the fight's first hit, pinned by two tests.

## Proposed Fix
Backlog RV-42: one printed reading (down to the ground on B's side, not at B), answered from the sources; the track says "toward X" only where the path reaches X's body; a prompt check refuses "toward X" beside "NOT toward X"; S-043's, F-075's, the CHANGELOG's and the golden comment's words corrected.

## Owner Ruling
ADR-O108 (owner_default; the owner confirms or strikes it)

## Related
- PLAN-007
- F-075
- ADR-O105
- ADR-O77

## Resolution
RV-42 (S-046, ADR-O108): the deflected kunai goes down to the ground on B's side, not at B, and its line reads "moving
down along -Z"; a prop track names a goal only where the prop's path reaches that performer's body
(renderers/prop_samples.py `reaches`; tests/test_prop_track.py::test_a_track_names_a_goal_only_where_the_path_reaches_it);
PROMPT_CONTRADICTION refuses "toward X" where the prompt says "NOT toward X"
(tests/test_prop_track.py::test_a_track_never_says_toward_what_the_prompt_says_not); S-043, F-075 and the CHANGELOG
corrected.
