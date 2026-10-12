"""FLOOR_PENETRATION (RV-14a, F-089; owner O72): no body sinks into the floor at any key.

Each key's forward-kinematics points (the contact points: head, torso, pelvis, elbows, hands, knees and soles) are
read against the floor: the lowest top among the scene's floors, or the convention's ground where the scene names no
floor. A point more than 0.15 m under it is refused, the tolerance O72 sets for a contact's two points.
Interpretation (Claude's, for owner review): a point is the part's centre line, so a part may sink by its radius, as a
foot's sole meets a surface in CONTACT_WORLD; a body over a raised top is judged against the floor, not the top, until
RV-22 gives surfaces their faces. Only the keys are checked here; between keys validators/between_keys_report.py
measures along the declared interpolation (RV-59a) and RV-59c refuses.
"""

from planner.dynamic_beat_validator import GROUND, surface_tops

TOLERANCE_M = 0.15  # owner O72


def floor_level(surfaces, ground_text):
    """The floor's height: the lowest top among the floors, else the convention's ground; None when neither is known."""
    tops = surface_tops(surfaces, ground_text)
    floors = [tops[s["id"]] for s in surfaces if s["kind"] == "floor" and s["id"] in tops]
    if floors:
        return min(floors)
    ground = GROUND.search(str(ground_text))
    return float(ground.group(1)) if ground else None


def refusals(bodies, floor):
    """[{code, slot, message}] for each key ({(entity, t): {id, points}}) whose lowest point lies over TOLERANCE_M under
    the floor."""
    if floor is None:
        return []
    out = []
    for (entity, t), body in sorted(bodies.items(), key=lambda item: (item[0][1], item[0][0])):
        part, point = min(body["points"].items(), key=lambda item: (item[1][1], item[0]))
        depth = round(floor - point[1], 3)
        if depth > TOLERANCE_M:
            out.append({"code": "FLOOR_PENETRATION", "slot": body["id"],
                        "message": f"{entity}'s {part.replace('_', ' ')} is {depth:g} m under the floor at {t:g} "
                                   f"(over {TOLERANCE_M:g} m, owner O72)"})
    return out
