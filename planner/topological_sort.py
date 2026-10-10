"""Deterministic build order for one modality (Kahn's algorithm).

Ties break by position in kernel/layer_order.yaml, so the same file always
yields the same order. A cycle is refused with the nodes that remain blocked.
"""

from kernel.canonical import ContractError

from .dependency_graph import active_nodes, edges


def build_order(order, modality):
    nodes = active_nodes(order, modality)
    position = {identity: index for index, identity in enumerate(nodes)}
    pending = {identity: set() for identity in nodes}
    for before, after in edges(order, modality):
        pending[after].add(before)
    result = []
    while pending:
        ready = sorted((identity for identity, needs in pending.items() if not needs), key=position.__getitem__)
        if not ready:
            raise ContractError("LAYER_CYCLE", "Layer dependencies contain a cycle", sorted(pending))
        chosen = ready[0]
        result.append(chosen)
        del pending[chosen]
        for needs in pending.values():
            needs.discard(chosen)
    return result
