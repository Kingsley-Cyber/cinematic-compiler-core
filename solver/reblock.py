"""The re-block solver (RV-35a, RV-96; F-127, F-207): the least change to a key's joints that meets stated goals, in
plain Python, re-derivable from its record.

A re-block moves some joints of one key so that named body points meet their goals: a point (a hand at a prop's
sample) or a height (a sole on the floor), each with an optional weight under 1 for a goal that may give (a sole's
place); `above` floors keep a contact point or a joint at or over a height (a knee or an ankle off the floor). Only
the listed joint components move, inside the genre's joint limits (library/joint_limits.yaml, widened for anime: owner
O11), narrowed by any stated bound; a sum limit (NK+HD) is not enforced, so the neck and the head are not freed
together. The cost is the sum of the squared degree changes plus GOAL_WEIGHT per square metre of weighted miss. The
search is a deterministic steepest descent: at each step size, from 16 down to 0.125 degrees, it takes the best of
every free component's two moves (ties broken by the components' sorted names) until no move improves, so the order
the caller lists them in cannot change the answer. A root component (`pos.x`, `pos.z`) moves the key's root, its
change counted in centimetres (a centimetre weighs as a degree) and its bound stated in metres. A clearance goal
(`--clear <entity>`, RV-59b, R-18) keeps the moving body clear of another at the key's instant and at every frame of
its two spans, posed along the declared interpolation (solver/interpolation.py), by CLEARANCE_M between their
capsules' surfaces, and `--floor` keeps its contact points over the floor less FLOOR_PENETRATION's 0.15 m there by
the same margin (RV-59c); their misses count like a goal's.
A recorded re-block is re-derived by its command, which the CLI prints with its result:
`python -m solver.reblock <example> <slot> --from <git revision> --root-y 0.4 --free Sp.x,RUL.x
--goal right_hand=1.4,0,3.77 --goal left_foot.y=0 --goal left_foot=0.46,0,3.54@0.01 --above head.y=0.65
--bound Sp.x=-30..45 --clear ninja_lean`.
"""

import argparse
import copy
import json
import math
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

from planner.dynamic_beat_validator import vanish_windows
from solver import floor_penetration, forward_kinematics, interpolation
from solver.euler_solver import effective_limits
from solver.quaternion import matrix

ROOT = Path(__file__).resolve().parents[1]
AXES = "xyz"
GOAL_WEIGHT = 1e8  # per square metre of miss: a millimetre's miss outweighs a degree of change
STEPS = (16.0, 8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125)
OPEN = (-360.0, 360.0)
CLEARANCE_M = 0.01  # between two bodies' surfaces on a cleared path: room for the angles' rounding (the check allows none)
EPSILON = 1e-9
CENTIMETRES = 100.0  # a root component's change is counted in centimetres
UNBOUND = (-1e9, 1e9)


def _get(key, name):
    joint, axis = _component(name)
    return key["pos"][axis] * CENTIMETRES if joint == "pos" else key["bones"][joint][axis]


def _set(key, name, value):
    joint, axis = _component(name)
    if joint == "pos":
        key["pos"][axis] = round(value / CENTIMETRES, 6) + 0.0
    else:
        key["bones"][joint][axis] = value


def limits(genre):
    """{"LUL.x": (low, high)}: each single joint's axis limit for the genre (owner O11); sums such as NK+HD are left out."""
    card = yaml.safe_load((ROOT / "library" / "joint_limits.yaml").read_text(encoding="utf-8"))
    return {f"{joint}.{axis}": tuple(float(v) for v in bounds)
            for joint, row in effective_limits(card, genre).items() if "+" not in joint for axis, bounds in row.items()}


def _component(name):
    joint, axis = name.split(".")
    return joint, AXES.index(axis)


def _misses(key, metres, goals, above, extra=None):
    points = forward_kinematics.points(key, metres)
    joints = forward_kinematics.joints(key, metres) if any(part not in points for part, _ in above) else {}
    total = 0.0
    for part, target, *weight in goals:
        point = forward_kinematics.part_point(points, part)
        if isinstance(target, (int, float)):  # a height
            miss = (point[1] - target) ** 2
        else:
            miss = sum((a - b) ** 2 for a, b in zip(point, target, strict=True))
        total += miss * (weight[0] if weight else 1.0)
    for part, floor in above:  # a contact point or a joint (an ankle, a knee)
        point = points[part] if part in points else joints.get(part) or forward_kinematics.part_point(points, part)
        total += max(0.0, floor - point[1]) ** 2
    return total + (extra(key) if extra else 0.0)


def _scene_keys(plan, envelope):
    """{entity: [key with its instant t, in time order]} for every key of the plan, timed by the envelope's beats."""
    times = {beat["id"]: beat["t"] for beat in envelope["nodes"]["beats"]["items"]}
    keys = {}
    for key in plan["keys"]:
        entity, beat = key["slot"].split("@")
        keys.setdefault(entity, []).append({**key, "t": times[beat]})
    return {entity: sorted(own, key=lambda k: k["t"]) for entity, own in keys.items()}


def _posed(own, t):
    """An entity's key at instant t, its pose between two of its keys, or None outside its keys."""
    for key in own:
        if abs(key["t"] - t) < EPSILON:
            return key
    before, after = [k for k in own if k["t"] < t], [k for k in own if k["t"] > t]
    return interpolation.pose(before[-1], after[0], t) if before and after else None


def _mm(a, b):
    return tuple(tuple(a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j] for j in range(3)) for i in range(3))


def _from(base, m, vector):
    return [base[i] + m[i][0] * vector[0] + m[i][1] * vector[1] + m[i][2] * vector[2] for i in range(3)]


POINTS = ("pelvis", "torso", "head", "left_knee", "right_knee", "left_sole", "right_sole", "left_elbow", "right_elbow",
          "left_hand", "right_hand")  # forward_kinematics.points: what FLOOR_PENETRATION reads


def _joints(key, metres):
    """forward_kinematics.joints unrounded, and the torso point, each chain's rotations composed once: the clearance's
    inner loop (a test holds the capsules to forward kinematics' on every key of the examples)."""
    bones, pelvis = key["bones"], list(key["pos"])
    root = matrix(key["rot"])
    trunk = _mm(root, matrix(bones["Sp"]))
    at = {"pelvis": pelvis, "chest": _from(pelvis, trunk, (0.0, metres["spine"], 0.0))}
    for side, sign, upper, lower in (("left", 1, "LUL", "LL"), ("right", -1, "RUL", "RL")):
        thigh = _mm(trunk, matrix(bones[upper]))
        shin = _mm(thigh, matrix(bones[lower]))
        at[f"{side}_hip"] = _from(pelvis, root, (sign * metres["hip"], 0.0, 0.0))
        at[f"{side}_knee"] = _from(at[f"{side}_hip"], thigh, (0.0, -metres["thigh"], 0.0))
        at[f"{side}_ankle"] = _from(at[f"{side}_knee"], shin, (0.0, -metres["shin"], 0.0))
        at[f"{side}_sole"] = _from(at[f"{side}_ankle"], shin, (0.0, -metres["ankle"], 0.0))
    for side, sign, upper, lower in (("left", 1, "LA", "LFA"), ("right", -1, "RA", "RFA")):
        arm = _mm(trunk, matrix(bones[upper]))
        at[f"{side}_shoulder"] = _from(at["chest"], trunk, (sign * metres["shoulder"], 0.0, 0.0))
        at[f"{side}_elbow"] = _from(at[f"{side}_shoulder"], arm, (0.0, -metres["upper_arm"], 0.0))
        at[f"{side}_hand"] = _from(at[f"{side}_elbow"], _mm(arm, matrix(bones[lower])), (0.0, -metres["forearm"], 0.0))
    neck = _mm(trunk, matrix(bones["NK"]))
    at["neck"] = _from(at["chest"], neck, (0.0, metres["neck"], 0.0))
    at["head"] = _from(at["neck"], _mm(neck, matrix(bones["HD"])), (0.0, metres["head"], 0.0))
    at["torso"] = _from(pelvis, trunk, (0.0, metres["torso_point"] * metres["spine"], 0.0))
    return at


def _capsules(key, metres, radii, at=None):
    """forward_kinematics.capsules unrounded, from `_joints`."""
    at = at or _joints(key, metres)
    return {name: (at[a], at[b], radii[r]) for name, (a, b, r) in forward_kinematics.CAPSULES.items()}


def _reach(start, end, radius):
    """A capsule's middle and the radius of a ball holding it, to pass over the pairs that cannot meet."""
    return [(a + b) / 2 for a, b in zip(start, end, strict=True)], math.dist(start, end) / 2 + radius


def clearance(plan, envelope, slot, others, margin=CLEARANCE_M, floor=None):
    """f(key) -> square metres, for a trial key of `slot` (RV-59b, R-18): over the key's instant and every frame of its
    two spans (the scene's fps, posed along the declared interpolation, a vanished body left out but a body at its own
    key always in, as S13 judges it), the sum of each overlap's squared depth plus `margin` between the moving body's
    capsules and those of each entity in `others`, and, with a `floor` height (RV-59c), of each contact point's depth
    plus `margin` under the floor less FLOOR_PENETRATION's tolerance."""
    genre, fps = envelope["scene"]["genre"], envelope["scene"]["fps"]
    metres, radii = forward_kinematics.segments(genre), forward_kinematics.radii(genre)
    keys = _scene_keys(plan, envelope)
    gone = [(entity, start, back) for entity, _, start, back in vanish_windows(envelope["nodes"]["beats"]["items"])]
    own = keys[slot.split("@")[0]]
    index = next(n for n, k in enumerate(own) if k["slot"] == slot)
    before, after = own[index - 1] if index else None, own[index + 1] if index + 1 < len(own) else None
    t0 = own[index]["t"]
    low, high = (before or own[index])["t"], (after or own[index])["t"]
    frames = [t0] + [t for t in (round(f / fps, 6) for f in range(math.floor(low * fps), math.ceil(high * fps) + 1))
                     if low + EPSILON < t < high - EPSILON and abs(t - t0) > EPSILON]

    def away(entity, t):
        return any(e == entity and start - EPSILON <= t and (back is None or t < back - EPSILON) for e, start, back in gone)

    # the farthest a capsule's surface reaches from the pelvis: a leg, an arm or the head drawn straight out
    body = max(metres["hip"] + metres["thigh"] + metres["shin"] + metres["ankle"],
                metres["spine"] + metres["shoulder"] + metres["upper_arm"] + metres["forearm"],
                metres["spine"] + metres["neck"] + metres["head"]) + max(radii.values())
    lowest = None if floor is None else floor - floor_penetration.TOLERANCE_M + margin
    fixed = []
    for t in sorted(frames):
        if abs(t - t0) > EPSILON and away(slot.split("@")[0], t):
            continue
        targets = []
        for other in others:
            at_key = any(abs(k["t"] - t) < EPSILON for k in keys[other])
            pose = _posed(keys[other], t) if at_key or not away(other, t) else None
            if pose is not None:
                capsules = _capsules(pose, metres, radii).values()
                targets += [((p, q, r), *_reach(p, q, r)) for p, q, r in capsules]
        if targets:  # a ball holding every capsule of the others, to pass over a frame the body cannot reach
            centre = [sum(target[1][i] for target in targets) / len(targets) for i in range(3)]
            fixed.append((t, targets, centre, max(math.dist(centre, middle) + far for _, middle, far in targets)))
        elif lowest is not None:
            fixed.append((t, [], None, None))

    def cost(key):
        trial, total = {**key, "t": t0}, 0.0
        for t, targets, centre, far in fixed:
            if abs(t - t0) < EPSILON:
                pose = trial
            else:
                pose = interpolation.pose(before, trial, t) if t < t0 else interpolation.pose(trial, after, t)
            at = None
            if lowest is not None:
                at = _joints(pose, metres)
                total += sum(max(0.0, lowest - at[name][1]) ** 2 for name in POINTS)
            if not targets or math.dist(pose["pos"], centre) > body + far + margin:
                continue
            for start, end, radius in _capsules(pose, metres, radii, at).values():
                middle, reach = _reach(start, end, radius)
                for (p, q, r), other_middle, other_reach in targets:
                    if math.dist(middle, other_middle) <= reach + other_reach + margin:
                        depth = radius + r + margin - forward_kinematics.segment_distance(start, end, p, q)
                        if depth > 0:
                            total += depth * depth
        return total

    return cost


def solve(key, metres, goals, free, bounds=None, above=(), joint_limits=None, extra=None):
    """(bones, misses): `solve_key`'s bones."""
    solved, misses = solve_key(key, metres, goals, free, bounds, above, joint_limits, extra)
    return solved["bones"], misses


def solve_key(key, metres, goals, free, bounds=None, above=(), joint_limits=None, extra=None):
    """(key, misses): `key` with the `free` components ("Sp.x", "pos.x") moved, inside `joint_limits` (from `limits`)
    narrowed by `bounds` ({component: (low, high)}, a root component's in metres; a start outside its span is first
    moved into it), by the least squared change that meets `goals` ([(part, [x, y, z] or a height[, weight])]), keeps
    every `above` point ([(part, height)]) at or over its height and leaves `extra` (a function of the key, square
    metres: `clearance`) at zero; misses is the weighted square of what is left unmet."""
    free = sorted(set(free))
    span = {}
    for name in free:
        if _component(name)[0] == "pos":
            stated = (bounds or {}).get(name)
            span[name] = tuple(v * CENTIMETRES for v in stated) if stated else UNBOUND
            continue
        low, high = (joint_limits or {}).get(name, OPEN)
        stated = (bounds or {}).get(name, OPEN)
        span[name] = (max(low, stated[0]), min(high, stated[1]))
    origin = {name: _get(key, name) for name in free}
    trial = copy.deepcopy(key)

    def cost(state):
        for name, value in state.items():
            _set(trial, name, value)
        change = sum((state[name] - origin[name]) ** 2 for name in free)
        return change + GOAL_WEIGHT * _misses(trial, metres, goals, above, extra)

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
        _set(result, name, value + 0.0)
    return result, _misses(result, metres, goals, above, extra)


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
    parser.add_argument("--clear", action="append", default=[], help="an entity kept clear between keys (RV-59b)")
    parser.add_argument("--floor", action="store_true", help="the body kept over the floor between keys (RV-59c)")
    args = parser.parse_args(argv)
    plan = _plan(args.example, args.revision, args.plan)
    envelope = json.loads((ROOT / "examples" / args.example / "envelope.json").read_text(encoding="utf-8"))
    genre = envelope["scene"]["genre"]
    key = copy.deepcopy(next(k for k in plan["keys"] if k["slot"] == args.slot))
    if args.root_y is not None:
        key["pos"] = [key["pos"][0], args.root_y, key["pos"][2]]
    above = [(part.removesuffix(".y"), float(value)) for part, value in (a.split("=") for a in args.above)]
    bounds = {name: tuple(float(v) for v in span.split("..")) for name, span in (b.split("=") for b in args.bound)}
    floor = None
    if args.floor:
        floor = floor_penetration.floor_level(envelope["nodes"]["surfaces"]["items"], envelope["scene"]["ax"].get("ground"))
    extra = clearance(plan, envelope, args.slot, args.clear, floor=floor) if args.clear or floor is not None else None
    solved, misses = solve_key(key, forward_kinematics.segments(genre), [_goal(g) for g in args.goal],
                               args.free.split(","), bounds, above, limits(genre), extra)
    command = "python -m solver.reblock " + " ".join(shlex.quote(a) for a in (argv if argv is not None else sys.argv[1:]))
    json.dump({"command": command, "slot": args.slot, "pos": solved["pos"], "bones": solved["bones"],
               "misses_m2": round(misses, 6)}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
