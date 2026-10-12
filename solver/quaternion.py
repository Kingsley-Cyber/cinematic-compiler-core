"""Rotations under the kernel convention: Euler degrees, intrinsic XYZ, right-handed (+Y up, facing +Z).

Intrinsic X then Y then Z composes as R = Rx(a) · Ry(b) · Rz(c) acting on column vectors.
+X pitches forward (nose down), +Y yaws left, +Z rolls clockwise (right shoulder down).
"""

import math
from functools import lru_cache


def _rx(a):
    c, s = math.cos(a), math.sin(a)
    return ((1, 0, 0), (0, c, -s), (0, s, c))


def _ry(a):
    c, s = math.cos(a), math.sin(a)
    return ((c, 0, s), (0, 1, 0), (-s, 0, c))


def _rz(a):
    c, s = math.cos(a), math.sin(a)
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))


def _mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def matrix(rot):
    return _matrix(*rot)


@lru_cache(maxsize=1 << 16)
def _matrix(a, b, c):
    """The rotation of one Euler triple, kept: a pose's chains turn by the same root and spine many times, and a solve
    re-poses the same unmoved joints at every trial (RV-59b)."""
    a, b, c = (math.radians(v) for v in (a, b, c))
    return _mul(_mul(_rx(a), _ry(b)), _rz(c))


def apply(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def quaternion(rot):
    """[w, x, y, z], w >= 0, rounded to 9 places."""
    return [round(v, 9) + 0.0 for v in _unit_quaternion(rot)]


def unit_quaternion(rot):
    """[w, x, y, z], w >= 0, unrounded: what a slerp and its read-back need (solver/interpolation.py), since rounding
    to 9 places blurs an angle at Y = +-90 degrees."""
    return list(_unit_quaternion(rot))


def _unit_quaternion(rot):
    m = matrix(rot)
    trace = m[0][0] + m[1][1] + m[2][2]
    if trace > 0:
        s = math.sqrt(trace + 1.0) * 2
        q = (0.25 * s, (m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s)
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2
        q = ((m[2][1] - m[1][2]) / s, 0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s)
    elif m[1][1] > m[2][2]:
        s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2
        q = ((m[0][2] - m[2][0]) / s, (m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s)
    else:
        s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2
        q = ((m[1][0] - m[0][1]) / s, (m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s)
    return tuple(-v for v in q) if q[0] < 0 else q


def uprightness(rot):
    """y-component of the rotated up axis: 1 upright, 0 sideways, -1 inverted."""
    return apply(matrix(rot), (0, 1, 0))[1]


def heading_degrees(vector):
    """World heading of a direction's horizontal part, degrees from +Z toward +X (performer's left)."""
    return math.degrees(math.atan2(vector[0], vector[2]))


def root_heading(rot):
    """Heading of the rotated forward axis (+Z) projected on the ground."""
    return heading_degrees(apply(matrix(rot), (0, 0, 1)))


def angle_between(a, b):
    return abs((a - b + 180) % 360 - 180)


def lateral_heading(rot):
    """Heading of (rotated lateral axis +X) x world up: unchanged by a flip about X, so it survives inversion."""
    lateral = apply(matrix(rot), (1, 0, 0))
    return heading_degrees((-lateral[2], 0, lateral[0]))


def horizontal(vector):
    return math.hypot(vector[0], vector[2])


def arc_degrees(rot1, rot2):
    """Shortest-arc angle between two orientations (what a slerp would sweep); stable near zero."""
    q1, q2 = _unit_quaternion(rot1), _unit_quaternion(rot2)
    if sum(a * b for a, b in zip(q1, q2, strict=True)) < 0:
        q2 = tuple(-v for v in q2)
    apart = math.sqrt(sum((a - b) ** 2 for a, b in zip(q1, q2, strict=True)))
    together = math.sqrt(sum((a + b) ** 2 for a, b in zip(q1, q2, strict=True)))
    return round(math.degrees(4 * math.atan2(apart, together)), 6) + 0.0


SUPPORTED = {"euler_order": "XYZ", "kind": "intrinsic", "handedness": "right", "units": "degrees"}


def require(convention):
    """This module implements one convention; refuse any other instead of silently reinterpreting angles."""
    from kernel.canonical import ContractError

    wrong = {k: convention.get(k) for k, v in SUPPORTED.items() if convention.get(k) != v}
    if wrong:
        raise ContractError("ROTATION_CONVENTION", "solver/quaternion.py implements intrinsic XYZ, right-handed, degrees",
                            wrong)


FACE_LEVEL = 0.2  # interpretation (Claude's, for owner review): a face this close to vertical has no heading of its own


def head_heading(key):
    """Heading of the face (owner O76, rule R-34): the forward axis through the whole chain, root, Sp, NK and HD. A face
    pointing almost straight up or down (a body on its back) has no horizontal heading, so it reads as the root's
    heading plus the neck and head yaw."""
    face = (0.0, 0.0, 1.0)
    for joint in ("HD", "NK", "Sp"):
        face = apply(matrix(key["bones"][joint]), face)
    face = apply(matrix(key["rot"]), face)
    if horizontal(face) >= FACE_LEVEL:
        heading = heading_degrees(face)
    else:
        heading = root_heading(key["rot"]) + key["bones"]["NK"][1] + key["bones"]["HD"][1]
    return round((heading + 180) % 360 - 180, 3) + 0.0
