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
# Owned sub-schemas embedded under $defs (the checker resolves document-local refs only).
EMBEDDED = {"Intent": ROOT / "schemas" / "intent_document.schema.json"}
VALIDATION_KEYS = ["schema", "invariants", "layer_dependency", "camera_kinematic_coupling", "post_generation"]


def _string(min_length=1):
    return {"type": "string", "minLength": min_length}


def _group(layer, step, projection=False):
    """A node/edge group tagged with its band and step; items may repeat the band tag."""
    properties = {"band": {"const": layer}}
    if step:
        properties["step_id"] = {"const": step}
    if projection:
        properties["projection"] = {"const": True}
    properties["items"] = {"type": "array", "items": {
        "type": "object", "required": ["id"], "properties": {"id": _string(), "band": {"const": layer}},
        "description": "Per-graph item fields are fixed by that layer's schema when its slice lands."}}
    return {"type": "object", "additionalProperties": False, "properties": properties,
            "required": ["band"] + (["step_id"] if step else []) + (["projection"] if projection else []) + ["items"]}


def _embed(name, path):
    """Copy a sub-schema into $defs, renaming its own $defs so references stay local and unique."""
    schema = json.loads(path.read_text(encoding="utf-8"))
    text = json.dumps({k: v for k, v in schema.items() if k not in ("$schema", "$id")})
    inner = json.loads(text.replace('"#/$defs/', f'"#/$defs/{name}_'))
    defs = {f"{name}_{key}": value for key, value in inner.pop("$defs", {}).items()}
    inner["description"] = f"Embedded from {path.relative_to(ROOT).as_posix()}. " + inner.get("description", "")
    return {name: inner, **defs}


def build(order):
    labels, steps = [], []
    groups = {"nodes": {}, "edges": {}}
    required = {"nodes": [], "edges": []}
    defs = {}
    for node in order["nodes"]:
        if node["band"] not in labels:
            labels.append(node["band"])
        step = node.get("step_id")
        if step:
            steps.append(step)
        name = "Group_" + (step or node["band"])
        defs.setdefault(name, _group(node["band"], step, node.get("projection", False)))
        for path in node["writes"]:
            kind, _, group = path.strip("/").partition("/")
            if kind in groups:
                groups[kind][group] = {"$ref": "#/$defs/" + name}
                if "when" not in node:
                    required[kind].append(group)
    for name, path in EMBEDDED.items():
        defs.update(_embed(name, path))
    carve_outs = sorted(path.split("/")[2] for node in order["nodes"] if node["id"] != "brief"
                        for path in node["writes"] if path.startswith("/scene/"))
    source = {"type": ["string", "null"],
              "pattern": "^(user|flag|default|beat_plan_end|kernel|card:[a-z][a-z0-9_]*|kernel\\+card:[a-z][a-z0-9_]*)$"}
    convention = json.loads((ROOT / "schemas" / "kernel_conventions.schema.json").read_text(encoding="utf-8"))
    quadrant = {"type": "object", "additionalProperties": False,
        "required": ["linear", "causal", "style", "quadrant", "strata", "load_bearing"],
        "properties": {"linear": {"type": "boolean"},
                       "causal": {"type": "object", "additionalProperties": False,
                                  "required": ["branching", "parallel_effects", "prerequisites"],
                                  "properties": {k: {"type": "integer", "minimum": 0, "maximum": 2}
                                                 for k in ("branching", "parallel_effects", "prerequisites")}},
                       "style": {"type": "integer", "minimum": 0, "maximum": 2},
                       "quadrant": {"enum": ["A", "B", "C", "D"]},
                       "strata": {"type": "array", "uniqueItems": True, "items": {"enum": [1, 2, 3, 4]}},
                       "load_bearing": {"type": "boolean"},
                       "carried_causes": {"type": "array", "items": _string(),
                                          "description": "Chained clip: the previous clip's unresolved causes (open beats)."}}}
    scene_properties = {
        "genre": {"enum": list(order["modalities"])}, "genre_source": source,
        "fps": {"type": "number", "exclusiveMinimum": 0}, "fps_source": source,
        "duration_s": {"type": "number", "exclusiveMinimum": 0}, "duration_source": source,
        "world": {"type": ["string", "null"], "pattern": "^[a-z][a-z0-9_]*$"}, "world_source": source,
        "setting": {"type": ["string", "null"], "minLength": 1}, "setting_source": source,
        "style_reference": {"type": ["string", "null"], "minLength": 1}, "style_reference_source": source,
        "ax": {"type": "object", "additionalProperties": False,
               "required": ["up", "forward", "ground", "unit", "rotation_convention"],
               "properties": {"up": convention["properties"]["up"], "forward": convention["properties"]["forward"],
                              "ground": _string(), "unit": {"enum": ["m", "scene_unit", None]},
                              "rotation_convention": convention["properties"]["rotation_convention"]}},
        "ax_source": source,
        "quadrant": quadrant,
        "chained_from": {"anyOf": [{"type": "null"}, {"$ref": "#/$defs/ChainedFrom"}],
                         "description": "M5.5: what this clip continues (planner/chaining.py), or null for a first clip."},
        "missing": {"type": "array", "uniqueItems": True, "items": {
            "enum": ["world", "setting", "style_reference", "choreography", "camera_plan", "geometry_anchors"]}},
        "ambiguous": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["field", "candidates", "reason"],
            "properties": {"field": {"enum": ["world"]}, "reason": _string(),
                           "candidates": {"type": "array", "minItems": 2, "items": _string()}}}},
        "unresolved_hints": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["hint", "field", "reason"],
            "properties": {"hint": _string(), "reason": _string(),
                           "field": {"enum": ["entities_hinted", "props_hinted"]}}}}}
    subject = {"type": "object", "additionalProperties": False, "required": ["kind", "id"],
               "properties": {"kind": {"enum": ["entity", "prop", "surface"]}, "id": _string()}}
    vec = {"anyOf": [{"type": "null"}, {"type": "array", "minItems": 3, "maxItems": 3, "items": {"type": "number"}}]}
    defs["ChainedFrom"] = {"type": "object", "additionalProperties": False,
        "required": ["envelope_sha256", "source_prompt", "world", "duration_s", "end_states", "active_contacts", "open_beats",
                     "last_shot"],
        "properties": {
            "envelope_sha256": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"}, "source_prompt": {"type": "string"},
            "world": {"type": ["string", "null"]}, "duration_s": {"type": "number", "exclusiveMinimum": 0},
            "end_states": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                      "required": ["subject", "conditions", "pos", "facing"],
                                                      "properties": {"subject": subject, "conditions": {"type": "object"},
                                                                     "pos": vec, "facing": vec}}},
            "active_contacts": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                           "required": ["a", "body_part", "b", "contact_type", "since"],
                                                           "properties": {"a": _string(), "body_part": _string(),
                                                                          "b": {"type": "object"},
                                                                          "contact_type": {"enum": ["possess", "support"]},
                                                                          "since": {"type": "number", "minimum": 0}}}},
            "open_beats": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                      "required": ["id", "label", "action"],
                                                      "properties": {"id": _string(), "label": _string(), "action": _string()}}},
            "last_shot": {"anyOf": [{"type": "null"}, {"type": "object", "additionalProperties": False,
                                                       "required": ["id", "side", "azimuth_deg", "scale", "target"],
                                                       "properties": {"id": _string(), "side": _string(),
                                                                      "azimuth_deg": {"type": "number"}, "scale": _string(),
                                                                      "target": _string()}}]}}}
    defs["Scene"] = {"type": "object", "additionalProperties": False,
        "description": "S02 writes the scene; carve-outs " + ", ".join(carve_outs) + " are written by later steps. "
                       "Every value names its source; `default` marks a filled default.",
        "required": list(scene_properties), "properties": scene_properties}
    defs["SceneS02"] = {"type": "object", "additionalProperties": False,
        "description": "The scene as S02 writes it (carve-outs absent).",
        "required": [k for k in scene_properties if k not in carve_outs],
        "properties": {k: v for k, v in scene_properties.items() if k not in carve_outs}}
    defs["Invariant"] = {"type": "object", "additionalProperties": False, "required": ["id", "band", "rule"],
        "properties": {"id": _string(), "band": {"enum": labels}, "rule": _string()}}
    defs["Validation"] = {"type": "object", "additionalProperties": False, "required": VALIDATION_KEYS,
        "properties": {key: {"enum": ["pass", "fail", None]} for key in VALIDATION_KEYS}}
    defs["Provenance"] = {"type": "object", "additionalProperties": False,
        "required": ["source_prompt", "compiler_version", "kernel_version", "layer_order_version", "kernel_hash",
                     "build_timestamp", "pass_history", "authored", "replan_count", "replan_layers",
                     "chained_from_envelope_hash"],
        "properties": {"source_prompt": {"type": "string"}, "compiler_version": _string(),
                       "kernel_version": {"const": KERNEL_VERSION},
                       "layer_order_version": {"const": LAYER_ORDER_VERSION},
                       "kernel_hash": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
                       "build_timestamp": _string(),
                       "chained_from_envelope_hash": {"anyOf": [{"type": "null"},
                                                                {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"}]},
                       "pass_history": {"type": "array", "items": {
                           "type": "object", "additionalProperties": False,
                           "required": ["pass", "commit", "duration_ms"],
                           "properties": {"pass": {"type": "string", "pattern": "^p[0-9]{2}_[a-z0-9_]+$"},
                                          "commit": _string(), "duration_ms": {"type": "number", "minimum": 0}}}},
                       "authored": {"type": "array", "items": {
                           "type": "object", "additionalProperties": False,
                           "required": ["step_id", "packet_sha256", "document_sha256", "author", "attempt"],
                           "properties": {"step_id": {"enum": steps},
                                          "packet_sha256": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
                                          "document_sha256": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
                                          "author": {"type": "object", "additionalProperties": False,
                                                     "required": ["host", "model"],
                                                     "properties": {"host": _string(), "model": _string()}},
                                          "attempt": {"type": "integer", "minimum": 1, "maximum": 3}}}},
                       "replan_count": {"type": "integer", "minimum": 0},
                       "replan_layers": {"type": "array", "items": {"enum": labels + steps}}}}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:cinematic-compiler:schema:cinematic_ir:{ENVELOPE_VERSION}",
        "title": "Cinematic IR: movement-graph envelope",
        "description": "Generated from kernel/layer_order.yaml by kernel/build_ir_schema.py; do not edit by hand.",
        "type": "object", "additionalProperties": False,
        "required": ["graph_version", "derived_from", "intent", "scene", "nodes", "edges", "invariants",
                     "validation", "provenance"],
        "properties": {
            "graph_version": {"const": ENVELOPE_VERSION},
            "derived_from": {"const": KERNEL_VERSION},
            "intent": {"$ref": "#/$defs/Intent"},
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
