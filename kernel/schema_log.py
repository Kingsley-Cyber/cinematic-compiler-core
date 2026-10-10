"""Append-only schema log: every schema change is recorded with its exact bytes hash.

`verify()` is the control: a schema whose bytes differ from its latest log entry,
a schema with no entry, an entry for a missing file, or an edited/reordered log
are all refused. Record a change with:

    python -m kernel.schema_log record schemas/x.schema.json --change created \
        --reason "..." --decided-by owner
"""

import argparse
import datetime
import hashlib
import json
from pathlib import Path

from .canonical import ContractError, load_json
from .version import LAYER_ORDER_VERSION

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "schemas" / "schema_log.jsonl"
CHANGES = {"created", "changed", "removed"}
DECIDERS = {"owner", "owner_default", "agent_fix"}
FIELDS = {"seq", "date", "schema", "change", "sha256", "previous_sha256", "schema_version",
          "layer_order_version", "reason", "decided_by"}


def _digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def schema_files(root=ROOT):
    return sorted(p.relative_to(root).as_posix() for p in (root / "schemas").rglob("*.schema.json"))


def entries(log=LOG):
    if not log.exists():
        return []
    rows = []
    for number, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ContractError("SCHEMA_LOG", "Blank line in schema log", f"line {number}")
        row = load_json(line)
        if set(row) != FIELDS:
            raise ContractError("SCHEMA_LOG", "Log entry fields differ from the log contract", f"line {number}")
        rows.append(row)
    return rows


def latest(rows):
    result = {}
    for row in rows:
        result[row["schema"]] = row
    return result


def verify(root=ROOT, log=None):
    """Refuse any drift between schema bytes and the log. Returns the latest entry per schema."""
    log = log or root / "schemas" / "schema_log.jsonl"
    rows = entries(log)
    for index, row in enumerate(rows, 1):
        if row["seq"] != index:
            raise ContractError("SCHEMA_LOG", "Log is not append-only: sequence gap or reorder", f"seq {row['seq']}")
        if row["change"] not in CHANGES or row["decided_by"] not in DECIDERS or not row["reason"].strip():
            raise ContractError("SCHEMA_LOG", "Entry needs a known change, decider and a reason", f"seq {index}")
    previous = {}
    for row in rows:
        expected = previous.get(row["schema"])
        if row["previous_sha256"] != expected:
            raise ContractError("SCHEMA_LOG", "Entry does not chain to the schema's previous hash", f"seq {row['seq']}")
        if (row["change"] == "created") != (expected is None):
            raise ContractError("SCHEMA_LOG", "Only a schema's first entry may be 'created'", f"seq {row['seq']}")
        previous[row["schema"]] = None if row["change"] == "removed" else row["sha256"]
    current = latest(rows)
    files = set(schema_files(root))
    for name in sorted(files):
        row = current.get(name)
        if row is None or row["change"] == "removed":
            raise ContractError("SCHEMA_UNLOGGED", "Schema file has no log entry", name)
        if _digest(root / name) != row["sha256"]:
            raise ContractError("SCHEMA_DRIFT", "Schema bytes differ from their latest log entry", name)
    for name, row in current.items():
        if row["change"] != "removed" and name not in files:
            raise ContractError("SCHEMA_MISSING", "Logged schema file is missing", name)
    return current


def record(schema, change, reason, decided_by, root=ROOT, log=None, today=None):
    """Append one entry after checking the existing log is intact."""
    log = log or root / "schemas" / "schema_log.jsonl"
    rows = entries(log)
    previous = latest(rows).get(schema)
    live = previous is not None and previous["change"] != "removed"
    if (change == "created") == live:
        raise ContractError("SCHEMA_LOG", "'created' is only for a schema with no live entry; use 'changed'", schema)
    path = root / schema
    if change == "removed":
        if path.exists():
            raise ContractError("SCHEMA_LOG", "Remove the file before recording its removal", schema)
        sha, version = None, None
    else:
        sha = _digest(path)
        if previous and previous["sha256"] == sha:
            raise ContractError("SCHEMA_LOG", "Schema bytes are unchanged since the last entry", schema)
        version = load_json(path.read_text(encoding="utf-8")).get("$id")
    row = {"seq": len(rows) + 1, "date": today or datetime.date.today().isoformat(), "schema": schema,
           "change": change, "sha256": sha,
           "previous_sha256": None if previous is None or previous["change"] == "removed" else previous["sha256"],
           "schema_version": version, "layer_order_version": LAYER_ORDER_VERSION, "reason": reason,
           "decided_by": decided_by}
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    verify(root, log)
    return row


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m kernel.schema_log")
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("schema")
    rec.add_argument("--change", choices=sorted(CHANGES), required=True)
    rec.add_argument("--reason", required=True)
    rec.add_argument("--decided-by", choices=sorted(DECIDERS), required=True)
    sub.add_parser("verify")
    args = parser.parse_args(argv)
    if args.command == "record":
        print(json.dumps(record(args.schema, args.change, args.reason, args.decided_by), sort_keys=True))
    else:
        print(json.dumps({name: row["sha256"] for name, row in verify().items()}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
