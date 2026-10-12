# F-192 — The hit's hold has no duration, its scale disagrees with the card, and a gone body can be framed

<!-- docs-version: 1.0 -->

## Type
gap

## Severity
medium

## Layer
L5.5

## Status
open

## Reported
2026-10-12

## Reporter
agent

## Legacy ID
—

## Evidence
- the fifth principal review, S-072 (docs/reports/2026-10-12-principal-review-5.md)
- S16, S17 and the prompt judge only the shot covering the hit's instant: a static shot ending 1/24 s after the 2.5 hit and a tracking shot after it pass
- the anime card's hit rule asks for medium to full; HIT_HOLD refuses only close-ups and inserts: the 2.5 hit held on an extreme wide at 12 m passes
- S16 reads no vanish windows and VANISHED_BODY does not read [CAMERA]: a shot may frame a body while it is gone
- the printed rule says "Hold on the frame of impact" while the 5.50 impact frame (a throw, not a hit) is a whip pan

## Description
O92's hold is judged at an instant, at any scale but a close one, and on the shot's subject list.

## Impact
The camera can leave a hit at once, hold it from far away, or frame a gone body.

## Proposed Fix
Backlog RV-90: HIT_HOLD's scale follows the grammar's impact scales; S16 refuses a gone subject and VANISHED_BODY reads [CAMERA]; the impact rule speaks of hits. The hold's duration, and whether every impact frame is held, wait for the owner.

## Owner Ruling
how long a hold lasts and whether every impact frame gets one (listed, F-197)

## Related
- RV-90
- F-155
- F-177
- ADR-O92

## Resolution
Open.
