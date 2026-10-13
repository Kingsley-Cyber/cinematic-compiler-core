"""The graphs as a cog wheel (owner, 2026-10-13): every layer flows as its contract declares (kernel/data_flow.yaml),
reads nothing no layer writes, turns on its own input, and every graph agrees with the graphs it references."""

import copy
import json

import pytest
import yaml
from conftest import ROOT

from validators import cross_graph, data_flow

pytestmark = pytest.mark.unit


@pytest.fixture(scope="module")
def traced():
    return data_flow._example_rows()


def _envelope(example):
    return json.loads((ROOT / "examples" / example / "envelope.json").read_text(encoding="utf-8"))


def test_every_layer_flows_as_its_contract_declares(traced):
    """DATA-FLOW CONTRACT: reads, writes, checks and fields passed downstream as declared; every layer turns on its
    own input (re-run on the envelope before it, it writes what the envelope holds); no phantom input."""
    assert data_flow.contract_problems(traced) == []


def test_a_layer_reading_what_it_does_not_declare_fails_the_contract(traced):
    declared = yaml.safe_load(data_flow.CONTRACT.read_text(encoding="utf-8"))
    broken = copy.deepcopy(declared)
    causal = next(layer for layer in broken["layers"] if layer["id"] == "causal")
    causal["reads"].remove("nodes.beats.causes")
    found = data_flow.contract_problems(traced, broken)
    assert [(p["code"], p["layer"]) for p in found] == [("DATA_FLOW_CONTRACT", "causal")]
    assert "undeclared ['nodes.beats.causes']" in found[0]["message"]


def test_a_read_no_layer_writes_is_a_phantom(traced):
    rows = copy.deepcopy(traced["wizard_vs_acrobat"])
    rows["camera"]["absent"].add("nodes.beats.invented_field")
    flow = data_flow.report(rows, written_anywhere=data_flow.written_in(traced))
    assert flow["camera"]["phantom"] == ["nodes.beats.invented_field"]


def test_a_field_written_and_read_by_no_later_layer_is_dead(traced):
    flow = data_flow.report(traced["reference_fight"], written_anywhere=data_flow.written_in(traced))
    assert "intent.confidence" in flow["intent"]["dead"]
    assert all(not f.endswith(".id") for row in flow.values() for f in row["dead"])  # identity is not data


def test_the_tracer_counts_a_copy_as_no_read():
    log = set()
    item = data_flow._Tracked({"a": 1, "b": {"c": 2}}, log, "nodes.x")
    clone = copy.deepcopy(item)
    assert log == set()
    clone["a"]
    assert log == {("nodes.x", "a", True)}
    item.get("missing")
    assert ("nodes.x", "missing", False) in log


@pytest.mark.parametrize("example", data_flow.EXAMPLES)
def test_every_graph_agrees_with_the_graphs_it_references(example):
    """CROSS-GRAPH CONSISTENCY."""
    assert cross_graph.problems(_envelope(example)) == []


def _first_contact(envelope):
    return envelope["nodes"]["contacts"]["items"][0]


@pytest.mark.parametrize("name, edit, expected", [
    ("a beat's performer that does not exist",
     lambda e: e["nodes"]["beats"]["items"][0].__setitem__("actor", "ghost"), "performer 'ghost' does not exist"),
    ("a contact's body part the beat does not declare",
     lambda e: _first_contact(e).__setitem__("body_part", "right_hand" if _first_contact(e)["body_part"] != "right_hand"
                                             else "left_hand"), "is not a contact beat"),
    ("a body part its performer does not declare",
     lambda e: _first_contact(e).__setitem__("body_part", "tail"), "'tail' is not a part"),
    ("a rule binding a beat that does not exist",
     lambda e: e["edges"]["beat_constraint"]["items"][0].__setitem__("from", "b99"), "from 'b99' is not in beats"),
    ("a rule that does not exist",
     lambda e: e["edges"]["beat_constraint"]["items"][0].__setitem__("to", "c_none"), "to 'c_none' is not in constraints"),
])
def test_each_broken_reference_is_named(name, edit, expected):
    envelope = _envelope("wizard_vs_acrobat")
    edit(envelope)
    assert any(expected in p["message"] for p in cross_graph.problems(envelope)), name
