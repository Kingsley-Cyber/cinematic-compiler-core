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
from planner.dependency_graph import is_active, node_index, owner_of, write_owners
from planner.topological_sort import build_order

KNOWN_VALIDATORS = {"schema", "coherence", "invariants", "constraint", "camera_rules",
                    "pose", "object", "state", "affordance"}
TOP_PATHS = {"/graph_version", "/derived_from", "/intent", "/scene", "/invariants", "/provenance"}
GROUP_PREFIXES = ("/nodes/", "/edges/", "/validation/", "/scene/")
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
    sequences = {}
    for modality in order["modalities"]:
        try:
            sequences[modality] = build_order(order, modality)
        except ContractError:
            sequences[modality] = None
    paths = sorted(owners)
    for path in paths:
        for other in paths:
            if other == path or not other.startswith(path + "/"):
                continue
            outer, inner = owners[path][0], owners[other][0]
            # A carve-out is allowed only when its owner always runs after the outer owner.
            later = all(seq is None or outer not in seq or inner not in seq or seq.index(inner) > seq.index(outer)
                        for seq in sequences.values())
            if outer == "pipeline" or inner == "pipeline" or outer == inner or not later:
                findings.append(_finding("OVERLAPPING_WRITE", "A nested path must be owned by a later step",
                                         [path, other]))
    findings.extend(_check_edges(order, owners, sequences))
    steps = [node["step_id"] for node in order["nodes"]]
    for node in order["nodes"]:
        if not STEP_ID.fullmatch(node["step_id"]):
            findings.append(_finding("STEP_ID", "Step IDs read S01, S02 ...", [node["id"], node["step_id"]]))
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
        ordered = [index[identity]["step_id"] for identity in sequence]
        if ordered != sorted(ordered) or len(set(ordered)) != len(ordered):
            findings.append(_finding("STEP_ORDER", "Step IDs must increase along the build order",
                                     [modality, list(zip(sequence, ordered, strict=True))]))
    return findings


def _check_edges(order, owners, sequences):
    """Every edge group declares endpoints that are node groups written no later than the edge group."""
    findings = []
    index = node_index(order)
    endpoints = order["edge_endpoints"]
    written = {path.split("/")[2] for path in owners if path.startswith("/edges/")}
    for group in sorted(written ^ set(endpoints)):
        findings.append(_finding("EDGE_ENDPOINTS", "Edge group and endpoint declarations must match", group))
    for node in order["nodes"]:
        if node.get("projection") and any(not path.startswith("/nodes/") for path in node["writes"]):
            findings.append(_finding("PROJECTION", "A projection step writes node groups only", node["id"]))
        if "projection" in node and node["projection"] is not True:
            findings.append(_finding("PROJECTION", "projection is either true or absent", node["id"]))
    for group in sorted(written & set(endpoints)):
        writer = owners["/edges/" + group][0]
        for end in endpoints[group]["from"] + endpoints[group]["to"]:
            if end == "scene":
                continue
            owner = owners.get("/nodes/" + end, [None])[0]
            if owner is None or owner == "pipeline" or index[owner].get("projection"):
                findings.append(_finding("EDGE_ENDPOINTS", "Endpoint is not a graph node group", [group, end]))
                continue
            for modality, seq in sequences.items():
                if seq is None or writer not in seq:
                    continue
                if owner not in seq or seq.index(owner) > seq.index(writer):
                    findings.append(_finding("EDGE_ENDPOINTS", "Endpoint group is not built before the edge group",
                                             [group, end, modality]))
    return findings


def check_envelope(envelope, order):
    findings = []
    modality = envelope["scene"]["genre"]
    index = node_index(order)
    owners = write_owners(order)
    labels = {node["band"] for node in order["nodes"]}
    for kind in ("nodes", "edges"):
        for group, value in envelope[kind].items():
            path = f"/{kind}/{group}"
            writer = owners.get(path, [None])[0]
            if writer in (None, "pipeline"):
                findings.append(_finding("UNKNOWN_GROUP", "Group has no owning layer in layer_order.yaml", path))
                continue
            node = index[writer]
            if value["band"] != node["band"] or value.get("step_id") != node.get("step_id"):
                findings.append(_finding("LAYER_TAG", "Group layer/step tag differs from its owning node",
                                         [path, [value["band"], value.get("step_id")],
                                          [node["band"], node.get("step_id")]]))
            stray = [item["id"] for item in value["items"] if item.get("band", node["band"]) != node["band"]]
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
        if invariant["band"] not in labels:
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
    """A pass may change only paths whose most specific owner is its node; earlier graphs stay untouched."""
    if node_id not in node_index(order):
        return [_finding("UNKNOWN_NODE", "Pass names an undeclared node", node_id)]
    return [_finding("WRITE_SCOPE", "Pass changed a path it does not own", [node_id, changed])
            for changed in _changed(before, after) if owner_of(order, changed) != node_id]
