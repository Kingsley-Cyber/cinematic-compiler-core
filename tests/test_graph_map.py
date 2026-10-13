"""The graph map and the graph reach (ADR-O113): every graph conforms to its schema section, and the prose prints a
growing share of what the graphs hold ("if the graph has it, the prompt prints it")."""

import json

import pytest
from conftest import ROOT

from validators import graph_map, graph_reach

pytestmark = pytest.mark.unit

# the fields the prose renderer reads per example (S-116: holds, camera, poses, points); each S18 slice raises them
READ_FLOOR = {"reference_fight": 146, "wizard_vs_acrobat": 134, "live_action_standoff": 120, "ugc_glasses_demo": 171}


@pytest.mark.parametrize("example", graph_map.EXAMPLES)
def test_every_graph_conforms_to_its_schema_section(example):
    envelope = json.loads((ROOT / "examples" / example / "envelope.json").read_text(encoding="utf-8"))
    assert graph_map.problems(envelope) == []


def test_every_group_and_section_is_mapped():
    assert graph_map.unmapped(graph_map.load_examples()) == ([], [])


def test_a_group_its_schema_refuses_is_named():
    envelope = json.loads((ROOT / "examples" / "wizard_vs_acrobat" / "envelope.json").read_text(encoding="utf-8"))
    envelope["edges"]["temporal"]["items"][0]["extra"] = 1
    assert [p["group"] for p in graph_map.problems(envelope)] == ["edges.temporal"]


@pytest.mark.parametrize("example", graph_map.EXAMPLES)
def test_the_prose_reads_at_least_its_floor_of_the_graphs(example):
    envelope = json.loads((ROOT / "examples" / example / "envelope.json").read_text(encoding="utf-8"))
    held, read = graph_reach.counts(envelope)
    assert read >= READ_FLOOR[example], (held, read)


def test_the_graph_map_document_is_current():
    assert (ROOT / "docs" / "graph_map.md").read_text(encoding="utf-8") == graph_map.markdown(graph_map.load_examples())
