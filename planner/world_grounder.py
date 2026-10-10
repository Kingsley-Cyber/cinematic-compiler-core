"""S02 helper: choose a world card for the setting text by match-term overlap; surfaces come from the card."""

from planner.card_loader import normalize


def ground_world(setting, cards, query=""):
    """(card_id or None, candidates). Highest count of shared words wins; ties stay ambiguous; zero is no match.

    A card with required_terms matches only when every one appears in the query, and each adds one to its score.
    """
    if not setting:
        return None, []
    words = set(normalize(setting).split())
    query_words = set(normalize(query).split())
    scores = {}
    for card in cards.values():
        if card["kind"] == "world":
            required = set(card.get("required_terms", []))
            if not required <= query_words:
                continue
            score = len(words & set(card["match_terms"]))
            if score:
                scores[card["card_id"]] = score + len(required)
    if not scores:
        return None, []
    best = max(scores.values())
    found = sorted(card_id for card_id, score in scores.items() if score == best)
    return (found[0] if len(found) == 1 else None), found


def surfaces_from_card(card):
    return [{"id": row["id"], "world_card_id": card["card_id"], "card_version": card["card_version"],
             "card_status": card["status"], "kind": row["kind"], "description": row["description"],
             **({"ax": row["ax"]} if "ax" in row else {})}
            for row in card["surfaces"]]
