"""ADR-O119 (R-37, R-38): the test budget holds its baseline and only lets it shrink."""

import importlib.util

import pytest
from conftest import ROOT

pytestmark = pytest.mark.unit
spec = importlib.util.spec_from_file_location("test_budget", ROOT / "scripts" / "test_budget.py")
budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget)
HELD = {"files": {"tests/test_big.py": {"tests": 30, "lines": 300}}, "slow": ["tests/test_big.py::slow"],
        "untested_codes": ["OLD_CODE"]}


def test_a_suite_at_its_baseline_passes():
    assert budget.problems(HELD, HELD, {"tests/test_big.py::slow": 0.4}) == []


def test_a_new_file_over_budget_or_a_grown_baseline_file_fails():
    now = {**HELD, "files": {"tests/test_big.py": {"tests": 31, "lines": 300}, "tests/test_new.py": {"tests": 21, "lines": 10}}}
    assert len(budget.problems(now, HELD, {"tests/test_big.py::slow": 0.4})) == 2


def test_a_baseline_entry_back_within_budget_must_leave_it():
    now = {"files": {}, "slow": [], "untested_codes": []}
    found = budget.problems(now, HELD, {"tests/test_big.py::slow": 0.01})
    assert len(found) == 3 and all("remove it from the baseline" in f for f in found)


def test_a_new_untested_check_code_fails():
    now = {**HELD, "untested_codes": ["OLD_CODE", "NEW_CODE"]}
    assert budget.problems(now, HELD, {"tests/test_big.py::slow": 0.4}) == ["check code NEW_CODE is named by no test"]
