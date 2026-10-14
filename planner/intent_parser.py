"""S01 intent parser (band L0): literal extraction, no model, no inference; place names also from world cards.

Rules (deterministic; an unmatched field stays null/empty and is named in `missing`):
- duration_s: <digits><optional space/hyphen><s|sec|secs|second|seconds>, or a number word with a
  space/hyphen before the unit ("ten-second").
- fps: <digits> fps | <digits> frames per second | fps <digits>.
- genre: "anime", "ugc"/"ugc ad", "live action"/"live-action" -> the declared modality names.
- setting: "in|on|at|inside|atop a|an|the <phrase>" or a comma segment, ending in a place noun: one of PLACE_NOUNS or the
  last word of a world card's name (library/worlds; owner, 2026-10-13: the cards name the places).
- entities_hinted: the words on each side of "vs"/"versus", the words before "product", and cast lines
  "<capital letter>: <description>" (up to three words before the first comma, e.g. "A: lean ninja, dark coat").
- props_hinted: "with|holding|wielding|carrying a|an|the|his|her|their|its <one or two words>", and each comma
  item of "props (<item>, <item>, ...)".
- style_reference: "in the style of <phrase>" or "<word>-style".
CLI flags override the query for genre and duration_s. Several distinct values for a single-valued
field give null plus an ambiguity entry, never a guess. String values are exact query substrings.
"""

import argparse
import re
import sys
from functools import cache
from pathlib import Path

import yaml

from kernel.canonical import ContractError, canonical_json

MODALITIES = ("live_action", "anime", "ugc_ad")
FIELDS = ("duration_s", "fps", "genre", "setting", "entities_hinted", "props_hinted", "style_reference")
SINGLE = ("duration_s", "fps", "genre", "setting", "style_reference")
MISSING_NAME = {"duration_s": "duration_s", "fps": "fps", "genre": "genre", "setting": "setting",
                "entities_hinted": "entities", "props_hinted": "props", "style_reference": "style_reference"}
NEVER_EXTRACTED = ("choreography", "camera_plan", "geometry_anchors")
CORE = ("duration_s", "fps", "genre", "setting", "entities_hinted")

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
                "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
                "thirty": 30, "forty": 40, "sixty": 60, "ninety": 90}
_UNIT = r"(?:seconds|second|secs|sec|s)\b"
_WORDS = "|".join(sorted(NUMBER_WORDS, key=len, reverse=True))
DURATION = re.compile(rf"(?<![\w.])(?:(\d+(?:\.\d+)?)\s*-?\s*|({_WORDS})(?:\s+|\s*-\s*)){_UNIT}", re.I)
FPS = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:fps|frames?\s+per\s+second)\b"
                 r"|\bfps\s*[:=]?\s*(\d+(?:\.\d+)?)(?![\w.])", re.I)
GENRES = (("live_action", re.compile(r"\blive[\s-]+action\b", re.I)),
          ("anime", re.compile(r"\banime\b", re.I)),
          ("ugc_ad", re.compile(r"\bugc(?:[\s-]+ad\b)?\b", re.I)))
PREPOSITION = re.compile(r"\b(?:in|on|at|inside|atop)\s+(?:a|an|the)\s+", re.I)
VERSUS = re.compile(r"\b(?:vs\.?|versus)(?=\s)", re.I)
PRODUCT = re.compile(r"\bproduct\b", re.I)
PROP = re.compile(r"\b(?:with|holding|wielding|carrying)\s+(?:a|an|the|his|her|their|its)\s+", re.I)
CAST = re.compile(r"(?:^|(?<=[.;]\s))([A-Z])\s*:\s+")
PROP_LIST = re.compile(r"\bprops?\s*\(([^)]*)\)", re.I)
STYLE_OF = re.compile(r"\bin the style of\s+", re.I)
STYLE_SUFFIX = re.compile(r"\b([A-Za-z0-9][A-Za-z0-9']*)-style\b", re.I)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'.-]*")
SEGMENT = re.compile(r"[^,;\n]+")

PLACE_NOUNS = {"courtyard", "rooftop", "rooftops", "roof", "street", "alley", "alleyway", "forest", "woods",
               "grove", "arena", "temple", "shrine", "kitchen", "bathroom", "bedroom", "room", "studio",
               "office", "desk", "beach", "city", "field", "meadow", "valley", "canyon", "dojo", "hall",
               "bridge", "cave", "garden", "market", "station", "warehouse", "lot", "gym", "park", "plaza",
               "castle", "battlefield", "desert", "mountain", "cliff", "ship", "train", "subway", "cafe",
               "bar", "classroom", "library", "stage", "ruins", "harbor", "pier", "docks", "lab",
               "laboratory", "hospital", "school", "store", "shop", "mall", "vanity", "countertop", "counter"}
WORLDS = Path(__file__).resolve().parents[1] / "library" / "worlds"


@cache
def place_nouns():
    """PLACE_NOUNS and the last word of every world card's names: a place the library has a card for reads as a place."""
    names = (n for p in sorted(WORLDS.glob("*.yaml")) for n in yaml.safe_load(p.read_text(encoding="utf-8"))["names"])
    return frozenset(PLACE_NOUNS | {n.split()[-1].lower() for n in names})


STOP = {"a", "an", "the", "and", "or", "of", "between", "with", "in", "on", "at", "while", "as", "where",
        "during", "under", "to", "for", "by", "from", "choreographed", "epic", "cinematic", "anime", "ugc",
        "ad", "live", "action", "fight", "fights", "battle", "duel", "scene", "showdown", "clash", "match",
        "short", "quick", "intense", "final", "demo", "video", "clip", "s", "sec", "secs", "second",
        "seconds", "fps", "vs", "vs.", "versus", "product"}


def _number(text):
    lowered = text.lower()
    if lowered in NUMBER_WORDS:
        return NUMBER_WORDS[lowered]
    value = float(text)
    return int(value) if value.is_integer() else value


def _evidence(raw, start, end):
    return {"source": "query", "span": [start, end], "text": raw[start:end]}


def _words(raw, start, end):
    return [(m.start() + start, m.end() + start, m.group().rstrip(".")) for m in WORD.finditer(raw[start:end])]


def _phrase(raw, words):
    """Exact substring covering the kept words; None when nothing remains."""
    if not words:
        return None
    start, end = words[0][0], words[0][0] + len(words[-1][2]) + (words[-1][0] - words[0][0])
    return start, end


def _stop(word):
    return word.lower() in STOP or any(ch.isdigit() for ch in word)


def _segments(raw):
    return [(m.start(), m.end()) for m in SEGMENT.finditer(raw)]


def _segment_of(segments, position):
    return next((s, e) for s, e in segments if s <= position < e)


def _collect(raw):
    found = {field: [] for field in FIELDS}
    for match in DURATION.finditer(raw):
        found["duration_s"].append((_number(match.group(1) or match.group(2)), _evidence(raw, *match.span())))
    for match in FPS.finditer(raw):
        found["fps"].append((_number(match.group(1) or match.group(2)), _evidence(raw, *match.span())))
    for name, pattern in GENRES:
        for match in pattern.finditer(raw):
            found["genre"].append((name, _evidence(raw, *match.span())))
    segments = _segments(raw)
    covered = set()
    for match in PREPOSITION.finditer(raw):
        seg_start, seg_end = _segment_of(segments, match.start())
        words = []
        for word in _words(raw, match.end(), seg_end):
            if word[2].lower() in STOP:
                break
            words.append(word)
        words = words[:5]
        if words and words[-1][2].lower() in place_nouns() and not words[0][2].lower().startswith("style"):
            start, end = _phrase(raw, words)
            found["setting"].append((raw[start:end], _evidence(raw, start, end)))
            covered.add(seg_start)
    for seg_start, seg_end in segments:
        words = _words(raw, seg_start, seg_end)
        if seg_start in covered or not words or words[-1][2].lower() not in place_nouns():
            continue
        if any(_stop(w[2]) and w[2].lower() not in {"a", "an", "the"} for w in words):
            continue
        kept = [w for w in words if w[2].lower() not in {"a", "an", "the"} or w is not words[0]]
        start, end = _phrase(raw, kept)
        found["setting"].append((raw[start:end], _evidence(raw, start, end)))
    for match in VERSUS.finditer(raw):
        seg_start, seg_end = _segment_of(segments, match.start())
        left = []
        for word in reversed(_words(raw, seg_start, match.start())):
            if _stop(word[2]) or len(left) == 3:
                break
            left.insert(0, word)
        right = []
        for word in _words(raw, match.end(), seg_end):
            if _stop(word[2]) or len(right) == 3:
                break
            right.append(word)
        for side in (left, right):
            if side:
                start, end = _phrase(raw, side)
                found["entities_hinted"].append((raw[start:end], _evidence(raw, start, end)))
    for match in PRODUCT.finditer(raw):
        seg_start, _ = _segment_of(segments, match.start())
        left = []
        for word in reversed(_words(raw, seg_start, match.start())):
            if _stop(word[2]) or len(left) == 3:
                break
            left.insert(0, word)
        if left:
            start, end = _phrase(raw, left)
            found["entities_hinted"].append((raw[start:end], _evidence(raw, start, end)))
    for match in CAST.finditer(raw):
        seg_start, seg_end = _segment_of(segments, match.end())
        words = []
        for word in _words(raw, match.end(), seg_end):
            if _stop(word[2]) or len(words) == 3:
                break
            words.append(word)
        if words:
            start, end = _phrase(raw, words)
            found["entities_hinted"].append((raw[start:end], _evidence(raw, start, end)))
    for match in PROP_LIST.finditer(raw):
        start = match.start(1)
        for item in SEGMENT.finditer(match.group(1)):
            words = _words(raw, start + item.start(), start + item.end())
            if words:
                begin, end = _phrase(raw, words)
                found["props_hinted"].append((raw[begin:end], _evidence(raw, begin, end)))
    for match in PROP.finditer(raw):
        _, seg_end = _segment_of(segments, match.end())
        words = []
        for word in _words(raw, match.end(), seg_end):
            if _stop(word[2]) or len(words) == 2:
                break
            words.append(word)
        if words:
            start, end = _phrase(raw, words)
            found["props_hinted"].append((raw[start:end], _evidence(raw, start, end)))
    for match in STYLE_OF.finditer(raw):
        _, seg_end = _segment_of(segments, match.end())
        words = _words(raw, match.end(), seg_end)
        if words:
            start, end = _phrase(raw, words)
            found["style_reference"].append((raw[start:end], _evidence(raw, start, end)))
    for match in STYLE_SUFFIX.finditer(raw):
        found["style_reference"].append((match.group(1), _evidence(raw, *match.span(1))))
    return found


def parse_intent(query, *, genre=None, duration_s=None):
    """Return the S01 Intent Document for one query and optional CLI flags."""
    if not isinstance(query, str):
        raise ContractError("INTENT_INPUT", "Query must be a string")
    if genre is not None and genre not in MODALITIES:
        raise ContractError("INTENT_FLAG", "Genre flag must be a declared modality", genre)
    if duration_s is not None and (isinstance(duration_s, bool) or not isinstance(duration_s, (int, float))
                                   or duration_s <= 0):
        raise ContractError("INTENT_FLAG", "Duration flag must be a positive number", duration_s)
    found = _collect(query)
    parsed, evidence, ambiguous = {}, {}, []
    flags = {"genre": genre, "duration_s": duration_s}
    for field in FIELDS:
        rows = sorted(found[field], key=lambda row: row[1]["span"])
        if field in flags and flags[field] is not None:
            parsed[field], evidence[field] = flags[field], [{"source": "flag"}]
            continue
        if field in SINGLE:
            values = []
            for value, _ in rows:
                if value not in values:
                    values.append(value)
            if len(values) == 1:
                parsed[field], evidence[field] = values[0], [row[1] for row in rows]
            else:
                parsed[field] = None
                if len(values) > 1:
                    ambiguous.append({"field": field, "candidates": [row[1] for row in rows],
                                      "reason": "The query states more than one distinct value."})
        else:
            items, proof = [], []
            for value, row in rows:
                if value.lower() not in {item.lower() for item in items}:
                    items.append(value)
                    proof.append(row)
            parsed[field] = items
            if items:
                evidence[field] = proof
    missing = [MISSING_NAME[field] for field in FIELDS if parsed[field] in (None, [])] + list(NEVER_EXTRACTED)
    extracted = sum(parsed[field] not in (None, []) for field in CORE)
    confidence = "high" if extracted == len(CORE) else "medium" if extracted >= 3 else "low"
    if ambiguous and confidence == "high":
        confidence = "medium"
    return {"step_id": "S01", "band": "L0", "raw_query": query, "flags": flags, "parsed": parsed,
            "evidence": evidence, "missing": missing, "ambiguous": ambiguous, "confidence": confidence}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m planner.intent_parser")
    parser.add_argument("query")
    parser.add_argument("--genre", choices=MODALITIES)
    parser.add_argument("--duration", type=float)
    args = parser.parse_args(argv)
    duration = args.duration
    if duration is not None and duration.is_integer():
        duration = int(duration)
    sys.stdout.write(canonical_json(parse_intent(args.query, genre=args.genre, duration_s=duration)))


if __name__ == "__main__":
    main()
