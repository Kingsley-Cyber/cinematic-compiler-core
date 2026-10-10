"""Kernel extraction: inventory the controls of LBN prompts and keep what every version states.

Fields read (verbatim, with byte spans): preface sentences, `ax` (comma list), `key` (space list),
`negative` (comma list) and `rules` (semicolon list). The kernel is the intersection over all
sources, in the first source's order. Each shared item's scope comes from kernel/kernel_scope.yaml
(the reviewed per-item reading); an item without exactly one scope entry is refused.

    python -m kernel_extraction.control_inventory          # rewrite kernel/invariants.yaml
    python -m kernel_extraction.control_inventory --check  # exit 1 if it would change
"""

import hashlib
import json
import re
import sys

import yaml

from kernel.canonical import ContractError
from planner.dependency_graph import ROOT

SOURCES = ["kernel/sources/lbn-2.3-adv.txt", "kernel/sources/lbn-2.4-adv-lma.txt"]
SCOPE_FILE = ROOT / "kernel" / "kernel_scope.yaml"
TARGET = ROOT / "kernel" / "invariants.yaml"
SPLIT = {"ax": ",", "key": " ", "negative": ",", "rules": ";"}
SCOPES = {"kernel", "kernel_actor", "kernel_prop", "scene_reference"}


def inventory(text):
    """[(field, item_text, [start, end])] with spans into the exact source text."""
    start = text.index('{"variant"')
    document = json.JSONDecoder().raw_decode(text[start:])[0]
    items = []
    cursor = 0
    for part in re.split(r"(?<=\.)\s+", text[:start]):
        sentence = part.strip().rstrip(".")
        if sentence:
            offset = text.index(sentence, cursor)
            items.append(("preface", sentence, [offset, offset + len(sentence)]))
            cursor = offset + len(sentence)
    for field, separator in SPLIT.items():
        cursor = text.index(f'"{field}":"', start) + len(field) + 4
        for part in document[field].split(separator):
            offset = text.index(part, cursor)
            items.append((field, part, [offset, offset + len(part)]))
            cursor = offset + len(part)
    return document["variant"], items


def build(root=ROOT):
    sources, inventories = [], []
    for name in SOURCES:
        raw = (root / name).read_bytes()
        variant, items = inventory(raw.decode("utf-8"))
        sources.append({"file": name, "variant": variant, "sha256": "sha256:" + hashlib.sha256(raw).hexdigest()})
        inventories.append(items)
    scope = yaml.safe_load(SCOPE_FILE.read_text(encoding="utf-8"))
    entries = {(row["field"], row["text"]): row for row in scope["items"]}
    if len(entries) != len(scope["items"]):
        raise ContractError("KERNEL_SCOPE", "kernel_scope.yaml lists an item twice")
    shared, seen = [], set()
    counters = {}
    for field, text, span in inventories[0]:
        counters[field] = counters.get(field, -1) + 1
        others = [next((s for f, t, s in items if (f, t) == (field, text)), None) for items in inventories[1:]]
        if (field, text) in seen or None in others:
            continue
        seen.add((field, text))
        row = entries.get((field, text))
        if row is None or row["scope"] not in SCOPES:
            raise ContractError("KERNEL_SCOPE", "Shared item has no valid scope entry", [field, text])
        item = {"id": f"k_{field}_{counters[field]:02d}", "field": field, "text": text, "scope": row["scope"],
                "reason": row["reason"], "reference_labels": row.get("reference_labels", []),
                "sources": [{"file": SOURCES[0], "span": span}] +
                           [{"file": name, "span": s} for name, s in zip(SOURCES[1:], others, strict=True)]}
        shared.append(item)
    extra = set(entries) - seen
    if extra:
        raise ContractError("KERNEL_SCOPE", "kernel_scope.yaml classifies text no longer shared", sorted(extra))
    return {"version": 1, "status": scope["status"], "basis": scope["basis"], "sources": sources, "items": shared}


def render(document):
    return yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=120)


def main():
    text = render(build())
    if "--check" in sys.argv:
        sys.exit(0 if TARGET.exists() and TARGET.read_text(encoding="utf-8") == text else 1)
    TARGET.write_text(text, encoding="utf-8")
    print(TARGET.relative_to(ROOT))


if __name__ == "__main__":
    main()
