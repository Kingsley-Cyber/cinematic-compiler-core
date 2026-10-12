# F-080 — A's limb and head words contradict the source's own words

<!-- docs-version: 1.0 -->

## Type
contradiction

## Severity
high

## Layer
L4c

## Status
resolved

## Reported
2026-10-11

## Reporter
agent

## Legacy ID
—

## Evidence
- the principal review, S-035 (docs/prompts/principal_review.md)
- examples/reference_fight/prose_mixed.txt line 25 (1.10): "L arm back-mid ... L leg forward-mid ... R arm forward-mid ... R leg back-mid"; the source (kernel/sources/lbn-2.3-adv.txt): "L:arm fwd mid bent3, leg back mid; R:arm back mid bent3, leg fwd mid"
- 13 of 22 A lines print "head back-high", including rows whose source words say the head points or faces down
- about 21 of 88 A limb words point the other way (the principal review, S-035 (docs/prompts/principal_review.md)); the DAG's sign question X21 (docs/sources/knowledge_dag_v1.md) was never ruled

## Description
The repo reads A's numbers under Q6, while some of the source's rows wrote their words under the other sign, so the prompt tells the model the opposite of what the owner wrote.

## Impact
Limbs and heads move the wrong way in render; the asymmetry of lead and trail is inverted.

## Proposed Fix
Backlog RV-05 (O88): where an A row's word disagrees with the source's own word, that joint's number flips so the derived word agrees; each flip is a recorded deviation; b06_c3 is measured again.

## Owner Ruling
ADR-O88

## Related
- PLAN-007
- ADR-O88
- ADR-O7

## Resolution
RV-05 (S-038, O88): 19 limb flips and 13 head flips in A's rows; A's printed limb words agree with the source's
fwd/back on 86 of 88 and no A line prints a head tipped back; the two hips at 0.6 keep their crouch (ADR-O103); each
flip recorded in tests/test_reference_fight_golden.py (WORD_FLIPS, HEAD_FLIPS).
