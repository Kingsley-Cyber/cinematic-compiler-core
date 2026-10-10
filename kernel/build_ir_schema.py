"""Generate schemas/cinematic_ir.schema.json (the MGRAPH envelope) from kernel/layer_order.yaml.

Group names and their layer tags come only from the DAG file. Per-graph item
schemas are added by each layer slice; until then an item needs a stable `id`.
After regenerating, record the change in the schema log:

    python -m kernel.build_ir_schema
    python -m kernel.schema_log record schemas/cinematic_ir.schema.json --change changed --reason "..." --decided-by ...
"""

import json
import sys

from planner.dependency_graph import ROOT, load

from .version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION

TARGET = ROOT / "schemas" / "cinematic_ir.schema.json"
VALIDATION_KEYS = ["schema", "invariants", "layer_dependency", "camera_kinematic_coupling", "post_generation"]


def _string(min_length=1):
    return {"type": "string", "minLength": min_length}


def build(order):
    labels = []
    groups = {"nodes": {}, "edges": {}}
    required = {"nodes": [], "edges": []}
    for node in order["nodes"]:
        if node["layer"] not in labels:
            labels.append(node["layer"])
        for path in node["writes"]:
            kind, _, group = path.strip("/").partition("/")
            if kind in groups:
                groups[kind][group] = {"$ref": "#/$defs/Group_" + node["layer"]}
                if "when" not in node:
                    required[kind].append(group)
    defs = {"Group_" + label: {
        "type": "object", "required": ["layer", "items"], "additionalProperties": False,
        "properties": {"layer": {"const": label}, "items": {"type": "array", "items": {"$ref": "#/$defs/Item"}}}}
        for label in labels}
    defs["Item"] = {"type": "object", "required": ["id"], "properties": {"id": _string()},
                    "description": "Per-graph item fields are fixed by that layer's schema when its slice lands."}
    defs["Scene"] = {"type": "object", "additionalProperties": False,
        "required": ["duration_s", "fps", "genre", "world", "setting", "ax"],
        "properties": {"duration_s": {"type": "number", "exclusiveMinimum": 0},
                       "fps": {"type": "integer", "minimum": 1},
                       "genre": {"enum": list(order["modalities"])},
                       "world": _string(), "setting": _string(),
                       "ax": {"type": "object", "description": "Axis and set geometry; fixed by the L0 slice."}}}
    defs["Invariant"] = {"type": "object", "additionalProperties": False, "required": ["id", "layer", "rule"],
        "properties": {"id": _string(), "layer": {"enum": labels}, "rule": _string()}}
    defs["Validation"] = {"type": "object", "additionalProperties": False, "required": VALIDATION_KEYS,
        "properties": {key: {"enum": ["pass", "fail", None]} for key in VALIDATION_KEYS}}
    defs["Provenance"] = {"type": "object", "additionalProperties": False,
        "required": ["source_prompt", "compiler_version", "kernel_version", "layer_order_version",
                     "build_timestamp", "pass_history", "replan_count", "replan_layers"],
        "properties": {"source_prompt": _string(), "compiler_version": _string(),
                       "kernel_version": {"const": KERNEL_VERSION},
                       "layer_order_version": {"const": LAYER_ORDER_VERSION},
                       "build_timestamp": _string(),
                       "pass_history": {"type": "array", "items": {
                           "type": "object", "additionalProperties": False,
                           "required": ["pass", "commit", "duration_ms"],
                           "properties": {"pass": {"type": "string", "pattern": "^p[0-9]{2}_[a-z0-9_]+$"},
                                          "commit": _string(), "duration_ms": {"type": "number", "minimum": 0}}}},
                       "replan_count": {"type": "integer", "minimum": 0},
                       "replan_layers": {"type": "array", "items": {"enum": labels}}}}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:cinematic-compiler:schema:cinematic_ir:{ENVELOPE_VERSION}",
        "title": "Cinematic IR: movement-graph envelope",
        "description": "Generated from kernel/layer_order.yaml by kernel/build_ir_schema.py; do not edit by hand.",
        "type": "object", "additionalProperties": False,
        "required": ["graph_version", "derived_from", "scene", "nodes", "edges", "invariants", "validation",
                     "provenance"],
        "properties": {
            "graph_version": {"const": ENVELOPE_VERSION},
            "derived_from": {"const": KERNEL_VERSION},
            "scene": {"$ref": "#/$defs/Scene"},
            "nodes": {"type": "object", "additionalProperties": False, "properties": groups["nodes"],
                      "required": required["nodes"]},
            "edges": {"type": "object", "additionalProperties": False, "properties": groups["edges"],
                      "required": required["edges"]},
            "invariants": {"type": "array", "items": {"$ref": "#/$defs/Invariant"}},
            "validation": {"$ref": "#/$defs/Validation"},
            "provenance": {"$ref": "#/$defs/Provenance"}},
        "$defs": defs}


def render(order):
    return json.dumps(build(order), indent=2, ensure_ascii=False) + "\n"


def main():
    text = render(load())
    if "--check" in sys.argv:
        sys.exit(0 if TARGET.exists() and TARGET.read_text(encoding="utf-8") == text else 1)
    TARGET.write_text(text, encoding="utf-8")
    print(TARGET.relative_to(ROOT))


if __name__ == "__main__":
    main()
