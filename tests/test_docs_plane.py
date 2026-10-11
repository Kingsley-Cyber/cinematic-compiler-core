"""The docs plane (owner O64, O67): the repo's indexes, canonical docs and their drift checks pass, and every check
refuses the one break it exists for (no check is decorative)."""

import re
import shutil

import pytest
from conftest import ROOT

from kernel import docs_plane

pytestmark = pytest.mark.integration
SKIP = shutil.ignore_patterns(".git", ".graphs", "examples", ".venv", "__pycache__", "*.egg-info", "graphify-out")


def test_the_docs_plane_passes_on_the_repo():
    assert docs_plane.problems() == []


def test_every_artifact_file_has_its_index_row_and_every_row_its_file():
    for kind, spec in docs_plane.KINDS.items():
        index = (ROOT / "docs" / "index" / f"{kind}.md").read_text(encoding="utf-8")
        files = {p.name for p in (ROOT / spec["folder"]).glob("*.md") if not p.name.startswith("_")}
        linked = set(re.findall(rf"\]\(\.\./{re.escape(spec['folder'].split('/')[-1])}/([^)]+\.md)\)", index))
        assert files == linked, kind


def _edit(path, old, new, count=1):
    def apply(root):
        target = root / path if isinstance(path, str) else next((root / path[0]).glob(path[1]))
        text = target.read_text(encoding="utf-8")
        assert old in text, (path, old)
        target.write_text(text.replace(old, new, count), encoding="utf-8")
    return apply


def _add_file(path, text):
    return lambda root: (root / path).write_text(text, encoding="utf-8")


BREAKS = [
    ("field 'Severity' is empty", _edit(("docs/findings", "F-016-*.md"), "## Severity\nhigh\n", "## Severity\n\n")),
    ("is not one of", _edit(("docs/findings", "F-016-*.md"), "## Status\nopen\n", "## Status\nfixed-ish\n")),
    ("checklist's caught_by", _edit(("docs/findings", "F-001-*.md"), "## Status\nresolved\n", "## Status\nopen\n")),
    ("link to missing file", _edit(("docs/sessions", "S-001-*.md"), "## Next\n", "## Next\nSee [x](nowhere.md).\n")),
    ("are not in the code", _edit("docs/plans/backlog.yaml", "codes: [BODY_HOLD_FRAMES,", "codes: [NO_SUCH_CODE,")),
    ("every new code is in the code", lambda root: (root / "docs/plans/backlog.yaml").open("a", encoding="utf-8").write(
        "  - {id: ZZ-01, title: x, status: ready, step: docs, plan: PLAN-005, depends_on: [], findings: [],"
        " codes: [CAUSE_REASON]}\n")),
    ("which is superseded", _edit("docs/rules.yaml", "source: [ADR-O46]", "source: [ADR-O45]")),
    ("does not say", _edit(("docs/decisions", "ADR-O45-*.md"), "## Superseded By\nADR-O46", "## Superseded By\n—")),
    ("is stale", _edit("docs/index/findings.md", "| F-001 |", "| F-001x |")),
    ("must start with its ID", _add_file("docs/sessions/S-099.md", "# S-098 — x\n")),
    ("is also used by", lambda root: shutil.copy(next((root / "docs/renders").glob("R1-*.md")),
                                                 root / "docs/renders/R1-copy.md")),
    ("does not match schemas/rules.schema.json", _edit("docs/rules.yaml", "id: R-01,", "id: R-1,")),
    ("differs from its source", _edit("schemas/graphs/temporal_graph.schema.json", '"enum": [\n            "touch",',
                                      '"enum": [\n            "tap",')),
    ("depends on unknown", _edit("docs/plans/backlog.yaml", "depends_on: [M9-02], findings: [F-022",
                                 "depends_on: [M9-99], findings: [F-022")),
]


@pytest.mark.parametrize("expected, edit", BREAKS, ids=[b[0] for b in BREAKS])
def test_each_check_refuses_its_break(expected, edit, tmp_path):
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=SKIP)
    edit(root)
    found = docs_plane.problems(root)
    assert any(expected in problem for problem in found), found


def test_a_frozen_doc_cannot_change_without_its_log_entry_and_version_bump(tmp_path):
    from kernel.canonical import ContractError
    from kernel.schema_log import DOCS

    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=SKIP)
    agents = root / "AGENTS.md"
    agents.write_text(agents.read_text(encoding="utf-8").replace("## 1. The golden rule", "## 1. The golden rules"),
                      encoding="utf-8")
    with pytest.raises(ContractError, match="differ from their latest log entry"):
        DOCS.verify(root)
    DOCS.record("AGENTS.md", "changed", "test: no bump", "owner", root=root)
    assert any("changed without a version bump" in p for p in docs_plane._freeze_problems(root))
    text = agents.read_text(encoding="utf-8")
    regenerated = docs_plane.fill_blocks(text, {"state": "- anything\n"})  # generated blocks are outside the digest
    agents.write_text(regenerated, encoding="utf-8")
    DOCS.verify(root)
