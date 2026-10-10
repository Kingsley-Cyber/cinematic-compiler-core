"""`cinematic` command line: compile, validate and inspect envelopes.

  cinematic compile "<query>" [--genre G] [--duration S] [--until NODE] [--plans DIR] [--packet-out F] [--out F]
  cinematic validate <envelope.json>
  cinematic graph <envelope.json> <group>

Exit codes: 0 ok · 2 contract refusal · 3 an authored step needs a document (packet written) ·
4 a gate failed (replan request written: the step to re-author, its packet and the findings).
"""

import argparse
import json
import sys
from pathlib import Path

from compiler import pipeline, replan_trigger
from compiler.authoring import AuthorRequired, StepFailed
from kernel.canonical import ContractError, canonical_json, load_json
from planner.beat_planner import prepare as prepare_beats
from validators.envelope_validator import validate_envelope

PREPARERS = {"temporal": prepare_beats}


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
    try:
        envelope = pipeline.run(query, genre=args.genre, duration_s=duration, until=args.until, plans=plans,
                                load_bearing=args.load_bearing, stamp=args.stamp)
    except AuthorRequired as needed:
        _write(canonical_json(needed.packet), args.packet_out)
        print(f"{needed.step_id} needs an authored document; packet written", file=sys.stderr)
        return 3
    except StepFailed as error:
        order = pipeline.load()
        node = next(n["id"] for n in order["nodes"] if n["step_id"] == error.step_id)
        target = replan_trigger.owning_step(node, args.genre)
        attempt = plans.get(target, {}).get("attempt", 1)
        before = pipeline.run(query, genre=args.genre, duration_s=duration, until=_previous(target), plans=plans)
        try:
            replan = replan_trigger.request(error, failed_node=node, attempt=attempt, prepare=PREPARERS[target],
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
    _write(canonical_json(envelope), args.out)
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
    comp.add_argument("--load-bearing", action="store_true")
    comp.add_argument("--stamp", action="store_true")
    val = sub.add_parser("validate")
    val.add_argument("envelope")
    gra = sub.add_parser("graph")
    gra.add_argument("envelope")
    gra.add_argument("group")
    args = parser.parse_args(argv)
    return {"compile": _compile, "validate": _validate, "graph": _graph}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
