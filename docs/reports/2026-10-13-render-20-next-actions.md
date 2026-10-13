# Next actions after render R20 (2026-10-13)

<!-- docs-version: 1.0 -->

Ordered by what the owner saw, each asked "does this turn a lie into a truth?" (SOUL.md). Each is a field or a check at
the layer that owns it, then the prompt prints it. Evidence: [confirmation](2026-10-13-render-20-confirmation.md).

## Build (no ruling needed: each fixes something R20 showed)

| # | Fix | Layer | What changes | Kills |
|---|---|---|---|---|
| 1 | Hands declared: each performer's hands empty or holding a named prop at every beat, printed on its staff lines; card invariants and capabilities that name a prop not in the scene are not printed | S06, S03, S17 | possession set per hand from the contacts; p03 scopes card rules to declared props | the kunai |
| 2 | Surfaces placed: every surface gets a position and size in metres (cards, cast drafts, the author); the prompt's spatial anchors print them; a beat that puts a body against a surface is checked against its place | S02, S04, S17 | world card / surface schema, S04 check, [SPATIAL ANCHORS] | the side pillar |
| 3 | One part, one job: refuse a part that strikes and supports at the same instant; a strike's verb says punch, kick, elbow or knee and must match its part | S04/S07 | a contact check; combat verb kinds | the punch-to-leg swap |
| 4 | Impact at contact: a contact may land at a time inside its beat, and the strike line is printed at that time | S04, S07, S17 | beat_plan `at` gains a time | the late impacts |
| 5 | No idle fighter: every performer has a line or an Effort at least every 1.5 s (the DAG's own density rule) | S04, S15 | a per-performer gap check | the frozen knight |
| 6 | Objects named in the prose exist: a weapon or tool in an action (sword, shield) is a declared prop or equipment | S02, S04 | a prose-to-props check; knight equipment | invented objects |
| 7 | Casting covers every hint and matches by name: normalised words, world names, one card per unknown performer | S01, S02, author | casting loop; ground_world | dropped performers |

## Needs the owner

| # | Question | Why |
|---|---|---|
| A | Put SOUL.md in the repo (public) so every session reads it? | The audit found it missing; it is the owner's text |
| B | May the prose print hold frame counts and the camera's position and aim? | O47 kept frame counts out after probes stretched them; the graph has both |
| C | Anticipation, follow-through and reaction as S04 fields (with times) for every strike? | The largest S04 change; it reshapes every beat plan |
| D | Genre style profiles (sakuga and others): which values? | M9-11 is blocked on the owner |
| E | Order: 1-7 first, then C, then the pose step's speed work? | The render loop over the speed loop |

## Then

Re-run an idea, the owner renders, the render log takes the verdict, and the next confirmation starts from it.
