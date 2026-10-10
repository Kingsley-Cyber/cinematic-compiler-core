"""Load the kernel files (each validated by its schema) and compute the kernel hash envelopes record."""

import hashlib
import json
from pathlib import Path

import yaml

from validators.schema_validator import validate_schema

ROOT = Path(__file__).resolve().parents[1]
HASHED = ("kernel/invariants.yaml", "kernel/state_vocabulary.yaml", "kernel/conventions.yaml")
SCHEMAS = {"invariants": "kernel_invariants", "state_vocabulary": "kernel_state_vocabulary",
           "conventions": "kernel_conventions", "owner_invariants": "kernel_owner_invariants"}


def load(name, root=ROOT):
    document = yaml.safe_load((root / "kernel" / f"{name}.yaml").read_text(encoding="utf-8"))
    schema = json.loads((root / "schemas" / f"{SCHEMAS[name]}.schema.json").read_text(encoding="utf-8"))
    validate_schema(document, schema)
    return document


def kernel_hash(root=ROOT):
    """sha256 over the kernel files every envelope depends on (path + bytes, fixed order)."""
    digest = hashlib.sha256()
    for name in HASHED:
        digest.update(name.encode("utf-8") + b"\0" + (root / name).read_bytes() + b"\0")
    return "sha256:" + digest.hexdigest()
