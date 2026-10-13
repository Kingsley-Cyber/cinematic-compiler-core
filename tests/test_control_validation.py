"""The control layer (owner, 2026-10-13): six checks of the compiler's structure, not its prompts, in one place, on
every commit. Each names the validator that holds it; the planted breaks for the first three live beside them
(tests/test_data_flow.py, tests/test_layer_dependency.py, tests/test_graph_map.py).

1. schema alignment: no layer reads a field no layer writes; the fields no later layer reads are held by the contract
2. transition validity: every layer reads and writes what kernel/data_flow.yaml declares, and turns on its own input
3. interdependency integrity: the layer order has no cycle, no missing dependency, no edge before its endpoints
4. canonical order: every joint list printed follows the kernel skeleton key (JOINTS_IN_CANONICAL_ORDER)
5. determinism: the prompt is the same from disk, from memory and with every key order reversed (DETERMINISM)
6. graph conformance: every graph matches its schema section and agrees with the graphs it references
"""

import copy
import json

import pytest
from conftest import ROOT

from compiler.examples import compile_example
from kernel.canonical import canonical_json
from planner.dependency_graph import load
from renderers import anime_renderer
from validators import cross_graph, data_flow, determinism, graph_map
from validators.layer_dependency_validator import check_layer_order

pytestmark = pytest.mark.unit
EXAMPLES = graph_map.EXAMPLES


@pytest.fixture(scope="module")
def traced():
    return data_flow._example_rows()


@pytest.fixture(scope="module")
def in_memory():
    """Each example's envelope as the pipeline holds it, before any serializer touches it."""
    return {name: compile_example(ROOT / "examples" / name) for name in EXAMPLES}


def test_1_and_2_every_layer_flows_as_declared_with_no_phantom(traced):
    assert data_flow.contract_problems(traced) == []


def test_3_the_layer_order_is_a_dag_with_every_dependency(traced):
    assert check_layer_order(load()) == []


def test_4_the_renderers_joint_order_is_the_kernels():
    assert tuple(anime_renderer.JOINT_ORDER) == determinism.canonical()
    assert determinism.joint_order_problems({}) == []


@pytest.mark.parametrize("example", EXAMPLES)
def test_4_and_5_the_prompt_is_the_same_from_disk_from_memory_and_in_any_key_order(example, in_memory):
    held = in_memory[example]
    disk = json.loads((ROOT / "examples" / example / "envelope.json").read_text(encoding="utf-8"))
    assert canonical_json(held) == canonical_json(disk)
    assert determinism.problems(held, in_memory=held) == []


def test_4_a_joint_list_out_of_order_is_refused():
    text = 'Joints {Sp: [1, 0, 0], HD: [0, 0, 0], LUL: [0, 0, 0]}'
    assert [p["code"] for p in determinism.joint_order_problems({"x": text})] == ["JOINTS_IN_CANONICAL_ORDER"]
    assert determinism.joint_order_problems({"x": '"joints":{"Sp":[1,0,0],"LUL":[0,0,0],"HD":[0,0,0]}'}) == []


def test_5_a_renderer_reading_the_dicts_order_is_refused(monkeypatch, in_memory):
    """The bug S-119 found, planted back: the LBN prompt takes the joint order from the dict."""
    monkeypatch.setattr(anime_renderer, "_joints", lambda bones: bones)
    held = copy.deepcopy(in_memory["reference_fight"])
    codes = {p["code"] for p in determinism.problems(held, in_memory=held)}
    assert codes == {"DETERMINISM", "JOINTS_IN_CANONICAL_ORDER"}


@pytest.mark.parametrize("example", EXAMPLES)
def test_6_every_graph_conforms_and_agrees(example):
    envelope = json.loads((ROOT / "examples" / example / "envelope.json").read_text(encoding="utf-8"))
    assert graph_map.problems(envelope) == []
    assert cross_graph.problems(envelope) == []
