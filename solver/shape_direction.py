"""SHAPE_DIRECTION (plan F9.1, owner O31, O73, O76): a declared Shape quality against the body's motion.

An Effort interval runs from its first key to the key that ends it (the actor's next key, or its last). The quality
shows in the root's path (rising, sinking: the root's height; advancing, retreating: travel along the facing) or in
the body's form (the arms' elevation and the knees' fold for rising and sinking, the spine's lean relative to the
root for advancing and retreating, the arms' spread for spreading and enclosing). A quality neither shows while its
opposite does is contradicted, and only that is refused (O73). A span with an airborne key that declares a turn is a
flight and is not judged (O76: the spine's tuck in a flip is not a lean). Interpretation (Claude's, for owner review):
the thresholds below; the root reading per R-34 uses the root's position and rotation, the support and the joints.
"""

import math

from solver.quaternion import apply, matrix
from solver.staff_geometry import DOWN, UP, _heading, bend_degrees, elevation_azimuth

OPPOSITE = {"rising": "sinking", "sinking": "rising", "advancing": "retreating", "retreating": "advancing",
            "spreading": "enclosing", "enclosing": "spreading"}
ROOT_M, LIMB_DEG, LEAN_DEG, SPREAD = 0.1, 15, 10, 0.15  # interpretation (Claude's, for owner review)


def form(key):
    """The arms' mean elevation, their spread (+X is the performer's left), the knees' mean fold and the spine's
    forward lean relative to the root, for one key."""
    arms = [apply(matrix(key["bones"][joint]), DOWN) for joint in ("LA", "RA")]
    chest = apply(matrix(key["bones"]["Sp"]), UP)
    return {"elevation": sum(elevation_azimuth(arm)[0] for arm in arms) / 2, "spread": (arms[0][0] - arms[1][0]) / 2,
            "knees": (bend_degrees(key["bones"]["LL"]) + bend_degrees(key["bones"]["RL"])) / 2,
            "lean": math.degrees(math.atan2(chest[2], chest[1]))}


def _shows(quality, first, last):
    rise = last["pos"][1] - first["pos"][1]
    heading = math.radians(_heading(first["rot"]))
    along = (last["pos"][0] - first["pos"][0]) * math.sin(heading) + (last["pos"][2] - first["pos"][2]) * math.cos(heading)
    a, b = form(first), form(last)
    path = {"rising": rise > ROOT_M, "sinking": rise < -ROOT_M, "advancing": along > ROOT_M,
            "retreating": along < -ROOT_M}.get(quality, False)
    body = {"rising": b["elevation"] - a["elevation"] > LIMB_DEG or a["knees"] - b["knees"] > LIMB_DEG,
            "sinking": a["elevation"] - b["elevation"] > LIMB_DEG or b["knees"] - a["knees"] > LIMB_DEG,
            "advancing": b["lean"] - a["lean"] > LEAN_DEG, "retreating": a["lean"] - b["lean"] > LEAN_DEG,
            "spreading": b["spread"] - a["spread"] > SPREAD, "enclosing": a["spread"] - b["spread"] > SPREAD}[quality]
    return path or body


def judge(quality, keys, supports):
    """'flight', 'shown', 'neither' or 'contradicted' for `quality` over `keys` (first to the ending key, in time
    order) with each key's support list."""
    if any(not support and key.get("turn", "none") != "none" for key, support in zip(keys[:-1], supports[:-1], strict=True)):
        return "flight"
    first, last = keys[0], keys[-1]
    if _shows(quality, first, last):
        return "shown"
    return "contradicted" if _shows(OPPOSITE[quality], first, last) else "neither"
