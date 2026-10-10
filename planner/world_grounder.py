"""S02 helper: choose a world card for the setting text by match-term overlap; surfaces come from the card."""

from planner.card_loader import normalize


def ground_world(setting, cards):
    """(card_id or None, candidates). Highest count of shared words wins; ties stay ambiguous; zero is no match."""
    if not setting:
        return None, []
    words = set(normalize(setting).split())
    scores = {}
    for card in cards.values():
        if card["kind"] == "world":
            score = len(words & set(card["match_terms"]))
            if score:
                scores[card["card_id"]] = score
    if not scores:
        return None, []
    best = max(scores.values())
    found = sorted(card_id for card_id, score in scores.items() if score == best)
    return (found[0] if len(found) == 1 else None), found


def surfaces_from_card(card):
    return [{"id": row["id"], "world_card_id": card["card_id"], "card_version": card["card_version"],
             "card_status": card["status"], "kind": row["kind"], "description": row["description"]}
            for row in card["surfaces"]]
