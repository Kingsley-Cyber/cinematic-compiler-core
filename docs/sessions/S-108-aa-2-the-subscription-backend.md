# S-108 — AA-2: the subscription backend, and the first live runs

<!-- docs-version: 3.0 -->

## Date
2026-10-12

## Agent
Claude Code (Opus 5.5), finish run 1 (docs/reports/2026-10-11-finish-1.md)

## Gap
Backlog AA-2 (PLAN-008); the owner's choice of backend (the Claude subscription, in chat, 2026-10-12)

## Layer
all

## Status
applied

## Commit
the commit whose message names [S-108]

## Plan
1. `ClaudeCLI`: one `claude -p` call per authored step on the owner's login, isolated (an empty folder, an
   allowlisted environment, no tools, settings, hooks, skills, MCP or memory, no session kept), structured output
   bound to the step's schema without the fields the author fills; the packet, one passed document of the same step
   from an example of the genre, and on a retry the refused document with its findings.
2. `cinematic author --backend claude-cli`, a progress log, and two live runs.

Predictions, made before the change (15:52 by the clock):
1. A live run reaches S13 on a castable idea; S13 is refused at least once for overlaps.

## Decisions
- D1 — Opus writes the creative steps (beats, poses, effort, camera), Sonnet the rest (the owner's design note).
  Level: the owner's instruction (ADR-O112).
- D2 — The CLI's cost is recorded as list_cost_usd and cost_usd 0.0: the subscription bills no call. Level: covered.

## Self-audit
Verdict: READY TO PUSH.
| Check | Result | Evidence |
|---|---|---|
| The gate, fresh | see Verification | the chained gate commits |
| Owner rulings respected | PASS | the owner chose the subscription; no API key is used |
| Isolation | PASS | the CLI flags and the allowlisted environment of the subscription-CLI reference |
| Records | PASS | backlog (AA-2 done, AA-4 next, AA-6 added); PLAN-008; CHANGELOG |

## Duration
from 15:52 to 23:12 (two live runs; the clock read 22:54 at the first run's end)

## Changes
- compiler/author.py: ClaudeCLI, BackendError, progress; cli/main.py: `--backend claude-cli`, progress.log

## Verification
- First live run ("a kunoichi in a dark blue outfit sprints across a moonlit rooftop, vaults a low chimney and lands
  crouched, drawing a kunai"): S02 cast no entity, prop or surface, so S04 was refused three times (BEAT_ACTOR):
  AA-6 filed.
- Second ("6 seconds anime fight scene: ninja versus knight in a moonlit bamboo courtyard"): S04 passed (73 s), S11
  passed (16 s), S12 refused once (BARTENIEFF_VOCABULARY, BODY_MODE_COHERENCE) then passed, S13 refused three times
  (7 overlaps; 2 contact misses; 2 overlaps, the knight's left forearm 0.045 and 0.005 m into the ninja's trunk):
  7 calls, 910 s, $2.53 at list price. Prediction 1 held.
