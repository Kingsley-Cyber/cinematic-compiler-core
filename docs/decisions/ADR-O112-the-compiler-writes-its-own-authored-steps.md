# ADR-O112 — The compiler writes its own authored steps (the automatic author)

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner

## Scope
all

## Decision
Owner, in chat, 2026-10-12, after learning that a new idea takes hours of in-session authoring: "the real fix. It
makes the compiler a generator. Every future fight is minutes, not hours. this is what i want." With a pasted design
note (one model call per authored layer, the packet as the prompt, structured output, the checks refuse, the refusal
goes back for up to three retries, the solver where math decides, every call logged and costed), which the owner
called "the soul of what i want, not an in depth exact prompt, its an idea".

## Context
Nine nodes are authored (S04 temporal, S08 hand roles, S11 kinematic, S12 Bartenieff, S13 motion, S14 facial, S15
effort, S16 camera, S17's render plan); a genre runs six to nine of them. The pipeline already raises AuthorRequired
with each step's sealed packet (its instructions, slots and limits) and GateFailed with the findings, so an author is
a loop around what exists. S05-S07, S09, S10 and the render's projection are derived, not authored. S13's keys are
authored poses: the re-block solver repairs them, it cannot invent them.

## Consequences
- PLAN-008 builds the automatic author: `cinematic author "<idea>"` runs the pipeline, hands each AuthorRequired
  packet to a model backend, binds and checks the document, sends a refusal back with the findings (three retries),
  logs every call, and writes the prompts when every step passes.
- The finish run's queue waits behind PLAN-008 (ADR-O110's pause ends with this instruction).
- Live model calls need the owner's choice of backend (the subscription CLI or a paid API with a budget); until then
  only the offline replay backend runs.

## Alternatives Considered
- Keep hand-authoring in session: hours per idea, the opposite of the owner's goal.

## Supersedes
—

## Superseded By
—

## Related
- ADR-O110
- PLAN-008
