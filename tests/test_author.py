"""The automatic author (PLAN-008, owner ADR-O112; AA-1): each authored step written by a backend from its sealed
packet, refusals sent back with their findings, every call logged."""

import copy
import json

import pytest
from conftest import ROOT

from compiler.author import AuthorFailed, Replay, author
from kernel.canonical import canonical_json

pytestmark = pytest.mark.unit
EXAMPLES = ROOT / "examples"


@pytest.mark.parametrize("example", ["reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo"])
def test_the_replay_backend_re_authors_each_example_byte_for_byte(example):
    """Written step by step from the packets the pipeline hands out, the examples' own plans give the golden envelope;
    one call per authored step, each passed."""
    query = json.loads((EXAMPLES / example / "request.json").read_text(encoding="utf-8"))["query"]
    envelope, calls = author(query, Replay(EXAMPLES / example / "plans"))
    assert canonical_json(envelope) == (EXAMPLES / example / "envelope.json").read_text(encoding="utf-8")
    assert [c["result"] for c in calls] == ["passed"] * len(calls)
    assert len({c["node"] for c in calls}) == len(calls) and all(c["attempt"] == 1 for c in calls)


class _Breaks(Replay):
    """Replay, but the motion document's first `times` attempts put the acrobat's first key 1.5 m under the floor."""

    name = "breaks"

    def __init__(self, folder, times):
        super().__init__(folder)
        self.times, self.seen = times, []

    def write(self, node, step_id, packet, findings=None):
        document, usage = super().write(node, step_id, packet, findings)
        if node == "motion":
            self.seen.append(findings)
            if len(self.seen) <= self.times:
                document = copy.deepcopy(document)
                key = next(k for k in document["keys"] if k["slot"].startswith("acrobat@"))
                key["pos"][1] -= 1.5
        return document, usage


def test_a_refusal_goes_back_with_its_findings_and_the_retry_passes():
    query = json.loads((EXAMPLES / "wizard_vs_acrobat" / "request.json").read_text(encoding="utf-8"))["query"]
    backend = _Breaks(EXAMPLES / "wizard_vs_acrobat" / "plans", times=1)
    envelope, calls = author(query, backend)
    motion = [c for c in calls if c["node"] == "motion"]
    assert [(c["attempt"], c["result"]) for c in motion] == [(1, "refused"), (2, "passed")]
    assert backend.seen[0] is None and "FLOOR_PENETRATION" in {f["code"] for f in backend.seen[1]}
    assert "render" in envelope["nodes"]


def test_a_step_refused_on_every_attempt_stops_the_run():
    query = json.loads((EXAMPLES / "wizard_vs_acrobat" / "request.json").read_text(encoding="utf-8"))["query"]
    with pytest.raises(AuthorFailed) as stopped:
        author(query, _Breaks(EXAMPLES / "wizard_vs_acrobat" / "plans", times=99))
    assert stopped.value.node == "motion" and [c["result"] for c in stopped.value.calls if c["node"] == "motion"] == \
        ["refused"] * 3
