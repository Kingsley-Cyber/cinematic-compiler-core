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
    motion = [c for c in calls if c["node"] == "motion" and c["backend"] != "reblock-solver"]
    assert [(c["attempt"], c["result"]) for c in motion] == [(1, "refused"), (2, "passed")]
    assert backend.seen[0] is None and "FLOOR_PENETRATION" in {f["code"] for f in backend.seen[1]}
    assert "render" in envelope["nodes"]


def test_a_step_refused_on_every_attempt_stops_the_run():
    query = json.loads((EXAMPLES / "wizard_vs_acrobat" / "request.json").read_text(encoding="utf-8"))["query"]
    with pytest.raises(AuthorFailed) as stopped:
        author(query, _Breaks(EXAMPLES / "wizard_vs_acrobat" / "plans", times=99))
    assert stopped.value.node == "motion" and [c["result"] for c in stopped.value.calls
                                               if c["node"] == "motion" and c["backend"] != "reblock-solver"] == ["refused"] * 3


def test_the_solver_repairs_an_overlap_between_keys_before_the_model_retries():
    """AA-4: without its in-betweens the wizard example's kick passes through the wizard's trunk on both sides of the
    contact; the solver alone places in-betweens one frame off the contact's key and S13 refuses nothing."""
    from compiler import pipeline
    from compiler.author import repair_motion
    from compiler.passes.derived import p13_motion
    folder = EXAMPLES / "wizard_vs_acrobat"
    query = json.loads((folder / "request.json").read_text(encoding="utf-8"))["query"]
    plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((folder / "plans").glob("*.json"))}
    envelope = pipeline.run(query, until="bartenieff", plans=plans)
    packet = p13_motion.prepare(envelope)
    bare = {**plans["motion"], "inbetweens": []}
    found = p13_motion.check(bare, packet)
    assert {f["code"] for f in found} == {"BODY_OVERLAP"}
    repaired = repair_motion(bare, found, envelope)
    assert p13_motion.check(repaired, packet) == []
    assert [(b["entity"], b["t"]) for b in repaired["inbetweens"]] == [("acrobat", 3.54167), ("acrobat", 3.70833)]
    assert repair_motion(bare, [{"code": "MOTION_POS"}], envelope) is None  # another kind only: the model's
    mixed = repair_motion(bare, [*found, {"code": "CONTACT_WORLD", "contact": "x", "message": "."}], envelope)
    assert p13_motion.check(mixed, packet) == []  # the overlaps repaired, the rest left for the model


class _Never:
    name = "never"

    def write(self, node, step_id, packet, findings=None):
        raise AssertionError(f"{node} was written again")


def test_a_re_run_takes_every_accepted_step_from_the_cache(tmp_path):
    """AA-7: each accepted document is kept by its packet's hash; a re-run of the same idea writes nothing."""
    folder = EXAMPLES / "wizard_vs_acrobat"
    query = json.loads((folder / "request.json").read_text(encoding="utf-8"))["query"]
    first, _ = author(query, Replay(folder / "plans"), cache=tmp_path)
    again, calls = author(query, _Never(), cache=tmp_path)
    assert canonical_json(again) == canonical_json(first) and {c["model"] for c in calls} == {"cache"}


def test_the_pose_step_is_written_in_pieces_and_a_retry_redoes_only_the_refused_piece():
    """AA-9: S13's slots go out in time windows of about five, every fighter of a beat in one piece, written at once
    and merged; a retry writes again only the pieces that hold a refused slot."""
    from compiler import author as module
    from compiler import pipeline
    from compiler.passes.derived import p13_motion
    folder = EXAMPLES / "wizard_vs_acrobat"
    query = json.loads((folder / "request.json").read_text(encoding="utf-8"))["query"]
    plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((folder / "plans").glob("*.json"))}
    packet = p13_motion.prepare(pipeline.run(query, until="bartenieff", plans=plans))
    committed = {k["slot"]: k for k in plans["motion"]["keys"]}
    beat_of = {s["slot"]: s["t"] for s in packet["slots"]}
    asked = []

    class Fake(module.ClaudeCLI):
        def _call(self, node, step_id, packet, findings, previous, note=None):
            slots = note.split("SLOTS: ")[1].split(" (")[0].split(", ")
            asked.append(slots)
            return {"keys": [committed[s] for s in slots], "inbetweens": plans["motion"]["inbetweens"]}, \
                {"model": "fake", "tokens_in": 1, "tokens_out": 1, "list_cost_usd": 0.0}

    backend = Fake("anime")
    document, usage = backend.write("motion", "S13", packet)
    assert sorted(k["slot"] for k in document["keys"]) == sorted(committed)
    assert len(asked) > 1 and usage["pieces"] == len(asked)
    times = [{beat_of[s] for s in piece} for piece in asked]
    assert all(not (a & b) for i, a in enumerate(times) for b in times[i + 1:])  # a beat is never split
    assert document["inbetweens"] == plans["motion"]["inbetweens"]
    asked.clear()
    backend.write("motion", "S13", packet, [{"code": "BODY_OVERLAP", "slot": "acrobat@b06", "message": "."}])
    assert len(asked) == 1 and "acrobat@b06" in asked[0]


def test_an_idea_the_library_cannot_cast_is_cast_from_new_draft_cards():
    """AA-6: S02 casts nobody from "a kunoichi ... on a moonlit rooftop"; the backend's rewrite and its draft cards (a
    kunoichi, a rooftop) cast the kunoichi on the roof; a castable idea stands as written; a new card is a draft."""
    import copy

    import yaml

    from compiler import pipeline
    from compiler.author import casting
    ninja = yaml.safe_load((ROOT / "library" / "archetypes" / "ninja.yaml").read_text(encoding="utf-8"))
    world = yaml.safe_load((ROOT / "library" / "worlds" / "bamboo_courtyard.yaml").read_text(encoding="utf-8"))
    kunoichi = {**copy.deepcopy(ninja), "card_id": "kunoichi", "names": ["kunoichi"], "status": "approved"}
    rooftop = {**copy.deepcopy(world), "card_id": "moonlit_rooftop", "names": ["moonlit rooftop"], "match_terms": ["rooftop"],
               "surfaces": [{"id": "roof", "kind": "floor", "description": "Flat roof at y=0."}]}

    class Caster:
        def cast(self, idea, index, schemas, findings=None):
            return {"query": "6 seconds anime fight scene. A: kunoichi, dark blue outfit. On a moonlit rooftop.",
                    "cards": [kunoichi, rooftop]}, {"model": "fake"}

    query, cards, new = casting("6 seconds anime: a kunoichi in dark blue sprints across a moonlit rooftop", Caster())
    envelope = pipeline.run(query, until="brief", cards=cards)
    assert [e["id"] for e in envelope["nodes"]["entities"]["items"]] == ["kunoichi"]
    assert [s["id"] for s in envelope["nodes"]["surfaces"]["items"]] == ["roof"]
    assert {c["card_id"]: c["status"] for c in new} == {"kunoichi": "draft", "moonlit_rooftop": "draft"}
    castable = "6 seconds anime fight scene: ninja versus knight in a moonlit bamboo courtyard"
    assert casting(castable, None)[0] == castable
