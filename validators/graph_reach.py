"""Graph reach (ADR-O113: if the graph has it, the prompt prints it): which fields of each graph group the prose
renderer reads while it renders an envelope, measured by tracking every key it touches. `reach(envelope)` gives, per
group, the fields held and the fields read; `python -m validators.graph_reach [envelope.json]` prints the table for the
four examples (or the envelope given). Reading is what printing needs; a field the renderer never reads cannot reach
the prompt.
"""

import copy
import json
import sys
from pathlib import Path

from planner.dependency_graph import ROOT
from validators.graph_map import EXAMPLES, MAP, _group

# the render node is the prompt itself, not a graph the prompt should print
OUTPUT = {"nodes.render"}


class _Tracked(dict):
    def __init__(self, data, log, group):
        super().__init__(data)
        self._log, self._group = log, group

    def _mark(self, key):
        self._log.setdefault(self._group, set()).add(key)

    def __getitem__(self, key):
        self._mark(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        self._mark(key)
        return super().get(key, default)

    def __contains__(self, key):
        self._mark(key)
        return super().__contains__(key)

    def items(self):
        for key in self:
            self._mark(key)
        return super().items()

    def values(self):
        for key in self:
            self._mark(key)
        return super().values()


def _tracked(envelope, log):
    envelope = copy.deepcopy(envelope)
    for _, _, where in MAP:
        holder = envelope
        for key in where[:-1]:
            holder = holder[key]
        group = holder.get(where[-1])
        if group is None:
            continue
        nested = isinstance(group, dict) and "items" in group
        items = [_Tracked(i, log, ".".join(where)) if isinstance(i, dict) else i for i in (group["items"] if nested else group)]
        if nested:
            group["items"] = items
        else:
            holder[where[-1]] = items
    return envelope


def reach(envelope):
    """{group: (fields held, fields the prose renderer reads)} for every graph group the envelope holds."""
    from renderers import prose_renderer

    render = envelope["nodes"]["render"]["items"][0]
    log = {}
    prose_renderer.render_all(_tracked(envelope, log), render["frame_parts"], render["labels"])
    out = {}
    for _, _, where in MAP:
        group = ".".join(where)
        items = _group(envelope, where)
        if not items or group in OUTPUT:
            continue
        held = {key for item in items if isinstance(item, dict) for key in item}
        out[group] = (held, held & log.get(group, set()))
    return out


def counts(envelope):
    """(fields held, fields read) summed over the groups."""
    found = reach(envelope)
    return sum(len(h) for h, _ in found.values()), sum(len(r) for _, r in found.values())


def markdown(envelopes):
    lines = ["| Envelope | Group | Held | Read | Never read |", "|---|---|---|---|---|"]
    for name, envelope in envelopes.items():
        for group, (held, read) in reach(envelope).items():
            lines.append(f"| {name} | {group} | {len(held)} | {len(read)} | {', '.join(sorted(held - read)) or '—'} |")
        held, read = counts(envelope)
        lines.append(f"| {name} | **all** | {held} | {read} | {held - read} never read |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    paths = sys.argv[1:] or [ROOT / "examples" / name / "envelope.json" for name in EXAMPLES]
    print(markdown({Path(p).parent.name: json.loads(Path(p).read_text(encoding="utf-8")) for p in paths}), end="")
