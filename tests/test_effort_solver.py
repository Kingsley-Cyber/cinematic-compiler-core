"""S14: coverage, consecutive intervals, closed LMA values, effort actions, effort-mode intensity, overlaps."""

import copy
import itertools
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p14_effort
from kernel.canonical import canonical_json
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["effort"]
PACKET = p14_effort.prepare(courtyard("motion"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "effort_graph.schema.json").read_text())


def interval(plan, actor, first):
    return next(i for i in plan["intervals"] if i["actor"] == actor and i["beats"][0] == first)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p14_effort.check(plan, PACKET)}


def test_courtyard_plan_passes():
    assert p14_effort.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def test_eight_basic_effort_actions_cover_every_weight_time_space_combination():
    combos = set(itertools.product(("light", "strong"), ("sustained", "sudden"), ("indirect", "direct")))
    assert set(p14_effort.ACTIONS) == combos and len(set(p14_effort.ACTIONS.values())) == 8
    assert set(p14_effort.ACTIONS.values()) | {"none"} == set(PACKET["vocabulary"]["effort_action"]["values"])


@pytest.mark.parametrize("code, change", [
    ("EFFORT_COVERAGE", lambda p: p["intervals"].pop(0)),
    ("EFFORT_COVERAGE", lambda p: interval(p, "acrobat", "b02")["beats"].insert(0, "b01")),
    ("EFFORT_INTERVAL", lambda p: interval(p, "acrobat", "b10").update(beats=["b10", "b12"])),
    ("EFFORT_INTERVAL", lambda p: interval(p, "wizard", "b03").update(beats=["b01"])),
    ("EFFORT_VOCABULARY", lambda p: interval(p, "wizard", "b06")["effort"].update(weight="heavy")),
    ("EFFORT_VOCABULARY", lambda p: interval(p, "wizard", "b06")["shape"].update(quality="spiral")),
    ("EFFORT_VOCABULARY", lambda p: interval(p, "wizard", "b06").update(effort_mode="frantic")),
    ("EFFORT_ACTION", lambda p: interval(p, "acrobat", "b02").update(effort_action="slash")),
    ("EFFORT_ACTION", lambda p: interval(p, "acrobat", "b01").update(effort_action="dab")),
    ("EFFORT_MODE", lambda p: interval(p, "wizard", "b05").update(intensity=0.95)),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


@pytest.mark.integration
def test_derived_spans_overlaps_scope_and_determinism(order):
    before = courtyard("motion")
    snapshot = copy.deepcopy(before)
    after, _ = p14_effort.run(before, PLAN, order=order)
    assert before == snapshot and check_pass_writes(order, "effort", before, after) == []
    nodes, edges = after["nodes"]["efforts"]["items"], after["edges"]["effort"]["items"]
    validate_schema({"efforts": nodes, "effort": edges}, GRAPH)
    by_id = {n["id"]: n for n in nodes}
    assert by_id["acrobat@b02-b04"]["t"] == 1.2 and by_id["acrobat@b02-b04"]["end"] == 2.6
    for edge in edges:
        left, right = by_id[edge["from"]], by_id[edge["to"]]
        assert left["actor"] != right["actor"] and edge["start"] < edge["end"]
        assert (edge["start"], edge["end"]) == (max(left["t"], right["t"]), min(left["end"], right["end"]))
    assert ("acrobat@b06-b07", "wizard@b06") in {(e["from"], e["to"]) for e in edges}
    assert canonical_json(after) == canonical_json(p14_effort.run(courtyard("motion"), PLAN, order=order)[0])
