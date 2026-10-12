"""Poses between keys (RV-59; F-159, F-089): an entity's body at any instant between two of its S13 keys, as the source
declares the motion: "Use slerp on all joint rotations. Root positions are exact."

Every joint's local rotation is slerped between its two keys; the root's position runs straight from key to key (it is
exact only at the keys); the root's rotation is slerped too, unless the earlier key declares a turn (a flip, a spin or a
cartwheel) of a half turn or more about its own axis (X, Y or Z), when its Euler angles run straight from key to key
along the turn, as the S13 edge's `euler_axis` says: a shortest-arc slerp would undo it. A declared turn under a half
turn is slerped, the shortest arc being that turn (RV-108, F-225).
`frames` gives every frame of the scene strictly between an entity's consecutive keys, leaving out a vanished body's
window (owner O18: it is gone). Interpretation (Claude's, for owner review): the straight root path. An in-between key
(ADR-O109, RV-59f) stands in its entity's sequence like a key and carries the turn of the key before it, so the
declared interpolation runs through it (`sequences`, `envelope_keys`).
"""

import math
from functools import lru_cache

from solver.quaternion import unit_quaternion
from solver.staff_geometry import TURNS

EPSILON = 1e-9
HALF_TURN = 180.0
LOCK = 1e-10  # |sin Y| within this of 1: Y is +-90 degrees, where the X and Z turns share one axis


def _slerp(q0, q1, s):
    dot = sum(a * b for a, b in zip(q0, q1, strict=True))
    if dot < 0:
        q1, dot = [-v for v in q1], -dot
    if dot > 0.9995:
        q = [a + s * (b - a) for a, b in zip(q0, q1, strict=True)]
    else:
        theta = math.acos(min(1.0, dot))
        q = [(math.sin((1 - s) * theta) * a + math.sin(s * theta) * b) / math.sin(theta) for a, b in zip(q0, q1, strict=True)]
    norm = math.sqrt(sum(v * v for v in q))
    return [v / norm for v in q]


def euler(q):
    """Euler degrees, intrinsic XYZ (R = Rx Ry Rz, the kernel convention), of a unit quaternion [w, x, y, z]. At Y = +-90
    degrees (gimbal lock) the X and Z turns share one axis and only their sum (Y = 90) or difference (Y = -90) is
    known; the whole of it is read as X and Z as 0, so the rotation is kept."""
    w, x, y, z = q
    r02 = 2 * (x * z + w * y)
    if abs(r02) > 1 - LOCK:
        sign = 1.0 if r02 > 0 else -1.0
        r10, r11 = 2 * (x * y + w * z), 1 - 2 * (x * x + z * z)
        return [math.degrees(math.atan2(sign * r10, r11)), 90.0 * sign, 0.0]
    r12, r22 = 2 * (y * z - w * x), 1 - 2 * (x * x + y * y)
    r01, r00 = 2 * (x * y - w * z), 1 - 2 * (y * y + z * z)
    return [math.degrees(math.atan2(-r12, r22)), math.degrees(math.asin(r02)), math.degrees(math.atan2(-r01, r00))]


@lru_cache(maxsize=1 << 16)
def _between(a, b, s):
    """The slerp of one joint's rotation, as Euler degrees, kept: a re-block re-poses its unmoved joints at every trial."""
    return tuple(euler(_slerp(unit_quaternion(a), unit_quaternion(b), s)))


def straight(a, b):
    """Whether the root's Euler angles run straight from key a to key b: a declared turn of a half turn or more about its
    own axis, which a shortest-arc slerp would undo (RV-108)."""
    turn = a.get("turn", "none")
    return turn != "none" and abs(b["rot"][TURNS[turn][0]] - a["rot"][TURNS[turn][0]]) >= HALF_TURN - EPSILON


def pose(a, b, t):
    """{pos, rot, bones, turn}: the pose of one entity at instant t between its keys a and b (a["t"] <= t <= b["t"])."""
    s = (t - a["t"]) / (b["t"] - a["t"]) if b["t"] > a["t"] + EPSILON else 0.0
    pos = [pa + s * (pb - pa) for pa, pb in zip(a["pos"], b["pos"], strict=True)]
    turn = a.get("turn", "none")
    if straight(a, b):  # the edge's euler_axis: the declared turn's angles run straight
        rot = [ra + s * (rb - ra) for ra, rb in zip(a["rot"], b["rot"], strict=True)]
    else:
        rot = list(_between(tuple(a["rot"]), tuple(b["rot"]), s))
    bones = {joint: list(_between(tuple(a["bones"][joint]), tuple(b["bones"][joint]), s)) for joint in a["bones"]}
    return {"pos": pos, "rot": rot, "bones": bones, "turn": turn}


def frames(keys, fps, gone=()):
    """{(entity, t): pose} at every frame strictly between an entity's consecutive keys (keys: {entity: [key, ...]}
    sorted by t), leaving out each vanished window ((entity, start, back) with back None for one that never returns)."""
    out = {}
    for entity, own in keys.items():
        for a, b in zip(own, own[1:], strict=False):
            first, last = math.floor(a["t"] * fps + EPSILON) + 1, math.ceil(b["t"] * fps - EPSILON) - 1
            for frame in range(first, last + 1):
                t = round(frame / fps, 6)
                if any(e == entity and start - EPSILON <= t and (back is None or t < back - EPSILON) for e, start, back in gone):
                    continue
                out[(entity, t)] = pose(a, b, t)
    return out


def sequences(keys, inbetweens=()):
    """{entity: [key, ...] in time order}: the keys ({entity: [key with t]}) joined by the in-betweens (ADR-O109), each
    carrying the turn of the key before it."""
    out = {entity: list(own) for entity, own in keys.items()}
    for between in inbetweens:
        own = out.setdefault(between["entity"], [])
        before = max((k for k in keys.get(between["entity"], []) if k["t"] < between["t"]), key=lambda k: k["t"], default=None)
        own.append({**between, "turn": before.get("turn", "none") if before else "none"})
    return {entity: sorted(own, key=lambda k: k["t"]) for entity, own in out.items()}


def envelope_keys(envelope):
    """{entity: [key, ...] in time order} from S13's graph: its keys and the in-betweens its follows edges carry."""
    keys = {}
    for key in envelope["nodes"]["motion"]["items"]:
        keys.setdefault(key["entity"], []).append(key)
    inbetweens = [between for edge in envelope.get("edges", {}).get("motion", {}).get("items", [])
                  for between in edge.get("inbetweens", [])]
    return sequences(keys, inbetweens)

