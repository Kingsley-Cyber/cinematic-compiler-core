"""Generate docs/reference/ from the repo's sources of truth; `--check` fails when the committed docs are stale.

Sources: kernel/layer_order.yaml (DAG, writes, edge endpoints), compiler/passes (step modules, authored or derived,
plan schemas, prompts), schemas/** (every schema, field by field), the three hash logs (latest entry per file),
library/** and kernel/*.yaml (data files and their schemas) and the Python import graph (internal modules and
external packages). Nothing is written by hand; the output is sorted and carries no timestamps.
"""

import ast
import json
import re
import sys
import tomllib

import yaml

from planner.dependency_graph import ROOT, is_active, load, node_index
from planner.topological_sort import build_order

OUT = ROOT / "docs" / "reference"
PACKAGES = ("kernel", "planner", "validators", "compiler", "solver", "kernel_extraction", "cli", "renderers")
LIBRARY_SCHEMAS = {"archetypes": "archetype_card", "worlds": "world_card", "ontology/objects": "object_card",
                   "body_modes": "body_mode_card", "effort_modes": "effort_mode_card",
                   "camera_conventions": "camera_convention_card", "camera_idioms": "camera_idiom_card",
                   "affordances": "affordance_library", "camera_grammar.yaml": "camera_grammar",
                   "camera_tempo.yaml": "camera_tempo", "role_templates.yaml": "role_templates"}
KERNEL_SCHEMAS = {"invariants.yaml": "kernel_invariants", "state_vocabulary.yaml": "kernel_state_vocabulary",
                  "conventions.yaml": "kernel_conventions", "owner_invariants.yaml": "kernel_owner_invariants",
                  "layer_order.yaml": None, "kernel_scope.yaml": None}


def rel(path):
    return path.relative_to(ROOT).as_posix()


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def link(path, label=None, depth=2):
    return f"[{label or path}]({'../' * depth}{path})"


# ---------------------------------------------------------------- sources


def latest_log_rows(log, key):
    rows = {}
    for line in (ROOT / log).read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row[key]] = row
    return rows


def step_modules():
    """node id -> (module path, module source) for every built step (compiler/passes/*/pNN_<node>.py)."""
    found = {}
    for path in sorted((ROOT / "compiler" / "passes").glob("*/p[0-9][0-9]_*.py")):
        found[path.stem[4:]] = path
    return found


def authored_nodes():
    from compiler.pipeline import AUTHORED

    return set(AUTHORED)


def constant(source, name):
    match = re.search(rf'^{name}\s*=\s*ROOT((?:\s*/\s*"[^"]+")+)', source, re.M)
    return "/".join(re.findall(r'"([^"]+)"', match.group(1))) if match else None


def module_imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    package = ".".join(path.relative_to(ROOT).with_suffix("").parts[:-1])
    internal, external = set(), set()
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = package.split(".")
                base = ".".join(parts[:len(parts) - node.level + 1] + ([base] if base else []))
            names = [base] + [f"{base}.{a.name}" for a in node.names]
        for name in names:
            top = name.split(".")[0]
            if top in PACKAGES:
                internal.add(name)
            elif top and name == names[0]:
                external.add(top)
    modules = {rel(p)[:-3].replace("/", ".") for pkg in PACKAGES for p in (ROOT / pkg).rglob("*.py")}
    resolved = {name if name in modules else name.rsplit(".", 1)[0] for name in internal}
    return sorted(m for m in resolved if m in modules and not m.endswith("__init__")), sorted(external)


def all_modules():
    return sorted((p for pkg in PACKAGES for p in (ROOT / pkg).rglob("*.py") if p.name != "__init__.py"), key=rel)


def closure(module_path, depth=2):
    by_name = {rel(p)[:-3].replace("/", "."): p for p in all_modules()}
    seen, frontier = {module_path}, [module_path]
    for _ in range(depth):
        nxt = []
        for path in frontier:
            for name in module_imports(path)[0]:
                target = by_name.get(name)
                if target and target not in seen and not name.startswith(("compiler.passes", "compiler.pipeline")):
                    seen.add(target)
                    nxt.append(target)
        frontier = nxt
    return seen


def data_inputs(paths):
    """Library and kernel data files a set of modules reads, found from literal references in their source."""
    found = set()
    for path in paths:
        source = path.read_text(encoding="utf-8")
        found |= {f"library/{m}.yaml" for m in re.findall(r'library_vocab\.load\("([a-z_]+)"\)', source)}
        found |= {f"library/{m}" for m in re.findall(r'(?:"library"|LIBRARY)\s*/\s*"([a-z_./]+)"', source)}
        found |= {f"kernel/{m}.yaml" for m in re.findall(r'(?:kernel_files\.load|load_kernel)\("([a-z_]+)"\)', source)}
        found |= {f"kernel/{m}" for m in re.findall(r'"kernel"\s*/\s*"([a-z_]+\.yaml)"', source)}
        if path.name == "card_loader.py":
            found |= {f"library/{v}" for v in re.findall(r'"[a-z]+": "([a-z/]+)"', source.split("FOLDERS", 1)[1].split("\n")[0])}
    return sorted(found)


def schema_files():
    return sorted((ROOT / "schemas").rglob("*.schema.json"), key=rel)


def schema_role(path):
    name = rel(path)
    if name.startswith("schemas/cards/"):
        return "library data file schema"
    if name.startswith("schemas/modality/"):
        return "genre (modality) schema for a complete envelope"
    if name.endswith("_plan.schema.json"):
        return "authored plan (input a step checks)"
    if name.startswith("schemas/graphs/"):
        return "graph output (what a step writes)"
    if "kernel_" in name:
        return "kernel data file schema"
    return {"schemas/cinematic_ir.schema.json": "the envelope (generated by kernel/build_ir_schema.py)",
            "schemas/intent_document.schema.json": "S01 Intent Document",
            "schemas/camera.schema.json": "S15 camera shot node (embedded in camera_plan)"}.get(name, "")


def referrers(path):
    """Non-test modules that name this schema file literally, or build its name dynamically and quote its stem."""
    stem = path.name[:-len(".schema.json")]
    stems = {stem, stem.removesuffix("_card")}
    found = []
    for module in all_modules():
        source = module.read_text(encoding="utf-8")
        literal = path.name in source
        dynamic = re.search(r"\{[^}]+\}(_card)?\.schema\.json", source) and any(f'"{s}"' in source for s in stems)
        if literal or dynamic:
            found.append(rel(module))
    return found


# ---------------------------------------------------------------- schema field tables


def resolve(node, root):
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 10:
        target = root
        for part in node["$ref"][2:].split("/"):
            target = target[part]
        node, seen = target, seen + 1
    return node


def type_of(node, root):
    node = resolve(node, root)
    if "const" in node:
        return f"const {json.dumps(node['const'])}"
    if "enum" in node:
        return "enum"
    for key in ("anyOf", "oneOf"):
        if key in node:
            return " \\| ".join(type_of(n, root) for n in node[key])
    kind = node.get("type", "any")
    return " \\| ".join(kind) if isinstance(kind, list) else kind


def constraints(node, root):
    node = resolve(node, root)
    parts = []
    if "enum" in node:
        parts.append("one of " + ", ".join(json.dumps(v) for v in node["enum"]))
    for key, label in (("pattern", "pattern"), ("minimum", "≥"), ("maximum", "≤"), ("exclusiveMinimum", ">"),
                       ("exclusiveMaximum", "<"), ("minItems", "min items"), ("maxItems", "max items"),
                       ("minLength", "min length"), ("minProperties", "min properties")):
        if key in node:
            parts.append(f"{label} `{node[key]}`" if key == "pattern" else f"{label} {node[key]}")
    if node.get("uniqueItems"):
        parts.append("unique")
    return "; ".join(parts)


def field_rows(node, root, path="", required=True, depth=0, stack=()):
    ref = node.get("$ref") if isinstance(node, dict) else None
    if ref in stack:
        return [(path, f"→ {ref.split('/')[-1]} (recursive)", "", "", "")]
    node = resolve(node, root)
    rows = []
    if path:
        rows.append((path, type_of(node, root), "yes" if required else "", constraints(node, root),
                     node.get("description", "")))
    if depth >= 6:
        return rows
    stack = stack + ((ref,) if ref else ())
    for key in ("anyOf", "oneOf"):
        for option in node.get(key, []):
            option_resolved = resolve(option, root)
            if option_resolved.get("type") == "object" or "properties" in option_resolved:
                rows += field_rows(option, root, path, required, depth + 1, stack)[1:]
    required_keys = set(node.get("required", []))
    for name, child in node.get("properties", {}).items():
        rows += field_rows(child, root, f"{path}.{name}" if path else name, name in required_keys, depth + 1, stack)
    for pattern, child in node.get("patternProperties", {}).items():
        rows += field_rows(child, root, f"{path}.<{pattern}>" if path else f"<{pattern}>", False, depth + 1, stack)
    extra = node.get("additionalProperties")
    if isinstance(extra, dict):
        rows += field_rows(extra, root, f"{path}.<any key>", False, depth + 1, stack)
    if "items" in node and isinstance(node["items"], dict):
        rows += field_rows(node["items"], root, f"{path}[]", True, depth + 1, stack)
    return rows


# ---------------------------------------------------------------- documents


def dependencies_doc(order):
    index = node_index(order)
    modules, authored = step_modules(), authored_nodes()
    lines = ["# Dependencies — the layer DAG", "",
             "Generated by `python -m kernel.build_docs` from `kernel/layer_order.yaml` and the step modules. "
             "Do not edit by hand.", ""]
    lines += ["## Step graph", "", "Arrows point from an input step to the step that reads it. "
              "Authored steps are written in-session from a sealed packet; derived steps are computed; "
              "UGC-only steps run for `ugc_ad` (thick border); S17 is not built (M7). Every step also reads "
              "`kernel/layer_order.yaml` (its owner tags and write scope).", "", "```mermaid", "flowchart TD"]
    for node in order["nodes"]:
        nid = node["id"]
        lines.append(f'  {nid}["{node["step_id"]} {nid}<br/>{node["band"]}"]')
    for node in order["nodes"]:
        for dep in node["depends_on"]:
            lines.append(f"  {dep} --> {node['id']}")
    groups = {"authored": [n for n in index if n in authored],
              "derived": [n for n in index if n in modules and n not in authored],
              "notbuilt": [n for n in index if n not in modules]}
    lines += ["  classDef authored fill:#e8f0ff,stroke:#3b6fd8", "  classDef derived fill:#eef7ee,stroke:#3c8a3c",
              "  classDef notbuilt fill:#f4f4f4,stroke:#999,stroke-dasharray:4 3",
              "  classDef ugc stroke-width:3px"]
    for name, ids in groups.items():
        if ids:
            lines.append(f"  class {','.join(ids)} {name}")
    ugc = [n["id"] for n in order["nodes"] if n.get("when") == ["ugc_ad"]]
    lines += [f"  class {','.join(ugc)} ugc", "```", ""]

    lines += ["## Steps", "", "| Step | Node | Band | Builds | Kind | Runs for | Depends on | Writes | Validated by | Code | "
              "Authored plan schema | Prompt | Data read (library / kernel) |", "|" + "---|" * 13]
    for node in order["nodes"]:
        nid, path = node["id"], modules.get(node["id"])
        source = path.read_text(encoding="utf-8") if path else ""
        kind = "not built (M7)" if not path else ("authored" if nid in authored else "derived") + (
            " · projection" if node.get("projection") else "")
        plan = constant(source, "PLAN_SCHEMA")
        prompt = constant(source, "PROMPT")
        if nid == "temporal":
            plan, prompt = "schemas/graphs/beat_plan.schema.json", "planner/prompts/beat_planning.txt"
        data = [d for d in data_inputs(closure(path)) if d != "kernel/layer_order.yaml"] if path else []
        lines.append("| " + " | ".join(cell(x) for x in (
            node["step_id"], nid, node["band"], node["builds"], kind, ", ".join(node.get("when", ["all"])),
            ", ".join(node["depends_on"]) or "—", "<br>".join(f"`{w}`" for w in node["writes"]),
            ", ".join(node["validated_by"]), link(rel(path)) if path else "—", link(plan) if plan else "—",
            link(prompt) if prompt else "—", "<br>".join(link(d) for d in data) or "—")) + " |")
    lines.append("")

    lines += ["## Build order per genre", ""]
    for genre in order["modalities"]:
        sequence = build_order(order, genre)
        lines.append(f"- **{genre}** ({len(sequence)} steps): " + " → ".join(
            f"{index[n]['step_id']} {n}" for n in sequence))
    lines.append("")

    lines += ["## Write ownership", "", "Every envelope path has exactly one owner; an inner path (carve-out) is owned by "
              "a later step and the outer owner never touches it.", "", "| Path | Owner |", "|---|---|"]
    rows = [(p, "pipeline") for p in order["pipeline_owned"]]
    rows += [(w, f"{n['step_id']} {n['id']}") for n in order["nodes"] for w in n["writes"]]
    lines += [f"| `{p}` | {o} |" for p, o in sorted(rows)]
    lines.append("")

    lines += ["## Node and edge groups", "", "| Group | Kind | Written by | Edge endpoints (from → to) |", "|---|---|---|---|"]
    endpoints = order["edge_endpoints"]
    for node in order["nodes"]:
        for write in node["writes"]:
            if write.startswith(("/nodes/", "/edges/")):
                _, kind, group = write.split("/")
                ends = endpoints.get(group)
                ends_text = f"{', '.join(ends['from'])} → {', '.join(ends['to'])}" if kind == "edges" and ends else ""
                lines.append(f"| `{group}` | {kind[:-1]} | {node['step_id']} {node['id']} | {ends_text} |")
    node_groups = sum(w.startswith("/nodes/") for n in order["nodes"] for w in n["writes"])
    edge_groups = sum(w.startswith("/edges/") for n in order["nodes"] for w in n["writes"])
    lines += ["", f"{node_groups} node groups, {edge_groups} edge groups.", ""]

    lines += ["## Steps active per genre", "", "| Step | " + " | ".join(order["modalities"]) + " |",
              "|---|" + "---|" * len(order["modalities"])]
    for node in order["nodes"]:
        lines.append(f"| {node['step_id']} {node['id']} | " + " | ".join(
            "yes" if is_active(node, g) else "—" for g in order["modalities"]) + " |")
    return "\n".join(lines) + "\n"


def schemas_doc():
    log = latest_log_rows("schemas/schema_log.jsonl", "schema")
    files = schema_files()
    lines = ["# Schemas", "", "Generated by `python -m kernel.build_docs` from `schemas/**` and `schemas/schema_log.jsonl`. "
             "Do not edit by hand. Every schema change is logged (append-only, hash-chained) and checked by "
             "`scripts/check.sh`.", "", f"{len(files)} schema files.", "", "## Index", "",
             "| Schema | Role | Title | Last logged change | Read by |", "|---|---|---|---|---|"]
    for path in files:
        schema = json.loads(path.read_text(encoding="utf-8"))
        row = log.get(rel(path), {})
        change = f"seq {row.get('seq')} · {row.get('date')} · {row.get('change')} · {row.get('decided_by')}" if row else "—"
        anchor = rel(path).replace("/", "").replace(".", "").replace("_", "")
        lines.append(f"| [{rel(path)}](#{anchor}) | {cell(schema_role(path))} | {cell(schema.get('title', ''))} | {change} | "
                     + "<br>".join(f"`{r}`" for r in referrers(path)) + " |")
    lines.append("")
    for path in files:
        schema = json.loads(path.read_text(encoding="utf-8"))
        row = log.get(rel(path), {})
        lines += [f"## {rel(path)}", "", f"- **Id:** `{schema.get('$id', '')}`", f"- **Role:** {schema_role(path)}",
                  f"- **Title:** {cell(schema.get('title', ''))}", f"- **Description:** {cell(schema.get('description', ''))}"]
        if row:
            lines += [f"- **Last change:** seq {row['seq']}, {row['date']}, {row['change']}, decided by "
                      f"{row['decided_by']}: {cell(row['reason'])}", f"- **sha256:** `{row['sha256']}`"]
        lines += ["- **Read by:** " + (", ".join(f"`{r}`" for r in referrers(path)) or "tests only"), ""]
        if rel(path) == "schemas/cinematic_ir.schema.json":
            lines += ["Top-level fields and the `$defs` each one uses (generated envelope; the item fields of each group "
                      "are fixed by that group's graph schema):", "", "| Field | Type | Required | Constraints | Description |",
                      "|---|---|---|---|---|"]
            rows = field_rows({k: v for k, v in schema.items() if k != "$defs"}, schema)
            rows = [r for r in rows if r[0].count(".") <= 1]
        else:
            lines += ["| Field | Type | Required | Constraints | Description |", "|---|---|---|---|---|"]
            rows = field_rows({k: v for k, v in schema.items() if k != "$defs"}, schema)
        lines += [f"| `{r[0]}` | {r[1]} | {r[2]} | {cell(r[3])} | {cell(r[4])} |" for r in rows]
        lines.append("")
    return "\n".join(lines) + "\n"


def library_doc():
    library_log = latest_log_rows("library/library_log.jsonl", "card")
    kernel_log = latest_log_rows("kernel/kernel_log.jsonl", "file")
    lines = ["# Data files — library and kernel", "", "Generated by `python -m kernel.build_docs`. Library files are drafts "
             "until the owner approves them; every file is logged in its hash-chained log.", "", "## Library", "",
             "| File | Schema | Status | Version | Last logged change |", "|---|---|---|---|---|"]
    for path in sorted((ROOT / "library").rglob("*.yaml"), key=rel):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        sub = rel(path)[len("library/"):]
        schema = LIBRARY_SCHEMAS.get(sub) or LIBRARY_SCHEMAS.get(sub.rsplit("/", 1)[0]) or (
            "vocabulary" if "vocabulary_id" in data else "—")
        row = library_log.get(rel(path), {})
        change = f"seq {row['seq']} · {row['date']} · {row['change']} · {row['decided_by']}" if row else "—"
        version = data.get("card_version", data.get("version", ""))
        schema_link = link(f"schemas/cards/{schema}.schema.json", schema) if schema != "—" else "—"
        lines.append(f"| {link(rel(path), sub)} | {schema_link} | {data.get('status', '')} | {version} | {change} |")
    lines += ["", "## Kernel", "", "| File | Schema | Status | Last logged change |", "|---|---|---|---|"]
    for name, schema in KERNEL_SCHEMAS.items():
        path = ROOT / "kernel" / name
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        row = kernel_log.get(rel(path), {})
        change = f"seq {row['seq']} · {row['date']} · {row['change']} · {row['decided_by']}" if row else "—"
        schema_link = link(f"schemas/{schema}.schema.json", schema) if schema else "— (read by planner/dependency_graph.py)"
        lines.append(f"| {link(rel(path), name)} | {schema_link} | {data.get('status', '') if isinstance(data, dict) else ''} | "
                     f"{change} |")
    return "\n".join(lines) + "\n"


def code_doc():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lines = ["# Code dependencies", "", "Generated by `python -m kernel.build_docs` from the import statements. "
             "Do not edit by hand.", "", "## External packages", "",
             f"- Runtime: {', '.join(f'`{d}`' for d in project['project']['dependencies'])} (Python "
             f"{project['project']['requires-python']})",
             f"- Development: {', '.join(f'`{d}`' for d in project['dependency-groups']['dev'])}",
             f"- Console script: `cinematic` → `{project['project']['scripts']['cinematic']}`", ""]
    edges = {}
    rows = []
    for path in all_modules():
        name = rel(path)[:-3].replace("/", ".")
        internal, external = module_imports(path)
        rows.append((name, internal, external))
        for target in internal:
            a, b = name.split(".")[0], target.split(".")[0]
            if a != b:
                edges[(a, b)] = edges.get((a, b), 0) + 1
    lines += ["## Package graph", "", "Arrow = imports (count of module-level imports).", "", "```mermaid", "flowchart LR"]
    lines += [f"  {a} -->|{n}| {b}" for (a, b), n in sorted(edges.items())]
    lines += ["```", "", "## Modules", "", "| Module | Imports (internal) | Imports (standard library / external) |",
              "|---|---|---|"]
    for name, internal, external in rows:
        lines.append(f"| `{name}` | {', '.join(f'`{i}`' for i in internal) or '—'} | {', '.join(external) or '—'} |")
    return "\n".join(lines) + "\n"


def readme(order):
    modules = step_modules()
    built = [n for n in order["nodes"] if n["id"] in modules]
    graphs = [n for n in built if any(w.startswith("/edges/") for w in n["writes"])]
    node_groups = sorted({w.split("/")[2] for n in built for w in n["writes"] if w.startswith("/nodes/")})
    edge_groups = sorted({w.split("/")[2] for n in built for w in n["writes"] if w.startswith("/edges/")})
    lines = ["# Reference documentation", "", "Generated by `python -m kernel.build_docs`; `scripts/check.sh` fails when "
             "these files are stale. Regenerate after changing the DAG, a schema, a library file or imports.", "",
             "| Document | What it covers |", "|---|---|",
             "| [dependencies.md](dependencies.md) | The step DAG (Mermaid), every step's inputs, outputs, code, plan schema, "
             "prompt and data files; build order per genre; write ownership; node/edge groups and edge endpoints |",
             "| [schemas.md](schemas.md) | Every schema file: role, readers, last logged change and every field with its "
             "type, requirement, constraints and description |",
             "| [library.md](library.md) | Every library and kernel data file: schema, status, last logged change |",
             "| [code.md](code.md) | External packages, package import graph, every module's imports |", "",
             "## Counts", "",
             f"- Steps built: {len(built)} of {len(order['nodes'])} "
             f"({', '.join(n['step_id'] for n in order['nodes'] if n['id'] not in modules) or 'none'} not built).",
             f"- Graphs (steps that write edges): {len(graphs)} — "
             + ", ".join(f"{n['step_id']} {n['id']}" for n in graphs) + ".",
             "- Other outputs: " + ", ".join(f"{n['step_id']} {n['id']} ({n['builds']})" for n in built if n not in graphs) + ".",
             f"- Node groups: {len(node_groups)}; edge groups: {len(edge_groups)}.",
             f"- Schema files: {len(schema_files())}; library files: {len(list((ROOT / 'library').rglob('*.yaml')))}; "
             f"Python modules: {len(all_modules())}."]
    for genre in order["modalities"]:
        sequence = [n for n in build_order(order, genre) if n in modules]
        count = sum(1 for n in sequence if any(w.startswith("/edges/") for w in node_index(order)[n]["writes"]))
        lines.append(f"- {genre}: {len(sequence)} built steps run, {count} of them graphs.")
    return "\n".join(lines) + "\n"


def render():
    order = load()
    return {"README.md": readme(order), "dependencies.md": dependencies_doc(order), "schemas.md": schemas_doc(),
            "library.md": library_doc(), "code.md": code_doc()}


def main():
    documents = render()
    if "--check" in sys.argv:
        stale = [name for name, text in documents.items()
                 if not (OUT / name).exists() or (OUT / name).read_text(encoding="utf-8") != text]
        for name in stale:
            print("STALE docs/reference/" + name)
        sys.exit(1 if stale else 0)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in documents.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", rel(OUT / name))


if __name__ == "__main__":
    main()
