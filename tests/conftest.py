import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

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
                groups[kind][group] = {"band": node["band"], "step_id": node["step_id"],
                                       **({"projection": True} if node.get("projection") else {}), "items": []}
    from compiler.pipeline import skeleton

    intent = parse_intent("10s fight, 24fps, moonlit bamboo courtyard", genre=modality)
    scene = expand(intent)["scene"]
    scene.update(duration_s=10, duration_source="user",
                 quadrant={"linear": True, "causal": {"branching": 0, "parallel_effects": 0, "prerequisites": 0},
                           "style": 0, "quadrant": "D", "strata": [1], "load_bearing": False})
    base = skeleton("10s fight, 24fps, moonlit bamboo courtyard")
    return {**base, "intent": intent, "scene": scene, "nodes": groups["nodes"], "edges": groups["edges"]}
