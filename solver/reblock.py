"""The re-block solver (RV-35a, F-127): the least change to a key's joints that meets stated goals, in plain Python.

A re-block moves some joints of one key so that named body points meet their goals: a point (a hand at a prop's
sample), a height (a sole on the floor) or a floor under a point (a head kept above a height). Everything else holds:
only the listed joint components move, each inside its bounds (the genre's joint limits and the move's own bounds,
such as a trunk lean that is no crawl). The solver minimises the sum of the squared degree changes plus a heavy
penalty for each goal's miss, by a deterministic pattern search over the free components (steps from 16 down to
0.125 degrees), so a recorded re-block can be re-derived from its goals, its free joints and its bounds: run
`python -m solver.reblock <example> <slot> --free Sp.x,RUL.x --goal right_hand=1.4,0,3.77 --goal left_foot.y=0`
(`--above head.y=0.9` keeps a point at or over a height; `--bound Sp.x=0..30` narrows a component).
"""

import argparse
import copy
import json
import sys
from pathlib import Path

from solver import forward_kinematics

AXES = "xyz"
GOAL_WEIGHT = 1e8  # per square metre of miss: a millimetre's miss outweighs a degree of change
STEPS = (16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125)


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


def solve(key, metres, goals, free, bounds, above=()):
    """(bones, misses): the bones of `key` with the `free` components ("Sp.x") moved inside `bounds` ({component: (low,
    high)}; a start outside its bounds is first moved into them) by the least squared change that meets `goals`
    ([(part, [x, y, z] or a height)], or with a third item, a weight under 1 for a goal that may give) and keeps every
    `above` point ([(part, height)]) at or over its height; misses is the weighted square of what is left unmet."""
    start = copy.deepcopy(key)
    trial = copy.deepcopy(key)
    origin = {name: key["bones"][_component(name)[0]][_component(name)[1]] for name in free}

    def cost(state):
        for name, value in state.items():
            joint, axis = _component(name)
            trial["bones"][joint][axis] = value
        change = sum((state[name] - origin[name]) ** 2 for name in free)
        return change + GOAL_WEIGHT * _misses(trial, metres, goals, above)

    state = {name: min(bounds.get(name, (-360.0, 360.0))[1], max(bounds.get(name, (-360.0, 360.0))[0], value))
             for name, value in origin.items()}
    best = cost(state)
    for step in STEPS:
        improved = True
        while improved:
            improved = False
            for name in free:
                low, high = bounds.get(name, (-360.0, 360.0))
                for sign in (1, -1):
                    value = round(min(high, max(low, state[name] + sign * step)), 3)
                    if value == state[name]:
                        continue
                    candidate = {**state, name: value}
                    score = cost(candidate)
                    if score < best - 1e-12:
                        state, best, improved = candidate, score, True
                        break
    cost(state)
    for name, value in state.items():
        joint, axis = _component(name)
        start["bones"][joint][axis] = value + 0.0
    return start["bones"], _misses(start, metres, goals, above)


def _target(text):
    values = [float(v) for v in text.split(",")]
    return values if len(values) == 3 else values[0]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("example")
    parser.add_argument("slot")
    parser.add_argument("--free", required=True, help="comma-separated joint components, e.g. Sp.x,RUL.x")
    parser.add_argument("--goal", action="append", default=[], help="part=x,y,z or part.y=height")
    parser.add_argument("--above", action="append", default=[], help="part.y=height kept at or over")
    parser.add_argument("--bound", action="append", default=[], help="component=low..high")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1] / "examples" / args.example
    plan = json.loads((root / "plans" / "motion.json").read_text(encoding="utf-8"))
    envelope = json.loads((root / "envelope.json").read_text(encoding="utf-8"))
    metres = forward_kinematics.segments(envelope["scene"]["genre"])
    key = next(k for k in plan["keys"] if k["slot"] == args.slot)
    goals = [(part.removesuffix(".y"), _target(value)) for part, value in (g.split("=") for g in args.goal)]
    above = [(part.removesuffix(".y"), float(value)) for part, value in (g.split("=") for g in args.above)]
    bounds = {name: tuple(float(v) for v in span.split("..")) for name, span in (b.split("=") for b in args.bound)}
    bones, misses = solve(key, metres, goals, args.free.split(","), bounds, above)
    json.dump({"slot": args.slot, "bones": bones, "misses_m2": round(misses, 6)}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
