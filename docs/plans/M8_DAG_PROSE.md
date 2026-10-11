# PLAN-002 — M8: structured-prose prompts and DAG conformance

<!-- docs-version: 1.0 -->

## Status
applied

## Owner
Kingsley (owner); Claude executes

## Created
2026-10-11

## Updated
2026-10-11

## Intent
Compile the owner's knowledge DAG's Master Template as structured prose in four movement modes beside LBN-2.4, and check every prompt against the DAG map row by row (M8.0-M8.12).

## Critical Path
The slices of this plan in [docs/plan.md](../plan.md) (from docs/plans/backlog.yaml).

---

# M8 — structured-prose prompts from the knowledge DAG, and DAG conformance

Spec for milestone M8 in [MASTER_PLAN.md](MASTER_PLAN.md). Source of the rules: the frozen DAG
[`docs/sources/knowledge_dag_v1.md`](../sources/knowledge_dag_v1.md) (sha256 108d317b), mapped row by row in
`kernel/knowledge_map.yaml`. Line numbers below (L…) are lines of that copy.

## Owner decisions (2026-10-11)

| # | Decision |
|---|---|
| O1 | Keep the LBN-2.4 prompt exactly as it is (kernel layout, uncompressed) and compile structured prose **alongside** it, composed as the DAG says. |
| O2 | Compile **all** movement-language modes: pure staff (C14), Mixed (C15), Upgraded Mixed (C16), Euler-heavy (C17), from one Master Template (C19). No per-scene choice (this settles V9). |
| O3 | The prose follows the DAG on "root exact": its RULES leave the kernel rule out and say "Laban support and contacts primary; Euler is precision override only" (modes that carry Euler). LBN-2.4 keeps the kernel rule. |
| O4 | The repo's layer order stands (S15 effort after S13 motion; S04 positions authoritative). The compiler builds every prose section from atoms the graphs already hold. M3/T5 are settled for the repo. |
| O5 | One local commit per slice when `scripts/check.sh` passes; no push without the owner. |
| O6 | A conformance test runs test prompts through every graph and layer and checks the final prompts against the DAG map: every mandatory and required row at least, each by named semantic codes. |

Still open (not blocking M8): P3.2-6 PRESERVE_AXIS (S16 keeps the 180-degree line unless a cut declares `cross`).

## What S17 produces after M8

`nodes.render` holds five items: `render` (LBN-2.4, unchanged, the uncompressed projection that owner invariant
`no_render_compression` is checked on) and four prose items `prose_pure_staff`, `prose_mixed`,
`prose_upgraded_mixed`, `prose_euler_heavy`. The prose is derived: a pure function of the envelope, no authoring.
Each example folder gains `prose_<mode>.txt`; `python -m compiler.examples` checks them byte for byte.

The prose modes are dual encodings (T11) of the same envelope; pure staff carries no numbers by design (O2), so
`no_render_compression` stays the LBN item's invariant. Each prose item has its own DAG coverage instead: every
slot has a staff line, and every prop state, causal edge, shot, frame part, rule and negative appears (minus the
root-exact rule, O3).

## The Master Template (C19, L501-L516; D8 wrapper L340-L344; D9 blocks L558-L566)

Sections in this order (intent first, constraints last: M1, T3, P3.2-7):

| # | Section | Built from (step) | Map rows |
|---|---|---|---|
| 1 | `[SCENE]` | query, genre, fps, duration (S01); setting, world (S02); one anchor phrase per entity from its archetype description, silhouette and costume (S02); props (S02); render intent (derived, below); "Render spec exactly." (kernel preface item) | M1, C23, C28, V12 |
| 2 | `[MOVEMENT LANGUAGE]` | fixed legend: staff rules (each line = one measure, no support = airborne, contact bow = touch, double bow = momentary, accent = strong impact, time in seconds), explicit/implied split, the density actually used, the precision-tag legend (closes audit X28), the mode statement | LBN, C1, C18 |
| 3 | `FORMAT` | `TIME  PERFORMER: SUPPORT [precision tags] \| LEFT \| RIGHT \| [relationship] \| path/notes` (L507) | LBN |
| 4 | `[LABAN STAFF – <MODE>]` | one line per slot (entity × beat), time order; Euler blocks per mode (below) | KF, C1, EXT1, EXT2, C14-C17 |
| 5 | `[IMPLIED GUIDANCE]` | per performer and per gap: declared Effort (S15), weight transfer (S11), secondary-motion lag on costume parts (S02), recovery after accents (S17 impacts), airborne arcs (S06 airborne spans) | C4, C2, LMA |
| 6 | `[MOTION CONTROL]` | interpolation (slerp joints; root trajectory derived), density bands measured on the scene (E1 bands), explicit = staff lines, implied = between them | C3 |
| 7 | `[SPATIAL ANCHORS]` | the frame convention (C29: up, forward, ground, intrinsic XYZ degrees, right-handed, +X = performer's left, joints local / root world), world surfaces and their geometry, start positions, height/depth use | C9, C29 |
| 8 | `[PROP STATE MACHINE – <prop>]` | per prop, ordered states from S06/S07 with times and holders; invariant line "never duplicated, never in two hands at once, never lost"; `CUSTODY: <label>.<prop>` for a prop that never changes holder | C5, C7, C24, C31 |
| 9 | `[CAUSAL LINKS]` | the S05 causal edges as one short `→` chain per thread (the two graphs V8 allows: this and section 8) | C6, V7, V8 |
| 10 | `[CAMERA]` | one line per S16 shot in words (time, move, angle, lens, holds, slow motion) + the genre card's rules; the beats each shot shows (shot program) | CAM, C10, C11, C25 |
| 11 | genre block (`[ANIME]`, `[UGC]`, `[LIVE ACTION]`) | S17 frame parts: impacts, smears (declared limb only), speedlines, holds, fx, ink | C12 |
| 12 | `[RULES]` | kernel and card rules (minus root exact, O3); precedence rule (O3); conservation laws (T10, 6 of 7); time-bounded end-state rules from S06 ("B never stands after 9.0", C13); span rules for support held across lines (C30); event-separation rules for similar strikes (C32) | C13, T10, C22, C30, C32, M3 |
| 13 | `[NEGATIVES]` | every negative constraint (S03), last | NEG, C13 |

### The staff line (LBN, L82-L98, L507, L522)

| Column | Derivation (step) | Note |
|---|---|---|
| TIME | slot time (S04) | seconds, two decimals |
| PERFORMER | actor label A, B… (S02 order) | as LBN-2.4 |
| SUPPORT | S11 support parts + S07 active supports: `NO SUPPORT` when airborne; parts with the surface when not the ground (`feet alternating ON THE wall`); level from the S06 posture (standing → place-mid, crouching/kneeling/inverted → place-low) | (interp.) for level |
| precision tags | `[f:…]`, `[h:…]` from the support parts; `[contact: …]` for possess/release | C18; legend in section 2 |
| LEFT / RIGHT | per limb (arm, leg) and the body: direction + level from the S13 key by forward kinematics in the Q6 convention, joints local to their parent (root → Sp → arms, NK → HD; root → legs) | 8 horizontal directions + place; levels as the owner's laban-notation lookup (mid inside ±45 degrees, place within 10 of vertical) (interp.); fold words from LFA/RFA/LL/RL bends, straight under 15 degrees. M8.1: derived directions match the 2.3 source's own words on 78% of limbs (its signs are inconsistent, X5/X21) |
| relationship | the performer's contacts in the slot's beat: touch → `contact bow`; a touch whose beat holds an S17 impact frame, on anything but a prop the performer holds → `[DOUBLE BOW + accent: X > Y]` (interp., L31; contacts are stamped at their beat's end, impact frames where the hit reads, so the beat window joins them); possess → `[contact: X-Y retained]`; release of a held thing → `[contact: Y ENDS – released]`; the contact time is written when it differs from the line time | M8.2: reference_fight strikes at 2.50 A (kunai), 4.70 A (knee), 6.60 B (elbow catch), 8.50 B (kunai drive); 5.50 B (shuriken throw) also reads as a strike because the volley's holder is 'unknown' in S06 |
| path / notes | travel to the performer's next line from the S04 anchors (direction relative to facing, metres, rising/dropping); SUPPORT reads `steps <direction> alternating` only when this line and the next stand on feet on the ground with no height change; declared turns from S13 → turn sign naming the axis and side; strike lines → `chain <initiation> > <follow-through>` (S12, KC); the beat's action sentence on the actor's line; S14 face words; each performer's last line → `hold sign to the end` | |

### Euler blocks per mode (D6 L506-L508, D7 L568, D10 L534-L551)

| Mode | Root + EulerXYZ | Joints dictionary |
|---|---|---|
| pure staff (C14) | none | none |
| Mixed (C15) | strike lines + each performer's first and last line | none |
| Upgraded Mixed (C16) | strike lines + each performer's last line | on the same lines |
| Euler-heavy (C17) | every line | every line |

"Strike line" = a line with a `DOUBLE BOW + accent`. The key selection reads D6/D7/D10's instances (D6 adds 0.00;
D7 names the strikes and the final crouch; D10 puts joints on those four) and is labelled (interp.).

### Render intent (C28, L1627), derived

motion: speed from the S15 time factor share, weight from the weight factor, acceleration from sudden intervals,
readability from the camera tempo · animation: genre style and style_reference, spacing from the density used,
smear and impact counts from the frame parts · choreography: principle from the S05 thread ("cause before effect,
one thread") and the final instruction from the S06 end states.

## Semantic codes (M8.4, `validators/prompt_validator.py`)

The validator reads a final prose prompt and the envelope (as a model would read the prompt, plus the facts to
compare against) and returns findings by code. Each mandatory and required map row lists its codes in a new
`codes` field. Planned codes:

| Code | The prompt is wrong when | Rows |
|---|---|---|
| `SECTION_MISSING` | a Master Template section is absent | T1, T2, T8, T9, C19 |
| `SECTION_ORDER` | sections are out of order (intent first, rules then negatives last) | M1, T3, T4, T5 |
| `PROSE_STALE` | the text is not the projection of the current envelope (an upstream change did not cascade) | M2 |
| `PRECEDENCE_RULE_MISSING` | a mode with Euler lacks "Laban support and contacts primary; Euler precision override" | M3 |
| `ROOT_EXACT_PRESENT` | the prose carries the root-exact rule (O3) | M3 |
| `PROMPT_CONTRADICTION` | two sections disagree: staff contact vs prop state, causal order vs line times, end-state rule vs last lines, fx 'ring' vs a 'no ring' negative (X29), camera hold vs genre-block hold | M4 |
| `KEY_LINE_MISSING` | a slot has no staff line | KF, C1 |
| `STAFF_FORMAT` | a line breaks FORMAT | LBN |
| `SUPPORT_MISMATCH` | SUPPORT disagrees with S11/S07 (airborne must read NO SUPPORT) | LBN, BIO, T7, M3 |
| `AIRBORNE_UNBOOKENDED` | an airborne span lacks a takeoff line or a landing line (B-8) | BIO, T7 |
| `GESTURE_MISMATCH` | a gesture word disagrees with the S13 key's derived direction/level | LBN |
| `EULER_MODE_MISMATCH` | Euler blocks are on the wrong lines for the mode, or numbers differ from S13 | EXT1, EXT2, C14-C17 |
| `SKELETON_KEY_MISSING` | a mode with joints lacks the joint legend | EXT2 |
| `EFFORT_UNDECLARED` | a performer's phrase has no Effort words | LMA, T6 |
| `KINETIC_CHAIN_MISSING` | a strike line lacks its follow-through order (S12) | KC |
| `KEY_GAP_UNGUIDED` | a performer's gap over 1.5 s between lines has no implied guidance for it | C2 |
| `IMPLIED_GUIDANCE_MISSING` | the section lacks Effort, weight transfer, lag, recovery or airborne-arc guidance | C1, C4 |
| `INTERPOLATION_UNDECLARED` | MOTION CONTROL lacks the interpolation | KF, C3 |
| `CONVENTION_MISSING` | the axis line lacks up, forward, ground, order, units, handedness or joint parenting | C29 |
| `SPATIAL_ANCHOR_MISSING` | a surface or a start position is missing | C9 |
| `PROP_TRACK_MISSING` | a prop has no state machine, or a state is missing | C5 |
| `PROP_STATE_ORDER` | states are out of time order or disagree with S06/S07 | C5, C7 |
| `PROP_INVARIANT_MISSING` | the never-duplicated / never-two-hands / never-lost line is missing | C5 |
| `CUSTODY_RULE_MISSING` | a prop that never changes holder lacks its CUSTODY rule | C24 |
| `CAUSAL_LIST_MISSING` | a causal edge is absent from CAUSAL LINKS | C6, GR |
| `REACTION_WITHOUT_CAUSE` | a line reacts to a contact that comes later (F2's named invalid state) | C21, C26, C27 |
| `CAUSAL_RULE_MISSING` | a lasting effect of a hard cause has no time-bounded rule | T9, C13, C22 |
| `CONSERVATION_RULE_MISSING` | one of the six laws (T10) is absent from RULES | T10 |
| `SPAN_RULE_MISSING` | a support held across lines is not stated as one continuous span | C30 |
| `EVENT_SEPARATION_MISSING` | two similar strikes by one performer lack a separation rule | C32 |
| `RULES_MISSING` | a rule constraint (except root exact) is absent | C13 |
| `NEGATIVES_MISSING` | a negative constraint is absent | NEG |
| `DISCONNECTED_CAMERA_MOTION` | a camera line has no motivation, or a shot misses the beats it shows | CAM, C25, C26 |
| `ANCHOR_PHRASE_MISSING` | an entity lacks its appearance phrase | C23 |
| `RENDER_INTENT_MISSING` | motion, animation or choreography intent is absent | C28 |
| `END_STATE_MISSING` | an entity's end position or support is absent | C22 |
| `STACKED_GRAPHS` | other than the two allowed graphs is embedded | GR, V8 |

M8.4 built all 37 (validators/prompt_validator.py; each fires on its break in tests/test_dag_conformance.py).
One KNOWN finding is accounted for, not hidden: reference_fight's fx 'pillar-top landing dust ring' and 'crash dust
ring' come verbatim from the owner's LBN-2.3/2.4 sources next to the kernel negative 'no ring' (audit X29); the
owner decides whether to reword them.

Codes for atoms the repo does not have yet stay listed against their rows as gaps until a slice adds the atom
(M8.4 added CHAIN_ORDER for KC, ANTICIPATION_MISSING for KF, PROP_TWO_HOLDERS for C5, SHOT_TRANSITION_MISSING for C25):
`JOINT_LIMIT` (B-3; the DAG gives no ranges, so it needs sourced numbers from the owner), `PHRASING_MISSING`
(L-Ph preparation → action → recuperation), `MOMENTUM_MISSING` (C22, T10), `PROP_KINEMATICS` (C31 position and
velocity agree with gravity), `POST_CONTACT_MISSING` (C21 compress / accelerate / follow-through), `TELEPORT`
(T10; the DAG gives no speed bound).

## Conformance test (M8.4, `tests/test_dag_conformance.py`)

- Test prompts: the four examples (`request.json` + `plans/`), which between them run every step S01-S17 across
  anime, ugc_ad and live_action; each is compiled from its query, not read from envelope.json.
- Per prompt: every active layer's group exists and is schema-valid, envelope validation is complete, LBN-2.4
  coverage is complete, and each of the four prose prompts returns no finding from the prompt validator.
- Per code: a broken prompt (one edit) raises it (negative test), so no code is decorative.
- Map: every mandatory and required row lists at least one code; every code is emitted by the validator; a row
  marked `enforced` has all its codes passing. Open gaps are an explicit list in the test; closing one without
  updating the list, or opening a new one, fails the test.

## Slices (one commit each)

| Slice | Content | Done when |
|---|---|---|
| M8.0 | this plan; map records O1-O4 (logged) | gate PASS |
| M8.1 | `solver/staff_geometry.py`: limb and body direction/level/fold from an S13 key, support words, turn signs | unit tests on hand-built poses (rest, arm forward 90, overhead, crouch, inverted, cartwheel) |
| M8.2 | `renderers/prose_renderer.py`: SCENE, MOVEMENT LANGUAGE, FORMAT, staff in four modes, RULES, NEGATIVES; render schema allows the prose items (logged); examples gain `prose_<mode>.txt` | four examples compile; byte-for-byte check |
| M8.3 | remaining sections: implied guidance, motion control, spatial anchors, prop state machines, causal links, camera, genre block, render intent | every section present in all four examples |
| M8.4 | `validators/prompt_validator.py` + map `codes` (logged) + conformance test | every mandatory and required row has codes; the examples pass; open gaps listed |
| M8.5+ | one gap per slice: C5 two holders on one prop (S07), C31 prop kinematics, C21 post-contact, phrasing, momentum; joint limits once the owner gives ranges | gap list empty |
