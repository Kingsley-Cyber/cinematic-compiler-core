# ADR-O109 — In-between keys on the repo's side where the declared interpolation draws a body through another or under the floor

<!-- docs-version: 1.0 -->

## Status
accepted

## Date
2026-10-12

## Decided By
owner_default

## Scope
L4c

## Decision
Answered from the sources under ADR-O101 (finish run 1, S-090, after principal review 7; F-220 option a): where the
declared interpolation between two of an entity's keys draws its body through another body, or a point more than 0.15
m under the floor, and no re-pose of the repo's keys inside their joint limits clears it with every contact inside
O72's 0.15 m, the repo adds explicit keys between them on its own side. An in-between key is one entity's pose at an
instant between two of its keys, with no beat and no contact of its own; it is checked like a key (joint limits, the
floor, the bodies, its supports) and printed in the prompt with its instant. In-between keys are densest around
impacts and support changes, as the DAG's density tiers say, and never every frame. The owner's rows (A in the
reference fight) get none: a span only the owner's rows could clear stays the owner's question (F-220 options b and
d).

## Context
- docs/sources/knowledge_dag_v1.md:253, the density tiers: "Dense | High-precision moments (kunai deflect, knee
  strike, kunai drive, substitution) | every 0.25–0.4 s".
- docs/sources/knowledge_dag_v1.md:257, D4's density_rules: "Use dense explicit keys (every 0.3–0.5s) during aerials,
  prop interactions, and impacts"; "Never leave more than 1.5s without either an explicit key".
- docs/sources/knowledge_dag_v1.md:259, D9: "Dense (explicit) on every support change, contact bow, accent, and aerial
  peak".
- docs/sources/knowledge_dag_v1.md:261, D4's final recommendations: never make every frame explicit ("it bloats the
  prompt and can hurt coherence"); always declare the interpolation method ("slerp + respect support + Laban").
- F-220 (S-087, S-089, corrected in S-090): by the fight's contacts the keys 0.3 to 0.5 s apart draw B's limbs through
  A, and B's crash sinks a sole 0.385 m; R-18 (no body through another), O72 (0.15 m).
- Principal review 7 (decisions; rules and shortcuts): option (a) adds and sets nothing aside, so R-06 and finish.md
  section 4 have the run answer it.

## Consequences
- RV-59f builds the in-between key: S13's plan may carry one entity's pose at an instant between two of its keys;
  S13's checks read it as a key; the renderer prints it with its instant; the re-block solver can place one.
- RV-59e (BODY_OVERLAP at every frame between keys) and RV-59c (FLOOR_PENETRATION there) follow, placing the repo's
  in-between keys where a re-pose cannot clear; B's 7.5 key is re-blocked first (the descent from the pillar involves
  no contact).
- A re-block of a repo key may move it as far as its joint limits and its contacts' O72 tolerance allow; S-087's 45
  degrees and 0.15 m were the builder's own probe bounds, not a ruling.
- The prompts grow; they are over the caps already (F-088), and delivery waits for that answer either way.

## Alternatives Considered
- (b) a contact's two bodies may overlap between keys within a stated number of frames of the contact: sets R-18 aside
  there, so it is the owner's (F-220).
- (c) contacts loosened inside O72's 0.15 m: within the rules, but it leaves a strike visibly short (the 4.7 knee 0.11
  m off the spine); kept for a span an in-between key cannot clear.
- (d) A's source rows re-posed or keyed between: the owner's (F-220).
- Beats added between the keys: a beat carries an action and a cause; an in-between pose has neither.

## Supersedes
—

## Superseded By
—

## Related
- F-220
- F-159
- F-089
- F-221
- ADR-O104
- ADR-O72
