"""S16: coverage, consecutive intervals, closed LMA values, effort actions, effort-mode intensity, overlaps."""

import copy
import itertools
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p16_effort
from kernel.canonical import canonical_json
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["effort"]
PACKET = p16_effort.prepare(courtyard("motion"))
GRAPH = json.loads((ROOT / "schemas" / "graphs" / "effort_graph.schema.json").read_text())


def interval(plan, actor, first):
    return next(i for i in plan["intervals"] if i["actor"] == actor and i["beats"][0] == first)


def codes(change):
    plan = copy.deepcopy(PLAN)
    change(plan)
    return {f["code"] for f in p16_effort.check(plan, PACKET)}


def test_courtyard_plan_passes():
    assert p16_effort.check(PLAN, PACKET) == [] and PACKET["packet_sha256"] == PLAN["packet_sha256"]


def test_eight_basic_effort_actions_cover_every_weight_time_space_combination():
    combos = set(itertools.product(("light", "strong"), ("sustained", "sudden"), ("indirect", "direct")))
    assert set(p16_effort.ACTIONS) == combos and len(set(p16_effort.ACTIONS.values())) == 8
    assert set(p16_effort.ACTIONS.values()) | {"none"} == set(PACKET["vocabulary"]["effort_action"]["values"])


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
    # plan F9.1, owner O73: the acrobat's spin spreads its arms; 'enclosing' (the plan before O73) contradicts it
    ("SHAPE_DIRECTION", lambda p: interval(p, "acrobat", "b05")["shape"].update(quality="enclosing")),
    ("EFFORT_MODE", lambda p: interval(p, "wizard", "b05").update(intensity=0.95)),
])
def test_each_rule_rejects_its_violation(code, change):
    assert code in codes(change)


@pytest.mark.integration
def test_derived_spans_overlaps_scope_and_determinism(order):
    before = courtyard("motion")
    snapshot = copy.deepcopy(before)
    after, _ = p16_effort.run(before, PLAN, order=order)
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
    assert canonical_json(after) == canonical_json(p16_effort.run(courtyard("motion"), PLAN, order=order)[0])


def test_shape_direction_skips_a_flight_and_judges_the_ground():
    """Owner O76: an airborne turn is a flight (the spine's tuck is not a lean); a grounded body is judged (O73)."""
    assert "SHAPE_DIRECTION" not in codes(lambda p: interval(p, "acrobat", "b12")["shape"].update(quality="advancing"))
    assert "SHAPE_DIRECTION" in codes(lambda p: interval(p, "acrobat", "b05")["shape"].update(quality="enclosing"))


def test_a_printed_shape_against_the_motion_is_refused():
    """SHAPE_DIRECTION in the prompt: B is dragged forward toward the pillar from 7.50, so 'retreating' contradicts it."""
    from validators import prompt_validator
    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    text = envelope["nodes"]["render"]["items"][0]["prose"]["mixed"]["text"]
    line = "- B 7.50–9.00: maintain sudden time, bound flow; shape advancing"
    assert line in text
    broken = text.replace(line, line.replace("advancing", "retreating"))
    assert "SHAPE_DIRECTION" in {f["code"] for f in prompt_validator.check(broken, envelope, "mixed")}

