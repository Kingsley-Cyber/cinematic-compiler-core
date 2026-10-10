"""Envelope schema: generated without drift, logged by hash, and enforcing its structure."""

import copy
import json
import shutil

import pytest
from conftest import ROOT, empty_envelope

from kernel import build_ir_schema, schema_log
from kernel.canonical import ContractError
from validators.schema_validator import check_schema, validate_schema

pytestmark = pytest.mark.unit


@pytest.mark.integration
def test_committed_schema_equals_generation_from_layer_order(order):
    assert (ROOT / "schemas" / "cinematic_ir.schema.json").read_text(encoding="utf-8") == build_ir_schema.render(order)


@pytest.mark.integration
def test_every_schema_matches_its_latest_log_entry():
    current = schema_log.verify()
    assert set(current) == set(schema_log.schema_files())


def test_schema_uses_only_supported_keywords(envelope_schema):
    check_schema(envelope_schema)


@pytest.mark.parametrize("modality", ["anime", "live_action", "ugc_ad"])
def test_empty_envelope_validates(order, envelope_schema, modality):
    assert validate_schema(empty_envelope(order, modality), envelope_schema)["status"] == "valid"


@pytest.mark.parametrize("change", ["graph_version", "extra_key", "missing_group", "group_tag", "bad_genre",
                                    "item_without_id", "invariant_layer", "pass_name"])
def test_schema_refuses_structural_errors(order, envelope_schema, change):
    envelope = empty_envelope(order, "anime")
    if change == "graph_version":
        envelope["graph_version"] = "MGRAPH-1.0"
    elif change == "extra_key":
        envelope["prompt"] = "not part of the IR"
    elif change == "missing_group":
        del envelope["nodes"]["beats"]
    elif change == "group_tag":
        envelope["nodes"]["camera"]["layer"] = "L5"
    elif change == "bad_genre":
        envelope["scene"]["genre"] = "documentary"
    elif change == "item_without_id":
        envelope["nodes"]["beats"]["items"].append({"t": 0})
    elif change == "invariant_layer":
        envelope["invariants"].append({"id": "prop_continuity", "layer": "L9", "rule": "props persist"})
    elif change == "pass_name":
        envelope["provenance"]["pass_history"].append({"pass": "temporal", "commit": "abc123", "duration_ms": 4})
    with pytest.raises(ContractError) as error:
        validate_schema(envelope, envelope_schema)
    assert error.value.code == "TARGET_SCHEMA"


@pytest.fixture
def sandbox(tmp_path):
    (tmp_path / "schemas").mkdir()
    shutil.copy(ROOT / "schemas" / "cinematic_ir.schema.json", tmp_path / "schemas" / "cinematic_ir.schema.json")
    schema_log.record("schemas/cinematic_ir.schema.json", "created", "test", "owner", root=tmp_path, today="2026-10-10")
    return tmp_path


def test_schema_log_control_refuses_drift_unlogged_and_missing_files(sandbox):
    schema = sandbox / "schemas" / "cinematic_ir.schema.json"
    schema.write_text(schema.read_text() + " ", encoding="utf-8")
    with pytest.raises(ContractError) as error:
        schema_log.verify(sandbox)
    assert error.value.code == "SCHEMA_DRIFT"
    row = schema_log.record("schemas/cinematic_ir.schema.json", "changed", "whitespace", "agent_fix", root=sandbox)
    assert row["seq"] == 2 and row["previous_sha256"] is not None
    (sandbox / "schemas" / "graphs").mkdir()
    (sandbox / "schemas" / "graphs" / "temporal_graph.schema.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ContractError) as error:
        schema_log.verify(sandbox)
    assert error.value.code == "SCHEMA_UNLOGGED"
    schema_log.record("schemas/graphs/temporal_graph.schema.json", "created", "test", "owner", root=sandbox)
    (sandbox / "schemas" / "graphs" / "temporal_graph.schema.json").unlink()
    with pytest.raises(ContractError) as error:
        schema_log.verify(sandbox)
    assert error.value.code == "SCHEMA_MISSING"
    schema_log.record("schemas/graphs/temporal_graph.schema.json", "removed", "test", "owner", root=sandbox)
    assert set(schema_log.verify(sandbox)) == {"schemas/cinematic_ir.schema.json",
                                               "schemas/graphs/temporal_graph.schema.json"}


def test_schema_log_is_append_only_and_hash_chained(sandbox):
    log = sandbox / "schemas" / "schema_log.jsonl"
    with pytest.raises(ContractError):
        schema_log.record("schemas/cinematic_ir.schema.json", "created", "again", "owner", root=sandbox)
    with pytest.raises(ContractError):
        schema_log.record("schemas/cinematic_ir.schema.json", "changed", "no byte change", "owner", root=sandbox)
    row = json.loads(log.read_text())
    for field, value in (("seq", 2), ("sha256", "sha256:" + "0" * 64), ("reason", " ")):
        edited = copy.deepcopy(row)
        edited[field] = value
        log.write_text(json.dumps(edited) + "\n", encoding="utf-8")
        with pytest.raises(ContractError) as error:
            schema_log.verify(sandbox)
        assert error.value.code in {"SCHEMA_LOG", "SCHEMA_DRIFT"}
