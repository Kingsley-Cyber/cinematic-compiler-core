"""The graph map (owner, 2026-10-13: "Map first. Migrate second. Check third."): every graph group the compiler writes
into an envelope, set against the schema section that declares it, measured on the four examples (and any envelope
given). For each group: whether its data conforms to its schema (GRAPH_SCHEMA), the fields its schema declares that
no envelope fills, the fields an envelope holds that its schema does not declare, and the groups or schema sections
with no partner. `python -m validators.graph_map > docs/graph_map.md` writes the map; `problems(envelope)` is the
conformance check the gate runs on every example.
"""

import json
import sys
from pathlib import Path

from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema

GRAPHS = ROOT / "schemas" / "graphs"
EXAMPLES = ("reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo")
# (schema file, schema section, where the envelope holds it): the section names that differ from the envelope's
# group names are written here (camera_edges, motion_edges, applications, invariants)
MAP = [
    ("brief_nodes", "entities", ("nodes", "entities")), ("brief_nodes", "props", ("nodes", "props")),
    ("brief_nodes", "surfaces", ("nodes", "surfaces")),
    ("constraint_graph", "constraints", ("nodes", "constraints")),
    ("constraint_graph", "applications", ("edges", "constraint_application")),
    ("constraint_graph", "invariants", ("invariants",)),
    ("temporal_graph", "beats", ("nodes", "beats")), ("temporal_graph", "temporal", ("edges", "temporal")),
    ("temporal_graph", "beat_constraint", ("edges", "beat_constraint")),
    ("causal_graph", "causal", ("edges", "causal")),
    ("state_graph", "states", ("nodes", "states")), ("state_graph", "state_transition", ("edges", "state_transition")),
    ("contact_graph", "contacts", ("nodes", "contacts")), ("contact_graph", "contact", ("edges", "contact")),
    ("hand_role_graph", "hand_role", ("nodes", "hand_role")),
    ("hand_role_graph", "hand_role_transition", ("edges", "hand_role_transition")),
    ("object_state_graph", "object_state", ("nodes", "object_state")),
    ("object_state_graph", "object_state_transition", ("edges", "object_state_transition")),
    ("affordance_graph", "affordance", ("nodes", "affordance")),
    ("affordance_graph", "affordance_dependency", ("edges", "affordance_dependency")),
    ("kinematic_graph", "kinematic", ("nodes", "kinematic")),
    ("kinematic_graph", "kinematic_transition", ("edges", "kinematic_transition")),
    ("bartenieff_graph", "bartenieff", ("nodes", "bartenieff")),
    ("bartenieff_graph", "bartenieff_transition", ("edges", "bartenieff_transition")),
    ("motion_graph", "motion", ("nodes", "motion")), ("motion_graph", "motion_edges", ("edges", "motion")),
    ("pose_mechanics_graph", "pose_mechanics", ("nodes", "pose_mechanics")),
    ("pose_mechanics_graph", "pose_mechanics_transition", ("edges", "pose_mechanics_transition")),
    ("facial_graph", "facial", ("nodes", "facial")), ("facial_graph", "facial_transition", ("edges", "facial_transition")),
    ("effort_graph", "efforts", ("nodes", "efforts")), ("effort_graph", "effort", ("edges", "effort")),
    ("camera_graph", "camera", ("nodes", "camera")), ("camera_graph", "camera_edges", ("edges", "camera")),
    ("render", "render", ("nodes", "render")),
]


def _schema(name):
    return json.loads((GRAPHS / f"{name}.schema.json").read_text(encoding="utf-8"))


def _items_schema(schema, section):
    """The schema of one item of a section (its `$ref` resolved), or None when the section is not an array."""
    node = schema["properties"][section]
    node = node.get("items") if node.get("type") == "array" else None
    while isinstance(node, dict) and "$ref" in node:
        node = schema["$defs"][node["$ref"].split("/")[-1]]
    return node


def _group(envelope, where):
    """The items an envelope holds at `where`, or None when it holds no such group."""
    value = envelope
    for key in where:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value.get("items") if isinstance(value, dict) and "items" in value else value


def problems(envelope):
    """[{code, group, message}]: GRAPH_SCHEMA for a group whose data its schema refuses (every group the map knows)."""
    out = []
    for name, section, where in MAP:
        items = _group(envelope, where)
        if items is None:
            continue
        schema = _schema(name)
        part = {**schema, "required": [section], "properties": {section: schema["properties"][section]}}
        try:
            validate_schema({section: items}, part)
        except Exception as refused:  # noqa: BLE001 - the validator's own error carries the path
            out.append({"code": "GRAPH_SCHEMA", "group": ".".join(where),
                        "message": f"{'.'.join(where)} does not conform to {name}.{section}: {str(refused)[:200]}"})
    return out


def measure(envelopes):
    """[{schema, section, group, declared, required, seen, never_filled, undeclared, conforms, items, envelopes}]."""
    rows = []
    for name, section, where in MAP:
        schema = _schema(name)
        item = _items_schema(schema, section)
        declared = sorted(item.get("properties", {})) if isinstance(item, dict) else []
        seen, count, holders = set(), 0, 0
        for envelope in envelopes.values():
            items = _group(envelope, where)
            if items is None:
                continue
            holders += 1
            for one in items if isinstance(items, list) else []:
                count += 1
                seen |= set(one) if isinstance(one, dict) else set()
        conforms = all(not [p for p in problems(e) if p["group"] == ".".join(where)] for e in envelopes.values())
        rows.append({"schema": name, "section": section, "group": ".".join(where), "declared": declared,
                     "required": sorted(item.get("required", [])) if isinstance(item, dict) else [],
                     "seen": sorted(seen), "never_filled": sorted(set(declared) - seen) if count else [],
                     "undeclared": sorted(seen - set(declared)) if declared else [], "conforms": conforms,
                     "items": count, "envelopes": holders,
                     "closed": isinstance(item, dict) and item.get("additionalProperties") is False})
    return rows


def unmapped(envelopes):
    """(envelope groups no schema section maps, schema sections no map entry names)."""
    mapped = {".".join(where) for _, _, where in MAP}
    groups = {f"{kind}.{group}" for e in envelopes.values() for kind in ("nodes", "edges") for group in e.get(kind, {})}
    sections = {(f.name.removesuffix(".schema.json"), s) for f in GRAPHS.glob("*_graph.schema.json")
                for s in json.loads(f.read_text(encoding="utf-8")).get("properties", {})}
    named = {(n, s) for n, s, _ in MAP}
    return sorted(groups - mapped), sorted(sections - named)


def load_examples(extra=()):
    envelopes = {name: json.loads((ROOT / "examples" / name / "envelope.json").read_text(encoding="utf-8"))
                 for name in EXAMPLES}
    for path in extra:
        envelopes[Path(path).parent.name] = json.loads(Path(path).read_text(encoding="utf-8"))
    return envelopes


def markdown(envelopes):
    rows = measure(envelopes)
    lost_groups, lost_sections = unmapped(envelopes)
    names = ", ".join(envelopes)
    out = ["# The graph map", "", "<!-- docs-version: 1.0 -->", "",
           f"Generated by `python -m validators.graph_map` from: {names}. Every graph group an envelope holds, set "
           "against the schema section that declares it (owner, 2026-10-13: map first, migrate second, check third).", "",
           "## 1. Graphs and their schemas", "",
           "| Group | Schema section | Items | Envelopes | Fields seen | Conforms |", "|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['group']} | {r['schema']}.{r['section']} | {r['items']} | {r['envelopes']} | {len(r['seen'])} | "
                   f"{'yes' if r['conforms'] else '**no**'} |")
    out += ["", "## 2. Schema sections", "",
            "| Schema section | Fields declared | Required | Closed (no extra fields) |", "|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['schema']}.{r['section']} | {len(r['declared'])} | {len(r['required'])} | "
                   f"{'yes' if r['closed'] else '**no**'} |")
    out += ["", "## 3. Comparison", "",
            "| Group | Declared, never filled | Held, not declared |", "|---|---|---|"]
    for r in rows:
        if r["never_filled"] or r["undeclared"]:
            out.append(f"| {r['group']} | {', '.join(r['never_filled']) or '—'} | {', '.join(r['undeclared']) or '—'} |")
    out += ["", f"Envelope groups no schema section declares: {', '.join(lost_groups) or 'none'}.",
            f"Schema sections no envelope group fills: {', '.join(f'{n}.{s}' for n, s in lost_sections) or 'none'}.", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(markdown(load_examples(sys.argv[1:])), end="")
