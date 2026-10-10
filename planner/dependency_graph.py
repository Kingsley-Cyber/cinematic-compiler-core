"""Load kernel/layer_order.yaml and resolve the compilation DAG for one modality.

The file is data, not code: this module reads it, checks its shape and derives
edges. Ordering rules live in planner/topological_sort.py; consistency rules in
validators/layer_dependency_validator.py.
"""

from pathlib import Path

import yaml

from kernel.canonical import ContractError

ROOT = Path(__file__).resolve().parents[1]
LAYER_ORDER = ROOT / "kernel" / "layer_order.yaml"
TOP_KEYS = {"version", "kernel", "envelope", "modalities", "pipeline_owned", "nodes"}
NODE_KEYS = {"id", "layer", "builds", "depends_on", "validated_by", "writes"}
OPTIONAL_NODE_KEYS = {"when", "external_inputs", "step"}
# A node checked by the constraint validator must run after the constraint graph exists.
ORDERING_VALIDATORS = {"constraint": "constraint"}


def load(path=LAYER_ORDER):
    order = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(order, dict) or set(order) != TOP_KEYS:
        raise ContractError("LAYER_ORDER_SHAPE", "Top-level keys must be exactly " + ", ".join(sorted(TOP_KEYS)))
    if not isinstance(order["nodes"], list) or not order["nodes"]:
        raise ContractError("LAYER_ORDER_SHAPE", "nodes must be a nonempty list")
    for index, node in enumerate(order["nodes"]):
        keys = set(node) if isinstance(node, dict) else set()
        if not NODE_KEYS <= keys or keys - NODE_KEYS - OPTIONAL_NODE_KEYS:
            raise ContractError("LAYER_ORDER_SHAPE", "Node keys differ from the layer-order contract",
                                f"nodes[{index}]")
        for key in ("depends_on", "validated_by", "writes", "when", "external_inputs"):
            value = node.get(key, [])
            if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
                raise ContractError("LAYER_ORDER_SHAPE", f"{key} must be a list of names", node.get("id"))
        if not all(isinstance(node[key], str) and node[key] for key in ("id", "layer", "builds") + (
                ("step",) if "step" in node else ())):
            raise ContractError("LAYER_ORDER_SHAPE", "id, layer, builds and step must be nonempty strings",
                                f"nodes[{index}]")
    return order


def node_index(order):
    return {node["id"]: node for node in order["nodes"]}


def is_active(node, modality):
    return "when" not in node or modality in node["when"]


def active_nodes(order, modality):
    if modality not in order["modalities"]:
        raise ContractError("MODALITY_UNKNOWN", "Modality is not declared in layer_order.yaml", modality)
    return [node["id"] for node in order["nodes"] if is_active(node, modality)]


def edges(order, modality):
    """(before, after) pairs among active nodes: data inputs plus validator ordering."""
    index = node_index(order)
    active = set(active_nodes(order, modality))
    result = []
    for node in order["nodes"]:
        if node["id"] not in active:
            continue
        for dependency in node["depends_on"]:
            if dependency in active:
                result.append((dependency, node["id"]))
            elif dependency in index and "when" not in index[dependency]:
                raise ContractError("LAYER_DEPENDENCY", "An unconditional dependency cannot be inactive", dependency)
        for validator, producer in ORDERING_VALIDATORS.items():
            if validator in node["validated_by"] and producer in active and producer != node["id"]:
                result.append((producer, node["id"]))
    return sorted(set(result), key=lambda pair: (pair[1], pair[0]))


def write_owners(order):
    """Envelope path -> owning node id (or 'pipeline')."""
    owners = {}
    for path in order["pipeline_owned"]:
        owners.setdefault(path, []).append("pipeline")
    for node in order["nodes"]:
        for path in node["writes"]:
            owners.setdefault(path, []).append(node["id"])
    return owners
