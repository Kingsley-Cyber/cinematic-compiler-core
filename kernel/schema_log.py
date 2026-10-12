"""Append-only hash logs: every schema (and every library card) change is recorded with its exact bytes hash.

`verify()` is the control: a file whose bytes differ from its latest log entry, a file with no
entry, an entry for a missing file, or an edited/reordered log are all refused. Record with:

    python -m kernel.schema_log record schemas/x.schema.json --change created --reason "..." --decided-by owner
    python -m kernel.schema_log --log library record library/worlds/x.yaml --change created --reason "..." ...
"""

import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

import yaml

from .canonical import ContractError, load_json
from .version import LAYER_ORDER_VERSION

ROOT = Path(__file__).resolve().parents[1]
CHANGES = {"created", "changed", "removed"}
DECIDERS = {"owner", "owner_default", "agent_fix"}


def _schema_version(path):
    return load_json(path.read_text(encoding="utf-8")).get("$id")


def _card_version(path):
    """A card's `card_version`, or a library file's `version` (F-078: 18 library files carry `version`, which the log
    read as None until S-044)."""
    card = yaml.safe_load(path.read_text(encoding="utf-8"))
    return f"{card.get('card_version', card.get('version'))}:{card.get('status')}"


def _kernel_version(path):
    if path.suffix != ".yaml":
        return None
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    return f"{document.get('version')}:{document.get('status')}"


class HashLog:
    def __init__(self, log, folder, pattern, key, version_key, read_version, digest=None):
        self.log, self.folder, self.pattern = log, folder, pattern
        self.key, self.version_key, self.read_version = key, version_key, read_version
        self.digest = digest or (lambda path: "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest())
        self.fields = {"seq", "date", key, "change", "sha256", "previous_sha256", version_key,
                       "layer_order_version", "reason", "decided_by"}

    def files(self, root=ROOT):
        patterns = (self.pattern,) if isinstance(self.pattern, str) else self.pattern
        found = {p.relative_to(root).as_posix() for pattern in patterns for p in (root / self.folder).glob(pattern)}
        return sorted(found)

    def entries(self, root=ROOT):
        path = root / self.log
        if not path.exists():
            return []
        rows = []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                raise ContractError("SCHEMA_LOG", "Blank line in log", f"{self.log} line {number}")
            row = load_json(line)
            if set(row) != self.fields:
                raise ContractError("SCHEMA_LOG", "Log entry fields differ from the log contract",
                                    f"{self.log} line {number}")
            rows.append(row)
        return rows

    def check_chain(self, rows):
        """The log itself: append-only sequence, known values, and each entry chained to its file's previous hash."""
        for index, row in enumerate(rows, 1):
            if row["seq"] != index:
                raise ContractError("SCHEMA_LOG", "Log is not append-only: sequence gap or reorder",
                                    f"seq {row['seq']}")
            if row["change"] not in CHANGES or row["decided_by"] not in DECIDERS or not row["reason"].strip():
                raise ContractError("SCHEMA_LOG", "Entry needs a known change, decider and a reason", f"seq {index}")
        previous = {}
        for row in rows:
            expected = previous.get(row[self.key])
            if row["previous_sha256"] != expected:
                raise ContractError("SCHEMA_LOG", "Entry does not chain to the file's previous hash",
                                    f"seq {row['seq']}")
            if (row["change"] == "created") != (expected is None):
                raise ContractError("SCHEMA_LOG", "Only a file's first entry may be 'created'", f"seq {row['seq']}")
            previous[row[self.key]] = None if row["change"] == "removed" else row["sha256"]

    def verify(self, root=ROOT):
        """Refuse any drift between file bytes and the log. Returns the latest entry per file."""
        rows = self.entries(root)
        self.check_chain(rows)
        current = {}
        for row in rows:
            current[row[self.key]] = row
        files = set(self.files(root))
        for name in sorted(files):
            row = current.get(name)
            if row is None or row["change"] == "removed":
                raise ContractError("SCHEMA_UNLOGGED", "File has no log entry", name)
            if self.digest(root / name) != row["sha256"]:
                raise ContractError("SCHEMA_DRIFT", "File bytes differ from their latest log entry", name)
        for name, row in current.items():
            if row["change"] != "removed" and name not in files:
                raise ContractError("SCHEMA_MISSING", "Logged file is missing", name)
        return current

    def record(self, name, change, reason, decided_by, root=ROOT, today=None):
        """Append one entry after checking the existing log is intact."""
        rows = self.entries(root)
        self.check_chain(rows)
        previous = None
        for row in rows:
            if row[self.key] == name:
                previous = row
        live = previous is not None and previous["change"] != "removed"
        if (change == "created") == live:
            raise ContractError("SCHEMA_LOG", "'created' is only for a file with no live entry; use 'changed'", name)
        path = root / name
        if change == "removed":
            if path.exists():
                raise ContractError("SCHEMA_LOG", "Remove the file before recording its removal", name)
            sha, version = None, None
        else:
            sha = self.digest(path)
            if previous and previous["sha256"] == sha:
                raise ContractError("SCHEMA_LOG", "File bytes are unchanged since the last entry", name)
            version = self.read_version(path)
        row = {"seq": len(rows) + 1, "date": today or datetime.date.today().isoformat(), self.key: name,
               "change": change, "sha256": sha, "previous_sha256": previous["sha256"] if live else None,
               self.version_key: version, "layer_order_version": LAYER_ORDER_VERSION, "reason": reason,
               "decided_by": decided_by}
        with (root / self.log).open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        self.check_chain(self.entries(root))
        return row


SCHEMAS = HashLog("schemas/schema_log.jsonl", "schemas", "**/*.schema.json", "schema", "schema_version",
                  _schema_version)
LIBRARY = HashLog("library/library_log.jsonl", "library", "**/*.yaml", "card", "card_version", _card_version)
KERNEL = HashLog("kernel/kernel_log.jsonl", "kernel", ("sources/*.txt", "kernel_scope.yaml", "invariants.yaml",
                                                       "state_vocabulary.yaml", "conventions.yaml", "owner_invariants.yaml",
                                                       "knowledge_map.yaml", "layer_order.yaml",  # layer order: F-078
                                                       "contact_world_exceptions.yaml"),  # F-123
                 "file", "file_version", _kernel_version)
GENERATED_BLOCK = re.compile(r"<!-- BEGIN GENERATED: (\w+) -->\n.*?<!-- END GENERATED: \1 -->", re.S)
DOCS_VERSION = re.compile(r"docs-version: (\S+?)(?: -->|$)", re.M)


def _docs_version(path):
    """A frozen doc's version: `version:` in YAML, else its `docs-version: X` marker (owner O64: no change without a bump)."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".yaml":
        return str(yaml.safe_load(text).get("version"))
    match = DOCS_VERSION.search(text)
    return match.group(1) if match else None


def _docs_digest(path):
    """The hand-written bytes only: generated blocks (kernel/docs_plane.py) change every session and are checked there."""
    text = GENERATED_BLOCK.sub(lambda m: f"<!-- GENERATED: {m.group(1)} -->", path.read_text(encoding="utf-8"))
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# Frozen docs (owner O64, O68, O69): the operating manual, the rulebook, the owner's and refactor guides, the ownership
# and versioning rules, the self-audit prompt, the bootstrap README, the commands, the artifact templates and CODEOWNERS.
DOCS = HashLog("docs/docs_log.jsonl", ".", ("AGENTS.md", "docs/rules.yaml", "docs/for_the_owner.md",
                                            "docs/how_to_refactor.md", "docs/ownership.md", "docs/versioning.md",
                                            "docs/prompts/*.md", ".claude/commands/*.md", "docs/bootstrap/README.md",
                                            "docs/*/_template.md", ".github/CODEOWNERS"),
               "file", "docs_version", _docs_version, digest=_docs_digest)
LOGS = {"schemas": SCHEMAS, "library": LIBRARY, "kernel": KERNEL, "docs": DOCS}


def schema_files(root=ROOT):
    return SCHEMAS.files(root)


def entries(log=None, root=ROOT):
    return SCHEMAS.entries(root)


def verify(root=ROOT, log=None):
    return SCHEMAS.verify(root)


def record(schema, change, reason, decided_by, root=ROOT, log=None, today=None):
    return SCHEMAS.record(schema, change, reason, decided_by, root=root, today=today)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m kernel.schema_log")
    parser.add_argument("--log", choices=sorted(LOGS), default="schemas")
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("path")
    rec.add_argument("--change", choices=sorted(CHANGES), required=True)
    rec.add_argument("--reason", required=True)
    rec.add_argument("--decided-by", choices=sorted(DECIDERS), required=True)
    sub.add_parser("verify")
    args = parser.parse_args(argv)
    target = LOGS[args.log]
    if args.command == "record":
        print(json.dumps(target.record(args.path, args.change, args.reason, args.decided_by), sort_keys=True))
    else:
        print(json.dumps({name: row["sha256"] for name, row in target.verify().items()}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
