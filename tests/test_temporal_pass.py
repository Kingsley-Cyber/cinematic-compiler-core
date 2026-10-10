"""S04 pass: packet binding, computed edges, duration source, write scope, determinism, authoring stop."""

import copy
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

from compiler import pipeline
from compiler.authoring import AuthorRequired, GateFailed
from compiler.passes.mandatory import p04_temporal
from kernel.canonical import ContractError, canonical_json
from planner.beat_planner import prepare
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
EXAMPLE = ROOT / "examples" / "wizard_vs_acrobat"
QUERY = json.loads((EXAMPLE / "request.json").read_text())["query"]
PLAN = json.loads((EXAMPLE / "plans" / "temporal.json").read_text())
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "temporal_graph.schema.json").read_text())


def before():
    return pipeline.run(QUERY, until="constraint")


def test_packet_is_deterministic_and_sealed():
    first, second = prepare(before()), prepare(before())
    assert canonical_json(first) == canonical_json(second)
    assert first["packet_sha256"] == PLAN["packet_sha256"]


@pytest.mark.integration
def test_s04_writes_only_its_paths_and_computes_its_edges(order):
    envelope = before()
    snapshot = copy.deepcopy(envelope)
    after, _ = p04_temporal.run(envelope, PLAN, order=order)
    assert envelope == snapshot
    assert check_pass_writes(order, "temporal", envelope, after) == []
    graph = {"beats": after["nodes"]["beats"]["items"], "temporal": after["edges"]["temporal"]["items"],
             "beat_constraint": after["edges"]["beat_constraint"]["items"]}
    validate_schema(graph, GRAPH)
    beats = graph["beats"]
    assert [b["id"] for b in beats] == sorted((b["id"] for b in PLAN["beats"]), key=lambda i: next(
        (x["t"], x["id"]) for x in PLAN["beats"] if x["id"] == i))
    for edge, (left, right) in zip(graph["temporal"], zip(beats, beats[1:], strict=False), strict=True):
        assert (edge["from"], edge["to"]) == (left["id"], right["id"])
        assert edge["gap"] == round(right["t"] - left["t"] - left["dur"], 6) and edge["duration"] == left["dur"]
    applied = {(r["target"]["kind"], r["target"]["id"], r["constraint_id"])
               for r in after["edges"]["constraint_application"]["items"]}
    for edge in graph["beat_constraint"]:
        b = next(x for x in beats if x["id"] == edge["from"])
        touched = {("entity", b["actor"])} | {(r["kind"], r["id"]) for r in b["participants"]}
        assert any((kind, ident, edge["to"]) in applied for kind, ident in touched)
    assert (after["scene"]["duration_s"], after["scene"]["duration_source"]) == (10, "user")


def test_duration_falls_back_to_the_last_beat_end():
    envelope = pipeline.run("anime fight scene: wizard versus acrobat in a moonlit bamboo courtyard", until="constraint")
    plan = copy.deepcopy(PLAN)
    plan["packet_sha256"] = prepare(envelope)["packet_sha256"]
    after, _ = p04_temporal.run(envelope, plan)
    assert (after["scene"]["duration_s"], after["scene"]["duration_source"]) == (10.0, "beat_plan_end")


def test_wrong_packet_and_failed_gates_are_refused():
    plan = copy.deepcopy(PLAN)
    plan["packet_sha256"] = "sha256:" + "0" * 64
    with pytest.raises(ContractError) as error:
        p04_temporal.run(before(), plan)
    assert error.value.code == "PACKET_MISMATCH"
    plan = copy.deepcopy(PLAN)
    plan["beats"][0]["actor"] = "dragon"
    with pytest.raises(GateFailed) as failed:
        p04_temporal.run(before(), plan)
    assert failed.value.code == "GATE_FAILED" and failed.value.findings[0]["code"] == "BEAT_ACTOR"
    assert failed.value.packet["packet_sha256"] == PLAN["packet_sha256"]


def test_pipeline_stops_with_the_packet_when_no_plan_is_given():
    with pytest.raises(AuthorRequired) as needed:
        pipeline.run(QUERY, until="temporal")
    assert needed.value.packet["packet_sha256"] == PLAN["packet_sha256"]
    envelope = pipeline.run(QUERY, until="temporal", plans={"temporal": PLAN})
    assert envelope["provenance"]["authored"][0]["step_id"] == "S04"


@pytest.mark.integration
def test_cli_is_byte_identical_across_processes_and_exits_3_without_a_plan():
    outputs = set()
    for seed in ("0", "5", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outputs.add(subprocess.run([sys.executable, "-m", "compiler.pipeline", QUERY, "--until", "temporal",
                                    "--plans", str(EXAMPLE / "plans")], cwd=ROOT, capture_output=True, text=True,
                                   env=env, check=True).stdout)
    assert outputs == {canonical_json(pipeline.run(QUERY, until="temporal", plans={"temporal": PLAN}))}
    result = subprocess.run([sys.executable, "-m", "compiler.pipeline", QUERY, "--until", "temporal"], cwd=ROOT,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 3 and json.loads(result.stdout)["packet_sha256"] == PLAN["packet_sha256"]
