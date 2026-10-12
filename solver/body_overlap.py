"""BODY_OVERLAP (RV-49, F-144, rule R-18): no body passes through another.

At each instant where two bodies both have an S13 key, every capsule of one (forward_kinematics.capsules: a segment's
axis between its two joints, its radius from the body card, draft) stays out of every capsule of the other: the least
distance between their axes is at least the sum of their radii. A contact between two bodies meets at their surfaces
(CONTACT_WORLD measures it there), so it overlaps nothing either.
Interpretation (Claude's, for owner review): only the keys' exact instants are checked here; between keys
validators/between_keys_report.py measures along the declared interpolation (RV-59a), solver/reblock.py's clearance
keeps a re-blocked key's spans clear (RV-59b) and S13 refuses an overlap at every frame there (RV-59e); a body's own
segments may cross each other; no depth is allowed (ALLOWANCE_M); a prop has no extent yet, so a
body through a prop is not checked.
"""

import itertools

from solver.forward_kinematics import segment_distance

ALLOWANCE_M = 0.0


def _words(text):
    return text.replace("_", " ")


def overlaps(bodies):
    """[(t, (entity, slot), (entity, slot), depth, segment, segment)]: for each pair of bodies at one instant, their
    deepest overlap, when any. bodies: {(entity, t): {"id": slot, "capsules": {segment: (start, end, radius)}}}."""
    at = {}
    for (entity, t), body in bodies.items():
        at.setdefault(t, {})[entity] = body
    out = []
    for t, here in sorted(at.items()):
        for a, b in itertools.combinations(sorted(here), 2):
            worst = max(((ra + rb - segment_distance(pa, qa, pb, qb), sa, sb)
                         for (sa, (pa, qa, ra)), (sb, (pb, qb, rb))
                         in itertools.product(sorted(here[a]["capsules"].items()), sorted(here[b]["capsules"].items()))),
                        default=None)
            if worst and worst[0] > ALLOWANCE_M + 1e-9:
                out.append((t, (a, here[a]["id"]), (b, here[b]["id"]), round(worst[0], 3), worst[1], worst[2]))
    return out


def refusals(bodies):
    return [{"code": "BODY_OVERLAP", "slot": first[1], "message": f"{_words(first[0])} {_words(one)} and "
             f"{_words(second[0])} {_words(other)} overlap by {depth:g} m at {t:g} (R-18: no body through another)"}
            for t, first, second, depth, one, other in overlaps(bodies)]
