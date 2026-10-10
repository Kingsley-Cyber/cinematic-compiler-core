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

## Built (S01–S03)
| Step | What it compiles | Code |
|---|---|---|
| S01 intent (L0) | query + flags → Intent Document at `/intent`; literal only, evidence per value, `missing`/`ambiguous` | `planner/intent_parser.py`, `compiler/passes/mandatory/p01_intent.py` |
| S02 brief (L0.5) | intent + library cards → `/scene`, entities, props, surfaces; cards only, no model | `planner/query_expander.py` + resolvers, `p02_brief.py` |
| S03 constraint | kernel + world + archetype rules → constraints, constraint_application, `/invariants` | `p03_constraint.py`, `kernel_extraction/control_inventory.py` |

Pipeline: `python -m compiler.pipeline "<query>" [--genre anime] [--until constraint]`.
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

## Open questions — S04 waits on 1–4; S13 waits on 5–6
1. **Rules on beats:** the catalog says the constraint graph lists the beats each rule applies to, but S03 runs
   before beats exist. Proposal: S04 writes its own beat↔rule edge group.
2. **Positions at L2:** the state graph holds position/orientation, but numbers arrive at S13. Proposal: the S04
   beat plan authors root position and facing per actor per beat (as LBN keys do).
3. **Contact type name:** graph table says touch/**grip**/support/release; catalog and diagram say
   touch/**possess**/support/release.
4. **Actors per beat:** catalog beat has one actor; interactions involve two. Proposal: one `actor` plus `participants`.
5. **Flip axes:** the L4c box says Y=cartwheel, Z=spin; in the kernel frame (Y up, facing +Z) Y is a spin and
   Z is a cartwheel.
6. **Euler XYZ:** intrinsic or extrinsic, and handedness, for the quaternion pass.

## Next
M1 in `docs/plans/MASTER_PLAN.md`: layer_order 1.5 (UGC chain S08→S09→S10), then S04–S07 per
`docs/plans/s04-s07-l1-l2.md`, then the wizard-vs-acrobat courtyard example through S07.
