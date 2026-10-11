"""S14 facial checks and words. Every rule reads the sealed packet (scene facts + face libraries).

- FACIAL_COVERAGE: one face per slot, none for a slot that does not exist.
- FACE_PROFILE_MISSING: every entity with a face has a face profile on its archetype card.
- FACS_AU: units come from library/facs_action_units.yaml, each once; the even form is not used for a one-side-only
  unit and the per-side form not for a both-sides-only unit; a per-side unit has at least one side and its sides differ.
- FACS_ASYMMETRY: the declared magnitude is the step difference between the sides (absent 0, A 1 ... E 5) and the
  dominant side is the stronger one; a unit present on both sides stays within its max_step_difference; a unit on
  one side only needs a laterality that allows it.
- FACS_PATTERN: a named pattern exists; its units take the declared forms, its forbidden units are absent, same-side
  patterns share one dominant side, and valence/arousal fall in its ranges.
- FACS_OCCLUSION: an active unit's region is visible in the entity's face profile.
- FACS_CONTRADICTION: no unit is both active and inactive; inactive units exist.
- VALENCE_RANGE: the label exists and its family is in the archetype's emotional range; a genuine display sits
  inside the label's valence and arousal ranges.
- FACIAL_KINEMATIC: a genuine display with arousal >= 0.5 needs kinematic tension moderate or high; arousal <= -0.5
  needs relaxed or moderate (draft thresholds; masked, suppressed and posed faces may disagree with the body).
- FACIAL_GAZE: the target is a scene entity or prop other than the face's owner, camera, or none.
- FACIAL_TRANSITION: onset frames fit in the beat; rapid <= 0.5 s, slow > 0.5 s; hold keeps the previous face's units
  in 0 frames; micro reaches its peak within 0.26 s and only leaks a masked or suppressed face (Yan et al. 2013).
- FACIAL_WORDS: the description carries no unit codes (the render is words only, owner F4).
"""

import json
import re

RANK = {None: 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
HIGH_AROUSAL, LOW_AROUSAL = 0.5, -0.5
MICRO_ONSET_S, RAPID_ONSET_S = 0.26, 0.5
CODE = re.compile(r"\bAU\s?\d", re.I)


def form(unit):
    if unit["bilateral"]:
        return "symmetric"
    return "unilateral" if None in (unit["left_intensity"], unit["right_intensity"]) else "asymmetric"


def sides(unit):
    if unit["bilateral"]:
        return unit["intensity"], unit["intensity"]
    return unit["left_intensity"], unit["right_intensity"]


def check(faces, packet):
    findings = []

    def add(code, message, slot, detail=None):
        row = {"code": code, "message": message, "slot": slot}
        if detail is not None:
            row["detail"] = detail
        findings.append(row)

    slots = {s["slot"]: s for s in packet["slots"]}
    seen = {}
    for face in faces:
        seen[face["slot"]] = seen.get(face["slot"], 0) + 1
    for slot_id in slots:
        if seen.get(slot_id, 0) != 1:
            add("FACIAL_COVERAGE", "Every slot needs exactly one face", slot_id)
    units, patterns = packet["units"], {p["id"]: p for p in packet["patterns"]}
    labels = {label["id"]: label for label in packet["emotions"]["labels"]}
    previous = {}
    for face in sorted((f for f in faces if f["slot"] in slots), key=lambda f: (slots[f["slot"]]["t"], f["slot"])):
        slot = slots[face["slot"]]
        sid, entity = face["slot"], slot["entity"]
        profile = packet["entities"][entity]["face_profile"]
        if profile is None:
            add("FACE_PROFILE_MISSING", f"{entity} has no face_profile on its archetype card", sid)
        active = [u["au"] for u in face["aus"]]
        for repeated in sorted({a for a in active if active.count(a) > 1}):
            add("FACS_AU", f"{repeated} is listed twice", sid)
        for unit in face["aus"]:
            spec = units.get(unit["au"])
            if spec is None:
                add("FACS_AU", f"{unit['au']} is not in the action-unit library", sid)
                continue
            shape = form(unit)
            if shape == "symmetric" and spec["laterality"] == "unilateral_only":
                add("FACS_AU", f"{unit['au']} only happens on one side", sid)
            if shape != "symmetric":
                left, right = sides(unit)
                if left is None and right is None:
                    add("FACS_AU", f"{unit['au']} needs at least one side", sid)
                    continue
                if left == right:
                    add("FACS_AU", f"{unit['au']} has equal sides: write it in the even form", sid)
                if spec["laterality"] == "bilateral_only":
                    add("FACS_ASYMMETRY", f"{unit['au']} cannot differ between the sides", sid)
                magnitude = abs(RANK[left] - RANK[right])
                stronger = "left" if RANK[left] > RANK[right] else "right"
                if unit["asymmetry"]["magnitude"] != magnitude or unit["asymmetry"]["dominant_side"] != stronger:
                    add("FACS_ASYMMETRY", f"{unit['au']} declares {unit['asymmetry']['dominant_side']} by "
                        f"{unit['asymmetry']['magnitude']}, the sides give {stronger} by {magnitude}", sid)
                if shape == "asymmetric" and magnitude > packet["max_step_difference"].get(unit["au"], 0):
                    add("FACS_ASYMMETRY", f"{unit['au']} sides differ by {magnitude} steps, bound "
                        f"{packet['max_step_difference'].get(unit['au'], 0)}", sid)
            if profile is not None and spec["region"] not in profile["visible_regions"]:
                add("FACS_OCCLUSION", f"{unit['au']} ({spec['region']}) is hidden by {entity}'s costume", sid)
        findings += [{"code": c, "message": m, "slot": sid} for c, m in _patterns(face, patterns)]
        for inactive in face["inactive_aus"]:
            if inactive not in units:
                add("FACS_CONTRADICTION", f"{inactive} is not in the action-unit library", sid)
            if inactive in active:
                add("FACS_CONTRADICTION", f"{inactive} is both active and listed as absent", sid)
        label = labels.get(face["emotion_label"])
        if label is None:
            add("VALENCE_RANGE", f"Emotion label {face['emotion_label']} is not in the library", sid)
        else:
            if profile is not None and label["family"] not in profile["emotional_range"]:
                add("VALENCE_RANGE", f"{entity} does not show {label['family']}", sid)
            if face["display_rule"] == "genuine" and not (label["valence"][0] <= face["valence"] <= label["valence"][1]
                                                          and label["arousal"][0] <= face["arousal"] <= label["arousal"][1]):
                add("VALENCE_RANGE", f"A genuine {label['id']} needs valence {label['valence']} and arousal "
                    f"{label['arousal']}", sid)
        tension = slot["kinematic"]["tension"]
        if face["display_rule"] == "genuine":
            if face["arousal"] >= HIGH_AROUSAL and tension not in ("moderate", "high"):
                add("FACIAL_KINEMATIC", f"A highly activated genuine face on a {tension} body", sid)
            if face["arousal"] <= LOW_AROUSAL and tension not in ("relaxed", "moderate"):
                add("FACIAL_KINEMATIC", f"A very calm genuine face on a {tension} body", sid)
        target = face["gaze_target"]
        if target == entity or target not in set(packet["entities"]) | set(packet["props"]) | {"camera", "none"}:
            add("FACIAL_GAZE", f"Gaze target {target} is not another scene entity or prop, camera or none", sid)
        findings += [{"code": c, "message": m, "slot": sid} for c, m in _transition(face, previous.get(entity), slot,
                                                                                    packet["fps"])]
        if CODE.search(face["description"]):
            add("FACIAL_WORDS", "Describe the face in words; unit codes stay in the aus list", sid)
        previous[entity] = face
    return findings


def _patterns(face, patterns):
    rows = []
    named = {u["asymmetry"]["pattern"] for u in face["aus"] if not u["bilateral"] and u["asymmetry"]["pattern"]}
    by_au = {u["au"]: u for u in face["aus"]}
    for name in sorted(named):
        pattern = patterns.get(name)
        if pattern is None:
            rows.append(("FACS_PATTERN", f"Pattern {name} is not in the asymmetry library"))
            continue
        for au, shape in pattern["units"].items():
            unit = by_au.get(au)
            if unit is None:
                rows.append(("FACS_PATTERN", f"{name} needs {au}"))
            elif shape != "any" and form(unit) != shape:
                rows.append(("FACS_PATTERN", f"{name} needs {au} {shape}, found {form(unit)}"))
        for au in pattern["forbidden"]:
            if au in by_au:
                rows.append(("FACS_PATTERN", f"{name} excludes {au}"))
        if pattern["same_side"]:
            dominant = {u["asymmetry"]["dominant_side"] for au in pattern["units"] if (u := by_au.get(au)) and not u["bilateral"]}
            if len(dominant) > 1:
                rows.append(("FACS_PATTERN", f"{name} keeps its units on one side"))
        if not (pattern["valence"][0] <= face["valence"] <= pattern["valence"][1]
                and pattern["arousal"][0] <= face["arousal"] <= pattern["arousal"][1]):
            rows.append(("FACS_PATTERN", f"{name} needs valence {pattern['valence']} and arousal {pattern['arousal']}"))
    return rows


def _transition(face, previous, slot, fps):
    rows, seconds = [], face["onset_frames"] / fps
    if seconds > slot["dur"] + 1e-9:
        rows.append(("FACIAL_TRANSITION", "The onset is longer than the beat"))
    if face["onset"] == "rapid" and seconds > RAPID_ONSET_S:
        rows.append(("FACIAL_TRANSITION", f"A rapid onset reaches its peak within {RAPID_ONSET_S} s"))
    if face["onset"] == "slow" and seconds <= RAPID_ONSET_S:
        rows.append(("FACIAL_TRANSITION", f"A slow onset takes longer than {RAPID_ONSET_S} s"))
    if face["onset"] == "hold" and (previous is None or face["onset_frames"] != 0
                                    or _units(previous) != _units(face)):
        rows.append(("FACIAL_TRANSITION", "A hold keeps the previous face's units unchanged, in 0 frames"))
    if face["onset"] == "micro" and (seconds > MICRO_ONSET_S or face["display_rule"] not in ("masked", "suppressed")):
        rows.append(("FACIAL_TRANSITION", f"A micro-expression peaks within {MICRO_ONSET_S} s and leaks a masked or "
                     "suppressed face"))
    return rows


def _units(face):
    return sorted(json.dumps(u, sort_keys=True) for u in face["aus"])


def _band(value, bands):
    return next(b["words"] for b in bands if value <= b["max"] + 1e-9)


def words(face, packet):
    """The render's words for one face: no unit codes, no numbers (owner F4)."""
    units, scale, emotions = packet["units"], packet["intensity_scale"], packet["emotions"]
    described = []
    for unit in face["aus"]:
        phrase = units[unit["au"]]["words"]
        left, right = sides(unit)
        if unit["bilateral"]:
            described.append(f"{phrase} ({scale[left]})")
        elif left is None or right is None:
            side, level = ("their left", left) if right is None else ("their right", right)
            described.append(f"{phrase} on {side} side only ({scale[level]})")
        else:
            described.append(f"{phrase} ({scale[left]} on their left, {scale[right]} on their right)")
    target = face["gaze_target"]
    gaze = {"camera": "looking into the lens", "none": "gaze unfocused"}.get(target, f"eyes on {target}")
    label = face["emotion_label"].replace("_", " ")
    return {"face": described, "not": [units[a]["absent"] for a in face["inactive_aus"] if a in units],
            "feeling": f"{label}, {_band(face['valence'], emotions['bands']['valence'])} and "
                       f"{_band(face['arousal'], emotions['bands']['arousal'])}",
            "display": emotions["display_rules"][face["display_rule"]], "gaze": gaze}
