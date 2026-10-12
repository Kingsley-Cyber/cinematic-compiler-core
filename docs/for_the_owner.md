# For the owner: this repo in plain English

<!-- docs-version: 1.1 -->

You don't need to read code to audit this repo. This page explains what it does, where every answer lives, what each
technical word means, and what is waiting for you.

## What the repo does

You write a scene request ("10 s anime fight, a lean ninja against a broad ninja, ..."). The compiler turns it into one
data file (the *envelope*) built in 18 steps, from what you asked for, to who and what is in the scene, to every beat,
cause, contact, pose, effort and camera shot. Then it writes the prompts you paste into a video model: one LBN-2.4 prompt
and four structured-prose prompts. Each prompt is checked against your knowledge DAG, row by row. A prompt counts as
done only when every row that applies passes. Claude never renders; you render, and your verdicts are logged.

## Where the answers live (read these, in this order)

| Question | Open |
|---|---|
| What is decided? | [index/decisions.md](index/decisions.md): every ruling you made, one file each |
| What is wrong or open? | [index/findings.md](index/findings.md): bugs, gaps, contradictions, questions, risks |
| What is being built, in what order? | [plan.md](plan.md) (the work queue) and [index/plans.md](index/plans.md) |
| What did each session do? | [index/sessions.md](index/sessions.md) |
| What did each render show? | [index/renders.md](index/renders.md): your words, Claude's notes kept apart |
| What are the rules? | [rules.md](rules.md): every rule, each with the ruling it comes from |
| In what order are the layers built? | [layer_order.md](layer_order.md) |
| How do agents work here? | [AGENTS.md](../AGENTS.md) |
| Who may change what? | [ownership.md](ownership.md) |

## What waits for you

<!-- BEGIN GENERATED: owner_rulings -->
- ADR-O67 (owner_default, confirm or strike): Docs-plane defaults
- ADR-O103 (owner_default, confirm or strike): At 0.6 A's hips keep the crouch: O88's flip there would break its own row
- ADR-O104 (owner_default, confirm or strike): "Genuine airborne or prop-moving misses" are contacts measured between keys or samples
- ADR-O105 (owner_default, confirm or strike): B's kunai leaves the hand once, at the 2.0 throw
- ADR-O106 (owner_default, confirm or strike): Version bumps follow docs/versioning.md as written
- ADR-O108 (owner_default, confirm or strike): The deflected kunai goes down to the ground on B's side, not at B
- ADR-O109 (owner_default, confirm or strike): In-between keys on the repo's side where the declared interpolation draws a body through another or under the floor
- F-051 (low): Draft library cards await owner review
- F-052 (low): Kernel scope numbers await owner review
- F-053 (medium): Claude's interpretations await owner review
- F-054 (low): Agent additions await owner review
- F-055 (low): M6 tools are undefined
- F-057 (low): The kernel rule 'substitution log reveals' reads against O48's staging
- F-059 (low): Reference-fight deviations from its own data await review
- F-060 (low): What is a motif?
- F-088 (high): Every prompt is over the length caps; fitting them needs the owner's call on what goes
- F-108 (medium): B's track departs from the source
- F-111 (medium): Limb words mix frames against the legend
- F-114 (medium): Do R-21, R-23 and R-25 bind render.txt?
- F-116 (medium): Rebinding re-stamps hashes instead of forcing re-authoring
- F-117 (high): F-013 and F-014 cannot close
- F-118 (low): O37 and the genre_profile schema disagree on where genre values live
- F-124 (medium): The 5.9 slide's exception: the prompt says both feet support while the soles are 0.35-0.55 m up
- F-133 (medium): The 37 scene_reference rules reach no scene
- F-143 (high): The Euler convention reads the source's turned leans as rolls and its backflip as a front flip
- F-148 (high): Source rows whose numbers contradict their own words: fix them or keep them?
- F-152 (high): O72's point measure and BODY_OVERLAP cannot both hold for body contacts
- F-153 (high): No compile can ever emit: render.txt cannot pass the Master Template rows
- F-154 (medium): Owner_default ADRs taken under O101 are counted as rulings the owner has not seen
- F-165 (medium): The log and the pellet do not follow the source at 3.7
- F-168 (low): The pre-commit gate waits for the owner's `make hooks`
- F-196 (high): The substitution's decoy: who declares it, where it stands, who may substitute
- F-197 (high): Hits and holds: what counts, how long, how wide, and which cuts hold
- F-198 (high): Which checklist rows must pass for a prompt to be a deliverable
- F-199 (medium): O23's key pose and O93's single instant
- F-200 (medium): The source, owner_default ADRs and decided_by as rulings
- F-201 (medium): R-21's reach beyond the fight
- F-202 (medium): The fight's open staging choices
- F-203 (medium): RV-20's layer-order ADR
- F-205 (medium): The anime body's arms reach the floor only with the trunk leaning 58 to 75 degrees
- F-211 (medium): Must each fighter's laban chain carry its side of the other's beats?
- F-215 (high): May a body point sit up to 0.15 m under the floor, or only by its radius?
- F-220 (high): By a contact the declared interpolation draws one body through the other, and B's crash through the floor
- F-223 (medium): The pickups' lean is checked by an angle sum the drawn body does not hold
- Backlog M9-03a blocked: GAP-04/05 checkable constraint form and the per-layer constraint run — owner approval of the checkable constraint schema (O61)
- Backlog RV-15c blocked: A strike's limb and a facing head point at their target, checked at S13 (B's keys re-aimed in RV-103b) — the owner's answer in F-148 (A's source facings: the check would refuse the golden's own rows, O10)
- Backlog RV-14b blocked: A held or embedded prop at its holder at every sample (the rope dart's line in RV-14c) — the owner's answer in F-148 (the climax: A's source right hand is 0.65-0.87 m from the kunai the source keeps in B's shoulder at 8.5-9.5)
- Backlog RV-87 blocked: The substitution's decoy is declared, stands in the scene from the first beat, and is measured where the actor stood; a substitution needs the capability — the owner's answers in F-196 (Q1-Q3: who declares the decoy, whether it stands from the first frame, who may substitute)
- Backlog RV-90b blocked: HIT_HOLD's scale follows the grammar's impact scales — the owner's answer in F-197 (Q3: may a hit be held at a wide scale)
- Backlog RV-64b blocked: The S04 packet carries the scene_reference rules — the owner's answer in F-133
- Backlog RV-13b blocked: Every prompt fits the caps (O97) — the owner's answers in F-088
- Backlog RV-20 blocked: external_inputs complete: the layer order states what each step depends on — an accepted ADR for the layer-order edit (R-09)
- Backlog RV-82b blocked: A shot on a declared turn looks along the turn's axis — the owner's answer in F-202 (a turn plane against the 180-degree side)
- Backlog RV-24 blocked: The launch check per O80's words: the prior beat, every launch — the owner's ruling on A's 5.1 backflip in F-099
- Backlog RV-26 blocked: Momentum at the true takeoff; the opening fall judged; each span re-timed or hung — the owner's span-by-span answer in F-101
- Backlog RV-27 blocked: Prop paths and times follow the source (R-17) — the owner's answers in F-165 and F-059
- Backlog RV-33 blocked: B's track follows the source (F-108's question answered by ADR-O105) — RV-52, which waits for the owner
- Backlog RV-36 blocked: Limb and head words read in one declared frame — the owner's answer in F-111
- Backlog RV-40 blocked: Rebinding forces re-authoring — the owner's answer in F-116
- Backlog RV-52 blocked: The Euler convention: the source's turned leans and its backflip (ADR-Q6) — the owner's answer in F-143 (ADR-Q6's label or its meaning)
- Backlog RV-53 blocked: The source rows whose numbers contradict their words; O95 against O88 on two action keys — the owner's answers in F-148 and F-149
- Backlog RV-55 blocked: Body contacts measured as the owner rules (O72's measure against BODY_OVERLAP) — the owner's answer in F-152
- Backlog RV-56 blocked: render.txt's deliverability as the owner rules (O1 with O94 and O13) — the owner's answer in F-153
- Backlog RV-63 blocked: A prop let go without a throw starts at rest; the dart's and the pellet's drops re-timed — the owner's answer on O90's timing in F-164
- Backlog M9-11 blocked: FR.7 genre cards; FR.6 money-shot frame parts (FR.2 moved to AS-05) — the owner's answer in F-118 (O37 or the genre profile)
<!-- END GENERATED: owner_rulings -->

To rule, tell the agent in chat. The agent writes it up as a decision file (an ADR), cites it in the rules if it
changes one, and the lists above update. You can also write the ADR yourself from
[decisions/_template.md](decisions/_template.md).

## How to check a claim

- **"Is X done?"** Find X in [plan.md](plan.md). A tick ✓ next to a code means that check exists in the code today.
  `done` means every check the slice promised exists, and the gate has passed with it.
- **"Why does the prompt say Y?"** Find the rule in [rules.md](rules.md), then open the ruling it cites.
- **"Did the agent change something it shouldn't?"** Every change to a schema, library card, kernel file or frozen doc
  is in a hash-chained log. The gate fails if a file's bytes differ from its last log entry. See [ownership.md](ownership.md).
- **"Is the repo healthy?"** One command, `scripts/verify.sh`, ends with `check: PASS` or stops at the first failure.

## Glossary

| Word | Meaning here |
|---|---|
| ADR | Architecture Decision Record: one file per decision you made (docs/decisions/). IDs keep the old names: O48, Q6, F2. |
| Agent | The AI coding assistant working in the repo (Claude). It follows AGENTS.md. |
| Authored step | A step whose content is written by the agent in the session, from a sealed packet. Steps S04, S08 and S11-S17. |
| Backlog / slice | One unit of work and one commit, listed in docs/plans/backlog.yaml and shown in plan.md. |
| Bartenieff | How the body coordinates a move: which part starts it and how it flows through the body. Step S12. |
| Beat | One timed event in the scene ("B throws the kunai, 2.0-2.5 s"). Step S04. |
| Card | A small data file describing an archetype, world, object, camera convention and so on (library/). `draft` until you approve it. |
| Causal link | "This happens because of that", with a printed reason. Step S05. |
| Checklist | The table judging each prompt against every row of your DAG map (examples/*/checklist.md). |
| CI | Continuous integration: GitHub runs the gate on every push (.github/workflows/). |
| Code (prompt code) | The name of one check, for example HIDDEN_PHRASING. A prompt that breaks it is refused. |
| CODEOWNERS | A GitHub file naming who must approve changes to which paths. |
| Commit / push | A commit saves a step locally. A push sends it to GitHub, and only on your word. |
| Contact | A touch, hold, support or release between a body part and something, at a time. Step S07. |
| DAG | Your knowledge DAG (docs/sources/knowledge_dag_v1.md), mapped row by row in kernel/knowledge_map.yaml. |
| Derived step | A step computed by code from earlier steps, with nothing written by hand. |
| Edge / node | A node is a thing (a beat, a contact, a pose). An edge connects two of them ("causes", "follows"). |
| Effort (Laban) | The quality of a move: weight, time, space, flow ("strong, sudden, direct"). Step S15. |
| Envelope | The one data file the compiler builds for a scene, holding every step's output. |
| Euler angles | A rotation written as three angles (X, Y, Z) in degrees. Flips turn about X, spins about Y, cartwheels about Z. |
| Finding | Something discovered (a bug, gap, question...), one file each in docs/findings/. |
| Forward kinematics | Working out where a hand or foot is in the world from the joint angles. Built at S13 (M9-06, S-027). |
| Gate / verifier | `scripts/verify.sh`: lint, tests, logs, examples, docs. It runs before every commit and in CI. |
| Golden | The reference fight that must compile exactly from your LBN reference prompt, apart from recorded deviations you approved. |
| graft / graphify | Code-map tools the agent uses before reading files, to save time and tokens. |
| Hash log | An append-only list of every change to a protected file, each entry tied to the file's exact bytes. |
| Index | One generated table listing every file of a kind (docs/index/). |
| Kernel | The 68 controls that both LBN-2.3 and LBN-2.4 state; the compiler prints them all. |
| Labanotation (staff) | Movement written as symbols, here written as words on staff lines (support, limbs, contacts). |
| Layer / step | One stage of the build (S01 intent ... S18 post-generation), with the owner labels L0 ... L6.5. |
| LBN-2.4 | The repo's full, numeric prompt format (render.txt). |
| Packet | The sealed input an authored step is written from. Its hash proves the step saw exactly that input. |
| Probe | A short 5 s render testing one wording question (docs/render_tests/). |
| Render | A video you made from a prompt, logged in docs/renders/ with its prompt hash. |
| Schema | The contract a data file must satisfy (schemas/), checked by the repo's own validator. |
| Seedance | The video model the repo is built for (O49), with no model cards. Other models come later as adapters. |
| Session | One working stretch of the agent, logged in docs/sessions/. |
| Structured prose | The four prose prompts (pure staff, Mixed, Upgraded Mixed, Euler-heavy) in your DAG's template. |
| Worktree | A second checkout of the repo used to work without disturbing the main folder. |
