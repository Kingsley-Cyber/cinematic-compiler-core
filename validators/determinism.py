"""Determinism (owner, 2026-10-13): a prompt is a function of its envelope's content, never of the order its keys
happen to sit in. The stored envelope sorts every key (kernel/canonical.py); the pipeline's own envelope keeps the
order each layer wrote. S-119 found the LBN prompt taking the joint order from the dict, so the same envelope gave
two prompts, one from memory and one from disk.

- JOINTS_IN_CANONICAL_ORDER: every joint list a prompt prints follows the kernel skeleton key (Sp, LUL, RUL, LL, RL,
  LA, RA, LFA, RFA, HD, NK), and the renderers' constant is that key.
- DETERMINISM: the envelope renders to the same bytes with every key order reversed, and the pipeline's in-memory
  envelope renders to the same bytes as the same envelope loaded from disk.

`python -m validators.determinism [envelope.json ...]` prints each prompt's hash both ways.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

from kernel.canonical import canonical_json
from kernel.kernel_files import load as load_kernel
from planner.dependency_graph import load
from solver.euler_solver import kernel_joints

LBN_JOINTS = re.compile(r'"joints":\{([^{}]*)\}')
PROSE_JOINTS = re.compile(r"Joints \{([^{}]*)\}")


def canonical():
    return tuple(kernel_joints(load_kernel("invariants")))


def joint_order_problems(texts):
    """[{code, message}] for each printed joint list out of the kernel order, in {name: prompt text}."""
    from renderers import anime_renderer

    order = canonical()
    out = []
    if tuple(anime_renderer.JOINT_ORDER) != order:
        out.append({"code": "JOINTS_IN_CANONICAL_ORDER",
                    "message": f"the renderers' joint order {anime_renderer.JOINT_ORDER} is not the kernel's {order}"})
    for name, text in texts.items():
        blocks = [re.findall(r'"(\w+)":', b) for b in LBN_JOINTS.findall(text)]
        blocks += [re.findall(r"(\w+): \[", b) for b in PROSE_JOINTS.findall(text)]
        for joints in blocks:
            rank = [order.index(j) if j in order else -1 for j in joints]
            if -1 in rank or rank != sorted(rank):
                out.append({"code": "JOINTS_IN_CANONICAL_ORDER",
                            "message": f"{name}: joints printed as {joints}, not in the kernel order"})
                break
    return out


def reverse_keys(value):
    """The same content with every object's keys in reverse order."""
    if isinstance(value, dict):
        return {key: reverse_keys(value[key]) for key in reversed(list(value))}
    if isinstance(value, list):
        return [reverse_keys(v) for v in value]
    return value


def render(envelope):
    """{prompt name: text}: S17 re-run on `envelope` (its document rebuilt from the render node)."""
    from validators import data_flow

    order = load()
    sequence = data_flow._sequence(envelope)
    after, _ = data_flow.run_layer("render", data_flow._strip(envelope, order, sequence, "render"), envelope, None, order)
    node = after["nodes"]["render"]["items"][0]
    return {"lbn": node["text"], **{f"prose_{mode}": row["text"] for mode, row in node["prose"].items()}}


def digest(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def problems(envelope, in_memory=None):
    """[{code, message}]: DETERMINISM when the prompts differ between key orders, or between `in_memory` (the
    pipeline's own envelope) and the same envelope loaded from disk; JOINTS_IN_CANONICAL_ORDER as above."""
    out = []
    disk = render(json.loads(canonical_json(envelope)))
    turned = render(reverse_keys(envelope))
    for name in disk:
        if digest(disk[name]) != digest(turned[name]):
            out.append({"code": "DETERMINISM", "message": f"{name}: the prompt changes with the envelope's key order"})
    if in_memory is not None:
        node = in_memory["nodes"]["render"]["items"][0]
        held = {"lbn": node["text"], **{f"prose_{mode}": row["text"] for mode, row in node["prose"].items()}}
        for name in disk:
            if digest(disk[name]) != digest(held[name]):
                out.append({"code": "DETERMINISM",
                            "message": f"{name}: the prompt from disk differs from the pipeline's in-memory prompt"})
    return out + joint_order_problems(disk)


if __name__ == "__main__":
    from validators.graph_map import load_examples

    envelopes = ({Path(p).parent.name: json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]}
                 or load_examples())
    for name, envelope in envelopes.items():
        disk, turned = render(envelope), render(reverse_keys(envelope))
        for prompt in disk:
            a, b = digest(disk[prompt]), digest(turned[prompt])
            print(f"{name} {prompt}: {a[7:23]} keys reversed {b[7:23]} {'SAME' if a == b else 'DIFFERS'}")
        for p in problems(envelope):
            print(f"  {p['code']}: {p['message']}")
