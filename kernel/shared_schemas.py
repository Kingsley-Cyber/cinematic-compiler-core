"""Shared schema definitions (owner O65): each lives once, in its own file, and is embedded where it is used.

The repo's validator resolves document-local references only (validators/schema_validator.py), so a schema that uses
a shared definition carries a copy under `$defs`, written here from the shared file, the way kernel/build_ir_schema.py
embeds the intent document. The properties that use it point at the copy with `{"$ref": "#/$defs/<Name>"}`.

- schemas/contact.schema.json: Contact, a touch, hold, support or release between a body part and a target.
- schemas/beat.schema.json: Beat and the definitions it uses (Ref, Vec3, Fact, Cause, PropSample; Contact embedded
  from contact.schema.json).
- schemas/rotation.schema.json: EulerXYZ, Turn and AxisDeclaration, the root rotation of a key pose.

`python -m kernel.shared_schemas` rewrites the copies; `--check` (scripts/verify.sh) refuses a copy that differs from
its source. A changed copy is a schema change: log the target with `python -m kernel.schema_log record`.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEAT_DEFS = ["Ref", "Vec3", "Fact", "Effect", "Contact", "Cause", "Beat", "PropSample"]
ROTATION_DEFS = ["EulerXYZ", "Turn", "AxisDeclaration"]
# target -> [(source, [definition names])], applied in order (contact into beat before beat into the graphs)
EMBEDS = {
    "schemas/beat.schema.json": [("schemas/contact.schema.json", ["Contact"])],
    "schemas/graphs/beat_plan.schema.json": [("schemas/beat.schema.json", BEAT_DEFS)],
    "schemas/graphs/temporal_graph.schema.json": [("schemas/beat.schema.json", BEAT_DEFS)],
    "schemas/graphs/motion_plan.schema.json": [("schemas/rotation.schema.json", ROTATION_DEFS)],
    "schemas/graphs/motion_graph.schema.json": [("schemas/rotation.schema.json", ROTATION_DEFS)],
}


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(document):
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def expected(root=ROOT):
    """{path: text} with every embedded copy equal to its source."""
    docs = {}
    for target, sources in EMBEDS.items():
        document = docs.get(target) or _load(root / target)
        for source, names in sources:
            shared = docs.get(source) or _load(root / source)
            defs = document.setdefault("$defs", {})
            for name in names:
                defs[name] = shared["$defs"][name]
        docs[target] = document
    return {root / path: _dump(document) for path, document in docs.items()}


def problems(root=ROOT):
    return [f"{path.relative_to(root)}: an embedded shared definition differs from its source "
            "(run python -m kernel.shared_schemas)" for path, text in expected(root).items()
            if path.read_text(encoding="utf-8") != text]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--check" in argv:
        found = problems()
        for problem in found:
            print("SCHEMA", problem)
        return 1 if found else 0
    for path, text in expected().items():
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
