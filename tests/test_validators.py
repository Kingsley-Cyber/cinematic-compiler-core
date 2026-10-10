"""The ported schema checker keeps its fail-closed behaviour."""

import pytest

from kernel.canonical import ContractError, canonical_json, content_hash, load_json
from validators.schema_validator import check_schema, validate_schema

pytestmark = pytest.mark.unit

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object", "required": ["id", "kind"], "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "pattern": "^[a-z_]+$"},
        "kind": {"enum": ["touch", "grip"]},
        "at": {"type": "number", "minimum": 0},
        "parts": {"type": "array", "items": {"$ref": "#/$defs/Part"}, "minItems": 1, "uniqueItems": True},
        "flag": {"not": {"const": False}}},
    "$defs": {"Part": {"type": "string", "minLength": 1}}}


def test_valid_instance_passes():
    value = {"id": "kick_staff", "kind": "touch", "at": 6, "parts": ["acr_r_foot"], "flag": True}
    assert validate_schema(value, SCHEMA)["status"] == "valid"


@pytest.mark.parametrize("value", [
    {"id": "kick_staff"},
    {"id": "Kick", "kind": "touch"},
    {"id": "kick", "kind": "slap"},
    {"id": "kick", "kind": "touch", "at": -1},
    {"id": "kick", "kind": "touch", "parts": []},
    {"id": "kick", "kind": "touch", "parts": ["a", "a"]},
    {"id": "kick", "kind": "touch", "parts": [""]},
    {"id": "kick", "kind": "touch", "flag": False},
    {"id": "kick", "kind": "touch", "extra": 1},
    {"id": "kick", "kind": "touch", "at": True},
])
def test_invalid_instances_are_refused(value):
    with pytest.raises(ContractError) as error:
        validate_schema(value, SCHEMA)
    assert error.value.code == "TARGET_SCHEMA"


@pytest.mark.parametrize("schema, code", [
    ({"type": "object", "format": "date"}, "SCHEMA_UNSUPPORTED"),
    ({"$ref": "other.schema.json#/x"}, "SCHEMA_UNSUPPORTED"),
    ({"$ref": "#/$defs/Missing"}, "SCHEMA_REFERENCE"),
    ({"type": "decimal"}, "SCHEMA_SHAPE"),
    ({"enum": []}, "SCHEMA_SHAPE"),
])
def test_unsupported_or_malformed_schemas_fail_before_any_instance(schema, code):
    with pytest.raises(ContractError) as error:
        check_schema(schema)
    assert error.value.code == code


def test_canonical_json_is_strict():
    assert canonical_json({"b": 1, "a": [1.5]}) == '{"a":[1.5],"b":1}\n'
    assert content_hash({"a": 1}) == content_hash({"a": 1})
    for text, code in (('{"a":1,"a":2}', "DUPLICATE_KEY"), ('{"a":NaN}', "NONFINITE_NUMBER"), ("{", "INVALID_JSON")):
        with pytest.raises(ContractError) as error:
            load_json(text)
        assert error.value.code == code
