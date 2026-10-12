"""In-between keys (ADR-O109, RV-59f): one entity's pose between two of its keys, checked like a key at S13, carried on
the follows edge it splits, run through by the declared interpolation, and placed by the re-block solver."""

import copy
import json

import pytest
from conftest import ROOT
from scenes import courtyard, courtyard_plans

from compiler.passes.derived import p13_motion
from solver import forward_kinematics, interpolation

pytestmark = pytest.mark.unit
PLAN = courtyard_plans()["motion"]
ENVELOPE = courtyard("bartenieff")
PACKET = p13_motion.prepare(ENVELOPE)


def _between(t=3.0, **change):
    """The acrobat's pose the declared interpolation gives at t (between its keys at 2.6 and 3.6, through the plan's own
    in-betweens), as an in-between."""
    slots = {s["slot"]: s for s in PACKET["slots"]}
    keys = sorted(({**k, "t": slots[k["slot"]]["t"]} for k in PLAN["keys"] if k["slot"].startswith("acrobat@")),
                  key=lambda k: k["t"])
    own = interpolation.sequences({"acrobat": keys}, [b for b in PLAN.get("inbetweens", []) if b["entity"] == "acrobat"])
    a = max((k for k in own["acrobat"] if k["t"] < t), key=lambda k: k["t"])
    b = min((k for k in own["acrobat"] if k["t"] > t), key=lambda k: k["t"])
    pose = interpolation.pose(a, b, t)
    between = {"entity": "acrobat", "t": t, "name": "kick_rising", "pos": [round(v, 6) for v in pose["pos"]],
               "rot": [round(v, 6) for v in pose["rot"]],
               "bones": {j: [round(v, 6) for v in pose["bones"][j]] for j in pose["bones"]},
               "description": "The heel rises toward the wizard."}
    return {**between, **change}


def _with(*inbetweens):
    """The courtyard's motion plan with these in-betweens added to its own."""
    return {**PLAN, "inbetweens": [*PLAN.get("inbetweens", []), *inbetweens]}


def _check(*inbetweens):
    return p13_motion.check(_with(*inbetweens), PACKET)


def test_a_clean_in_between_passes_and_the_graph_carries_it():
    """A pose on the declared interpolation's own path, on a frame of its own, passes every S13 check; the follows edge
    it splits carries it with its points, and the keys read from the graph run through it."""
    between = _between()
    assert _check(between) == []
    graph = p13_motion.build(ENVELOPE, _with(between), PACKET)
    edge = next(e for e in graph["/edges/motion"] if e["from"] == "acrobat@b05")
    assert [(b["id"], b["t"]) for b in edge["inbetweens"]] == [("acrobat@3", 3.0), ("acrobat@3.55", 3.55)]
    assert edge["inbetweens"][0]["points"] == forward_kinematics.points(between, PACKET["segments"])
    sequence = interpolation.envelope_keys({"nodes": {"motion": {"items": graph["/nodes/motion"]}},
                                            "edges": {"motion": {"items": graph["/edges/motion"]}}})["acrobat"]
    assert 3.0 in [k["t"] for k in sequence]


@pytest.mark.parametrize("change, code", [
    ({"t": 2.6}, "INBETWEEN_SPAN"),                       # on a key's frame
    ({"t": 12.0}, "INBETWEEN_SPAN"),                      # after the entity's last key
    ({"bones": "drop HD"}, "MOTION_JOINTS"),
    ({"bones": "LL.x 170"}, "JOINT_LIMIT"),               # the anime knee bends to 165
    ({"pos": "x + 30"}, "TELEPORT"),                      # 30 m in 0.4 s
    ({"pos": "y - 1.5"}, "FLOOR_PENETRATION"),
    ({"pos": "at the wizard"}, "BODY_OVERLAP"),
])
def test_an_in_between_is_checked_like_a_key(change, code):
    """ADR-O109 (RV-59f): its span, the kernel joints and their limits, its root's speed to its neighbours (owner O12),
    the floor (owner O72) and the other bodies at its instant (R-18): each fails alone."""
    between = _between()
    if "t" in change:
        between = _between(**change) if change["t"] < 10 else {**between, "t": change["t"]}
    elif change.get("bones") == "drop HD":
        between["bones"] = {j: v for j, v in between["bones"].items() if j != "HD"}
    elif change.get("bones") == "LL.x 170":
        between["bones"]["LL"] = [170, 0, 0]
    elif change.get("pos") == "x + 30":
        between["pos"] = [between["pos"][0] + 30, between["pos"][1], between["pos"][2]]
    elif change.get("pos") == "y - 1.5":
        between["pos"] = [between["pos"][0], between["pos"][1] - 1.5, between["pos"][2]]
    else:
        wizard = next(k for k in PLAN["keys"] if k["slot"] == "wizard@b05")
        between["pos"] = list(wizard["pos"])
    found = [f for f in _check(between) if f.get("slot") == f"acrobat@{between['t']:g}"]
    assert code in {f["code"] for f in found}, found


def test_the_re_block_solver_places_an_in_between(tmp_path, capsys):
    """ADR-O109 (RV-59f): `<entity>@<t>` names an in-between, started from the pose the declared interpolation gives
    there; on B's span from 6.3 to 6.6 in the reference fight one at 6.45 clears every frame of A's cartwheel elbow
    with B's arms, spine and root free (measured on S-094; the use itself is RV-59e's)."""
    from solver import body_overlap, reblock
    plan_path = tmp_path / "motion.json"
    plan = json.loads((ROOT / "examples" / "reference_fight" / "plans" / "motion.json").read_text(encoding="utf-8"))
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    assert reblock.main(["reference_fight", "ninja_broad@6.45", "--plan", str(plan_path), "--free",
                         "LA.x,LA.y,LA.z,LFA.x,RA.x,RA.y,RA.z,RFA.x,Sp.x,Sp.z,pos.x,pos.z", "--clear", "ninja_lean"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert (out["entity"], out["t"], out["misses_m2"]) == ("ninja_broad", 6.45, 0.0)
    placed = copy.deepcopy(plan)
    placed["inbetweens"] = [{k: out[k] for k in ("entity", "t", "pos", "rot", "bones")} | {"name": "brace", "description": "."}]
    envelope = json.loads((ROOT / "examples" / "reference_fight" / "envelope.json").read_text(encoding="utf-8"))
    keys = reblock._scene_keys(placed, envelope)
    metres, radii = forward_kinematics.segments("anime"), forward_kinematics.radii("anime")
    for frame in range(152, 159):  # 6.333 to 6.583
        t = round(frame / 24, 6)
        bodies = {(e, t): {"id": e, "capsules": forward_kinematics.capsules(reblock._posed(own, t), metres, radii)}
                  for e, own in keys.items()}
        assert body_overlap.overlaps(bodies) == [], t


def _rendered_with(between):
    """The courtyard at the camera stage with `between` (if any) added to its motion edges, as S13 builds them, and the
    render plan's frame parts."""
    from scenes import courtyard as stage
    envelope = copy.deepcopy(stage("camera"))
    graph = p13_motion.build(ENVELOPE, _with(between) if between else PLAN, PACKET)
    envelope["edges"]["motion"]["items"] = graph["/edges/motion"]
    return envelope, courtyard_plans()["render"]["frame_parts"]


def test_render_txt_prints_an_in_between_at_its_instant():
    """ADR-O109 (RV-59i): the LBN projection prints an in-between as a row of its actor at its instant, in time order,
    marked as an in-between key, and its coverage counts the in-betweens, so a projection that skipped one reads
    incomplete."""
    from renderers import anime_renderer
    envelope, frame_parts = _rendered_with(_between())
    rendered = anime_renderer.render(envelope, frame_parts)
    spec = json.loads(rendered["text"][rendered["text"].index("{"):])
    rows = spec[rendered["labels"]["acrobat"]]
    assert [float(r["t"]) for r in rows] == sorted(float(r["t"]) for r in rows)
    row = next(r for r in rows if r["label"] == "kick_rising")
    assert row["t"] == 3 and row["desc"].startswith("IN-BETWEEN key (no beat, no contact)")
    assert rendered["coverage"]["complete"] and rendered["coverage"]["groups"]["inbetweens"]["rendered"] == 3
    skipped = anime_renderer._Coverage(envelope).report(set(), set(), set())
    assert "acrobat@3" in skipped["groups"]["inbetweens"]["missing"] and not skipped["complete"]


def test_every_prose_mode_prints_the_in_between_keys():
    """ADR-O109 (RV-59i, RV-59e): each prose mode prints the in-between keys inside its [MOTION CONTROL] (the Master
    Template has no section of their own: C19, V8), each with its time, performer and pose words, Root and Joints in
    all but the pure staff; the motion control counts them among the explicit keys."""
    from renderers import prose_renderer
    envelope, frame_parts = _rendered_with(_between())
    labels = {"wizard": "A", "acrobat": "B"}
    plain, _ = _rendered_with(None)
    prompts = prose_renderer.render_all(envelope, frame_parts, labels)
    before = prose_renderer.render_all(plain, frame_parts, labels)
    for mode, prompt in prompts.items():
        text = prompt["text"]
        block = text[text.index("[MOTION CONTROL]"):].split("\n\n")[0]
        line = next(row for row in block.splitlines() if row.startswith("3.00 B: kick rising | L arm "))
        assert ("Root [" in line and "Joints {" in line) == (mode != "pure_staff"), mode
        assert "Explicit = the staff lines and the in-between keys;" in block and "[IN-BETWEEN" not in text
        assert "kick rising" not in before[mode]["text"]
    import re

    def gaps(text):  # the density line's three counts, summed: one per pair of consecutive explicit keys
        return sum(int(n) for n in re.search(r"Density \(measured\): (\d+) dense gaps under 0\.6 s, (\d+) medium from "
                                               r"0\.6 to 0\.9 s, (\d+) sparse", text).groups())
    assert gaps(prompts["mixed"]["text"]) == gaps(before["mixed"]["text"]) + 1


def test_s13_refuses_a_body_through_another_between_keys():
    """F-159 (RV-59e, R-18): S13 refuses two bodies overlapping at any frame between keys, each posed by the declared
    interpolation through its keys and in-betweens; without its two in-betweens the acrobat's kick at 3.6 is drawn
    through the wizard's trunk on both sides of the contact, and with them S13 refuses nothing."""
    bare = {**PLAN, "inbetweens": []}
    found = [f for f in p13_motion.check(bare, PACKET) if f["code"] == "BODY_OVERLAP"]
    assert [(f["slot"], "between keys" in f["message"]) for f in found] == [("acrobat@b05", True), ("acrobat@b06", True)]
    assert p13_motion.check(PLAN, PACKET) == []


# RV-59e (F-159, F-220, ADR-O109; S-097): the commands that placed the in-between keys, run in order from each plan as it
# stood before them (no in-betweens), every component inside the joint limits (O11), no contact moved.
ARMS = "LA.x,LA.y,LA.z,LFA.x,RA.x,RA.y,RA.z,RFA.x,Sp.x,Sp.z,pos.x,pos.z"
BODY = "Sp.x,Sp.z,LA.x,LA.y,LA.z,LFA.x,RA.x,RA.y,RA.z,RFA.x,pos.x,pos.y,pos.z"
LEGS = "LUL.x,LUL.y,LUL.z,RUL.x,RUL.y,RUL.z,LL.x,RL.x"
KICK = "RUL.x,RUL.y,RUL.z,RL.x,LUL.x,LUL.z,LL.x,Sp.x,Sp.y,Sp.z,pos.x,pos.y,pos.z"
INBETWEEN_COMMANDS = {
    "reference_fight": [["ninja_broad@6.45", "--free", ARMS, "--clear", "ninja_lean"],
                        ["ninja_broad@6.7", "--free", ARMS, "--clear", "ninja_lean"],
                        ["ninja_broad@4.75", "--free", BODY, "--clear", "ninja_lean"],
                        ["ninja_broad@8.45", "--free", BODY, "--clear", "ninja_lean"],
                        ["ninja_broad@8.75", "--free", BODY + "," + LEGS, "--clear", "ninja_lean", "--floor"]],
    "wizard_vs_acrobat": [["acrobat@3.55", "--free", KICK, "--clear", "wizard"],
                          ["acrobat@3.7", "--free", KICK, "--clear", "wizard"]],
}


@pytest.mark.parametrize("example", sorted(INBETWEEN_COMMANDS))
def test_the_in_betweens_re_derive_from_their_recorded_commands(example, tmp_path, capsys):
    """F-159 (RV-59e): each in-between the examples carry is what its recorded command gives, the commands run in order
    from the plan without in-betweens, each result joining the plan before the next."""
    from solver import reblock
    plan = json.loads((ROOT / "examples" / example / "plans" / "motion.json").read_text(encoding="utf-8"))
    committed = {(b["entity"], b["t"]): (b["pos"], b["rot"], b["bones"]) for b in plan["inbetweens"]}
    path, plan["inbetweens"] = tmp_path / "motion.json", []
    for command in INBETWEEN_COMMANDS[example]:
        path.write_text(json.dumps(plan), encoding="utf-8")
        assert reblock.main([example, command[0], "--plan", str(path), *command[1:]]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["misses_m2"] == 0.0, command[0]
        plan["inbetweens"].append({k: out[k] for k in ("entity", "t", "pos", "rot", "bones")} | {"name": "x", "description": "."})
    assert {(b["entity"], b["t"]): (b["pos"], b["rot"], b["bones"]) for b in plan["inbetweens"]} == committed
