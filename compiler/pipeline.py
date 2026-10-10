"""Run implemented passes in the DAG's build order (kernel/layer_order.yaml), stopping at a named node.

The pipeline owns /graph_version, /derived_from and /provenance. With `stamp=False` (tests, examples) the
time- and commit-dependent provenance fields are fixed placeholders, so the same inputs give the same bytes.
"""

import argparse
import json
import subprocess
import sys
import time
from importlib import metadata
from pathlib import Path

from compiler.authoring import AuthorRequired, record
from kernel.canonical import ContractError, canonical_json
from kernel.kernel_files import kernel_hash
from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION
from planner.dependency_graph import ROOT, is_active, load, node_index
from planner.topological_sort import build_order

from .passes.derived import p11_kinematic
from .passes.mandatory import p01_intent, p02_brief, p03_constraint, p04_temporal, p05_causal, p06_state, p07_contact

AUTHORED = {"temporal": p04_temporal, "kinematic": p11_kinematic}

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
                           "pass_history": [], "authored": [], "replan_count": 0, "replan_layers": [],
                           "chained_from_envelope_hash": None}}


def sequence_for(order, genre):
    if genre:
        return build_order(order, genre)
    # No genre yet: only nodes every modality runs; nothing modality-specific is assumed.
    index = node_index(order)
    return [n for n in build_order(order, order["modalities"][0])
            if all(is_active(index[n], m) for m in order["modalities"])]


def run(query, *, genre=None, duration_s=None, until="constraint", cards=None, plans=None, load_bearing=False,
        stamp=False):
    order = load()
    index = node_index(order)
    plans = plans or {}

    def authored(node):
        module = AUTHORED[node]

        def step(envelope):
            plan = plans.get(node)
            if plan is None:
                raise AuthorRequired(index[node]["step_id"], module.prepare(envelope))
            after, packet = module.run(envelope, plan, order=order)
            provenance = after["provenance"]
            provenance["authored"].append(record(index[node]["step_id"], packet, plan))
            provenance["replan_count"] += plan["attempt"] - 1
            provenance["replan_layers"].extend([index[node]["step_id"]] * (plan["attempt"] - 1))
            return after
        return step

    passes = {"intent": lambda env: p01_intent.run(env, query, genre=genre, duration_s=duration_s, order=order),
              "brief": lambda env: p02_brief.run(env, cards=cards, order=order),
              "constraint": lambda env: p03_constraint.run(env, cards=cards, order=order),
              "causal": lambda env: p05_causal.run(env, order=order, load_bearing=load_bearing),
              "state": lambda env: p06_state.run(env, order=order),
              "contact": lambda env: p07_contact.run(env, order=order),
              **{node: authored(node) for node in AUTHORED}}
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
    parser.add_argument("--duration", type=float)
    parser.add_argument("--plans", help="folder of authored documents named <node>.json")
    parser.add_argument("--packet-out", help="where to write the packet when a step needs authoring")
    parser.add_argument("--load-bearing", action="store_true", help="scene is load-bearing for the film (stratum 4)")
    parser.add_argument("--stamp", action="store_true", help="record build time, commit and pass durations")
    args = parser.parse_args(argv)
    plans = {}
    if args.plans:
        plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(args.plans).glob("*.json"))}
    duration = int(args.duration) if args.duration is not None and args.duration.is_integer() else args.duration
    try:
        envelope = run(args.query, genre=args.genre, duration_s=duration, until=args.until, plans=plans,
                       load_bearing=args.load_bearing, stamp=args.stamp)
    except AuthorRequired as needed:
        text = canonical_json(needed.packet)
        if args.packet_out:
            Path(args.packet_out).write_text(text, encoding="utf-8")
            print(f"{needed.step_id} needs authoring; packet written to {args.packet_out}", file=sys.stderr)
        else:
            sys.stdout.write(text)
        sys.exit(3)
    sys.stdout.write(canonical_json(envelope))


if __name__ == "__main__":
    main()
