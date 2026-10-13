"""`cinematic` command line: compile, validate and inspect envelopes.

  cinematic compile "<query>" [--genre G] [--duration S] [--until NODE] [--plans DIR] [--packet-out F] [--out F]
  cinematic author "<idea>" --out DIR [--backend replay --replay-from DIR] [--genre G] [--duration S]
  cinematic validate <envelope.json>
  cinematic graph <envelope.json> <group>

Exit codes: 0 ok · 2 contract refusal · 3 an authored step needs a document (packet written) ·
4 a gate failed (replan request written: the step to re-author, its packet and the findings) ·
5 a prompt is not a deliverable (owner O94, R-19): nothing is written; each prompt's checklist counts and the rows
that keep it from being one go to stderr.
`author` (PLAN-008, owner ADR-O112) writes every authored step with a backend and always writes what it made to --out:
envelope.json, the prompts, calls.jsonl (one line per model call) and, when a prompt is not a deliverable,
deliverable.txt with the rows that keep it from being one. Exit 0 when every step passed, 6 when a step was refused
on all its attempts (its findings in refused.json).
"""

import argparse
import json
import sys
from pathlib import Path

from compiler import pipeline, replan_trigger
from compiler.authoring import AuthorRequired, StepFailed
from kernel.canonical import ContractError, canonical_json, load_json
from validators import checklist
from validators.envelope_validator import validate_envelope


def _write(text, path):
    if path:
        Path(path).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def _compile(args):
    plans = {}
    if args.plans:
        plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(args.plans).glob("*.json"))}
    duration = int(args.duration) if args.duration is not None and float(args.duration).is_integer() else args.duration
    query = Path(args.query[1:]).read_text(encoding="utf-8").strip() if args.query.startswith("@") else args.query
    previous = json.loads(Path(args.chain_from).read_text(encoding="utf-8")) if args.chain_from else None
    try:
        envelope = pipeline.run(query, genre=args.genre, duration_s=duration, until=args.until, plans=plans,
                                load_bearing=args.load_bearing, stamp=args.stamp, previous=previous)
    except AuthorRequired as needed:
        _write(canonical_json(needed.packet), args.packet_out)
        print(f"{needed.step_id} needs an authored document; packet written", file=sys.stderr)
        return 3
    except StepFailed as error:
        order = pipeline.load()
        node = next(n["id"] for n in order["nodes"] if n["step_id"] == error.step_id)
        target = replan_trigger.owning_step(node, args.genre)
        attempt = plans.get(target, {}).get("attempt", 1)
        before = pipeline.run(query, genre=args.genre, duration_s=duration, until=_previous(target), plans=plans,
                              previous=previous)
        try:
            replan = replan_trigger.request(error, failed_node=node, attempt=attempt, prepare=pipeline.AUTHORED[target].prepare,
                                            envelope_before=before, genre=args.genre)
        except ContractError as exhausted:
            print(f"stopped: {exhausted}", file=sys.stderr)
            return 2
        _write(canonical_json(replan), args.packet_out)
        print(f"gate failed at {replan['failed_step_id']}; re-author {replan['step_id']} (attempt {replan['attempt']})",
              file=sys.stderr)
        return 4
    except ContractError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    if "render" in envelope["nodes"]:
        refused = checklist.refusals(envelope)  # owner O94: every emitted prompt is a deliverable (R-19)
        if refused:
            print("refused: " + "\n".join(refused), file=sys.stderr)
            return 5
    _write(canonical_json(envelope), args.out)
    return 0


def _author(args):
    from compiler import author

    query = Path(args.query[1:]).read_text(encoding="utf-8").strip() if args.query.startswith("@") else args.query
    if args.backend == "replay":
        backend = author.Replay(args.replay_from)
    elif args.backend == "claude-cli":  # AA-2: the owner's Claude subscription
        from planner.intent_parser import parse_intent
        backend = author.ClaudeCLI(args.genre or parse_intent(query)["parsed"]["genre"])
    else:
        print(f"no backend named {args.backend} (replay, claude-cli)", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    duration = int(args.duration) if args.duration is not None and float(args.duration).is_integer() else args.duration
    try:
        progress = (out / "progress.log").open("w", encoding="utf-8")

        def say(line):
            progress.write(line + "\n")
            progress.flush()
        envelope, calls = author.author(query, backend, genre=args.genre, duration_s=duration, progress=say)
    except author.BackendError as failed:
        print(f"stopped: {failed} ({failed.path})", file=sys.stderr)
        return 7
    except author.AuthorFailed as stopped:
        (out / "calls.jsonl").write_text("".join(json.dumps(c) + "\n" for c in stopped.calls), encoding="utf-8")
        (out / "refused.json").write_text(canonical_json({"node": stopped.node, "findings": stopped.findings}), encoding="utf-8")
        print(f"stopped: {stopped}", file=sys.stderr)
        return 6
    (out / "calls.jsonl").write_text("".join(json.dumps(c) + "\n" for c in calls), encoding="utf-8")
    (out / "envelope.json").write_text(canonical_json(envelope), encoding="utf-8")
    texts = {"render.txt": checklist.render_text(envelope), **checklist.prose_texts(envelope)}
    for name, text in texts.items():
        (out / name).write_text(text, encoding="utf-8")
    refused = checklist.refusals(envelope)
    if refused:
        (out / "deliverable.txt").write_text("\n".join(refused) + "\n", encoding="utf-8")
    cost = sum(c.get("cost_usd") or 0 for c in calls)
    print(f"{len(calls)} calls, ${cost:.2f}; prompts in {out}", file=sys.stderr)
    return 0


def _previous(node):
    order = pipeline.load()
    sequence = pipeline.sequence_for(order, None)
    return sequence[sequence.index(node) - 1]


def _validate(args):
    envelope = load_json(Path(args.envelope).read_text(encoding="utf-8"))
    report = validate_envelope(envelope)
    sys.stdout.write(canonical_json(report))
    return 0 if report["ok"] else 1


def _graph(args):
    envelope = load_json(Path(args.envelope).read_text(encoding="utf-8"))
    for kind in ("nodes", "edges"):
        if args.group in envelope.get(kind, {}):
            sys.stdout.write(canonical_json({"kind": kind, "group": args.group, **envelope[kind][args.group]}))
            return 0
    print(f"no group named {args.group}", file=sys.stderr)
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cinematic")
    sub = parser.add_subparsers(dest="command", required=True)
    comp = sub.add_parser("compile")
    comp.add_argument("query", help="query text, or @file")
    comp.add_argument("--genre")
    comp.add_argument("--duration", type=float)
    comp.add_argument("--until", default="contact")
    comp.add_argument("--plans")
    comp.add_argument("--packet-out")
    comp.add_argument("--out")
    comp.add_argument("--chain-from", help="previous clip's envelope.json; this clip continues it")
    comp.add_argument("--load-bearing", action="store_true")
    comp.add_argument("--stamp", action="store_true")
    aut = sub.add_parser("author")
    aut.add_argument("query", help="the idea, or @file")
    aut.add_argument("--out", required=True)
    aut.add_argument("--backend", default="replay")
    aut.add_argument("--replay-from", help="replay: a folder of committed plans")
    aut.add_argument("--genre")
    aut.add_argument("--duration", type=float)
    val = sub.add_parser("validate")
    val.add_argument("envelope")
    gra = sub.add_parser("graph")
    gra.add_argument("envelope")
    gra.add_argument("group")
    args = parser.parse_args(argv)
    return {"compile": _compile, "author": _author, "validate": _validate, "graph": _graph}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
