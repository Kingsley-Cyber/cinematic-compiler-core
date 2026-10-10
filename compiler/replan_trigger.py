"""Replan trigger: a failed gate goes back to the authored step that can fix it, with its findings.

An authored step's own gate failure re-issues that step's packet. A derived step (S05–S07) failing routes to
the nearest authored step upstream (S04 for L1/L2). Each step allows its first attempt plus two re-authoring
attempts; a third failure stops with REPLAN_EXHAUSTED. Attempts are recorded in provenance by the pipeline.
"""

from compiler.authoring import StepFailed
from kernel.canonical import ContractError
from planner.dependency_graph import load, node_index
from planner.topological_sort import build_order

MAX_ATTEMPTS = 3
AUTHORED_NODES = ("temporal",)


def owning_step(failed_node, genre=None, order=None):
    """The authored node a failure at `failed_node` is fixed in."""
    order = order or load()
    sequence = build_order(order, genre or order["modalities"][0])
    upstream = [n for n in sequence[:sequence.index(failed_node) + 1] if n in AUTHORED_NODES]
    if not upstream:
        raise ContractError("REPLAN_TARGET", "No authored step upstream can fix this failure", failed_node)
    return upstream[-1]


def request(error, *, failed_node, attempt, prepare, envelope_before, genre=None):
    """Build the replan request handed back to the author, or stop when the attempts are used up."""
    if attempt >= MAX_ATTEMPTS:
        raise ContractError("REPLAN_EXHAUSTED", "The step failed its first attempt and two re-authoring attempts",
                            failed_node)
    target = owning_step(failed_node, genre)
    findings = error.findings if isinstance(error, StepFailed) else [{"code": error.code, "message": error.message}]
    order = load()
    return {"step_id": node_index(order)[target]["step_id"], "failed_step_id": node_index(order)[failed_node]["step_id"],
            "attempt": attempt + 1, "max_attempts": MAX_ATTEMPTS, "findings": findings,
            "packet": prepare(envelope_before)}
