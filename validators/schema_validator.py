"""Explicit JSON Schema subset (Draft 2020-12 keywords listed in KEYWORDS).

Ported unchanged in behaviour from ai-video-compiler `video_compiler/schema_validation.py`
lines 1-192 (phase4-wip e49273a). Not a general Draft 2020-12 implementation:
unsupported vocabulary fails before instance validation, including in branches the
instance does not select. Only document-local `#/` references; nothing is fetched.
"""

import re

from kernel.canonical import ContractError, check_finite, content_hash

ANNOTATIONS = {"$schema", "$id", "title", "description", "$comment", "default", "examples"}
KEYWORDS = ANNOTATIONS | {"$ref", "$defs", "type", "const", "enum", "required", "properties",
                         "patternProperties", "additionalProperties", "items", "prefixItems",
                         "minItems", "maxItems", "uniqueItems", "minLength", "maxLength", "pattern",
                         "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
                         "oneOf", "anyOf", "allOf", "not"}
TYPES = {"null", "boolean", "integer", "number", "string", "array", "object"}


def _resolve(root, ref):
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise ContractError("SCHEMA_UNSUPPORTED", "Only document-local JSON pointers are supported", str(ref))
    node = root
    try:
        for key in ref[2:].split("/"):
            node = node[key.replace("~1", "/").replace("~0", "~")]
    except (KeyError, TypeError) as error:
        raise ContractError("SCHEMA_REFERENCE", "Unresolved local schema reference", ref) from error
    return node


def _inspect(node, root, path="$", refs=(), seen=None):
    if seen is not None:
        if id(node) in seen:
            return
        seen.add(id(node))
    if isinstance(node, bool):
        return
    if not isinstance(node, dict):
        raise ContractError("SCHEMA_SHAPE", "Schema must be an object or boolean", path)
    unknown = set(node) - KEYWORDS
    if unknown:
        raise ContractError("SCHEMA_UNSUPPORTED", "Unsupported schema keywords: " + ", ".join(sorted(unknown)), path)
    if "$schema" in node and node["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        raise ContractError("SCHEMA_UNSUPPORTED", "Only the declared Draft 2020-12 subset is supported", path)
    if "$ref" in node:
        ref = node["$ref"]
        if ref in refs and seen is None:
            raise ContractError("SCHEMA_UNSUPPORTED", "Recursive schema references are not supported", ref)
        _inspect(_resolve(root, ref), root, ref, (*refs, ref), seen)
    if "type" in node:
        names = node["type"] if isinstance(node["type"], list) else [node["type"]]
        if not names or any(not isinstance(n, str) or n not in TYPES for n in names):
            raise ContractError("SCHEMA_SHAPE", "Unknown schema type", path)
    for key in ("required",):
        if key in node and (not isinstance(node[key], list) or any(not isinstance(v, str) for v in node[key])):
            raise ContractError("SCHEMA_SHAPE", "Required must list property names", path)
    if "enum" in node and (not isinstance(node["enum"], list) or not node["enum"]):
        raise ContractError("SCHEMA_SHAPE", "Enum must be a nonempty list", path)
    for key in ("minItems", "maxItems", "minLength", "maxLength"):
        if key in node and (type(node[key]) is not int or node[key] < 0):
            raise ContractError("SCHEMA_SHAPE", "Length bound must be a nonnegative integer", path + "." + key)
    for key in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
        if key in node and type(node[key]) not in (int, float):
            raise ContractError("SCHEMA_SHAPE", "Numeric bound must be a number", path + "." + key)
    if "uniqueItems" in node and not isinstance(node["uniqueItems"], bool):
        raise ContractError("SCHEMA_SHAPE", "uniqueItems must be boolean", path)
    for key in ("properties", "patternProperties", "$defs"):
        if key not in node:
            continue
        if not isinstance(node[key], dict):
            raise ContractError("SCHEMA_SHAPE", "Expected schema map", path + "." + key)
        for name, child in node[key].items():
            if key == "patternProperties":
                _pattern(name, path)
            _inspect(child, root, path + "." + key + "." + name, refs, seen)
    if "pattern" in node:
        _pattern(node["pattern"], path)
    for key in ("items", "additionalProperties", "not"):
        if key in node:
            _inspect(node[key], root, path + "." + key, refs, seen)
    for key in ("prefixItems", "oneOf", "anyOf", "allOf"):
        if key in node:
            if not isinstance(node[key], list) or (key != "prefixItems" and not node[key]):
                raise ContractError("SCHEMA_SHAPE", "Expected list of schemas", path + "." + key)
            for i, child in enumerate(node[key]):
                _inspect(child, root, f"{path}.{key}[{i}]", refs, seen)


def _pattern(pattern, path):
    try:
        return re.compile(pattern)
    except (re.error, TypeError) as error:
        raise ContractError("SCHEMA_SHAPE", "Unsupported regular expression", path) from error


def _equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_equal(x, y) for x, y in zip(a, b, strict=True))
    return a == b


def _matches_type(value, name):
    return {"null": value is None, "boolean": isinstance(value, bool),
            "number": type(value) in (int, float),
            "integer": type(value) in (int, float) and value % 1 == 0,
            "string": isinstance(value, str), "array": isinstance(value, list),
            "object": isinstance(value, dict)}[name]


def _check(value, schema, root, path, active_refs=()):
    def fail(message):
        raise ContractError("TARGET_SCHEMA", message, path)
    if schema is True:
        return
    if schema is False:
        fail("Value is forbidden by the schema")
    if "$ref" in schema:
        binding = (schema["$ref"], path)
        if binding in active_refs:
            raise ContractError("SCHEMA_REFERENCE", "Reference cycle does not descend into instance data",
                                schema["$ref"])
        _check(value, _resolve(root, schema["$ref"]), root, path, (*active_refs, binding))
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_matches_type(value, n) for n in types):
            fail("Expected " + "/".join(types))
    if "const" in schema and not _equal(value, schema["const"]):
        fail("Value differs from schema constant")
    if "enum" in schema and not any(_equal(value, candidate) for candidate in schema["enum"]):
        fail("Value is outside the schema vocabulary")
    for key in ("oneOf", "anyOf", "allOf", "not"):
        if key not in schema:
            continue
        options = [schema[key]] if key == "not" else schema[key]
        passed = 0
        for option in options:
            try:
                _check(value, option, root, path, active_refs)
                passed += 1
            except ContractError as error:
                if error.code != "TARGET_SCHEMA":
                    raise
        if not {"oneOf": passed == 1, "anyOf": passed > 0,
                "allOf": passed == len(options), "not": passed == 0}[key]:
            fail("Value does not satisfy " + key)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                fail("Missing required property " + key)
        properties = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        for key, item in value.items():
            selected = [properties[key]] if key in properties else []
            selected.extend(sub for pattern, sub in patterns.items() if re.search(pattern, key))
            if not selected:
                selected = [schema.get("additionalProperties", True)]
            for sub in selected:
                _check(item, sub, root, path + "/" + key.replace("~", "~0").replace("/", "~1"), active_refs)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or ("maxItems" in schema and len(value) > schema["maxItems"]):
            fail("Array length violates schema")
        if schema.get("uniqueItems") and any(_equal(x, y) for i, x in enumerate(value) for y in value[:i]):
            fail("Array items must be unique")
        prefix = schema.get("prefixItems", [])
        for i, item in enumerate(value):
            _check(item, prefix[i] if i < len(prefix) else schema.get("items", True), root, f"{path}/{i}", active_refs)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or ("maxLength" in schema and len(value) > schema["maxLength"]):
            fail("String length violates schema")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            fail("String does not match schema pattern")
    if type(value) in (int, float) and (("minimum" in schema and value < schema["minimum"]) or
                ("maximum" in schema and value > schema["maximum"]) or
                ("exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]) or
                ("exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"])):
        fail("Number violates schema bound")


def validate_schema(instance, schema):
    check_finite(schema)
    check_finite(instance)
    _inspect(schema, schema)
    _check(instance, schema, schema, "$")
    return {"status": "valid", "scope": "supported_json_schema_keywords_not_domain_semantics",
            "schema_hash": content_hash(schema), "instance_hash": content_hash(instance),
            "regex_dialect": "Python_re; source patterns require compatibility review"}


def check_schema(schema):
    """Refuse unsupported keywords or malformed schema structure without an instance."""
    check_finite(schema)
    _inspect(schema, schema)
    return content_hash(schema)
