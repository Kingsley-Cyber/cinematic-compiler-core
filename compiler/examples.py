"""Committed examples must recompile byte-for-byte and carry the current kernel hash (stale = gate failure).

Layout: examples/<name>/request.json {"query", "genre", "duration_s", "until"}, optional plans/<node>.json
(authored inputs), envelope.json (expected canonical output) and, once S17 has run, render.txt (the rendered prompt,
exactly the render node's text, ready to paste into a video model).
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


def render_text(envelope):
    render = envelope.get("nodes", {}).get("render")
    return render["items"][0]["text"] + "\n" if render else None


def check_all():
    problems, current = [], kernel_hash()
    for folder in sorted(p for p in EXAMPLES.iterdir() if p.is_dir()) if EXAMPLES.exists() else []:
        expected = (folder / "envelope.json").read_text(encoding="utf-8")
        if json.loads(expected)["provenance"]["kernel_hash"] != current:
            problems.append(f"{folder.name}: built against an older kernel")
            continue
        envelope = compile_example(folder)
        if canonical_json(envelope) != expected:
            problems.append(f"{folder.name}: recompiled bytes differ from envelope.json")
        text, path = render_text(envelope), folder / "render.txt"
        if (text is None) != (not path.exists()) or (text is not None and path.read_text(encoding="utf-8") != text):
            problems.append(f"{folder.name}: render.txt does not match the envelope's render")
    return problems


def main():
    if "--write" in sys.argv:
        for name in sys.argv[sys.argv.index("--write") + 1:]:
            folder = EXAMPLES / name
            envelope = compile_example(folder)
            (folder / "envelope.json").write_text(canonical_json(envelope), encoding="utf-8")
            print("wrote", folder / "envelope.json")
            if render_text(envelope) is not None:
                (folder / "render.txt").write_text(render_text(envelope), encoding="utf-8")
                print("wrote", folder / "render.txt")
        return
    problems = check_all()
    for problem in problems:
        print("STALE", problem)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
