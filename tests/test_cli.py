"""`cinematic` CLI: compile (packet exit 3, replan exit 4, stop exit 2), validate, graph."""

import copy
import json
import subprocess
import sys

import pytest
from conftest import ROOT
from scenes import COURTYARD, COURTYARD_PLAN, COURTYARD_QUERY, CUP_QUERY, cup_plan

from compiler import pipeline

pytestmark = pytest.mark.integration


def cli(*args):
    return subprocess.run([sys.executable, "-m", "cli.main", *args], cwd=ROOT, capture_output=True, text=True, check=False)


def test_compile_reproduces_the_example_and_stops_for_a_packet():
    result = cli("compile", COURTYARD_QUERY, "--plans", str(COURTYARD / "plans"))
    assert result.returncode == 0 and result.stdout == (COURTYARD / "envelope.json").read_text(encoding="utf-8")
    result = cli("compile", COURTYARD_QUERY)
    assert result.returncode == 3 and json.loads(result.stdout)["packet_sha256"] == COURTYARD_PLAN["packet_sha256"]


def write_plan(tmp_path, plan):
    folder = tmp_path / "plans"
    folder.mkdir(exist_ok=True)
    (folder / "temporal.json").write_text(json.dumps(plan), encoding="utf-8")
    return folder


def test_authored_gate_failure_returns_a_replan_request(tmp_path):
    plan = copy.deepcopy(COURTYARD_PLAN)
    plan["beats"][0]["actor"] = "dragon"
    result = cli("compile", COURTYARD_QUERY, "--plans", str(write_plan(tmp_path, plan)))
    replan = json.loads(result.stdout)
    assert result.returncode == 4 and (replan["step_id"], replan["failed_step_id"], replan["attempt"]) == ("S04", "S04", 2)
    assert replan["packet"]["packet_sha256"] == COURTYARD_PLAN["packet_sha256"]
    assert replan["findings"][0]["code"] == "BEAT_ACTOR"


def test_derived_failure_routes_to_the_beat_plan_and_stops_after_two_retries(tmp_path):
    plan = cup_plan(pipeline.run(CUP_QUERY, until="constraint"))
    plan["beats"][2]["requires"][0]["value"] = "knight"
    result = cli("compile", CUP_QUERY, "--plans", str(write_plan(tmp_path, plan)))
    replan = json.loads(result.stdout)
    assert result.returncode == 4 and (replan["step_id"], replan["failed_step_id"]) == ("S04", "S06")
    plan["attempt"] = 3
    result = cli("compile", CUP_QUERY, "--plans", str(write_plan(tmp_path, plan)))
    assert result.returncode == 2 and "REPLAN_EXHAUSTED" in result.stderr


def test_validate_and_graph(tmp_path):
    assert cli("validate", str(COURTYARD / "envelope.json")).returncode == 0
    envelope = json.loads((COURTYARD / "envelope.json").read_text())
    envelope["nodes"]["beats"]["band"] = "L2"
    envelope["provenance"]["kernel_hash"] = "sha256:" + "1" * 64
    (tmp_path / "bad.json").write_text(json.dumps(envelope), encoding="utf-8")
    result = cli("validate", str(tmp_path / "bad.json"))
    codes = {row["code"] for row in json.loads(result.stdout)["findings"]}
    assert result.returncode == 1 and {"STALE_KERNEL", "LAYER_TAG"} <= codes
    shown = json.loads(cli("graph", str(COURTYARD / "envelope.json"), "causal").stdout)
    assert shown["kind"] == "edges" and shown["step_id"] == "S05"
    assert cli("graph", str(COURTYARD / "envelope.json"), "lighting").returncode == 1
