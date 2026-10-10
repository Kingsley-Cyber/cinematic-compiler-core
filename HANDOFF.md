# HANDOFF — cinematic-compiler (core)

Updated 2026-10-10. This folder (`~/Documents/cinematic-compiler-core`) is the working repo: full git history, no
URCP and no Beads. The old `~/Documents/cinematic-compiler` is superseded and can be deleted once you're happy.
No remote; nothing has been pushed.

## Resume in three commands
```bash
mise exec -- uv sync --locked
scripts/check.sh
DO_NOT_TRACK=1 graft --dir .graphs/graft build . --no-gitignore --no-ignore
```

## Built (S01–S07, milestone M1)
| Step | What it compiles | Code |
|---|---|---|
| S01 intent (L0) | query + flags → Intent Document at `/intent`; literal only, evidence per value, `missing`/`ambiguous` | `planner/intent_parser.py`, `compiler/passes/mandatory/p01_intent.py` |
| S02 brief (L0.5) | intent + library cards → `/scene`, entities, props, surfaces; cards only, no model | `planner/query_expander.py` + resolvers, `p02_brief.py` |
| S03 constraint | kernel + world + archetype rules → constraints, constraint_application, `/invariants` | `p03_constraint.py`, `kernel_extraction/control_inventory.py` |
| S04 temporal | authored beat plan (in-session, hash-bound packet) → beats, temporal, beat_constraint, duration | `planner/beat_planner.py`, `planner/dynamic_beat_validator.py`, `p04_temporal.py` |
| S05 causal | beat causes → causal edges (linear) + `scene.quadrant` | `p05_causal.py` |
| S06 state | replay → states per subject per beat + transitions | `solver/prop_state_machine.py`, `validators/continuity_validator.py`, `p06_state.py` |
| S07 contact | contact events, lifecycle, holder/prop-change cross-checks | `p07_contact.py` |

Pipeline: `python -m compiler.pipeline "<query>" [--genre anime] [--until contact] [--plans DIR]`; an authored step
with no plan exits 3 and prints (or `--packet-out`) its packet. Example: `examples/wizard_vs_acrobat/` (through S07).
Kernel = the 68 controls both LBN-2.3-ADV and LBN-2.4-ADV-LMA state (`kernel/sources/`), scoped per item.

## Controls
Three append-only, hash-chained logs (`schemas/schema_log.jsonl`, `library/library_log.jsonl`,
`kernel/kernel_log.jsonl`); generated files checked against regeneration; 167 tests; all in `scripts/check.sh`.

## Owner decisions so far
Step IDs S01–S17 carry order (L labels are names); keys `step_id`/`band`; constraint built after S02 and before
the event graphs; effort (L5) before camera (L5.5); entity definitions at L0.5, state tracks at L2; S01 writes
`/intent`, S02 writes `/scene`; post-generation stays `validation.post_generation`; S02 cards only (no model);
starter cards drafted by Claude; kernel = LBN-2.3 ∩ 2.4; beat plans written in-session (no paid API);
linear causality only; closed kernel state vocabulary. Full log: `docs/layer_dependency.md`, plans in `docs/plans/`.

## Waiting for owner review (draft)
- 11 library cards (`library/`), all `status: draft`.
- `kernel/kernel_scope.yaml`: kernel 20, per-actor 6, per-prop 5, reference fight only 37.

## Open questions and next work
All six questions are decided (see **Decided this round** in
[docs/plans/MASTER_PLAN.md](docs/plans/MASTER_PLAN.md)). Next task: **M1.5** (CLI, replan trigger), then M2. Completed work is struck through
under **Done**.
