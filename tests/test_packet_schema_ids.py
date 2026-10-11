"""Every authored step's packet names the current $id of its plan schema (S-013: S04 named beat_plan 1.3 after 1.4)."""

import json
import re

import pytest
from conftest import ROOT

pytestmark = pytest.mark.unit
PINNED = re.compile(r"urn:cinematic-compiler:schema:([a-z_]+):(\d+\.\d+)")


def test_packets_name_the_schema_versions_on_disk():
    sources = [ROOT / "planner" / "beat_planner.py", *sorted((ROOT / "compiler" / "passes" / "derived").glob("p*.py"))]
    pinned = {(name, version) for path in sources for name, version in PINNED.findall(path.read_text(encoding="utf-8"))}
    assert pinned
    for name, version in sorted(pinned):
        on_disk = json.loads((ROOT / "schemas" / "graphs" / f"{name}.schema.json").read_text(encoding="utf-8"))["$id"]
        assert on_disk.endswith(f":{version}"), (name, version, on_disk)
