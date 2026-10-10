"""Resolve the closed kernel state vocabulary against one scene's entities, props and surfaces."""

from kernel import kernel_files


def resolve(entities, props, surfaces, vocabulary=None):
    """{"entity": {property: values}, "prop": {prop_id: {property: values}}, "surface": {property: values}}."""
    vocabulary = vocabulary or kernel_files.load("state_vocabulary")
    ids = {"entities": [e["id"] for e in entities], "props": [p["id"] for p in props], "surfaces": [s["id"] for s in surfaces]}

    def values(rule):
        return list(rule.get("values", [])) + list(ids.get(rule.get("values_from"), [])) + list(rule.get("extra", []))

    resolved = {"entity": {name: values(rule) for name, rule in vocabulary["actor_properties"].items()},
                "prop": {}, "surface": {name: values(rule) for name, rule in vocabulary["surface_properties"].items()}}
    for prop in props:
        table = {name: values(rule) for name, rule in vocabulary["prop_properties"].items()}
        if vocabulary["prop_card_states"]:
            table.update({row["property"]: list(row["values"]) for row in prop["states"]})
        resolved["prop"][prop["id"]] = table
    return resolved


def allowed(resolved, subject, prop):
    """Allowed values for one subject's property, or None if the property is not in the vocabulary."""
    if subject["kind"] == "prop":
        return resolved["prop"].get(subject["id"], {}).get(prop)
    return resolved[subject["kind"]].get(prop)
