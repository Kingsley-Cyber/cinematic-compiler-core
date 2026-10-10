"""Run implemented passes in the DAG's build order (kernel/layer_order.yaml), stopping at a named node.

The pipeline owns /graph_version, /derived_from and /provenance. With `stamp=False` (tests, examples) the
time- and commit-dependent provenance fields are fixed placeholders, so the same inputs give the same bytes.
"""

import argparse
import subprocess
import sys
import time
from importlib import metadata

from kernel.canonical import ContractError, canonical_json
from kernel.kernel_files import kernel_hash
from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION
from planner.dependency_graph import ROOT, is_active, load, node_index
from planner.topological_sort import build_order

from .passes.mandatory import p01_intent, p02_brief, p03_constraint

VALIDATION_KEYS = ("schema", "invariants", "layer_dependency", "camera_kinematic_coupling", "post_generation")
UNSTAMPED = "unstamped"


def _compiler_version():
    try:
        return "cinematic-compiler@" + metadata.version("cinematic-compiler")
    except metadata.PackageNotFoundError:
        return "cinematic-compiler@unknown"


def _commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def skeleton(query="", *, stamp=False):
    """Pipeline-owned containers and provenance only; every layer path is written by its pass."""
    return {"graph_version": ENVELOPE_VERSION, "derived_from": KERNEL_VERSION, "nodes": {}, "edges": {},
            "invariants": [], "validation": dict.fromkeys(VALIDATION_KEYS),
            "provenance": {"source_prompt": query, "compiler_version": _compiler_version(),
                           "kernel_version": KERNEL_VERSION, "layer_order_version": LAYER_ORDER_VERSION,
                           "kernel_hash": kernel_hash(),
                           "build_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if stamp else UNSTAMPED,
                           "pass_history": [], "replan_count": 0, "replan_layers": [],
                           "chained_from_envelope_hash": None}}


def sequence_for(order, genre):
    if genre:
        return build_order(order, genre)
    # No genre yet: only nodes every modality runs; nothing modality-specific is assumed.
    index = node_index(order)
    return [n for n in build_order(order, order["modalities"][0])
            if all(is_active(index[n], m) for m in order["modalities"])]


def run(query, *, genre=None, duration_s=None, until="constraint", cards=None, stamp=False):
    order = load()
    index = node_index(order)
    passes = {"intent": lambda env: p01_intent.run(env, query, genre=genre, duration_s=duration_s, order=order),
              "brief": lambda env: p02_brief.run(env, cards=cards, order=order),
              "constraint": lambda env: p03_constraint.run(env, cards=cards, order=order)}
    sequence = sequence_for(order, genre)
    if until not in sequence:
        raise ContractError("PIPELINE_TARGET", "Unknown node, or one that needs a genre to be active", until)
    commit = _commit() if stamp else UNSTAMPED
    envelope = skeleton(query, stamp=stamp)
    for node in sequence[:sequence.index(until) + 1]:
        if node not in passes:
            raise ContractError("PASS_MISSING", "This node's pass is not implemented yet", node)
        started = time.perf_counter()
        envelope = passes[node](envelope)
        envelope["provenance"]["pass_history"].append({
            "pass": f"p{index[node]['step_id'][1:]}_{node}", "commit": commit,
            "duration_ms": round((time.perf_counter() - started) * 1000, 3) if stamp else 0})
    return envelope


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m compiler.pipeline")
    parser.add_argument("query")
    parser.add_argument("--genre")
    parser.add_argument("--until", default="constraint")
    parser.add_argument("--stamp", action="store_true", help="record build time, commit and pass durations")
    args = parser.parse_args(argv)
    sys.stdout.write(canonical_json(run(args.query, genre=args.genre, until=args.until, stamp=args.stamp)))


if __name__ == "__main__":
    main()
