"""Checks that the layer DAG, an envelope and each pass obey kernel/layer_order.yaml.

- check_layer_order: the DAG file itself (versions, references, ownership, cycles).
- check_envelope: every node/edge group carries its owner's layer tag; groups of
  layers inactive for the scene's modality hold no items.
- check_pass_writes: a pass changed only the envelope paths its node owns, so no
  pass mutates an earlier layer's graph.
Each returns a list of findings; an empty list means the check passed.
"""

import re

from kernel.canonical import ContractError
from kernel.version import ENVELOPE_VERSION, KERNEL_VERSION, LAYER_ORDER_VERSION
from planner.dependency_graph import is_active, node_index, write_owners
from planner.topological_sort import build_order

KNOWN_VALIDATORS = {"schema", "coherence", "invariants", "constraint", "camera_rules",
                    "pose", "object", "state", "affordance"}
TOP_PATHS = {"/graph_version", "/derived_from", "/scene", "/invariants", "/provenance"}
GROUP_PREFIXES = ("/nodes/", "/edges/", "/validation/")
STEP_ID = re.compile(r"S[0-9]{2}")


def _finding(code, message, subject=None):
    return {"code": code, "message": message, "subject": subject}


def check_layer_order(order):
    findings = []
    for key, expected in (("kernel", KERNEL_VERSION), ("envelope", ENVELOPE_VERSION), ("version", LAYER_ORDER_VERSION)):
        if order[key] != expected:
            findings.append(_finding("VERSION_DRIFT", f"{key} differs from kernel/version.py", order[key]))
    ids = [node["id"] for node in order["nodes"]]
    duplicates = sorted({identity for identity in ids if ids.count(identity) > 1})
    if duplicates:
        findings.append(_finding("DUPLICATE_NODE", "Node ids must be unique", duplicates))
    index = node_index(order)
    for node in order["nodes"]:
        for dependency in node["depends_on"]:
            if dependency not in index or dependency == node["id"]:
                findings.append(_finding("UNKNOWN_DEPENDENCY", "Dependency is undeclared or self-referential",
                                         [node["id"], dependency]))
                continue
            for modality in node.get("when", order["modalities"]):
                if not is_active(index[dependency], modality) and "when" in node:
                    findings.append(_finding("CONDITIONAL_DEPENDENCY",
                                             "A conditional node needs its dependencies in every modality it runs in",
                                             [node["id"], dependency, modality]))
        if "when" in node and (not node["when"] or set(node["when"]) - set(order["modalities"])):
            findings.append(_finding("UNKNOWN_MODALITY", "when must name declared modalities", node["id"]))
        unknown = set(node["validated_by"]) - KNOWN_VALIDATORS
        if unknown:
            findings.append(_finding("UNKNOWN_VALIDATOR", "validated_by names an unregistered check",
                                     [node["id"], sorted(unknown)]))
    owners = write_owners(order)
    for path, writers in sorted(owners.items()):
        if len(writers) > 1:
            findings.append(_finding("SHARED_WRITE", "Each envelope path has exactly one owner", [path, writers]))
        if path not in TOP_PATHS and not (path.startswith(GROUP_PREFIXES) and path.count("/") == 2):
            findings.append(_finding("UNKNOWN_PATH", "Write path is not a declared envelope location", path))
    paths = sorted(owners)
    for path in paths:
        for other in paths:
            if other != path and other.startswith(path + "/"):
                findings.append(_finding("OVERLAPPING_WRITE", "Write paths may not nest", [path, other]))
    steps = [node["step"] for node in order["nodes"]]
    for node in order["nodes"]:
        if not STEP_ID.fullmatch(node["step"]):
            findings.append(_finding("STEP_ID", "Step IDs read S01, S02 ...", [node["id"], node["step"]]))
    if len(set(steps)) != len(steps):
        repeated = sorted({step for step in steps if steps.count(step) > 1})
        findings.append(_finding("STEP_ID", "Step IDs must be unique", repeated))
    index = node_index(order)
    for modality in order["modalities"]:
        try:
            sequence = build_order(order, modality)
        except ContractError as error:
            findings.append(_finding(error.code, error.message, [modality, error.path]))
            continue
        # Step IDs, not layer numbers, encode order: they must rise along every build order.
        ordered = [index[identity]["step"] for identity in sequence]
        if ordered != sorted(ordered) or len(set(ordered)) != len(ordered):
            findings.append(_finding("STEP_ORDER", "Step IDs must increase along the build order",
                                     [modality, list(zip(sequence, ordered, strict=True))]))
    return findings


def check_envelope(envelope, order):
    findings = []
    modality = envelope["scene"]["genre"]
    index = node_index(order)
    owners = write_owners(order)
    labels = {node["layer"] for node in order["nodes"]}
    for kind in ("nodes", "edges"):
        for group, value in envelope[kind].items():
            path = f"/{kind}/{group}"
            writer = owners.get(path, [None])[0]
            if writer in (None, "pipeline"):
                findings.append(_finding("UNKNOWN_GROUP", "Group has no owning layer in layer_order.yaml", path))
                continue
            node = index[writer]
            if value["layer"] != node["layer"] or value.get("step") != node.get("step"):
                findings.append(_finding("LAYER_TAG", "Group layer/step tag differs from its owning node",
                                         [path, [value["layer"], value.get("step")],
                                          [node["layer"], node.get("step")]]))
            stray = [item["id"] for item in value["items"] if item.get("layer", node["layer"]) != node["layer"]]
            if stray:
                findings.append(_finding("LAYER_TAG", "Item layer tag differs from its group", [path, stray]))
            if not is_active(node, modality) and value["items"]:
                findings.append(_finding("INACTIVE_LAYER_DATA", "A layer inactive for this modality holds items",
                                         [path, modality]))
    for node in order["nodes"]:
        if not is_active(node, modality):
            continue
        for path in node["writes"]:
            kind, _, group = path.strip("/").partition("/")
            if kind in ("nodes", "edges") and group not in envelope[kind]:
                findings.append(_finding("MISSING_GROUP", "An active layer's group is absent", [path, modality]))
    for invariant in envelope["invariants"]:
        if invariant["layer"] not in labels:
            findings.append(_finding("LAYER_TAG", "Invariant names an undeclared layer", invariant["id"]))
    return findings


def _changed(before, after, path=""):
    if before == after and type(before) is type(after):
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        rows = []
        for key in sorted(before.keys() | after.keys()):
            child = path + "/" + key.replace("~", "~0").replace("/", "~1")
            rows.extend(_changed(before[key], after[key], child) if key in before and key in after else [child])
        return rows
    return [path or "/"]


def check_pass_writes(order, node_id, before, after):
    """A pass may change only the paths its node owns; earlier graphs stay untouched."""
    node = node_index(order).get(node_id)
    if node is None:
        return [_finding("UNKNOWN_NODE", "Pass names an undeclared node", node_id)]
    allowed = node["writes"]
    return [_finding("WRITE_SCOPE", "Pass changed a path it does not own", [node_id, changed])
            for changed in _changed(before, after)
            if not any(changed == path or changed.startswith(path + "/") for path in allowed)]
