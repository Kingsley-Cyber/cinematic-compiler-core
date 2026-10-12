"""PROMPT_LENGTH (owner O97, RV-13, F-088): a prompt is delivered only within a documented target's cap, 3,500
characters for Runway or 1,000 words for BytePlus. No prompt names its target yet (R-16 leaves the targets to M7), so a
prompt must fit at least one of the two. The cap refuses delivery (`cinematic compile` and the checklist's deliverable
column, owner O94), not conformance: the golden passes conformance with nothing set aside (owner O10). Fitting the
prompts under the caps waits for the owner's answer in F-088 (RV-13b).
Interpretation (Claude's, for owner review): a word is a run of non-space characters; an unnamed target is either one.
"""

CAPS = {"Runway": ("characters", 3500), "BytePlus": ("words", 1000)}  # owner O97


def measure(text):
    """{characters, words} of one prompt."""
    return {"characters": len(text), "words": len(text.split())}


def fits(text):
    """The targets whose cap the prompt fits, in CAPS order."""
    size = measure(text)
    return [target for target, (unit, cap) in CAPS.items() if size[unit] <= cap]


def problems(text):
    """[(code, message)]: PROMPT_LENGTH when the prompt fits no target's cap, else nothing."""
    if fits(text):
        return []
    size = measure(text)
    over = "; ".join(f"{size[unit]:,} {unit} over {target}'s {cap:,}" for target, (unit, cap) in CAPS.items())
    return [("PROMPT_LENGTH", f"{over} (owner O97)")]
