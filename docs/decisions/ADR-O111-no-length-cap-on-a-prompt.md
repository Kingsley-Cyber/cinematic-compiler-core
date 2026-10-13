# ADR-O111 — No length cap on a prompt

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
Owner, in chat, 2026-10-12, after `cinematic compile` refused every example prompt for PROMPT_LENGTH: "hey whatever is
telling you to shorten to 3500 remove that rule or constraint."

## Context
O97 (RV-13) refused delivery of a prompt that fit neither Runway's 3,500 characters nor BytePlus's 1,000 words; every
prompt of the four examples is over both (12.9k to 61.6k characters), and F-088 waited for the owner's call on what
to cut.

## Consequences
- validators/prompt_length.py and PROMPT_LENGTH are removed: a prompt's length never refuses its delivery
  (`cinematic compile`, the checklist's deliverable column); R-19 says so (rules 7.3).
- Both of O97's caps go (the words cap refused the same prompts). Nothing is trimmed to fit; F-088 is resolved and
  RV-13b withdrawn.
- A prompt is still a deliverable only when no applicable DAG-map row FAILs or reads NOT CHECKED (R-19).

## Alternatives Considered
- Drop only the 3,500-character cap: the 1,000-word cap would still refuse every prompt.

## Supersedes
- ADR-O97 (its caps)

## Superseded By
—

## Related
- ADR-O97
- F-088
- RV-13
- RV-13b
