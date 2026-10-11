"""Staff words for one S13 key pose (M8.1): limb and body direction, level and fold; support words; turn signs.

Derived only; these are the atoms the structured-prose renderer writes into each staff line. Frame: the Q6
convention (kernel/conventions.yaml): +Y up, the performer faces +Z, +X is the performer's left, Euler intrinsic XYZ
in degrees, joints local to their parent. Chain: root -> Sp -> (NK -> HD, LA -> LFA, RA -> RFA) and root ->
(LUL -> LL, RUL -> RL); at rest the body is upright and every limb hangs straight down.

- Arms are read in the chest frame and legs in the pelvis frame (gesture directions are relative to the body's
  front), so a joint's own rotation gives its direction. The head is read in the chest frame through NK and HD.
- The body (trunk) is read against gravity around the performer's heading, so a lean from the root or from the
  spine reads the same: "forward-high (30 lean)".
- Direction: the nearest of the eight horizontal directions (45-degree sectors around the front). Level follows the
  owner's laban-notation lookup (quaternion -> direction/level): mid while the elevation stays inside +-45 degrees
  (forward 60 and forward 120 read mid), high from +45 up, low from -45 down; place-high / place-low within 10
  degrees of straight up or down (so 'overhead 170' stays forward-high, as in the lookup). Interpretation, stated
  in the prompt legend; checked against the 2.3 source's own words (tests/test_staff_geometry.py).
- Fold: the lower segment's bend (LFA/RFA, LL/RL) in 15-degree steps; under 15 degrees reads "straight". The body and
  head read upright while within 10 degrees of vertical (place-high).
- Support level: hands, torso and other parts read place-low; feet read place-low when the posture is crouching or
  kneeling or a supporting knee bends 60 degrees or more, otherwise place-mid (interpretation; there is no toe atom).
"""

import math

from .quaternion import apply, horizontal, lateral_heading, matrix, quaternion, root_heading

UP, DOWN, FORWARD = (0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0)
SECTORS = ("forward", "left-forward", "left", "left-back", "back", "right-back", "right", "right-forward")
LEVEL_EDGE, PLACE_EDGE = 45, 80
FOLD_STEP, STRAIGHT_UNDER = 15, 15
LOW_KNEE = 60
LIMBS = {"left": (("arm", "LA", "LFA"), ("leg", "LUL", "LL")), "right": (("arm", "RA", "RFA"), ("leg", "RUL", "RL"))}
TURNS = {"flip": (0, "lateral", ("forward", "backward")), "spin": (1, "vertical", ("to the left", "to the right")),
         "cartwheel": (2, "sagittal", ("toward the performer's right", "toward the performer's left"))}


def elevation_azimuth(vector):
    """Elevation above the horizontal plane and azimuth from the front toward the performer's left, in degrees."""
    x, y, z = vector
    length = math.sqrt(x * x + y * y + z * z)
    elevation = math.degrees(math.asin(max(-1.0, min(1.0, y / length))))
    return round(elevation, 6), round(math.degrees(math.atan2(x, z)), 6)


def _nearest(value, step):
    """Half-up rounding to a step (Python's round() would send ties to the even step)."""
    return math.floor(value / step + 0.5) * step


def direction_word(vector):
    """'forward-mid', 'left-back-high', 'place-low' ... for a direction in the reading frame."""
    elevation, azimuth = elevation_azimuth(vector)
    if elevation > PLACE_EDGE:
        return "place-high"
    if elevation < -PLACE_EDGE:
        return "place-low"
    level = "high" if elevation >= LEVEL_EDGE else "low" if elevation <= -LEVEL_EDGE else "mid"
    return f"{SECTORS[_nearest(azimuth, 45) // 45 % 8]}-{level}"


def bend_degrees(rot):
    w = quaternion(rot)[0]
    return math.degrees(2 * math.acos(min(1.0, abs(w))))


def fold_word(rot):
    bend = bend_degrees(rot)
    return "straight" if bend < STRAIGHT_UNDER else f"folded {_nearest(bend, FOLD_STEP)}"


def _heading(rot):
    forward = apply(matrix(rot), FORWARD)
    return root_heading(rot) if horizontal(forward) >= 0.5 else lateral_heading(rot)


def body_word(key):
    """The trunk against gravity around the performer's heading: None when upright (place-high), 'inverted'
    (place-low), otherwise its direction and lean, e.g. 'forward-high (30 lean)'."""
    chest_up = apply(matrix(key["rot"]), apply(matrix(key["bones"]["Sp"]), UP))
    h = math.radians(_heading(key["rot"]))
    forward, left = (math.sin(h), 0.0, math.cos(h)), (math.cos(h), 0.0, -math.sin(h))
    local = (sum(a * b for a, b in zip(chest_up, left, strict=True)), chest_up[1],
             sum(a * b for a, b in zip(chest_up, forward, strict=True)))
    word = direction_word(local)
    if word in ("place-high", "place-low"):
        return None if word == "place-high" else "inverted"
    return f"{word} ({_nearest(90 - elevation_azimuth(local)[0], 5)} lean)"


def head_word(key):
    """The head against the chest through NK and HD: None when upright (place-high), otherwise its direction."""
    word = direction_word(apply(matrix(key["bones"]["NK"]), apply(matrix(key["bones"]["HD"]), UP)))
    return None if word == "place-high" else word


def pose_words(key):
    """Every limb's direction and fold, the body and the head, for one key pose."""
    sides = {side: {name: direction_word(apply(matrix(key["bones"][upper]), DOWN)) for name, upper, _ in limbs}
             | {f"lower_{name}": fold_word(key["bones"][lower]) for name, _, lower in limbs}
             for side, limbs in LIMBS.items()}
    return {"body": body_word(key), "head": head_word(key), **sides}


def _part(part):
    side, _, name = part.partition("_")
    return (side, name) if side in ("left", "right") and name else (None, part)


def support_words(parts, *, posture=None, knee_folds=None, surfaces=None):
    """SUPPORT words and precision tags for S11 support parts.

    `knee_folds` maps 'left'/'right' to the knee bend in degrees; `surfaces` maps a part to the surface it rests on
    (from S07 support contacts), the ground when absent.
    """
    if not parts:
        return {"words": "NO SUPPORT", "tags": ""}
    knee_folds, surfaces = knee_folds or {}, surfaces or {}
    groups = {}
    for part in sorted(parts):
        side, name = _part(part)
        groups.setdefault((name, surfaces.get(part, "ground")), []).append(side)
    words, tags = [], []
    for (name, surface), sides in sorted(groups.items()):
        if name == "foot":
            low = posture in ("crouching", "kneeling") or any(knee_folds.get(s, 0) >= LOW_KNEE for s in sides)
            level = "place-low" if low else "place-mid"
        else:
            level = "place-low"
        if len(sides) == 2:
            who, noun = "both ", {"foot": "feet", "hand": "hands"}.get(name, name + "s")
        else:
            who, noun = (sides[0].upper() + " " if sides[0] else ""), name.replace("_", " ")
        on = "" if surface == "ground" else f" ON THE {surface.replace('_', ' ')}"
        words.append(f"{who}{noun} {level}{on}")
        letter = "both" if len(sides) == 2 else (sides[0][0].upper() if sides[0] else None)
        prefix = {"foot": "f", "hand": "h"}.get(name, name)
        tag = f"{prefix}:{letter}" if letter else prefix
        tags.append(f"[{tag}{'' if surface == 'ground' else '_on_' + surface}]")
    text = " + ".join(words)
    if posture == "inverted" and all(_part(p)[1] != "foot" for p in parts):
        text += " (inverted)"
    return {"words": text, "tags": " ".join(tags)}


def turn_words(key, following=None):
    """Turn sign for a key's declared turn, with its side from the change before the performer's next key."""
    if key.get("turn", "none") == "none":
        return None
    axis, plane, sides = TURNS[key["turn"]]
    sign = {"flip": "flip", "spin": "turn", "cartwheel": "cartwheel"}[key["turn"]] + " sign"
    if following is None:
        return f"{sign} ({plane} axis)"
    delta = following["rot"][axis] - key["rot"][axis]
    return f"{sign} ({plane} axis, {sides[0] if delta >= 0 else sides[1]}, {round(abs(delta))})"
