# cinematic-compiler: Claude Code context

After a context compaction or in a new session, start with [docs/bootstrap/README.md](docs/bootstrap/README.md)
(`/bootstrap`): the resume steps, the generated state, the environment, the working agreements and the lessons. Then
read [AGENTS.md](AGENTS.md) fully and follow its nine-step session protocol: the five indexes in `docs/index/`,
`scripts/verify.sh` before and after every change, one gap per commit at the layer that owns it, the self-audit
(`/self-audit`) before asking the owner to commit or push. Navigate with graft and graphify (`make graphs`) before
reading files. The owner renders; never render, never call a paid model API, never push without the owner.

## The gate (owner, 2026-10-11)

```yaml
gate:
  - layer_order_matches_plan
  - rules_match_dag
  - golden_passes
  - no_shortcuts_survive
  - soul_check_passes        # NEW
  - fight_works              # NEW
```

The owner's definition of done (ADR-O98). `scripts/verify.sh` enforces only part of it today; PLAN-007 names what each
item still needs. A shortcut never passes the gate: fix the cause at the layer that owns it, name the gap as a finding
with a backlog slice, or ask the owner and wait (the no-shortcuts principle, docs/prompts/no_shortcuts.md).

## Anti reward hacking (owner, 2026-10-11)

The owner's clause, word for word (ADR-O100):

```text
<anti_reward_hacking>
The objective is to correctly implement the requested behavior, not merely
produce a passing score.

Rules:

1. Treat existing tests, assertions, fixtures, expected outputs, evaluators,
   and verification code as immutable unless the user explicitly asks to
   change them.

2. Never delete, skip, disable, weaken, mock away, or rewrite a failing test
   merely to make the test suite pass.

3. Never:
   - hardcode visible test inputs or expected outputs;
   - add test-only branches to production code;
   - redefine equality, comparison, hashing, or serialization to fool checks;
   - suppress exceptions, warnings, failures, or timeouts to create false success;
   - tamper with exit codes, coverage results, snapshots, fixtures, or test discovery;
   - inspect, reconstruct, or copy hidden evaluation answers;
   - copy a known solution when independent implementation is required.

4. When a test fails:
   - diagnose the runtime cause;
   - fix the implementation;
   - rerun the original test;
   - verify that the solution generalizes beyond the visible example.

5. If the specification and tests conflict, stop and report the exact conflict.
   Do not change either side without explicit user direction.

6. Report verification honestly. Include the command run, its result, and any
   remaining failures. A failing test with an accurate diagnosis is preferable
   to a passing test obtained through a shortcut.

Before declaring completion, confirm:
- existing tests and evaluation files are unchanged;
- no tests were skipped or removed;
- the implementation satisfies the requested behavior;
- the original relevant tests pass.
</anti_reward_hacking>
```
