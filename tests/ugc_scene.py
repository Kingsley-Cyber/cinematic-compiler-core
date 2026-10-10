"""The UGC glasses demo as a test fixture: compile it up to a step with its authored plans."""

import json

from conftest import ROOT

from compiler import pipeline

FOLDER = ROOT / "examples" / "ugc_glasses_demo"
QUERY = json.loads((FOLDER / "request.json").read_text())["query"]


def ugc_plans():
    return {path.stem: json.loads(path.read_text()) for path in sorted((FOLDER / "plans").glob("*.json"))}


def glasses(until, **overrides):
    return pipeline.run(QUERY, until=until, plans={**ugc_plans(), **overrides})
