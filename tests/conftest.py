import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from planner.dependency_graph import is_active, load  # noqa: E402


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
                groups[kind][group] = {"layer": node["layer"], "items": []}
    return {
        "graph_version": "MGRAPH-1.1", "derived_from": "LBN-2.4",
        "scene": {"duration_s": 10, "fps": 24, "genre": modality, "world": "bamboo_courtyard",
                  "setting": "moonlit bamboo courtyard", "ax": {"up": "Y", "forward": "+Z", "ground": "y=0"}},
        "nodes": groups["nodes"], "edges": groups["edges"], "invariants": [],
        "validation": {"schema": None, "invariants": None, "layer_dependency": None,
                       "camera_kinematic_coupling": None, "post_generation": None},
        "provenance": {"source_prompt": "10s anime fight, 24fps, moonlit bamboo courtyard",
                       "compiler_version": "cinematic-compiler@0.1.0", "kernel_version": "LBN-2.4",
                       "layer_order_version": "1.0", "build_timestamp": "2026-10-10T00:00:00Z",
                       "pass_history": [], "replan_count": 0, "replan_layers": []}}
