"""Canonical JSON and content hashes for envelopes, schemas and receipts.

Ported from ai-video-compiler `video_compiler/serialization.py` and `errors.py` (phase4-wip e49273a).
"""

import hashlib
import json
import math


class ContractError(Exception):
    """A typed refusal: `code` is stable for tests, `message` is for people."""

    def __init__(self, code, message, path=None):
        super().__init__(f"{code}: {message}" + (f" at {path}" if path else ""))
        self.code, self.message, self.path = code, message, path


def check_finite(value, path="$"):
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError("NONFINITE_NUMBER", "JSON and canonical records require finite numbers", path)
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ContractError("FIELD_TYPE", "Object keys must be strings", path)
            check_finite(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            check_finite(child, f"{path}[{index}]")


def canonical_json(value):
    check_finite(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    except (TypeError, ValueError) as error:
        raise ContractError("FIELD_TYPE", str(error)) from error


def content_hash(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ContractError("DUPLICATE_KEY", f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value):
    raise ContractError("NONFINITE_NUMBER", f"Invalid JSON number: {value}")


def load_json(text):
    """Strict JSON: duplicate keys and NaN/Infinity are refused, not silently accepted."""
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except json.JSONDecodeError as error:
        raise ContractError("INVALID_JSON", str(error)) from error
    check_finite(value)
    return value
