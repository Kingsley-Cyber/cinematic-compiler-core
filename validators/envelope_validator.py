"""Validate an envelope at any stage: owner tags, every present group against its graph schema, scene and intent,
kernel freshness; a complete envelope is also checked against the full envelope schema and its genre schema."""

import json

from kernel.kernel_files import kernel_hash
from planner.dependency_graph import ROOT, is_active, load
from planner.modality import load as load_modality
from validators.layer_dependency_validator import check_envelope
from validators.schema_validator import ContractError, validate_schema

GRAPHS = ROOT / "schemas" / "graphs"
GROUP_SCHEMAS = {  # schema file -> {schema key: (kind, envelope group)}
    "brief_nodes": {"entities": ("nodes", "entities"), "props": ("nodes", "props"), "surfaces": ("nodes", "surfaces")},
    "constraint_graph": {"constraints": ("nodes", "constraints"), "applications": ("edges", "constraint_application"),
                         "invariants": ("top", "invariants")},
    "temporal_graph": {"beats": ("nodes", "beats"), "temporal": ("edges", "temporal"),
                       "beat_constraint": ("edges", "beat_constraint")},
    "causal_graph": {"causal": ("edges", "causal")},
    "state_graph": {"states": ("nodes", "states"), "state_transition": ("edges", "state_transition")},
    "contact_graph": {"contacts": ("nodes", "contacts"), "contact": ("edges", "contact")},
    "kinematic_graph": {"kinematic": ("nodes", "kinematic"), "kinematic_transition": ("edges", "kinematic_transition")},
    "bartenieff_graph": {"bartenieff": ("nodes", "bartenieff"), "bartenieff_transition": ("edges", "bartenieff_transition")},
    "motion_graph": {"motion": ("nodes", "motion"), "motion_edges": ("edges", "motion")},
    "effort_graph": {"efforts": ("nodes", "efforts"), "effort": ("edges", "effort")},
    "camera_graph": {"camera": ("nodes", "camera"), "camera_edges": ("edges", "camera")},
    "render": {"render": ("nodes", "render")},
}


def _items(envelope, kind, group):
    if kind == "top":
        return envelope.get(group)
    found = envelope.get(kind, {}).get(group)
    return None if found is None else found["items"]


def validate_envelope(envelope):
    findings = []

    def attempt(label, value, schema):
        try:
            validate_schema(value, schema)
        except ContractError as error:
            findings.append({"code": "SCHEMA", "message": f"{label}: {error.message}", "detail": error.path})

    order = load()
    envelope_schema = json.loads((ROOT / "schemas" / "cinematic_ir.schema.json").read_text(encoding="utf-8"))
    defs = envelope_schema["$defs"]
    if envelope.get("provenance", {}).get("kernel_hash") != kernel_hash():
        findings.append({"code": "STALE_KERNEL", "message": "Built against a different kernel", "detail": None})
    if "intent" in envelope:
        attempt("intent", envelope["intent"], {"$ref": "#/$defs/Intent", "$defs": defs})
    scene = envelope.get("scene")
    if scene is not None:
        carve = {k: v for k, v in scene.items() if k not in defs["SceneS02"]["properties"]}
        attempt("scene", {k: v for k, v in scene.items() if k not in carve}, {"$ref": "#/$defs/SceneS02", "$defs": defs})
        for key, value in carve.items():
            attempt(f"scene.{key}", value, defs["Scene"]["properties"].get(key, False))
        findings.extend(row for row in check_envelope_partial(envelope, order))
    for name, parts in GROUP_SCHEMAS.items():
        present = {key: _items(envelope, *where) for key, where in parts.items()}
        if all(value is not None for value in present.values()):
            attempt(name, present, json.loads((GRAPHS / f"{name}.schema.json").read_text(encoding="utf-8")))
    genre = (scene or {}).get("genre")
    required = [p.split("/")[2] for n in order["nodes"] if genre and is_active(n, genre)
                for p in n["writes"] if p.startswith(("/nodes/", "/edges/"))]
    complete = bool(genre) and all(any(g in envelope.get(k, {}) for k in ("nodes", "edges")) for g in required)
    if complete:
        attempt("envelope", envelope, envelope_schema)
        attempt("modality", envelope, load_modality(genre))
    return {"ok": not findings, "complete": complete, "findings": findings}


def check_envelope_partial(envelope, order):
    """Owner tags for the groups present; missing groups are expected before the pipeline finishes."""
    return [row for row in check_envelope(envelope, order) if row["code"] != "MISSING_GROUP"]
