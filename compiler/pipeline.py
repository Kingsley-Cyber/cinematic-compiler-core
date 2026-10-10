"""Run implemented passes in the DAG's build order (kernel/layer_order.yaml), stopping at a named node."""

import argparse
import sys

from kernel.canonical import ContractError, canonical_json
from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION
from planner.dependency_graph import is_active, load, node_index
from planner.topological_sort import build_order

from .passes.mandatory import p01_intent, p02_brief, p03_constraint

VALIDATION_KEYS = ("schema", "invariants", "layer_dependency", "camera_kinematic_coupling", "post_generation")


def skeleton():
    """Pipeline-owned containers only; every layer path is written by its pass."""
    return {"graph_version": ENVELOPE_VERSION, "derived_from": KERNEL_VERSION, "nodes": {}, "edges": {},
            "invariants": [], "validation": dict.fromkeys(VALIDATION_KEYS)}


def run(query, *, genre=None, duration_s=None, until="constraint", cards=None):
    order = load()
    passes = {"intent": lambda env: p01_intent.run(env, query, genre=genre, duration_s=duration_s, order=order),
              "brief": lambda env: p02_brief.run(env, cards=cards, order=order),
              "constraint": lambda env: p03_constraint.run(env, cards=cards, order=order)}
    if genre:
        sequence = build_order(order, genre)
    else:
        # No genre yet: only nodes every modality runs; nothing modality-specific is assumed.
        index = node_index(order)
        sequence = [n for n in build_order(order, order["modalities"][0])
                    if all(is_active(index[n], m) for m in order["modalities"])]
    if until not in sequence:
        raise ContractError("PIPELINE_TARGET", "Unknown node, or one that needs a genre to be active", until)
    envelope = skeleton()
    for node in sequence[:sequence.index(until) + 1]:
        if node not in passes:
            raise ContractError("PASS_MISSING", "This node's pass is not implemented yet", node)
        envelope = passes[node](envelope)
    return envelope


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m compiler.pipeline")
    parser.add_argument("query")
    parser.add_argument("--genre")
    parser.add_argument("--until", default="constraint")
    args = parser.parse_args(argv)
    sys.stdout.write(canonical_json(run(args.query, genre=args.genre, until=args.until)))


if __name__ == "__main__":
    main()
