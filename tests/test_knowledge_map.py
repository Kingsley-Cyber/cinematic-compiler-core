"""kernel/knowledge_map.yaml: every node of the frozen knowledge DAG is mapped once, onto real steps and real checks."""

import ast
import hashlib
import re

import pytest
import yaml
from conftest import ROOT

from renderers.prose_renderer import MODES

pytestmark = pytest.mark.unit
MAP = yaml.safe_load((ROOT / "kernel" / "knowledge_map.yaml").read_text(encoding="utf-8"))
SOURCE = ROOT / MAP["source"]["path"]
FROZEN_SHA256 = "108d317b83e5033b3791ec9bb4377e65d35d1419f52023edfcf9575afdd6f208"
NODE = re.compile(r'^\s*(\w+)\["')
EXCLUDED = [f"P3.2-{n}" for n in range(1, 11)] + [f"P4.2-{n}" for n in range(1, 4)]
CLASSES = {"mandatory", "required", "style", "projection", "evidence", "excluded"}
STATUSES = {"enforced", "partial", "missing", "clashes_with_repo", "excluded"}
FIELDS = {"id", "name", "anchor", "class", "step", "status", "note"}


def mermaid_ids():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = lines.index("```mermaid")
    end = lines.index("```", start + 1)
    return [m.group(1) for line in lines[start + 1:end] if (m := NODE.match(line))]


def definitions(path):
    """Qualified function names in a Python file (`f`, `Class.method`, `outer.inner`) with their source."""
    source = path.read_text(encoding="utf-8")
    found = {}

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                name = prefix + child.name
                if isinstance(child, ast.FunctionDef):
                    decorators = "".join(ast.get_source_segment(source, d) for d in child.decorator_list)
                    found[name] = decorators + ast.get_source_segment(source, child)
                visit(child, name + ".")

    visit(ast.parse(source), "")
    return found


def locator_problems(locator):
    """Why a locator does not resolve: missing file, function, test, or a code neither of them names."""
    path = ROOT / locator["file"]
    if not path.is_file():
        return [f"{locator['file']} does not exist"]
    problems = []
    code = locator.get("code")
    if "check" in locator:
        body = definitions(path).get(locator["check"])
        if body is None:
            problems.append(f"{locator['file']} has no function {locator['check']}")
        elif code and f'"{code}"' not in body:
            problems.append(f"{locator['check']} does not emit {code}")
    if "test" in locator:
        test_file, test_name = locator["test"].split("::")
        body = definitions(ROOT / test_file).get(test_name) if (ROOT / test_file).is_file() else None
        if body is None:
            problems.append(f"{locator['test']} does not exist")
        elif code and f'"{code}"' not in body:
            problems.append(f"{locator['test']} does not exercise {code}")
    return problems


def test_the_frozen_copy_keeps_its_hash():
    data = SOURCE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == MAP["source"]["sha256"] == FROZEN_SHA256
    assert len(data) == MAP["source"]["bytes"]


def test_every_dag_node_is_mapped_exactly_once():
    ids = mermaid_ids()
    assert len(ids) == len(set(ids)) == MAP["source"]["nodes"] == 96
    mapped = [row["id"] for row in MAP["rows"] if row["class"] != "excluded"]
    assert set(ids) - set(mapped) == set(), "unmapped DAG nodes"
    assert sorted({i for i in mapped if mapped.count(i) > 1}) == [], "DAG nodes mapped twice"
    assert set(mapped) - set(ids) == set(), "rows for nodes the DAG does not have"
    excluded = [row["id"] for row in MAP["rows"] if row["class"] == "excluded"]
    assert sorted(excluded) == sorted(EXCLUDED) and len(excluded) == MAP["source"]["excluded_items"]


def test_rows_use_known_fields_classes_statuses_and_steps():
    order = yaml.safe_load((ROOT / "kernel" / "layer_order.yaml").read_text(encoding="utf-8"))
    steps = {node["step_id"] for node in order["nodes"]} | {"all"}
    for row in MAP["rows"]:
        assert FIELDS <= set(row) <= FIELDS | {"enforced_by", "codes", "gaps", "not_applicable", "applies_when"}, row["id"]
        assert row["class"] in CLASSES and row["status"] in STATUSES, row["id"]
        assert row["step"] in steps, row["id"]
        if row["class"] == "excluded":
            assert row["status"] in ("excluded", "clashes_with_repo"), row["id"]
        else:
            assert row["status"] != "excluded", row["id"]
        if row["class"] == "evidence":
            assert row["status"] != "enforced", row["id"]
        assert row["note"].strip(), row["id"]


def test_not_applicable_and_menus_follow_owner_o14():
    """N/A on every prompt only for the superseded layer orders; menu rows name the mode, genre or menu that selects them."""
    assert sorted(row["id"] for row in MAP["rows"] if "not_applicable" in row) == ["T3", "T4"]
    assert all("O14" in row["not_applicable"] for row in MAP["rows"] if "not_applicable" in row)
    menus = {row["id"]: row["applies_when"] for row in MAP["rows"] if "applies_when" in row}
    assert menus == {"C11": {"genre": ["ugc_ad"]}, "C14": {"mode": "pure_staff"}, "C15": {"mode": "mixed"},
                     "C16": {"mode": "upgraded_mixed"}, "C17": {"mode": "euler_heavy"},
                     "V4": {"selection": "V4 alteration goal"}, "V5": {"selection": "V5 style template"}}
    assert {when["mode"] for when in menus.values() if "mode" in when} == set(MODES)


def test_locators_name_real_files_functions_and_tests():
    problems = [(row["id"], p) for row in MAP["rows"] for loc in row.get("enforced_by", [])
                for p in locator_problems(loc)]
    assert problems == []


def test_an_enforced_row_names_a_check_and_a_test_that_fails_when_it_is_broken():
    """A full locator, or semantic codes (each proven to fire by tests/test_dag_conformance.py) and no open gap."""
    for row in (r for r in MAP["rows"] if r["status"] == "enforced"):
        located = any({"file", "check", "code", "test"} <= set(loc) for loc in row.get("enforced_by", []))
        assert located or (row.get("codes") and not row.get("gaps")), row["id"]


def test_mandatory_and_required_rows_name_their_codes_or_gaps():
    source = (ROOT / "validators" / "prompt_validator.py").read_text(encoding="utf-8")
    proofs = (ROOT / "tests" / "test_dag_conformance.py").read_text(encoding="utf-8")
    for row in MAP["rows"]:
        if row["class"] in ("mandatory", "required"):
            assert row.get("codes") or row.get("gaps"), row["id"]
        if row.get("gaps"):
            assert row["status"] != "enforced", row["id"]
        for code in row.get("codes", []):
            assert f'"{code}"' in source and f'"{code}"' in proofs, (row["id"], code)


def test_a_broken_locator_is_caught():
    good = {"file": "compiler/authoring.py", "check": "bind", "code": "PACKET_MISMATCH",
            "test": "tests/test_temporal_pass.py::test_wrong_packet_and_failed_gates_are_refused"}
    assert locator_problems(good) == []
    for edit in ({"file": "compiler/missing.py"}, {"check": "no_such_function"}, {"code": "NO_SUCH_CODE"},
                 {"test": "tests/test_temporal_pass.py::test_no_such_test"}):
        assert locator_problems({**good, **edit}) != [], edit
