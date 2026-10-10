"""S02 query expander (band L0.5): resolve the Intent Document against library cards; no model.

- duration_s, fps, setting, style_reference come only from the intent (query or flag).
- genre comes from the intent, or from the matched world card when that card lists exactly one genre.
- world, ax and surfaces come only from the matched world card.
- each entity/prop hint becomes an entity (archetype card) or a prop (object card); the card's kind decides.
Everything unresolved is listed in scene.missing, scene.ambiguous or scene.unresolved_hints.
"""

import argparse
import sys

from kernel.canonical import canonical_json
from planner.archetype_resolver import entity_from_card
from planner.card_loader import load_cards, match
from planner.entity_grounder import prop_from_card
from planner.intent_parser import parse_intent
from planner.world_grounder import ground_world, surfaces_from_card

SCENE_FIELDS = ("duration_s", "fps", "genre", "world", "setting", "style_reference", "ax")
NEVER_RESOLVED = ("choreography", "camera_plan", "geometry_anchors")


def _intent_source(intent, field):
    rows = intent["evidence"].get(field, [])
    return "intent:flag" if rows and rows[0]["source"] == "flag" else "intent:query"


def expand(intent, cards=None):
    cards = load_cards() if cards is None else cards
    parsed = intent["parsed"]
    scene = {field: None for field in SCENE_FIELDS}
    sources, ambiguous, unresolved = {}, [], []
    for field in ("duration_s", "fps", "genre", "setting", "style_reference"):
        if parsed[field] is not None:
            scene[field], sources[field] = parsed[field], _intent_source(intent, field)
    world_id, candidates = ground_world(parsed["setting"], cards)
    surfaces = []
    if world_id:
        world = cards[world_id]
        scene["world"], scene["ax"] = world_id, dict(world["ax"])
        sources["world"] = sources["ax"] = "card:" + world_id
        surfaces = surfaces_from_card(world)
        if scene["genre"] is None and len(world["genres"]) == 1:
            scene["genre"], sources["genre"] = world["genres"][0], "card:" + world_id
    elif len(candidates) > 1:
        ambiguous.append({"field": "world", "candidates": candidates,
                          "reason": "The setting matches several world cards equally."})
    entities, props, used = [], [], {}
    for field in ("entities_hinted", "props_hinted"):
        for hint, evidence in zip(parsed[field], intent["evidence"].get(field, []), strict=True):
            card_id, found = match(hint, cards, {"archetype", "object"})
            if card_id is None:
                reason = "No card matches this hint." if not found else "Several cards match: " + ", ".join(found)
                unresolved.append({"hint": hint, "field": field, "reason": reason})
                continue
            used[card_id] = used.get(card_id, 0) + 1
            identity = card_id if used[card_id] == 1 else f"{card_id}_{used[card_id]}"
            card = cards[card_id]
            if card["kind"] == "archetype":
                entities.append(entity_from_card(identity, card, hint, evidence))
            else:
                props.append(prop_from_card(identity, card, hint, evidence))
    missing = [field for field in SCENE_FIELDS if scene[field] is None] + list(NEVER_RESOLVED)
    scene.update(sources=sources, missing=missing, ambiguous=ambiguous, unresolved_hints=unresolved)
    return {"scene": scene, "entities": entities, "props": props, "surfaces": surfaces}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m planner.query_expander")
    parser.add_argument("query")
    parser.add_argument("--genre")
    args = parser.parse_args(argv)
    sys.stdout.write(canonical_json(expand(parse_intent(args.query, genre=args.genre))))


if __name__ == "__main__":
    main()
