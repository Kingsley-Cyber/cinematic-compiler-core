"""The re-block solver (RV-35a, RV-96; F-127, F-207): the least change to a key's joints that meets stated goals, in
plain Python, re-derivable from its record.

A re-block moves some joints of one key so that named body points meet their goals: a point (a hand at a prop's
sample) or a height (a sole on the floor), each with an optional weight under 1 for a goal that may give (a sole's
place); `above` floors keep a point at or over a height (a knee off the floor). Only the listed joint components move,
inside the genre's joint limits (library/joint_limits.yaml, widened for anime: owner O11), narrowed by any stated
bound; a sum limit (NK+HD) is not enforced, so the neck and the head are not freed together. The cost is the sum of
the squared degree changes plus GOAL_WEIGHT per square metre of weighted miss. The search is a deterministic steepest
descent: at each step size, from 16 down to 0.125 degrees, it takes the best of every free component's two moves (ties
broken by the components' sorted names) until no move improves, so the order the caller lists them in cannot change
the answer. A recorded re-block is re-derived by its command, which the CLI prints with its result:
`python -m solver.reblock <example> <slot> --from <git revision> --root-y 0.4 --free Sp.x,RUL.x
--goal right_hand=1.4,0,3.77 --goal left_foot.y=0 --goal left_foot=0.46,0,3.54@0.01 --above head.y=0.65
--bound Sp.x=-30..45`.
"""

import argparse
import copy
import json
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

from solver import forward_kinematics
from solver.euler_solver import effective_limits

ROOT = Path(__file__).resolve().parents[1]
AXES = "xyz"
GOAL_WEIGHT = 1e8  # per square metre of miss: a millimetre's miss outweighs a degree of change
STEPS = (16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125)
OPEN = (-360.0, 360.0)


def limits(genre):
    """{"LUL.x": (low, high)}: each single joint's axis limit for the genre (owner O11); sums such as NK+HD are left out."""
    card = yaml.safe_load((ROOT / "library" / "joint_limits.yaml").read_text(encoding="utf-8"))
    return {f"{joint}.{axis}": tuple(float(v) for v in bounds)
            for joint, row in effective_limits(card, genre).items() if "+" not in joint for axis, bounds in row.items()}


def _component(name):
    joint, axis = name.split(".")
    return joint, AXES.index(axis)


def _misses(key, metres, goals, above):
    points = forward_kinematics.points(key, metres)
    total = 0.0
    for part, target, *weight in goals:
        point = forward_kinematics.part_point(points, part)
        if isinstance(target, (int, float)):  # a height
            miss = (point[1] - target) ** 2
        else:
            miss = sum((a - b) ** 2 for a, b in zip(point, target, strict=True))
        total += miss * (weight[0] if weight else 1.0)
    for part, floor in above:
        total += max(0.0, floor - forward_kinematics.part_point(points, part)[1]) ** 2
    return total


def solve(key, metres, goals, free, bounds=None, above=(), joint_limits=None):
    """(bones, misses): the bones of `key` with the `free` components ("Sp.x") moved, inside `joint_limits` (from
    `limits`) narrowed by `bounds` ({component: (low, high)}; a start outside its span is first moved into it), by the
    least squared change that meets `goals` ([(part, [x, y, z] or a height[, weight])]) and keeps every `above` point
    ([(part, height)]) at or over its height; misses is the weighted square of what is left unmet."""
    free = sorted(set(free))
    span = {}
    for name in free:
        low, high = (joint_limits or {}).get(name, OPEN)
        stated = (bounds or {}).get(name, OPEN)
        span[name] = (max(low, stated[0]), min(high, stated[1]))
    origin = {name: key["bones"][_component(name)[0]][_component(name)[1]] for name in free}
    trial = copy.deepcopy(key)

    def cost(state):
        for name, value in state.items():
            joint, axis = _component(name)
            trial["bones"][joint][axis] = value
        change = sum((state[name] - origin[name]) ** 2 for name in free)
        return change + GOAL_WEIGHT * _misses(trial, metres, goals, above)

    state = {name: min(span[name][1], max(span[name][0], value)) for name, value in origin.items()}
    best = cost(state)
    for step in STEPS:
        while True:
            moves = []
            for name in free:
                low, high = span[name]
                for sign in (1, -1):
                    value = round(min(high, max(low, state[name] + sign * step)), 3)
                    if value != state[name]:
                        moves.append((cost({**state, name: value}), name, -sign, value))
            if not moves:
                break
            score, name, _, value = min(moves)
            if score >= best - 1e-12:
                break
            state, best = {**state, name: value}, score
    result = copy.deepcopy(key)
    for name, value in state.items():
        joint, axis = _component(name)
        result["bones"][joint][axis] = value + 0.0
    return result["bones"], _misses(result, metres, goals, above)


def _goal(text):
    """'part=x,y,z@w' or 'part.y=h@w' as (part, target[, weight])."""
    part, value = text.split("=", 1)
    value, _, weight = value.partition("@")
    values = [float(v) for v in value.split(",")]
    goal = (part.removesuffix(".y"), values if len(values) == 3 else values[0])
    return (*goal, float(weight)) if weight else goal


def _plan(example, revision=None, path=None):
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    relative = f"examples/{example}/plans/motion.json"
    if revision:
        return json.loads(subprocess.run(["git", "-C", str(ROOT), "show", f"{revision}:{relative}"], capture_output=True,
                                         text=True, check=True).stdout)
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("example")
    parser.add_argument("slot")
    parser.add_argument("--from", dest="revision", help="the git revision whose motion plan holds the start key")
    parser.add_argument("--plan", help="a motion plan file holding the start key (instead of --from)")
    parser.add_argument("--root-y", type=float, help="the start key's root height, when the re-block moves it")
    parser.add_argument("--free", required=True, help="comma-separated joint components, e.g. Sp.x,RUL.x")
    parser.add_argument("--goal", action="append", default=[], help="part=x,y,z or part.y=height, with @weight")
    parser.add_argument("--above", action="append", default=[], help="part.y=height kept at or over")
    parser.add_argument("--bound", action="append", default=[], help="component=low..high")
    args = parser.parse_args(argv)
    plan = _plan(args.example, args.revision, args.plan)
    envelope = json.loads((ROOT / "examples" / args.example / "envelope.json").read_text(encoding="utf-8"))
    genre = envelope["scene"]["genre"]
    key = copy.deepcopy(next(k for k in plan["keys"] if k["slot"] == args.slot))
    if args.root_y is not None:
        key["pos"] = [key["pos"][0], args.root_y, key["pos"][2]]
    above = [(part.removesuffix(".y"), float(value)) for part, value in (a.split("=") for a in args.above)]
    bounds = {name: tuple(float(v) for v in span.split("..")) for name, span in (b.split("=") for b in args.bound)}
    bones, misses = solve(key, forward_kinematics.segments(genre), [_goal(g) for g in args.goal], args.free.split(","),
                          bounds, above, limits(genre))
    command = "python -m solver.reblock " + " ".join(shlex.quote(a) for a in (argv if argv is not None else sys.argv[1:]))
    json.dump({"command": command, "slot": args.slot, "pos": key["pos"], "bones": bones, "misses_m2": round(misses, 6)},
              sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
