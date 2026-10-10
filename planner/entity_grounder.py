"""S02 helper: turn an object card into an L0.5 prop definition (copied fields, never invented)."""

PROP_FIELDS = ("description", "parts", "materials", "states", "affordances", "grips")
GROUP_FIELDS = ("count", "unit_name", "group_name")


def prop_from_card(identity, card, hint, evidence):
    item = {"id": identity, "card_id": card["card_id"], "card_version": card["card_version"],
            "card_status": card["status"], "hint": hint, "hint_evidence": evidence, "name": card["names"][0]}
    item.update({field: card[field] for field in PROP_FIELDS})
    item.update({field: card[field] for field in GROUP_FIELDS if field in card})
    return item
