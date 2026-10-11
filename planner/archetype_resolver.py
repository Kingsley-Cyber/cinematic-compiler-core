"""S02 helper: turn an archetype card into an L0.5 entity definition (copied fields, never invented)."""

ENTITY_FIELDS = ("description", "silhouette", "costume", "parts", "capabilities", "modes")


def entity_from_card(identity, card, hint, evidence):
    item = {"id": identity, "card_id": card["card_id"], "card_version": card["card_version"],
            "card_status": card["status"], "hint": hint, "hint_evidence": evidence, "name": card["names"][0]}
    item.update({field: card[field] for field in ENTITY_FIELDS})
    if "face_profile" in card:
        item["face_profile"] = card["face_profile"]
    return item
