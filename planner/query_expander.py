"""S02 query expander (band L0.5): resolve the Intent Document against library cards; no model.

- genre comes only from the query or --genre; missing genre stops here (GENRE_REQUIRED).
- fps comes from the query/flag, else the genre schema default (fps_source: default).
- setting and style_reference come only from the query; duration is S04's (beat plan).
- world and surfaces come only from the matched world card; ax = kernel conventions (+ the card's unit).
- each entity/prop hint becomes an entity (archetype card) or a prop (object card); the card's kind decides.
Every value names its source; everything unresolved is listed in missing, ambiguous or unresolved_hints.
"""

import argparse
import sys

from kernel import kernel_files
from kernel.canonical import ContractError, canonical_json
from planner import modality
from planner.archetype_resolver import entity_from_card
from planner.card_loader import load_cards, match
from planner.entity_grounder import prop_from_card
from planner.intent_parser import parse_intent
from planner.world_grounder import ground_world, surfaces_from_card

RESOLVABLE = ("world", "setting", "style_reference")
NEVER_RESOLVED = ("choreography", "camera_plan", "geometry_anchors")


def _intent_source(intent, field):
    rows = intent["evidence"].get(field, [])
    return "flag" if rows and rows[0]["source"] == "flag" else "user"


def expand(intent, cards=None):
    cards = load_cards() if cards is None else cards
    parsed = intent["parsed"]
    if parsed["genre"] is None:
        raise ContractError("GENRE_REQUIRED", "Genre is missing: add --genre (live_action, anime or ugc_ad) "
                            "or name it in the query", intent["raw_query"])
    genre = parsed["genre"]
    conventions = kernel_files.load("conventions")
    scene = {"genre": genre, "genre_source": _intent_source(intent, "genre")}
    if parsed["fps"] is not None:
        scene.update(fps=parsed["fps"], fps_source=_intent_source(intent, "fps"))
    else:
        scene.update(fps=modality.default_fps(genre), fps_source="default")
    for field in ("setting", "style_reference"):
        value = parsed[field]
        scene.update({field: value, field + "_source": "user" if value is not None else None})
    ax = {"up": conventions["up"], "forward": conventions["forward"], "ground": conventions["ground"], "unit": None,
          "rotation_convention": conventions["rotation_convention"]}
    world_id, candidates = ground_world(parsed["setting"], cards)
    surfaces, ambiguous, unresolved = [], [], []
    if world_id:
        world = cards[world_id]
        if any(world["ax"][key] != ax[key] for key in ("up", "forward", "ground")):
            raise ContractError("WORLD_AX_CONFLICT", "World card axes differ from the kernel conventions", world_id)
        ax["unit"] = world["ax"]["unit"]
        surfaces = surfaces_from_card(world)
    elif len(candidates) > 1:
        ambiguous.append({"field": "world", "candidates": candidates,
                          "reason": "The setting matches several world cards equally."})
    scene.update(world=world_id, world_source="card:" + world_id if world_id else None, ax=ax,
                 ax_source="kernel+card:" + world_id if world_id else "kernel", chained_from=None)
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
    missing = [field for field in RESOLVABLE if scene[field] is None] + list(NEVER_RESOLVED)
    scene.update(missing=missing, ambiguous=ambiguous, unresolved_hints=unresolved)
    return {"scene": scene, "entities": entities, "props": props, "surfaces": surfaces}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m planner.query_expander")
    parser.add_argument("query")
    parser.add_argument("--genre")
    args = parser.parse_args(argv)
    sys.stdout.write(canonical_json(expand(parse_intent(args.query, genre=args.genre))))


if __name__ == "__main__":
    main()
