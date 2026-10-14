"""Pose words to joint angles (PLAN-010 Phase 2, step 7): the inverse of solver/staff_geometry.py `pose_words`.

The S13 model will write each free limb's intent as the staff words the prompt already prints ("forward-high",
"folded 45"); this module gives the joint angles that read back as those words, so the solver starts from the model's
intent and only moves what a target or a support needs. A direction word names a sector: its azimuth (the eight
45-degree directions around the body's front, toward the performer's left positive) and its level's elevation (mid
0, high HIGH_DEG, low -HIGH_DEG, place-high and place-low straight up and down). An upper limb's angles are found by
search over its pitch and roll so that its bone, hanging down at rest, points along the sector's centre; a fold sets
the lower limb's bend (an arm folds with a negative pitch, a leg with a positive one, as the examples write them).
Round trip: `pose_words` of the result reads the words given (tests/test_intent.py).
"""

import math
from functools import cache

from .quaternion import apply, matrix
from .staff_geometry import DOWN, LIMBS, SECTORS, UP, direction_word, fold_word

HIGH_DEG = 62.5  # the middle of the high band (45 to 80 degrees), and of the low band below
AZIMUTH = {name: 45 * i if i <= 4 else 45 * i - 360 for i, name in enumerate(SECTORS)}
FOLD_SIGN = {"arm": -1, "leg": 1}


def word_vector(word):
    """The unit direction at the centre of a direction word's sector, in the reading frame (+X left, +Y up, +Z front)."""
    if word == "place-high":
        return UP
    if word == "place-low":
        return DOWN
    sector, _, level = word.rpartition("-")
    elevation = {"high": HIGH_DEG, "mid": 0.0, "low": -HIGH_DEG}[level]
    e, a = math.radians(elevation), math.radians(AZIMUTH[sector])
    return (math.cos(e) * math.sin(a), math.sin(e), math.cos(e) * math.cos(a))


def _angle(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(u, v, strict=True))))))


def _search(rest, target, steps=(30, 10, 3, 1)):
    """[pitch, 0, roll] whose rotation turns `rest` closest to `target` (a coarse grid, then finer around the best),
    inside pitch -180..180 and roll -90..90; among equally close angles the one nearest rest (an arm straight out to
    the side reads the same at every pitch: S-136)."""
    def score(x, z):
        return (round(_angle(apply(matrix([x, 0, z]), rest), target), 6), abs(x) + abs(z), x, z)
    best = min(score(x, z) for x in range(-180, 181, steps[0]) for z in range(-90, 91, steps[0]))
    for step in steps[1:]:
        _, _, bx, bz = best
        best = min([best] + [score(x, z) for x in (bx + step * i for i in range(-3, 4)) if -180 <= x <= 180
                             for z in (bz + step * i for i in range(-3, 4)) if -90 <= z <= 90])
    return [round(best[2], 6) + 0.0, 0.0, round(best[3], 6) + 0.0]


def limb_angles(word):
    """An upper limb's angles for a direction word (the bone hangs down at rest)."""
    return list(_limb(word))


@cache
def _limb(word):
    return tuple(_search(DOWN, word_vector(word)))


def fold_angles(word, kind):
    """A lower limb's angles for a fold word ("straight" or "folded 45")."""
    bend = 0.0 if word == "straight" else float(word.split()[1])
    return [FOLD_SIGN[kind] * bend, 0.0, 0.0]


def bones_from_words(words, base=None):
    """The limbs' bones for a pose's words ({left: {arm, lower_arm, leg, lower_leg}, right: ...}); the joints the words
    do not name (spine, neck, head) come from `base` or rest."""
    bones = {name: list(v) for name, v in (base or {}).items()}
    for side, limbs in LIMBS.items():
        for kind, upper, lower in limbs:
            bones[upper] = limb_angles(words[side][kind])
            bones[lower] = fold_angles(words[side][f"lower_{kind}"], kind)
    return bones


def reads_back(bones):
    """The limb words these bones read as (pose_words' limbs, without the body and head)."""
    return {side: {kind: direction_word(apply(matrix(bones[upper]), DOWN)) for kind, upper, _ in limbs}
            | {f"lower_{kind}": fold_word(bones[lower]) for kind, _, lower in limbs} for side, limbs in LIMBS.items()}


def _search_word(make, read, word, ranges=((-180, 180), (-90, 90)), steps=(15, 5, 1)):
    """The [x, 0, z] whose `make` reads back as `word` (`read`), nearest rest among those that do; None when none does."""
    best = None
    for x in range(ranges[0][0], ranges[0][1] + 1, steps[0]):
        for z in range(ranges[1][0], ranges[1][1] + 1, steps[0]):
            if read(make([x, 0, z])) == word and (best is None or abs(x) + abs(z) < abs(best[0]) + abs(best[2])):
                best = [x, 0, z]
    return None if best is None else [float(v) for v in best]


def spine_angles(word, rot):
    """The spine (Sp) for a body word ("forward-high (30 lean)", None for upright) under the root's rotation `rot`."""
    from .staff_geometry import body_word
    rest = {"Sp": [0, 0, 0], "NK": [0, 0, 0], "HD": [0, 0, 0]}
    if body_word({"rot": rot, "bones": rest}) == word:  # the root alone already reads as the word (upright or not)
        return [0.0, 0.0, 0.0]
    found = _search_word(lambda sp: {"rot": rot, "bones": {**rest, "Sp": sp}}, body_word, word, steps=(5, 5, 5))
    return found if found is not None else [0.0, 0.0, 0.0]


def head_angles(word):
    """The head (HD, the neck at rest) for a head word (None for upright)."""
    if word is None:
        return [0.0, 0.0, 0.0]
    from .staff_geometry import head_word
    found = _search_word(lambda hd: {"bones": {"NK": [0, 0, 0], "HD": hd}}, head_word, word)
    return found if found is not None else [0.0, 0.0, 0.0]


def resolve_key(key, limits=None):
    """A key or in-between with its `bones` from its `words` when it carries none (PLAN-010: the model writes words, the
    compiler the angles), each component inside `limits` ({"LA.x": (low, high)}, solver/reblock.py `limits`); a key
    that carries bones (the owner's source poses, or the solver's repair) keeps them."""
    if "bones" in key or "words" not in key:
        return key
    words = key["words"]
    bones = bones_from_words({side: words[side] for side in ("left", "right")})
    bones |= {"Sp": spine_angles(words.get("body"), key["rot"]), "NK": [0.0, 0.0, 0.0], "HD": head_angles(words.get("head"))}
    for joint, angles in bones.items():
        for i, axis in enumerate("xyz"):
            low, high = (limits or {}).get(f"{joint}.{axis}", (-math.inf, math.inf))
            angles[i] = min(high, max(low, angles[i]))
    return {**key, "bones": bones}


def resolve(document, limits=None):
    """The motion document with every key's and in-between's bones resolved from its words (`resolve_key`)."""
    return {**document, "keys": [resolve_key(k, limits) for k in document["keys"]],
            **({"inbetweens": [resolve_key(b, limits) for b in document["inbetweens"]]} if "inbetweens" in document else {})}


def words_of(key):
    """The words a key with bones reads as (the model's view of an angle-written key: a guide example's)."""
    from .staff_geometry import pose_words
    return {k: v for k, v in pose_words(key).items()}
