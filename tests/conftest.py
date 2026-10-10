import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION  # noqa: E402
from planner.dependency_graph import is_active, load  # noqa: E402
from planner.intent_parser import parse_intent  # noqa: E402
from planner.query_expander import expand  # noqa: E402


@pytest.fixture
def order():
    return copy.deepcopy(load())


@pytest.fixture
def envelope_schema():
    return json.loads((ROOT / "schemas" / "cinematic_ir.schema.json").read_text(encoding="utf-8"))


def empty_envelope(order, modality):
    """A structurally valid envelope with every active layer's groups present and empty."""
    groups = {"nodes": {}, "edges": {}}
    for node in order["nodes"]:
        if not is_active(node, modality):
            continue
        for path in node["writes"]:
            kind, _, group = path.strip("/").partition("/")
            if kind in groups:
                groups[kind][group] = {"band": node["band"], "step_id": node["step_id"], "items": []}
    intent = parse_intent("10s fight, 24fps, moonlit bamboo courtyard", genre=modality)
    return {
        "graph_version": ENVELOPE_VERSION, "derived_from": KERNEL_VERSION,
        "intent": intent, "scene": expand(intent)["scene"],
        "nodes": groups["nodes"], "edges": groups["edges"], "invariants": [],
        "validation": {"schema": None, "invariants": None, "layer_dependency": None,
                       "camera_kinematic_coupling": None, "post_generation": None},
        "provenance": {"source_prompt": "10s anime fight, 24fps, moonlit bamboo courtyard",
                       "compiler_version": "cinematic-compiler@0.1.0", "kernel_version": KERNEL_VERSION,
                       "layer_order_version": LAYER_ORDER_VERSION, "build_timestamp": "2026-10-10T00:00:00Z",
                       "pass_history": [], "replan_count": 0, "replan_layers": []}}
