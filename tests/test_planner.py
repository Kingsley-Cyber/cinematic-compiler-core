"""S01 intent parser gates: schema, determinism, completeness, non-invention (owner spec 2026-10-10)."""

import copy
import json
import os
import random
import subprocess
import sys

import pytest
from conftest import ROOT, empty_envelope

from compiler.passes.mandatory import p01_intent
from kernel.canonical import ContractError, canonical_json
from planner.dependency_graph import node_index
from planner.intent_parser import FIELDS, GENRES, MISSING_NAME, NEVER_EXTRACTED, NUMBER_WORDS, parse_intent
from validators.layer_dependency_validator import check_pass_writes
from validators.schema_validator import validate_schema

pytestmark = pytest.mark.unit
SCHEMA = json.loads((ROOT / "schemas" / "intent_document.schema.json").read_text(encoding="utf-8"))
CORPUS = ["10s anime fight, 24fps, moonlit bamboo courtyard", "ugc 15s, glasses product demo",
          "wizard vs superman variant", "", "5 seconds", "10s anime fight, 15 seconds", "anime ugc ad, 30 fps",
          "10 seconds choreographed wizard versus acrobat fight scene in a stone courtyard, wizard with a staff",
          "live-action duel on the rooftop in the style of Wong Kar-wai", "Ghibli-style chase, 12 fps, 8 sec",
          "ten-second ugc ad, hands holding a coffee cup, kitchen counter", "   ", "24 frames per second, 2.5s"]


def test_owner_examples():
    cases = {
        "10s anime fight, 24fps, moonlit bamboo courtyard":
            {"duration_s": 10, "fps": 24, "genre": "anime", "setting": "moonlit bamboo courtyard",
             "entities_hinted": [], "props_hinted": [], "style_reference": None},
        "ugc 15s, glasses product demo":
            {"duration_s": 15, "fps": None, "genre": "ugc_ad", "setting": None,
             "entities_hinted": ["glasses"], "props_hinted": [], "style_reference": None},
        "wizard vs superman variant":
            {"duration_s": None, "fps": None, "genre": None, "setting": None,
             "entities_hinted": ["wizard", "superman variant"], "props_hinted": [], "style_reference": None},
        "": {field: [] if field.endswith("hinted") else None for field in FIELDS},
        "5 seconds": {"duration_s": 5, "fps": None, "genre": None, "setting": None,
                      "entities_hinted": [], "props_hinted": [], "style_reference": None},
    }
    for query, parsed in cases.items():
        assert parse_intent(query)["parsed"] == parsed, query
    assert parse_intent("wizard vs superman variant")["missing"][:2] == ["duration_s", "fps"]
    empty = parse_intent("")
    assert empty["missing"] == [MISSING_NAME[f] for f in FIELDS] + list(NEVER_EXTRACTED)
    assert empty["confidence"] == "low"
    assert parse_intent("10s anime fight, 24fps, moonlit bamboo courtyard")["confidence"] == "medium"


@pytest.mark.parametrize("query", CORPUS)
def test_schema_gate(query):
    assert validate_schema(parse_intent(query), SCHEMA)["status"] == "valid"


def test_intent_schema_genres_match_declared_modalities(order):
    genres = SCHEMA["properties"]["parsed"]["properties"]["genre"]["enum"]
    assert genres == [None, *order["modalities"]]
    assert SCHEMA["properties"]["flags"]["properties"]["genre"]["enum"] == genres


@pytest.mark.integration
def test_determinism_gate_is_byte_identical_across_processes():
    query = CORPUS[7]
    outputs = set()
    for seed in ("0", "1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        result = subprocess.run([sys.executable, "-m", "planner.intent_parser", query, "--genre", "anime"],
                                cwd=ROOT, capture_output=True, text=True, env=env, check=True)
        outputs.add(result.stdout)
    assert outputs == {canonical_json(parse_intent(query, genre="anime"))}


@pytest.mark.parametrize("query", CORPUS)
def test_completeness_gate(query):
    document = parse_intent(query)
    for field in FIELDS:
        extracted = document["parsed"][field] not in (None, [])
        assert extracted != (MISSING_NAME[field] in document["missing"]), (query, field)
        assert extracted == (field in document["evidence"]), (query, field)
    assert document["missing"][-3:] == list(NEVER_EXTRACTED)


def _number_in(text):
    token = next(part for part in text.replace("-", " ").split() if part.lower() in NUMBER_WORDS or part[0].isdigit())
    digits = "".join(ch for ch in token if ch.isdigit() or ch == ".").rstrip(".")
    value = NUMBER_WORDS.get(token.lower()) if token.lower() in NUMBER_WORDS else float(digits)
    return value


@pytest.mark.parametrize("query", CORPUS)
def test_non_invention_gate(query):
    document = parse_intent(query)
    for field, rows in document["evidence"].items():
        for row in rows:
            if row["source"] == "query":
                start, end = row["span"]
                assert query[start:end] == row["text"]
        value = document["parsed"][field]
        if field in ("duration_s", "fps"):
            assert all(_number_in(row["text"]) == value for row in rows)
        elif field == "genre":
            assert all(dict(GENRES)[value].fullmatch(row["text"]) for row in rows if row["source"] == "query")
        elif isinstance(value, list):
            assert [row["text"] for row in rows] == value
        else:
            assert rows[0]["text"] == value
    for ambiguity in document["ambiguous"]:
        assert document["parsed"][ambiguity["field"]] is None


FILLER = ["anime", "fight", "moonlit", "courtyard", "wizard", "kick", "slow", "camera", "dusk", "rain", "blade",
          "crowd", "spin", "leap", "shadow", "glow", "dust"]


def _filler(rng):
    return " ".join(rng.choice(FILLER) for _ in range(rng.randint(0, 4)))


def test_fuzz_number_followed_by_seconds_unit():
    rng = random.Random(20261010)
    for _ in range(500):
        number = rng.choice([rng.randint(1, 600), round(rng.uniform(0.5, 60), 1)])
        unit = rng.choice(["s", " s", " sec", " secs", " second", " seconds", "-second", "sec"])
        query = f"{_filler(rng)} {number}{unit}, {_filler(rng)}".strip()
        assert parse_intent(query)["parsed"]["duration_s"] == number, query


def test_fuzz_fps():
    rng = random.Random(1010)
    for _ in range(500):
        number = rng.choice([rng.randint(1, 120), round(rng.uniform(8, 60), 3)])
        form = rng.choice(["{n}fps", "{n} fps", "{n} FPS", "fps {n}", "fps: {n}", "{n} frames per second"])
        query = f"{_filler(rng)} {form.format(n=number)} {_filler(rng)}".strip()
        document = parse_intent(query)
        assert document["parsed"]["fps"] == number, query
        assert document["parsed"]["duration_s"] is None, query


def test_flags_override_with_flag_evidence_and_bad_flags_refuse():
    document = parse_intent("10s ugc ad, glasses product demo", genre="anime", duration_s=8)
    assert (document["parsed"]["genre"], document["parsed"]["duration_s"]) == ("anime", 8)
    assert document["evidence"]["genre"] == [{"source": "flag"}] == document["evidence"]["duration_s"]
    for kwargs in ({"genre": "ugc"}, {"duration_s": 0}, {"duration_s": True}):
        with pytest.raises(ContractError) as error:
            parse_intent("x", **kwargs)
        assert error.value.code == "INTENT_FLAG"


def test_conflicts_are_ambiguous_and_repeats_are_not():
    document = parse_intent("anime ugc ad, 10s, 10 seconds, 24 fps, 30 fps")
    assert document["parsed"]["genre"] is None and document["parsed"]["fps"] is None
    assert {row["field"] for row in document["ambiguous"]} == {"genre", "fps"}
    assert document["parsed"]["duration_s"] == 10 and len(document["evidence"]["duration_s"]) == 2


@pytest.mark.integration
def test_s01_pass_writes_only_intent_and_never_mutates_input(order):
    before = empty_envelope(order, "anime")
    del before["intent"]
    snapshot = copy.deepcopy(before)
    after = p01_intent.run(before, CORPUS[0], order=order)
    assert before == snapshot
    assert after["intent"] == parse_intent(CORPUS[0])
    assert check_pass_writes(order, "intent", before, after) == []
    assert check_pass_writes(order, "brief", before, after)[0]["code"] == "WRITE_SCOPE"


def test_pass_files_are_named_from_their_step_id(order):
    index = node_index(order)
    expected = {f"p{node['step_id'][1:]}_{identity}.py" for identity, node in index.items()}
    files = {path.name for path in (ROOT / "compiler" / "passes").rglob("p[0-9][0-9]_*.py")}
    assert files and files <= expected
