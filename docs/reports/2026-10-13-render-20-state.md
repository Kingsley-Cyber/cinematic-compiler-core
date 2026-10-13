# State after render R20 (2026-10-13)

<!-- docs-version: 1.0 -->

Written for the owner's confirmation pass (the owner's `confirmation-prompt`: state, confirmation, next actions).
Every claim here was checked against the code at b910b95; the evidence is in
[the confirmation](2026-10-13-render-20-confirmation.md), the work in [next actions](2026-10-13-render-20-next-actions.md).

## Where the repo is

| What | State | Evidence |
|---|---|---|
| Idea in, prompt out | Works for an idea S02 can cast. `cinematic author "<idea>" --backend claude-cli` writes every authored step on the owner's Claude subscription, retries on the checks' findings, repairs poses with the solver. | compiler/author.py; S-107 to S-113 |
| Speed | The ninja-versus-knight idea: 26.6 min (S-109), then 10.2 min (S-111). Two runs with the pose step split in parallel stopped at S13 (S-112). | docs/plans/008-automatic-author.md |
| Any idea | Casting drafts cards for what the library lacks; the kunoichi on a rooftop now casts (S-113). It stops once it has one performer and a place, so a second unknown performer is dropped. | compiler/author.py `casting` |
| Gate | 763 tests, docs plane PASS. It passed the prompt R20 failed on. | scripts/verify.sh |
| Owner's last render | R20, the author's first prompt, failed: a kunai appeared, the pillar sat to the side, the punch became a leg, the knight froze, the impacts landed late. | docs/renders/R20-author-1-ninja-versus-knight.md |

## What R20 proved

The checks measure what the envelope declares; they cannot see what the prompt invites or leaves unsaid. Each failure
the owner saw traces to a field that is missing or to words the prompt prints without a field behind them:

| What the owner saw | Cause in the code (confirmed) |
|---|---|
| A kunai appeared | The ninja card's invariant ("a thrown weapon leaves the hand"), its capability `throw_kunai` and its description ("short blades and thrown weapons") are printed whether or not a prop exists (compiler/passes/mandatory/p03_constraint.py:64-69); nothing declares the hands empty (S06 `possession` stays `unknown`; S08 hand roles run for UGC only). |
| The pillar on the side | Surfaces have no position (brief_nodes surface schema: a free-text `ax` only; the pillar has none). The beats put the ninja's crash 1.5 m to the side of the fight's axis while the camera line says the pillar is behind. |
| The punch became a leg | At the hand strike (2.20) both of A's feet land at the same instant (b04_c2, b04_c3); at the kick (5.30) the right foot is both striking and on the ground (b08_c1, b08_c3). No check refuses a part that strikes and supports at once. |
| The knight froze | 2.4 s with no line (B 2.20-4.60) and no Effort from 3.00 to 4.60; the prompt's own gap guidance says "carry ... through". No per-performer gap ceiling exists. |
| The impacts landed late | A contact lands at its beat's start or end only (beat_plan `at`); the strike line is printed at 1.60 and its contact at 2.20. |

## What the critique got right and wrong

Of the "112 missing things", 109 checked: 56 exist, 31 are partial, 22 are missing. All the documents, workflows and
controls exist, and most named validators exist under other names. The true gaps cluster in four places: what a
hand holds, where a surface is, when a contact lands inside a beat, and what the prompt prints of what the graph
already has (camera position and aim, hold frames, per-limb points are computed but not printed in the prose).

## Open owner rulings that bear on this

ADR-O109 (in-between keys), F-215 (floor allowance), F-143 (turned spins), O47 (the prose prints no frame counts,
after probes stretched them), M9-11 (genre profile values, blocked on the owner).
