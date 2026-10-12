"""S17 pass (band L6, projection, authored frame parts): render the envelope into the full LBN-2.x layout.

Authored: frame-part directives (impact, smear, speedlines, holds, fx, ink). Checks: impacts sit on contact onsets or
impact shots, and one time per hit (IMPACT_CONTACT_SYNC, O23); a smear names one subject and, for a body, one part
(smear only on the declared limb or prop) and sits on a sudden effort of that body or an event of that prop;
speedlines likewise; holds sit on beat boundaries; fx inside the scene; a hold on an impact frame (a hit) is a camera
hold on every body present, never a close-up (HIT_HOLD, owner O92, R-21); and the projection's coverage is complete
(owner invariant no_render_compression).
Derived: the render node (renderers/anime_renderer.py;
ugc_renderer.py for ugc_ad): target, variant, text, sha256, coverage, frame parts; and (M8, owner O1-O3) `prose`, the
knowledge DAG's structured-prose prompts in four movement modes (renderers/prose_renderer.py).
"""

from compiler.authoring import run_authored, seal
from planner import hits
from planner.dependency_graph import ROOT, load
from planner.dynamic_beat_validator import vanish_windows
from renderers import anime_renderer, live_renderer, prose_renderer, ugc_renderer

NODE, STEP = "render", "S17"
RENDERERS = {"ugc_ad": ugc_renderer, "live_action": live_renderer}  # anime uses the anime LBN layout
PLAN_SCHEMA = ROOT / "schemas" / "graphs" / "frame_parts_plan.schema.json"
PROMPT = ROOT / "planner" / "prompts" / "frame_parts.txt"
ONSETS = ("touch", "possess", "support")


def renderer(envelope):
    return RENDERERS.get(envelope["scene"]["genre"], anime_renderer)


def prepare(envelope):
    scene = envelope["scene"]
    beats = sorted(envelope["nodes"]["beats"]["items"], key=lambda b: (b["t"], b["id"]))
    return seal({
        "step_id": STEP, "band": "L6", "kind": "frame_parts_plan", "schema": "urn:cinematic-compiler:schema:frame_parts_plan:1.0",
        "instructions": PROMPT.read_text(encoding="utf-8"),
        "scene": {"genre": scene["genre"], "fps": scene["fps"], "duration_s": scene["duration_s"]},
        "beats": [{k: b[k] for k in ("id", "t", "dur", "actor", "label", "action")} for b in beats],
        "entities": {e["id"]: e["parts"] for e in envelope["nodes"]["entities"]["items"]},
        "props": sorted(p["id"] for p in envelope["nodes"]["props"]["items"]),
        "contacts": [{"id": c["id"], "t": c["t"], "contact_type": c["contact_type"], "a": c["a"]["id"], "b": c["b"]["id"],
                      "part": c["body_part"]} for c in envelope["nodes"]["contacts"]["items"]],
        "prop_changes": [{"subject": s["subject"]["id"], "t": s["t"]} for s in envelope["nodes"]["states"]["items"]
                         if s["subject"]["kind"] == "prop"],
        "efforts": [{k: e[k] for k in ("id", "actor", "t", "end")} | {"time": e["effort"]["time"]}
                    for e in envelope["nodes"]["efforts"]["items"]],
        "shots": [{"id": s["id"], "t": s["t"], "dur": s["dur"], "intent": s["intent"], "scale": s["framing"]["scale"]}
                  for s in envelope["nodes"]["camera"]["items"]]})


def _near(a, b, fps):
    return abs(a - b) <= 0.5 / fps + 1e-9


def _event(subject, t0, t1, packet):
    """A sudden effort of a body, or a contact/state change of a prop, overlapping the window."""
    if subject in packet["entities"]:
        return any(e["actor"] == subject and e["time"] == "sudden" and e["t"] < t1 and e["end"] > t0 for e in packet["efforts"])
    return any(t0 <= c["t"] <= t1 for c in packet["contacts"] if subject in (c["a"], c["b"])) or any(
        t0 <= s["t"] <= t1 for s in packet["prop_changes"] if s["subject"] == subject)


def impact_sync(envelope, impacts):
    """IMPACT_CONTACT_SYNC (owner O23, backlog M9-02): one time per hit. Every impact frame has a touch, or a support or
    possess that starts, on that frame (a body hitting a surface counts: interpretation, e.g. a crash or a slam into a
    pillar; so does a catch or a blade lodging, O93); every strike (prose_renderer.strike_contacts) lands on an impact
    frame. The fix is upstream: the contact's `at` in the S04 plan, or the impact frame here."""
    fps = envelope["scene"]["fps"]
    contacts = envelope["nodes"]["contacts"]["items"]
    onsets = [c["t"] for c in contacts if c["contact_type"] in ("touch", "support", "possess")]
    findings = [{"code": "IMPACT_CONTACT_SYNC", "message": f"Impact at {t} has no touch or support onset on that frame"}
                for t in impacts if not any(_near(t, x, fps) for x in onsets)]
    strikes = prose_renderer.strike_contacts(envelope, impacts)
    for c in contacts:
        if c["id"] in strikes and not any(_near(c["t"], t, fps) for t in impacts):
            findings.append({"code": "IMPACT_CONTACT_SYNC", "message": f"Strike {c['id']} at {c['t']} lands on no impact frame",
                             "detail": [c["a"]["id"], c["body_part"], c["b"]["id"]]})
    return findings


def hit_hold(envelope, frame):
    """HIT_HOLD (owner O92, R-21, F-083, F-155): every hit from the contacts (planner/hits.py) and every hold on an
    impact frame is a hit, and the shot covering it holds the camera still (static) with every body present at that
    instant in frame (a vanished body is not, O18), at no close-up or insert, whatever S17 holds. The fix is upstream,
    in the S16 shot; playback is S16's PLAYBACK_RAMP."""
    fps = envelope["scene"]["fps"]
    gone = vanish_windows(envelope["nodes"]["beats"]["items"])
    findings = []
    for t in hits.hold_times(envelope, frame):
        shot = next((s for s in envelope["nodes"]["camera"]["items"]
                     if s["t"] - 0.5 / fps <= t < s["t"] + s["dur"] - 0.5 / fps), None)
        present = sorted(e["id"] for e in envelope["nodes"]["entities"]["items"]
                         if not any(actor == e["id"] and start < t - 1e-9 and (back is None or t < back - 1e-9)
                                    for actor, _, start, back in gone))
        if shot is None:
            findings.append({"code": "HIT_HOLD", "message": f"The hit at {t} has no shot"})
            continue
        problems = [f"{x} is not in frame" for x in present if x not in shot["framing"]["subjects"]]
        if any(word in shot["framing"]["scale"] for word in prose_renderer.CLOSE):
            problems.append(f"a {shot['framing']['scale']} is a close-up")
        if shot["movement"]["kind"] != "static":
            problems.append(f"the camera moves ({shot['movement']['kind']})")
        if problems:
            findings.append({"code": "HIT_HOLD", "message": f"The hit at {t} in {shot['id']} is no camera hold on the bodies: "
                             + "; ".join(problems) + " (owner O92)", "slot": shot["id"]})
    return findings


def check(document, packet, envelope=None):
    findings = []
    frame = document["frame_parts"]
    fps, end = packet["scene"]["fps"], packet["scene"]["duration_s"]
    onsets = [c["t"] for c in packet["contacts"] if c["contact_type"] in ONSETS]
    impact_shots = [s["t"] for s in packet["shots"] if s["intent"] == "impact"]
    boundaries = sorted({b["t"] for b in packet["beats"]} | {round(b["t"] + b["dur"], 6) for b in packet["beats"]})
    subjects = set(packet["entities"]) | set(packet["props"])
    for t in frame["impact"]:
        if not any(_near(t, x, fps) for x in onsets + impact_shots):
            findings.append({"code": "FRAME_IMPACT", "message": f"Impact at {t} is no contact onset or impact shot"})
    for kind in ("smear", "speedlines"):
        for item in frame[kind]:
            label = f"{kind} {item['t0']}-{item['t1']} {item['subject']}"
            if not 0 <= item["t0"] < item["t1"] <= end or item["subject"] not in subjects:
                findings.append({"code": "FRAME_" + kind.upper(), "message": f"{label}: window or subject is not in the scene"})
                continue
            if kind == "smear":
                body = item["subject"] in packet["entities"]
                if body and item["part"] not in packet["entities"][item["subject"]]:
                    findings.append({"code": "FRAME_SMEAR", "message": f"{label}: a body smear names one of its parts"})
                if not body and item["part"] is not None:
                    findings.append({"code": "FRAME_SMEAR", "message": f"{label}: a prop smear names no part"})
            if not _event(item["subject"], item["t0"], item["t1"], packet):
                findings.append({"code": "FRAME_" + kind.upper(), "message": f"{label}: nothing fast happens to the subject"})
    for hold in frame["holds"]:
        if not any(_near(hold["t"], b, fps) for b in boundaries):
            findings.append({"code": "FRAME_HOLD", "message": f"Hold at {hold['t']} is not on a beat boundary"})
    for fx in frame["fx"]:
        if not 0 <= fx["t"] <= end or (fx["t_end"] is not None and not fx["t"] < fx["t_end"] <= end):
            findings.append({"code": "FRAME_FX", "message": f"fx at {fx['t']} is outside the scene"})
    if envelope is not None:
        findings += impact_sync(envelope, frame["impact"]) + hit_hold(envelope, frame)
        coverage = renderer(envelope).render(envelope, frame)["coverage"]
        if not coverage["complete"]:
            missing = {g: row["missing"] for g, row in coverage["groups"].items() if row["missing"]}
            findings.append({"code": "RENDER_COVERAGE", "message": "no_render_compression: the render misses items",
                             "detail": {"groups": missing, "constraints": coverage["constraints"]["missing"]}})
    return findings


def build(envelope, document, packet):
    result = renderer(envelope).render(envelope, document["frame_parts"])
    prose = prose_renderer.render_all(envelope, document["frame_parts"], result["labels"])
    return {"/nodes/render": [{"id": "render", **result, "frame_parts": document["frame_parts"], "prose": prose}]}


def run(envelope, document, *, order=None):
    return run_authored(envelope, document, node_id=NODE, step_id=STEP, prepare=prepare, schema_path=PLAN_SCHEMA,
                        check=lambda doc, packet: check(doc, packet, envelope), build=build, order=order or load())
