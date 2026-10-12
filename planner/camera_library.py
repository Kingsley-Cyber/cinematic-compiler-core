"""Camera library (S16): grammar, tempo, per-genre conventions and per-archetype idioms, each schema-checked."""

import json
import re
from functools import cache

import yaml

from kernel.canonical import ContractError
from planner import library_vocab
from planner.dependency_graph import ROOT
from validators.schema_validator import validate_schema

LIBRARY = ROOT / "library"


def _load(path, schema_name):
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    validate_schema(document, json.loads((ROOT / "schemas" / "cards" / f"{schema_name}.schema.json").read_text(encoding="utf-8")))
    return document


@cache
def grammar():
    return _load(LIBRARY / "camera_grammar.yaml", "camera_grammar")


@cache
def tempo():
    return _load(LIBRARY / "camera_tempo.yaml", "camera_tempo")


# F-187 (RV-85): the camera terms a rule's words may use, in the grammar's vocabulary and the common synonyms reviewers
# used (interpretation, Claude's, for owner review: the synonym list); each must be one its fields allow.
TERMS = [
    ("scale", "extreme_close", r"\bextreme close[- ]?ups?\b|\bECUs?\b"),
    ("scale", "close", r"(?<!extreme )\bclose[- ]?ups?\b|\bcut close\b|\bclose shots?\b|\btight\b"),
    ("scale", "medium_close", r"\bmedium[- ]close\b"),
    ("scale", "medium_wide", r"\bmedium[- ]wide\b"),
    ("scale", "medium", r"\bmedium\b(?![- ](?:close|wide))"),
    ("scale", "full", r"\bfull\b"),
    ("scale", "extreme_wide", r"\bextreme wide\b"),
    ("scale", "wide", r"(?<!extreme )(?<!medium-)(?<!medium )\bwide\b"),
    ("scale", "insert", r"\binserts?\b|\bdetail shots?\b"),
    ("movement", "static", r"\bholds?\b|\bheld\b|\bstatic\b|\blocked[- ]off\b"),
    ("movement", "pan", r"(?<!whip )(?<!whip-)\bpans?\b"),
    ("movement", "tilt", r"\btilts?\b"),
    ("movement", "dolly_in", r"\bdolly in\b|\bpush(?:es|ing)?\b"),
    ("movement", "dolly_out", r"\bdolly out\b|\bpull(?:s|ing)? (?:out|back)\b"),
    ("movement", "truck", r"\btrucks?\b"),
    ("movement", "pedestal", r"\bpedestal\b"),
    ("movement", "crane", r"\bcranes?\b"),
    ("movement", "orbit", r"\borbits?\b"),
    ("movement", "tracking", r"\btrack(?:s|ing)?\b"),
    ("movement", "whip_pan", r"\bwhip(?:s|[- ]pans?)?\b"),
    ("movement", "zoom", r"\bzooms?\b"),
    ("playback", "slow", r"\bslow[- ]?(?:motion|mo)\b|\bslowed\b|\bhalf[- ]speed\b|\bbullet[- ]time\b|\bovercrank(?:ed|ing)?\b"),
    ("playback", "ramp", r"\b(?:speed[- ]?)?ramp(?:s|ed|ing)?\b"),
    ("playback", "freeze", r"\bfreeze(?:[- ]?frames?)?\b|\bfreezes\b|\bfrozen\b"),
    ("playback", "fast", r"\bfast[- ](?:motion|forward)\b|\bspeed(?:s|ed)? up\b|\bsped up\b|\bundercrank(?:ed|ing)?\b"),
]
HIT_WORDS = re.compile(r"\b(?:blows?|hits?|impacts?|strikes?|struck)\b", re.I)
BETWEEN_HITS = re.compile(r"\bbetween (?:blows|hits|impacts|strikes)\b", re.I)


def terms(words):
    """{(field, value)} the words ask for, read with TERMS (F-187)."""
    return {(field, value) for field, value, pattern in TERMS if re.search(pattern, words, re.I)}


def rule_problems(rule, playback=("normal",)):
    """[message] for one card rule (F-177, F-187; RV-71b, RV-85): its words ask only what its fields ask, a rule whose
    words speak of a hit is a hit rule, every scale, movement and playback is the grammar's, playback stays in the card's
    list, and a hit rule asks for a static hold on every body present at an impact scale (owner O92, R-21).
    Interpretation (Claude's, for owner review): the triggers and asks are read from each rule's words."""
    fields = library_vocab.load("camera_subdivisions")["fields"]
    words = {"scale": fields["framing.scale"]["values"], "movement": fields["movement.kind"]["values"],
             "playback": fields["playback.treatment"]["values"]}
    impact = next(r["in"] for r in grammar()["intents"]["impact"] if r["field"] == "framing.scale")
    asks, problems = rule["asks"], []
    said = rule.get("statement") or rule.get("prefer", "")  # what the prompt prints, or what the S16 author reads
    for field, value in sorted(terms(said)):  # F-187 (RV-85): the words ask only what the fields ask
        if value not in asks.get(field, []):
            problems.append(f"{rule['id']}: its words ask for {value} ({field}), which its fields do not")
    named = BETWEEN_HITS.sub("", " ".join(rule.get(key, "") for key in ("statement", "when", "prefer")))
    if HIT_WORDS.search(named) and rule["trigger"] != "hit":  # a rule about a hit is held to O92 whatever its label
        problems.append(f"{rule['id']}: its words speak of a hit, so its trigger is hit")
    for key, known in words.items():
        problems += [f"{rule['id']}: {value} is no {key} of the grammar" for value in asks.get(key, []) if value not in known]
    problems += [f"{rule['id']}: {value} playback is not the card's" for value in asks.get("playback", [])
                 if value not in playback]
    if rule["trigger"] == "hit" and (not set(asks.get("scale", impact)) <= set(impact) or asks.get("movement") != ["static"]
                                     or asks.get("subjects") != "all_present"):
        problems.append(f"{rule['id']}: a hit is a static hold on every body present at {', '.join(impact)} (owner O92)")
    return problems


def _checked(card, rules, playback):
    problems = [p for rule in card[rules] for p in rule_problems(rule, playback)]
    if problems:
        raise ContractError("CAMERA_CARD", "; ".join(problems), card["card_id"])
    return card


def convention(genre):
    card = _load(LIBRARY / "camera_conventions" / f"{genre}.yaml", "camera_convention_card")
    return _checked(card, "conventions", card["playback"])


def idioms(archetypes):
    """{archetype: idioms} from the idiom card each archetype names (its `camera_idioms`, else its own id; F-177)."""
    found = {}
    for archetype in archetypes:
        card = LIBRARY / "archetypes" / f"{archetype}.yaml"
        name = _load(card, "archetype_card").get("camera_idioms", archetype) if card.exists() else archetype
        path = LIBRARY / "camera_idioms" / f"{name}.yaml"
        if path.exists():
            found[archetype] = _checked(_load(path, "camera_idiom_card"), "idioms", ("normal",))["idioms"]
    return found
