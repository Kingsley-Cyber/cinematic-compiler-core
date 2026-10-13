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


class BackendError(ContractError):
    """The backend could not return a document (the model or its CLI failed, not the checks)."""

    def __init__(self, node, detail):
        super().__init__("BACKEND_FAILED", f"the backend wrote no document for {node}", detail)


ROOT = Path(__file__).resolve().parents[1]
GUIDES = {"anime": "wizard_vs_acrobat", "live_action": "live_action_standoff", "ugc_ad": "ugc_glasses_demo"}
FRONTIER = ("temporal", "motion", "effort", "camera")  # the creative steps (PLAN-008)
FILLED = ("step_id", "band", "packet_sha256", "author", "attempt")  # the author sets these; the model never copies them
ENV = ("HOME", "PATH", "USER", "LOGNAME", "SHELL", "TMPDIR", "LANG")


def _schema(node):
    """The step's document schema without the fields the author fills."""
    schema = json.loads(pipeline.AUTHORED[node].PLAN_SCHEMA.read_text(encoding="utf-8"))
    schema["required"] = [f for f in schema.get("required", []) if f not in FILLED]
    schema["properties"] = {k: v for k, v in schema.get("properties", {}).items() if k not in FILLED}
    for key in ("$schema", "$id"):
        schema.pop(key, None)
    return schema


class ClaudeCLI:
    """The subscription backend (AA-2, owner's choice 2026-10-12): one `claude -p` call per step on the owner's Claude
    login, no per-call bill. Isolated: an empty working folder, an allowlisted environment, no tools, no settings,
    hooks, skills, MCP or memory (--safe-mode, --setting-sources project, --strict-mcp-config), no session kept. The
    model reads the step's packet (its instructions are the brief), the step's schema, and one document of the same
    step that passed in an example of the scene's genre (its shape, not its content); a retry adds the refused
    document and the findings. The frontier model writes the creative steps, a faster one the rest."""

    name = "claude-cli"

    def __init__(self, genre, frontier="claude-opus-5-5", other="claude-sonnet-5-5", timeout_s=1800):
        self.genre, self.frontier, self.other, self.timeout_s = genre, frontier, other, timeout_s
        self.previous = {}

    def _guide(self, node):
        path = ROOT / "examples" / GUIDES.get(self.genre, "wizard_vs_acrobat") / "plans" / f"{node}.json"
        if not path.exists():
            path = next((ROOT / "examples").glob(f"*/plans/{node}.json"), None)
        if path is None:
            return None
        return {k: v for k, v in json.loads(path.read_text(encoding="utf-8")).items() if k not in FILLED}

    def write(self, node, step_id, packet, findings=None):
        import os
        import subprocess
        import tempfile

        model = self.frontier if node in FRONTIER else self.other
        parts = [f"STEP {step_id} ({node}). THE PACKET (its `instructions` are your brief; follow them exactly):",
                 canonical_json(packet)]
        guide = self._guide(node)
        if guide is not None:
            parts += ["A DOCUMENT FOR THIS STEP THAT PASSED IN ANOTHER SCENE (its shape and level of detail, not its "
                      "content; write yours for this packet's slots):", canonical_json(guide)]
        if findings:
            parts += ["YOUR PREVIOUS DOCUMENT:", canonical_json(self.previous.get(node, {})),
                      "THE STEP'S CHECKS REFUSED IT FOR THESE FINDINGS. Fix every one and return the whole document:",
                      canonical_json(findings)]
        system = ("You author one step of a cinematic compiler. Write the step's document for the packet you are given, "
                  "exactly as its instructions say, as JSON matching the schema. Return only the document.")
        env = {k: os.environ[k] for k in ENV if k in os.environ}
        argv = ["claude", "-p", "--output-format", "json", "--json-schema", json.dumps(_schema(node)),
                "--system-prompt", system, "--tools", "", "--safe-mode", "--setting-sources", "project",
                "--strict-mcp-config", "--no-session-persistence", "--model", model]
        detail = None
        for _ in range(2):  # one more try when the CLI itself fails
            with tempfile.TemporaryDirectory() as folder:
                try:
                    done = subprocess.run(argv, input="\n\n".join(parts), capture_output=True, text=True, cwd=folder,
                                          env=env, timeout=self.timeout_s)
                except subprocess.TimeoutExpired:
                    detail = f"timed out after {self.timeout_s} s"
                    continue
            try:
                reply = json.loads(done.stdout)
            except json.JSONDecodeError:
                detail = (done.stderr or done.stdout)[-500:]
                continue
            document = reply.get("structured_output")
            if reply.get("is_error") or not isinstance(document, dict):
                detail = str(reply.get("result"))[-500:]
                continue
            usage = reply.get("usage", {})
            self.previous[node] = document
            return ({**document, "step_id": packet.get("step_id", step_id), "band": packet.get("band"),
                     "author": {"host": "cinematic author (claude -p, subscription)", "model": model}},
                    {"model": model, "tokens_in": usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
                     + usage.get("cache_read_input_tokens", 0), "tokens_out": usage.get("output_tokens", 0),
                     "cost_usd": 0.0, "list_cost_usd": round(reply.get("total_cost_usd") or 0.0, 4),
                     "billing": "subscription"})
        raise BackendError(node, detail)


def _sequence(query, genre):
    return pipeline.sequence_for(pipeline.load(), genre or parse_intent(query)["parsed"]["genre"])


def author(query, backend, *, genre=None, duration_s=None, until="render", load_bearing=False, progress=None):
    """(envelope, calls): the compiled envelope with every authored step written by `backend`, and the call log;
    `progress(line)`, when given, hears each call as it returns and each refusal."""
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
        if progress:
            progress(f"{index[node]['step_id']} {node} refused: " + ", ".join(sorted({f.get('code', '?') for f in findings})))
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
        if progress:
            progress(f"{index[node]['step_id']} {node} attempt {attempts[node]} written by {usage.get('model')} in "
                     f"{calls[-1]['duration_s']:.0f} s")
