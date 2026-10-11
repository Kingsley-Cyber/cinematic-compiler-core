"""Re-bind authored example plans after a change that leaves their content valid (HANDOFF, "Re-binding").

For each authored step in build order, compile until the active step before it, prepare the step's packet and copy
packet_sha256 and step_id into the plan; nothing else changes. Run it after a prompt, library, schema-id or upstream
plan edit, then rewrite the examples (`python -m compiler.examples --write ...`) and prove with the gate.

    python -m compiler.rebind                      # report plans whose packet moved (no writes)
    python -m compiler.rebind --write NAME [NAME]  # re-bind those examples
"""

import json
import sys

from compiler import pipeline
from compiler.examples import EXAMPLES
from kernel.canonical import ContractError
from planner.dependency_graph import load

ORDER = [node["id"] for node in load()["nodes"]]


def _envelope_before(request, node, plans):
    for before in reversed(ORDER[:ORDER.index(node)]):
        try:
            return pipeline.run(request["query"], genre=request.get("genre"), duration_s=request.get("duration_s"),
                                until=before, plans=plans)
        except ContractError as error:  # a step inactive for this genre: step back further
            if error.code != "PIPELINE_TARGET":
                raise
    raise ContractError("PIPELINE_TARGET", "No active step before this one", node)


def rebind(names, write=False):
    """[(example, node)] whose plan packet_sha256 or step_id differs from the freshly prepared packet."""
    moved = []
    for name in names:
        folder = EXAMPLES / name
        request = json.loads((folder / "request.json").read_text(encoding="utf-8"))
        for node in [n for n in ORDER if (folder / "plans" / f"{n}.json").exists()]:
            plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (folder / "plans").glob("*.json")}
            packet = pipeline.AUTHORED[node].prepare(_envelope_before(request, node, plans))
            path = folder / "plans" / f"{node}.json"
            plan = json.loads(path.read_text(encoding="utf-8"))
            if (plan.get("packet_sha256"), plan.get("step_id")) != (packet["packet_sha256"], packet["step_id"]):
                moved.append((name, node))
                if write:
                    plan["packet_sha256"], plan["step_id"] = packet["packet_sha256"], packet["step_id"]
                    path.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return moved


def main():
    write = "--write" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(
        p.name for p in EXAMPLES.iterdir() if (p / "request.json").exists())
    moved = rebind(names, write=write)
    for name, node in moved:
        print(("re-bound " if write else "moved ") + f"{name} {node}")
    sys.exit(0 if write or not moved else 1)


if __name__ == "__main__":
    main()
