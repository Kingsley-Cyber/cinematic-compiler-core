"""S17 camera checks. Every rule reads the sealed packet (scene facts + library), never the envelope.

- tiling: shots run in time order from 0 to the scene end with no gap or overlap; ids unique; the first shot opens,
  except in a chained clip (M5.5), where it cuts from the previous clip's last shot under the axis and jump-cut rules;
- coverage: every beat is shown by a shot whose window overlaps it;
- vocabulary: closed values from library/camera_subdivisions.yaml; ids resolve to scene entities/props/surfaces;
- motivation: the ref resolves for its kind and falls inside the shot (beat, entity, contact, effort, geometry,
  causal edge, genre convention);
- axis (180-line): the declared side equals the derived side; a left/right switch between consecutive shots must be
  declared `cross` and the genre must allow crossing; `cross` without a switch is refused;
- aim (F-090, RV-15a, RV-15b): a shot aims at the middle of the extent of the parts its scale shows (the grammar's
  visible_parts) of its target, both axis performers for `midpoint`, from the S13 keys (the packet's `points`); an
  insert aims at its detail, a part of its target or a prop (the packet's `prop_points`), and a detail that names
  neither is refused (CAMERA_VOCABULARY);
- coupling (camera shows what matters): each shown beat's actor is a subject; each contact onset in the window is
  shown (entity is a subject, the part is visible at the scale or is the insert detail); every subject is in frame;
- framing (VERTICAL_FRAMING, F-090, RV-15a, RV-15b): every part the scale shows of each subject (an insert's detail)
  and every framed prop with a point projects inside the frame, up and down as well as across, at every listed beat
  of a static shot and at the first beat of a moving one (S17 does not model a moving camera's path, F-204);
- composition: declared screen placement agrees with the projected screen x of each subject's place: a performer's
  pelvis, the root (owner O72), or its detail in an insert on it; a prop's point (left/right sign and order);
- continuity: no jump cut (same target and scale with an azimuth change under the grammar's minimum) unless the cut
  is declared jump_cut;
- genre: transition, playback, rig, roll, shot length and required intents per library/camera_conventions/<genre>;
- playback (owner O92, F-083, PLAYBACK_RAMP): every shot plays at normal speed (x1): the clip has a fixed length, so
  no slow motion, ramp or freeze fits it;
- hits (owner O92, F-155, RV-57, HIT_HOLD): the shot covering each hit the contacts give (the packet's `hits`,
  planner/hits.py) holds the camera still, with every body present then among its subjects, at no close-up or insert;
- coherence: scale vs frame height, lens perspective vs focal length, rig vs movement and stability, playback speed
  vs treatment, camera blur needs movement, insert needs a detail, focus/relation subjects are framed, a following
  relation needs movement;
- intent: the grammar's intent requirements and the tempo's shot-length range;
- faces (S15 scenes only): a face that carries its beat is shown by a shot listing that beat which frames the entity
  at a scale showing the head, with the face turned toward the camera (under 90 degrees); its stronger side faces the
  camera unless the shot is frontal (within the grammar's frontal_deg).
"""

from planner import library_vocab
from solver import camera_geometry as geometry
from solver import pose_mechanics
from solver.forward_kinematics import part_point

EPSILON = 1e-6
STILL = ("locked", "smooth")  # the grammar's stabilities that hold a frame still (a hit's hold, owner O92)
VALUE_FIELDS = ("framing.scale", "lens.perspective", "focus.depth_of_field", "focus.transition", "movement.kind",
                "movement_quality.easing", "movement_quality.stability", "support.rig", "relation_to_action.mode",
                "position.side", "playback.treatment", "blur.motion_blur", "editing.transition_in", "editing.axis",
                "motivation.kind", "intent")
PLACEMENT_RANK = {"left_third": 0, "center": 1, "right_third": 2}
FOLLOWING = ("lead", "follow", "counter")


def value(shot, field):
    if "." not in field:
        return shot[field]
    group, key = field.split(".", 1)
    return shot[group][key]


def shown(shot, packet, entity, beat=None):
    """{part: point} of the entity that the shot's scale shows (the grammar's visible_parts), at the beat's key (the
    shot's first beat by default); an insert shows its detail alone, when the detail is a part of this entity, its
    target (RV-15b). None without the entity's body points or anything of it to show."""
    beat = beat or min(shot["beats"], key=lambda b: packet["beat_index"][b])
    body = packet.get("points", {}).get(beat, {}).get(entity)
    if body is None:
        return None
    if shot["framing"]["scale"] == "insert":
        detail = shot["framing"]["detail"]
        if not detail or detail in packet["props"] or entity != shot["position"]["target"]:
            return None
        point = part_point(body, detail)
        return {detail: point} if point is not None else None
    parts = packet["grammar"]["visible_parts"].get(shot["framing"]["scale"])
    if parts is None:
        return None
    return {part: body[part] for part in parts if part in body} or None


def framed(shot, packet, subject, beat):
    """{name: point} of one subject the shot must hold in frame at the beat: a performer's shown parts, or a prop's
    point when it has one (F-090, RV-15b)."""
    if subject in packet["props"]:
        point = packet.get("prop_points", {}).get(beat, {}).get(subject)
        return {subject: point} if point is not None else {}
    return shown(shot, packet, subject, beat) or {}


def _detail(shot, packet, beat):
    """The point an insert's detail names at the beat: a part of its target (forward kinematics' contact points) or a
    prop (RV-15b); None when it names neither."""
    detail = shot["framing"]["detail"]
    if detail in packet["props"]:
        return packet.get("prop_points", {}).get(beat, {}).get(detail)
    body = packet.get("points", {}).get(beat, {}).get(shot["position"]["target"])
    return part_point(body, detail) if body and detail else None


def _place(shot, packet, subject, beat):
    """A subject's place on screen: a prop's point; a performer's pelvis, the root (owner O72), or the detail of an
    insert on it (F-090, RV-15a, RV-15b)."""
    if subject in packet["props"]:
        return packet.get("prop_points", {}).get(beat, {}).get(subject)
    detail = shown(shot, packet, subject, beat) if shot["framing"]["scale"] == "insert" else None
    return next(iter(detail.values())) if detail else packet["positions"][beat].get(subject)


def _centre(points):
    """The middle of the points' extent on each axis: the frame centres what it shows (F-090, RV-15a)."""
    return [(min(p[i] for p in points) + max(p[i] for p in points)) / 2 for i in range(3)]


def derive(shot, packet):
    """The shot's camera at its first beat: the aim (the middle of what its scale shows of its target), the camera
    position, the side of the action axis, the field of view, the frame height and each subject's screen x."""
    grammar, sensor = packet["grammar"], packet["grammar"]["sensor_mm"]
    first = min(shot["beats"], key=lambda b: packet["beat_index"][b])
    positions, axis = packet["positions"][first], packet["axis"]
    target = shot["position"]["target"]  # F-090: what the scale shows of the target (RV-15a), an insert's detail (RV-15b)
    if shot["framing"]["scale"] == "insert":
        points = [point for point in [_detail(shot, packet, first)] if point is not None]
    else:
        bodies = [shown(shot, packet, e) for e in (axis if target == "midpoint" else [target])]
        points = [point for body in bodies for point in body.values()] if bodies and all(bodies) else []
    aim_point = _centre(points) if points else geometry.aim(target, positions, axis, grammar["aim_height_m"])
    camera = geometry.camera_position(aim_point, shot["position"]["distance_m"], shot["angle"]["elevation_deg"],
                                      shot["angle"]["azimuth_deg"])
    side = geometry.side(camera, positions[axis[0]], positions[axis[1]], grammar["on_axis_m"]) if len(axis) == 2 else "none"
    focal = shot["lens"]["focal_length_mm"]
    screen = {}
    for subject in shot["framing"]["subjects"]:
        point = _place(shot, packet, subject, first)
        if point is not None:
            screen[subject] = geometry.screen_x(camera, aim_point, point, focal, sensor)
    framed = {e: body for e in shot["framing"]["subjects"] if (body := packet.get("points", {}).get(first, {}).get(e))}
    return {"camera_pos": geometry.rounded(camera), "aim": geometry.rounded(aim_point), "height_m": round(camera[1], 6) + 0.0,
            "side": side, "fov_deg": geometry.fov_degrees(focal, sensor),
            "frame_height_m": geometry.frame_height(shot["position"]["distance_m"], focal, sensor), "screen_x": screen,
            "silhouette": pose_mechanics.silhouette(camera, aim_point, framed)}  # PLAN-009 PM-4 (S-129)


def _framing(shot, packet, geo):
    """VERTICAL_FRAMING (F-090, RV-15a, RV-15b): every part the shot's scale shows of each subject (an insert's detail)
    and every framed prop with a point projects inside the frame, up and down as well as across: at every listed
    beat's key in a static shot, whose camera stands where S17 derived it, and at the first beat's key in a moving one
    (S17 does not model a moving camera's path, F-204)."""
    rows = []
    beats = sorted(shot["beats"], key=lambda b: packet["beat_index"][b])
    detail = shot["framing"]["detail"] if shot["framing"]["scale"] == "insert" else None
    for beat in beats if shot["movement"]["kind"] == "static" else beats[:1]:
        held = {subject if part == subject else f"{subject}'s {part}": point for subject in shot["framing"]["subjects"]
                for part, point in framed(shot, packet, subject, beat).items()}
        if detail in packet["props"] and _detail(shot, packet, beat) is not None:
            held.setdefault(detail, _detail(shot, packet, beat))  # an insert's prop detail, framed or not
        for name, point in sorted(held.items()):
            xy = geometry.screen_xy(geo["camera_pos"], geo["aim"], point, shot["lens"]["focal_length_mm"],
                                    packet["grammar"]["sensor_mm"])
            if xy is None or abs(xy[0]) > 1 + EPSILON or abs(xy[1]) > 1 + EPSILON:
                where = "behind the camera" if xy is None else f"out of frame at screen ({xy[0]:.2f}, {xy[1]:.2f})"
                rows.append(("VERTICAL_FRAMING", f"At {beat}, {name} is {where}", None))
    return rows


def _hit_holds(shots, packet):
    """HIT_HOLD (owner O92, F-155, RV-57): each hit from the contacts is a camera hold on every body present then."""
    fps, out = packet["scene"]["fps"], []
    for t in sorted({h["t"] for h in packet.get("hits", [])}):
        bodies = sorted({b for h in packet["hits"] if h["t"] == t for b in h["bodies"]})
        shot = next((s for s in shots if s["t"] - 0.5 / fps <= t < s["t"] + s["dur"] - 0.5 / fps), None)
        if shot is None:
            out.append(("HIT_HOLD", f"The hit at {t:g} has no shot", None))
            continue
        problems = [f"{x} is not in frame" for x in bodies if x not in shot["framing"]["subjects"]]
        if any(word in shot["framing"]["scale"] for word in ("insert", "close")):
            problems.append(f"a {shot['framing']['scale']} is a close-up")
        if shot["movement"]["kind"] != "static":
            problems.append(f"the camera moves ({shot['movement']['kind']})")
        if shot["movement_quality"]["stability"] not in STILL:  # F-177 (RV-71a): a static shot on a shaky rig moves
            problems.append(f"the camera is {shot['movement_quality']['stability']}")
        if problems:
            out.append(("HIT_HOLD", f"The hit at {t:g} in {shot['id']} is no camera hold on the bodies: "
                        + "; ".join(problems) + " (owner O92)", shot))
    return out


def check(shots, packet):
    """Returns (findings, derived geometry per shot id)."""
    findings = []

    def add(code, message, shot=None, detail=None):
        row = {"code": code, "message": message}
        if shot is not None:
            row["slot"] = shot["id"]
        if detail is not None:
            row["detail"] = detail
        findings.append(row)

    ordered = sorted(shots, key=lambda s: (s["t"], s["id"]))
    findings.extend(_tiling(ordered, packet))
    shown = {b for s in shots for b in s["beats"]}
    for beat in packet["beats"]:
        if beat["id"] not in shown:
            add("CAMERA_COVERAGE", f"Beat {beat['id']} is shown by no shot")
    derived = {}
    for shot in ordered:
        problems = _references(shot, packet)
        for code, message in problems:
            add(code, message, shot)
        if problems:
            continue
        derived[shot["id"]] = geo = derive(shot, packet)
        for code, message, detail in (_motivation(shot, packet) + _coupling(shot, packet, geo) + _composition(shot, geo)
                                      + _framing(shot, packet, geo)
                                      + _genre(shot, packet) + _coherence(shot, packet, geo) + _intent(shot, packet)):
            add(code, message, shot, detail)
        if shot["position"]["side"] != geo["side"]:
            add("CAMERA_AXIS", f"Declared side {shot['position']['side']} but the camera is {geo['side']}", shot)
        if (shot["playback"]["treatment"], shot["playback"]["speed"]) != ("normal", 1):
            add("PLAYBACK_RAMP", f"Playback {shot['playback']['treatment']} x{shot['playback']['speed']:g} in a fixed-length "
                "clip (owner O92: no slow motion or ramps)", shot)
    for code, message, shot in _hit_holds(ordered, packet):
        add(code, message, shot)
    for previous, shot in zip(ordered, ordered[1:], strict=False):
        if previous["id"] in derived and shot["id"] in derived:
            for code, message in _cut(previous, shot, derived, packet):
                add(code, message, shot)
    last = packet.get("chained_last_shot")
    if last and ordered and ordered[0]["id"] in derived:
        carried = {"id": last["id"], "position": {"target": last["target"]}, "framing": {"scale": last["scale"]},
                   "angle": {"azimuth_deg": last["azimuth_deg"]}}
        for code, message in _cut(carried, ordered[0], {**derived, last["id"]: {"side": last["side"]}}, packet):
            add(code, f"Across the clip cut: {message}", ordered[0])
    for code, message, slot in _faces(ordered, derived, packet):
        add(code, message, {"id": slot})
    present = {s["intent"] for s in shots}
    for intent in packet["convention"]["required_intents"]:
        if intent not in present:
            add("CAMERA_GENRE", f"The {packet['scene']['genre']} convention requires a {intent} shot")
    return findings, derived


def _tiling(ordered, packet):
    findings, clock, seen = [], 0.0, set()
    for index, shot in enumerate(ordered):
        if shot["id"] in seen:
            findings.append({"code": "CAMERA_TILING", "message": "Shot ids are unique", "slot": shot["id"]})
        seen.add(shot["id"])
        if abs(shot["t"] - clock) > EPSILON:
            findings.append({"code": "CAMERA_TILING", "message": f"Shot starts at {shot['t']}, expected {round(clock, 6)}",
                             "slot": shot["id"]})
        clock = shot["t"] + shot["dur"]
        opens = index == 0 and "chained_last_shot" not in packet
        if (shot["editing"]["transition_in"] == "open") != opens:
            findings.append({"code": "CAMERA_TILING", "message": "Only the first shot of a first clip opens", "slot": shot["id"]})
    if ordered and abs(clock - packet["scene"]["duration_s"]) > EPSILON:
        findings.append({"code": "CAMERA_TILING", "message": f"Shots end at {round(clock, 6)}, the scene at "
                         f"{packet['scene']['duration_s']}"})
    return findings


def _references(shot, packet):
    problems = []
    vocabulary = {"fields": packet["vocabulary"]}
    for field in VALUE_FIELDS:
        problems += [("CAMERA_VOCABULARY", p) for p in library_vocab.problems(vocabulary, field, value(shot, field), [])]
    for placement in shot["composition"]["placement"].values():
        problems += [("CAMERA_VOCABULARY", p) for p in library_vocab.problems(vocabulary, "composition.placement", placement, [])]
    beats = packet["beat_index"]
    for beat_id in shot["beats"]:
        if beat_id not in beats:
            problems.append(("CAMERA_COVERAGE", f"Beat {beat_id} does not exist"))
        else:
            beat = packet["beats"][beats[beat_id]]
            if beat["t"] >= shot["t"] + shot["dur"] - EPSILON or beat["t"] + beat["dur"] <= shot["t"] + EPSILON:
                problems.append(("CAMERA_COVERAGE", f"Beat {beat_id} is outside the shot window"))
    subjects = set(packet["entities"]) | set(packet["props"])
    framed = shot["framing"]["subjects"]
    problems += [("CAMERA_VOCABULARY", f"Subject {s} is not a scene entity or prop") for s in framed if s not in subjects]
    target = shot["position"]["target"]
    if target != "midpoint" and target not in packet["entities"]:
        problems.append(("CAMERA_VOCABULARY", f"Position target {target} is not an entity or midpoint"))
    detail = shot["framing"]["detail"]
    if shot["framing"]["scale"] == "insert" and detail is not None and detail not in packet["props"] and not any(
            part_point(bodies.get(target), detail) for bodies in packet.get("points", {}).values() if bodies.get(target)):
        problems.append(("CAMERA_VOCABULARY", f"Insert detail {detail} is neither a part of {target} nor a prop (RV-15b)"))
    if target == "midpoint" and len(packet["axis"]) != 2:
        problems.append(("CAMERA_VOCABULARY", "midpoint needs two entities"))
    for key in shot["composition"]["placement"]:
        if key not in framed:
            problems.append(("CAMERA_VOCABULARY", f"Placed subject {key} is not framed"))
    anchor = shot["composition"]["depth_anchor"]
    if anchor is not None and anchor not in set(packet["surfaces"]) | set(packet["props"]):
        problems.append(("CAMERA_VOCABULARY", f"Depth anchor {anchor} is not a surface or prop"))
    parts = {p for s in framed for p in packet["entities"].get(s, {}).get("parts", [])}
    for item in shot["blur"]["affected"]:
        if item not in set(framed) | parts:
            problems.append(("CAMERA_VOCABULARY", f"Blurred {item} is not a framed subject or one of its parts"))
    return problems


def _window(shot, packet, t):
    end = shot["t"] + shot["dur"]
    last = abs(end - packet["scene"]["duration_s"]) <= EPSILON
    return shot["t"] - EPSILON <= t < end - EPSILON or (last and abs(t - end) <= EPSILON)


def _motivation(shot, packet):
    kind, ref = shot["motivation"]["kind"], shot["motivation"]["ref"]
    beats = set(shot["beats"])
    if kind == "beat_type":
        ok = ref in beats
    elif kind == "entity_focus":
        ok = ref in shot["framing"]["subjects"] and ref in packet["entities"]
    elif kind == "contact_event":
        ok = any(c["id"] == ref and _window(shot, packet, c["t"]) for c in packet["contacts"])
    elif kind == "effort_quality":
        ok = any(e["id"] == ref and e["t"] < shot["t"] + shot["dur"] - EPSILON and e["end"] > shot["t"] + EPSILON
                 for e in packet["efforts"])
    elif kind == "spatial_geometry":
        ok = ref in packet["surfaces"] or ref in packet["props"]
    elif kind == "narrative_intent":
        ok = any(e["id"] == ref and (e["from"] in beats or e["to"] in beats) for e in packet["causal"])
    else:
        ok = ref in {c["id"] for c in packet["convention"]["conventions"]}
    return [] if ok else [("CAMERA_MOTIVATION", f"Motivation {kind}:{ref} does not resolve inside this shot", None)]


def _coupling(shot, packet, geo):
    rows = []
    framed, scale = shot["framing"]["subjects"], shot["framing"]["scale"]
    visible = [shot["framing"]["detail"]] if scale == "insert" else packet["grammar"]["visible_parts"][scale]
    for beat_id in shot["beats"]:
        actor = packet["beats"][packet["beat_index"][beat_id]]["actor"]
        if actor not in framed:
            rows.append(("CAMERA_COUPLING", f"{beat_id} actor {actor} is not framed", None))
    for contact in packet["contacts"]:
        if _window(shot, packet, contact["t"]):
            if contact["entity"] not in framed or contact["part"] not in visible:
                rows.append(("CAMERA_COUPLING", f"Contact {contact['id']} ({contact['entity']} {contact['part']}) is not "
                             f"visible in a {scale} shot", None))
    for subject, x in geo["screen_x"].items():
        if x is None or abs(x) > 1 + EPSILON:
            rows.append(("CAMERA_COUPLING", f"Subject {subject} is out of frame", x))
    return rows


def _composition(shot, geo):
    rows, placed = [], shot["composition"]["placement"]
    for subject, placement in placed.items():
        x = geo["screen_x"].get(subject)
        if x is None:
            continue
        if (placement == "left_third" and x >= 0) or (placement == "right_third" and x <= 0) or (placement == "center"
                                                                                                and abs(x) > 0.5):
            rows.append(("CAMERA_COMPOSITION", f"{subject} placed {placement} but projects at x={x}", x))
    for a in placed:
        for b in placed:
            if PLACEMENT_RANK[placed[a]] < PLACEMENT_RANK[placed[b]] and geo["screen_x"].get(a) is not None \
                    and geo["screen_x"].get(b) is not None and geo["screen_x"][a] >= geo["screen_x"][b]:
                rows.append(("CAMERA_COMPOSITION", f"{a} is placed left of {b} but projects right of it", None))
    return rows


def _genre(shot, packet):
    rows, convention = [], packet["convention"]
    for field, allowed in (("editing.transition_in", "transitions"), ("playback.treatment", "playback"), ("support.rig", "rigs")):
        if value(shot, field) not in convention[allowed]:
            rows.append(("CAMERA_GENRE", f"{field}={value(shot, field)} is not used in {convention['genre']}", None))
    if abs(shot["angle"]["roll_deg"]) > convention["max_roll_deg"]:
        rows.append(("CAMERA_GENRE", f"Roll beyond {convention['max_roll_deg']} degrees", None))
    low, high = convention["shot_duration_s"]
    if not low - EPSILON <= shot["dur"] <= high + EPSILON:
        rows.append(("CAMERA_GENRE", f"Shot length outside {low}-{high} s", None))
    return rows


def _coherence(shot, packet, geo):
    rows, grammar = [], packet["grammar"]
    scale = shot["framing"]["scale"]
    low, high = grammar["scale_frame_height_m"][scale]
    if not low <= geo["frame_height_m"] <= high:
        rows.append(("CAMERA_COHERENCE", f"A {scale} needs a frame height of {low}-{high} m", geo["frame_height_m"]))
    low, high = grammar["lens_perspective_mm"][shot["lens"]["perspective"]]
    if not low <= shot["lens"]["focal_length_mm"] <= high:
        rows.append(("CAMERA_COHERENCE", f"{shot['lens']['perspective']} perspective needs {low}-{high} mm", None))
    rig, kind = shot["support"]["rig"], shot["movement"]["kind"]
    if kind not in grammar["rig_movements"][rig]:
        rows.append(("CAMERA_COHERENCE", f"A {rig} cannot {kind}", None))
    if shot["movement_quality"]["stability"] not in grammar["rig_stability"][rig]:
        rows.append(("CAMERA_COHERENCE", f"A {rig} is not {shot['movement_quality']['stability']}", None))
    treatment, speed = shot["playback"]["treatment"], shot["playback"]["speed"]
    expected = {"normal": speed == 1, "slow": 0 < speed < 1, "fast": speed > 1, "freeze": speed == 0, "ramp": speed != 1}
    if not expected[treatment]:
        rows.append(("CAMERA_COHERENCE", f"Playback {treatment} does not match speed {speed}", None))
    if shot["blur"]["motion_blur"] in ("camera", "both") and kind == "static":
        rows.append(("CAMERA_COHERENCE", "Camera motion blur needs camera movement", None))
    if (scale == "insert") != (shot["framing"]["detail"] is not None):
        rows.append(("CAMERA_COHERENCE", "An insert names its detail; other scales do not", None))
    framed = shot["framing"]["subjects"]
    for field in ("focus.target", "relation_to_action.subject"):
        if value(shot, field) not in framed:
            rows.append(("CAMERA_COHERENCE", f"{field}={value(shot, field)} is not framed", None))
    if shot["relation_to_action"]["mode"] in FOLLOWING and kind == "static":
        rows.append(("CAMERA_COHERENCE", f"A camera that {shot['relation_to_action']['mode']}s must move", None))
    return rows


def _intent(shot, packet):
    rows, intent = [], shot["intent"]
    focus = shot["focus"]["target"]
    facts = {"focus.target_kind": "entity" if focus in packet["entities"] else "prop" if focus in packet["props"] else "other"}
    for rule in packet["grammar"]["intents"].get(intent, []):
        current = facts[rule["field"]] if rule["field"] in facts else value(shot, rule["field"])
        if ("in" in rule and current not in rule["in"]) or ("not_in" in rule and current in rule["not_in"]):
            rows.append(("CAMERA_INTENT", f"A {intent} shot needs {rule['field']} "
                         f"{'in' if 'in' in rule else 'not in'} {rule.get('in', rule.get('not_in'))}", current))
    low, high = packet["tempo"]["shot_duration_s"][intent]
    if not low - EPSILON <= shot["dur"] <= high + EPSILON:
        rows.append(("CAMERA_INTENT", f"A {intent} shot lasts {low}-{high} s", shot["dur"]))
    return rows


def _cut(previous, shot, derived, packet):
    rows = []
    sides = {derived[previous["id"]]["side"], derived[shot["id"]]["side"]}
    switched = sides == {"left", "right"}
    crossing = shot["editing"]["axis"] == "cross"
    if switched and not crossing:
        rows.append(("CAMERA_AXIS", "The cut switches sides of the action axis without declaring cross"))
    if crossing and not switched:
        rows.append(("CAMERA_AXIS", "cross is declared but the camera stays on its side"))
    if crossing and packet["convention"]["cross_line"] == "forbidden":
        rows.append(("CAMERA_GENRE", f"{packet['scene']['genre']} never crosses the axis"))
    same = (previous["position"]["target"] == shot["position"]["target"]
            and previous["framing"]["scale"] == shot["framing"]["scale"])
    change = geometry.azimuth_change(previous["angle"]["azimuth_deg"], shot["angle"]["azimuth_deg"])
    if same and change < packet["grammar"]["min_cut_angle_deg"] and shot["editing"]["transition_in"] != "jump_cut":
        rows.append(("CAMERA_CONTINUITY", f"Jump cut: same target and scale with only {change} degrees between shots"))
    return rows


def _faces(shots, derived, packet):
    """Faces that carry their beat must be seen, and their stronger side must face the camera."""
    rows = []
    grammar = packet["grammar"]
    for face in packet.get("faces", []):
        if face["salience"] != "carries_beat":
            continue
        seen, sides_shown = False, set()
        for shot in shots:
            geo = derived.get(shot["id"])
            scale = shot["framing"]["scale"]
            head = (scale != "insert" and "head" in grammar["visible_parts"][scale]) or shot["framing"]["detail"] == "head"
            if geo is None or face["beat"] not in shot["beats"] or face["entity"] not in shot["framing"]["subjects"] or not head:
                continue
            first = min(shot["beats"], key=lambda b: packet["beat_index"][b])
            spot = packet["positions"][first][face["entity"]]
            to_camera = geometry.heading_to(spot, geo["camera_pos"])
            off = geometry.azimuth_change(face["head_heading_deg"], to_camera)
            if off >= 90:
                continue
            seen = True
            if off <= grammar["frontal_deg"]:
                sides_shown |= {"left", "right"}
            else:
                left_heading = face["head_heading_deg"] + 90  # the performer's left (+X when facing +Z)
                sides_shown.add("left" if geometry.azimuth_change(left_heading, to_camera) < 90 else "right")
        if not seen:
            rows.append(("FACE_FRAMING", f"{face['entity']}'s face carries {face['beat']} but no shot shows it turned "
                         "toward the camera", face["slot"]))
        elif face["dominant_sides"] and not set(face["dominant_sides"]) <= sides_shown:
            rows.append(("FACE_ASYMMETRY_VISIBLE", f"{face['entity']}'s stronger side ({', '.join(face['dominant_sides'])}) "
                         f"is turned away from every shot of {face['beat']}", face["slot"]))
    return rows
