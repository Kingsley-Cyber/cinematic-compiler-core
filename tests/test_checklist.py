"""M8.10 per-prompt DAG checklist (validators/checklist.py): every prompt of every example judged on all 84 map rows."""

import json

import pytest
from conftest import ROOT

from compiler.examples import EXAMPLES
from validators import checklist, prompt_validator

pytestmark = pytest.mark.integration
FIGHT = EXAMPLES / "reference_fight"


@pytest.fixture(scope="module")
def tables():
    return {name: checklist.evaluate(name) for name in checklist.names()}


def _results(table, label):
    column = next(c for c in table["columns"] if c["label"] == label)
    return {row["id"]: cell for row, cell in zip(table["rows"], column["cells"], strict=True)}


def _judge(text, mode, lbn=False):
    envelope = json.loads((FIGHT / "envelope.json").read_text(encoding="utf-8"))
    found = checklist.fired(text, envelope, mode, lbn)
    return {row["id"]: checklist.judge(row, found, mode, envelope["scene"]["genre"], lbn) for row in checklist.rows()}


def test_every_example_has_a_current_checklist_next_to_its_prompts(tables):
    assert checklist.names() == sorted(p.name for p in EXAMPLES.iterdir() if (p / "request.json").exists())
    for name, table in tables.items():
        path = EXAMPLES / name / "checklist.md"
        assert path.read_text(encoding="utf-8") == checklist.markdown(name, table), f"{name}: run --write"
    assert checklist.main([]) == 0


def test_each_prompt_is_judged_on_all_84_rows_once(tables):
    ids = [row["id"] for row in checklist.rows()]
    assert len(ids) == len(set(ids)) == 84
    for table in tables.values():
        assert [c["label"] for c in table["columns"]] == ["LBN", "Pure", "Mixed", "Upgr", "Euler"]
        for column in table["columns"]:
            assert len(column["cells"]) == 84
            assert all(result in checklist.RESULTS and evidence for result, evidence in column["cells"])


def test_not_applicable_comes_only_from_the_owner_rulings(tables):
    modes = dict((label, mode) for label, _, mode in checklist.PROMPTS)
    for table in tables.values():
        for column in table["columns"]:
            for row, (result, _) in zip(table["rows"], column["cells"], strict=True):
                if result != checklist.NA:
                    continue
                when = row.get("applies_when", {})
                excluded = row["status"] == "excluded" and not row.get("codes")  # owner O94 (RV-11)
                assert ("not_applicable" in row or excluded or when.get("mode") not in (None, modes[column["label"]])
                        or table["genre"] not in when.get("genre", [table["genre"]])), row["id"]


def test_dag_excluded_rows_are_not_applicable_unless_a_code_checks_them():
    """Owner O94 (RV-11, F-085): a row the DAG excludes is N/A, unless a code checks it: P3.2-5's ROOT_EXACT_PRESENT
    still judges, since a FAIL there breaks owner O3."""
    rows = {row["id"]: row for row in checklist.rows()}
    assert checklist.judge(rows["P3.2-1"], {}, "mixed", "anime", False)[0] == checklist.NA
    assert checklist.judge(rows["P3.2-5"], {}, "mixed", "anime", False)[0] == checklist.PASS
    assert checklist.judge(rows["P3.2-5"], {"ROOT_EXACT_PRESENT": ["x"]}, "mixed", "anime", False)[0] == checklist.FAIL


def test_a_section_the_codes_read_must_be_there(tables):
    """LBN-2.4 has no staff, so C17 (its Euler-heavy mode) fails instead of passing on silence."""
    assert set(prompt_validator.READS) == set(prompt_validator.CODES)
    lbn = _results(tables["reference_fight"], "LBN")
    assert lbn["C17"][0] == checklist.FAIL and "cannot pass" in lbn["C17"][1]
    assert lbn["V8"][0] == checklist.FAIL and "cam" in lbn["V8"][1]
    assert lbn["P3.2-5"] == (checklist.PASS, "pass: ROOT_EXACT_PRESENT (owner O3 keeps 'root exact' in LBN-2.4)")


def test_a_broken_prompt_turns_its_rows_red():
    text = (FIGHT / "prose_pure_staff.txt").read_text(encoding="utf-8")
    clean = _judge(text, "pure_staff")
    assert {clean[i][0] for i in ("GR", "T9", "P3.2-5", "C14")} == {checklist.PASS}
    broken = _judge(text.replace("[CAUSAL LINKS]\n", "", 1) + "\nA root exact\n", "pure_staff")
    assert broken["GR"][0] == broken["T9"][0] == checklist.FAIL
    assert "cannot pass: the prompt has no [CAUSAL LINKS]" in broken["GR"][1]
    assert broken["P3.2-5"][0] == checklist.FAIL and "ROOT_EXACT_PRESENT" in broken["P3.2-5"][1]


def test_rows_without_a_prompt_check_are_never_passed(tables):
    for table in tables.values():
        for column in table["columns"]:
            for row, (result, _) in zip(table["rows"], column["cells"], strict=True):
                if result == checklist.PASS:
                    assert row.get("codes") and row["status"] in ("enforced", "excluded"), row["id"]
                    assert not row.get("gaps"), row["id"]


def test_union_and_deliverable_rules():
    ok, red, unchecked, na = checklist.PASS, checklist.FAIL, checklist.OPEN, checklist.NA
    assert checklist.union([red, red, ok, na, unchecked]) == ok
    assert checklist.union([red, unchecked, na]) == unchecked
    assert checklist.union([red, red, na]) == red
    assert checklist.union([na, na]) == na
    assert checklist.deliverable([ok, na, ok])
    assert not checklist.deliverable([ok, unchecked]) and not checklist.deliverable([red])


def test_the_gate_refuses_every_prompt_with_a_red_row(tables, capsys):
    refused = sum(not checklist.deliverable([r for r, _ in c["cells"]]) for t in tables.values() for c in t["columns"])
    assert checklist.main(["--gate"]) == (1 if refused else 0)
    assert f"deliverable prompts: {20 - refused} of 20" in capsys.readouterr().out


def test_findings_name_real_rows_examples_and_codes():
    ids = {row["id"] for row in checklist.rows()}
    assert (ROOT / checklist.FINDINGS_DOC).is_file()
    for finding, (where, rows, caught) in checklist.FINDINGS.items():
        assert set(rows) <= ids and set(where) <= set(checklist.names()), finding
        assert set(caught) <= set(prompt_validator.CODES), finding


def test_no_pass_is_contradicted_by_an_uncaught_render_finding(tables):
    """Owner 2026-10-11: a render that contradicts a PASS row makes it NOT CHECKED until a code catches what it saw."""
    for name, table in tables.items():
        for column in table["columns"]:
            for row, (result, _) in zip(table["rows"], column["cells"], strict=True):
                uncaught = [f for f, caught in checklist.findings_for(name, row) if not caught]
                assert not (result == checklist.PASS and uncaught), (name, column["label"], row["id"])
    fight = _results(tables["reference_fight"], "Pure")
    assert fight["M1"][0] == checklist.PASS and "ENTRANCE_UNSTATED" in fight["M1"][1]  # F10 caught (M9-08b, S-016)
    assert fight["C6"][0] == checklist.PASS  # F1, F2 are caught by CAUSE_REASON
    assert fight["C24"][0] == checklist.PASS  # F11 is caught by PROP_FIRST_STATE
    assert fight["C7"][0] == fight["C31"][0] == checklist.PASS  # F8 is caught by PROP_LINE_MISSING
    assert fight["C23"][0] == checklist.OPEN and "F13" in fight["C23"][1]  # F9 caught, F13 (set drift) still open
