"""The automatic author (PLAN-008, owner ADR-O112): an idea in, a prompt out.

`author(query, backend)` runs the pipeline. At each authored step it hands the step's sealed packet to the backend
(one call per step; the packet, with its instructions, is the prompt), binds the returned document to the packet,
and lets the step's own checks judge it. A refusal goes back to the step that can fix it (compiler/replan_trigger.py:
a derived step's failure to the nearest authored step upstream) with its findings, and every document written after
that step is dropped, since it was sealed to a packet that may change. Each step has its first attempt and two more
(replan_trigger.MAX_ATTEMPTS); a third refusal stops the run with AuthorFailed, naming the step and its findings.
Every call is logged: the step, the backend and model, the attempt, its size, tokens and cost, its time and whether
the checks passed it.

A backend has `name` and `write(node, step_id, packet, findings) -> (document, usage)`; `usage` holds model,
tokens_in, tokens_out and cost_usd. `Replay` is the offline backend: an example's committed plans, which proves the
loop without a model (AA-1). Live backends are AA-2 and AA-5.
"""

import json
import time
from pathlib import Path

from compiler import pipeline, replan_trigger
from compiler.authoring import AuthorRequired, GateFailed, StepFailed
from kernel.canonical import ContractError, canonical_json
from planner.dependency_graph import node_index
from planner.intent_parser import parse_intent


class AuthorFailed(ContractError):
    """A step was refused on every attempt; `node`, `findings` and `calls` say where and why."""

    def __init__(self, node, findings, calls):
        super().__init__("AUTHOR_FAILED", f"{node} was refused on all {replan_trigger.MAX_ATTEMPTS} attempts", findings)
        self.node, self.findings, self.calls = node, findings, calls


class Replay:
    """The offline backend (AA-1): an example's committed plans, written back as they are."""

    name = "replay"

    def __init__(self, folder):
        self.plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(folder).glob("*.json"))}

    def write(self, node, step_id, packet, findings=None):
        return dict(self.plans[node]), {"model": "replay", "tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0}


def _sequence(query, genre):
    return pipeline.sequence_for(pipeline.load(), genre or parse_intent(query)["parsed"]["genre"])


def author(query, backend, *, genre=None, duration_s=None, until="render", load_bearing=False):
    """(envelope, calls): the compiled envelope with every authored step written by `backend`, and the call log."""
    order = pipeline.load()
    index = node_index(order)
    node_of = {spec["step_id"]: node for node, spec in index.items()}
    sequence = _sequence(query, genre)
    resolved = genre or parse_intent(query)["parsed"]["genre"]
    plans, attempts, calls, last = {}, {}, [], None

    def run(target):
        return pipeline.run(query, genre=genre, duration_s=duration_s, until=target, plans=plans,
                            load_bearing=load_bearing)

    def refuse(node, findings):
        for call in reversed(calls):
            if call["node"] == node:
                call.update(result="refused", findings=[f.get("code", "?") for f in findings])
                break
        if attempts.get(node, 0) >= replan_trigger.MAX_ATTEMPTS:
            raise AuthorFailed(node, findings, calls)

    while True:
        try:
            envelope = run(until)
        except AuthorRequired as needed:
            node, packet, findings = node_of[needed.step_id], needed.packet, None
        except StepFailed as failed:  # an authored step's gate (GateFailed) or a derived step's check
            node = replan_trigger.owning_step(node_of[failed.step_id], resolved)
            findings = failed.findings
            refuse(node, findings)
            own = isinstance(failed, GateFailed) and node_of[failed.step_id] == node
            packet = failed.packet if own else pipeline.AUTHORED[node].prepare(run(sequence[sequence.index(node) - 1]))
        except ContractError as error:  # a document the schema or the packet binding refuses: the step just written
            if last is None:
                raise
            node, findings = last, [{"code": error.code, "message": str(error)}]
            refuse(node, findings)
            packet = pipeline.AUTHORED[node].prepare(run(sequence[sequence.index(node) - 1]))
        else:
            for call in calls:
                call.setdefault("result", "passed")
            return envelope, calls
        for later in sequence[sequence.index(node) + 1:]:
            if plans.pop(later, None) is not None:  # written for a packet this step may change
                next(c for c in reversed(calls) if c["node"] == later).setdefault("result", "dropped")
        attempts[node] = attempts.get(node, 0) + 1
        started = time.perf_counter()
        document, usage = backend.write(node, index[node]["step_id"], packet, findings)
        plans[node] = {**document, "packet_sha256": packet["packet_sha256"], "attempt": attempts[node]}
        last = node
        calls.append({"step_id": index[node]["step_id"], "node": node, "attempt": attempts[node],
                      "backend": backend.name, **usage, "input_chars": len(canonical_json(packet)),
                      "output_chars": len(canonical_json(plans[node])),
                      "duration_s": round(time.perf_counter() - started, 3)})
