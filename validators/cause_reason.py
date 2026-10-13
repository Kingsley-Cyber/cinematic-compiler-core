"""CAUSE_REASON: a causal link's `why` must state a cause, not restate the timeline (DAG C6 and audit X40; owner render
R4, 2026-10-11: "he substituted but nothing warranted this ... is there a causal graph?").

A reason fails when it is
- too short to state a cause (fewer than MIN_WORDS words);
- an identifier ('throw_kunai', 'b05') instead of words;
- a template: the same words, once the link's own names are removed, on TEMPLATE_LINKS or more links
  ("<beat> leads straight into the next exchange", "The stand-off answers itself");
- about nobody and nothing: it names no performer, prop, surface, contacted part or action of either beat.
Used by S05 (the graph gate) and the prompt validator (the printed reason).
"""

import re

MIN_WORDS = 5
TEMPLATE_LINKS = 3
IDENTIFIER = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b|\bb\d{2}\b")
WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
GENERIC = {"from", "above", "below", "into", "onto", "over", "under", "behind", "toward", "towards", "with", "the",
           "and", "off", "down", "out", "for", "opponent"}


def labels(envelope):
    """The performer labels the render assigns (A, B, ... in entity order)."""
    return {e["id"]: chr(ord("A") + i) for i, e in enumerate(envelope["nodes"]["entities"]["items"])}


# the fields that name each kind of thing: a surface has no name or hint, its kind names it (data-flow trace: S05 read
# a surface's name and hint, which no layer writes)
NAMING = {"entities": ("id", "name", "hint"), "props": ("id", "name", "hint"), "surfaces": ("id", "kind")}


def _names(envelope):
    """{id: words} for every entity, prop and surface: the words of the fields that name it (NAMING)."""
    out = {}
    for group, fields in NAMING.items():
        for item in envelope["nodes"].get(group, {}).get("items", []):
            text = " ".join(str(item[k]) for k in fields).replace("_", " ").lower()
            out[item["id"]] = {w for w in WORD.findall(text) if len(w) >= 3 and w not in GENERIC}
    return out


def vocabulary(cause, effect, envelope):
    """(words, performer labels) that tie a reason to its two beats."""
    names, tags = _names(envelope), labels(envelope)
    ids = {cause["actor"], effect["actor"]} | {p["id"] for b in (cause, effect) for p in b.get("participants", [])}
    words = set().union(*(names.get(i, set()) for i in ids))
    for beat in (cause, effect):
        words |= {w for w in beat["label"].split("_") if len(w) >= 4 and w not in GENERIC}
        for contact in beat.get("contacts", []):
            for side in ("a", "b"):
                words |= {w for w in str(contact[side].get("part") or "").split("_") if len(w) >= 4}
    words = {w[:-1] if w.endswith("e") and len(w) >= 5 else w for w in words}  # circle -> circling, slide -> sliding
    return words, {tags[i] for i in ids if i in tags}


def _names_a_performer(text, tags):
    """A label counts as a name, not the article 'A': followed by "'s", or not at a sentence start."""
    for tag in tags:
        for match in re.finditer(rf"\b{re.escape(tag)}\b", text):
            before = text[:match.start()].rstrip()
            if text[match.end():match.end() + 2] == "'s" or (before and before[-1] not in ".!?:"):
                return True
    return False


def _skeleton(why, words, tags):
    kept = [w.lower() for w in WORD.findall(IDENTIFIER.sub(" ", why))
            if w not in tags and not any(w.lower().startswith(v) for v in words)]
    return " ".join(kept)


def problems(edges, beats, envelope):
    """[(edge id, message)] for every causal link whose reason does not state a cause."""
    by_id = {b["id"]: b for b in beats}
    out, skeletons = [], {}
    for edge in edges:
        why = (edge.get("why") or "").strip()
        cause, effect = by_id.get(edge["from"]), by_id.get(edge["to"])
        if cause is None or effect is None:
            continue
        words, tags = vocabulary(cause, effect, envelope)
        if len(WORD.findall(why)) < MIN_WORDS:
            out.append((edge["id"], f"'{why}' is too short to state a cause"))
        if IDENTIFIER.search(why):
            out.append((edge["id"], f"'{why}' names an identifier ({IDENTIFIER.search(why).group(0)}), not a cause"))
        said = {w.lower() for w in WORD.findall(why)}
        if not _names_a_performer(why, tags) and not any(w.startswith(v) for w in said for v in words):
            out.append((edge["id"], f"'{why}' names no performer, prop, surface, part or action of either beat"))
        skeletons.setdefault(_skeleton(why, words, tags), []).append(edge["id"])
    for skeleton, ids in skeletons.items():
        if len(ids) >= TEMPLATE_LINKS:
            out += [(i, f"the same reason ('{skeleton}') on {len(ids)} links: a template, not a cause") for i in ids]
    return out
