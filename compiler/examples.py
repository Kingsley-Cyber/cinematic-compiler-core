"""Committed examples must recompile byte-for-byte and carry the current kernel hash (stale = gate failure).

Layout: examples/<name>/request.json {"query", "genre", "duration_s", "until"}, optional plans/<node>.json
(authored inputs), and envelope.json (expected canonical output).
"""

import json
import sys

from kernel.canonical import canonical_json
from kernel.kernel_files import kernel_hash
from planner.dependency_graph import ROOT

EXAMPLES = ROOT / "examples"


def compile_example(folder):
    from compiler import pipeline

    request = json.loads((folder / "request.json").read_text(encoding="utf-8"))
    plans = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in sorted((folder / "plans").glob("*.json"))}
    kwargs = {"genre": request.get("genre"), "duration_s": request.get("duration_s"), "until": request["until"]}
    if plans:
        kwargs["plans"] = plans
    return pipeline.run(request["query"], **kwargs)


def check_all():
    problems, current = [], kernel_hash()
    for folder in sorted(p for p in EXAMPLES.iterdir() if p.is_dir()) if EXAMPLES.exists() else []:
        expected = (folder / "envelope.json").read_text(encoding="utf-8")
        if json.loads(expected)["provenance"]["kernel_hash"] != current:
            problems.append(f"{folder.name}: built against an older kernel")
        elif canonical_json(compile_example(folder)) != expected:
            problems.append(f"{folder.name}: recompiled bytes differ from envelope.json")
    return problems


def main():
    if "--write" in sys.argv:
        for name in sys.argv[sys.argv.index("--write") + 1:]:
            folder = EXAMPLES / name
            (folder / "envelope.json").write_text(canonical_json(compile_example(folder)), encoding="utf-8")
            print("wrote", folder / "envelope.json")
        return
    problems = check_all()
    for problem in problems:
        print("STALE", problem)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
