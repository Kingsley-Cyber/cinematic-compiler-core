"""M8.2 structured-prose prompts (owner O1-O3): Master Template sections, one staff line per slot, Euler blocks per mode,
root exact left out of the prose only, every other rule and negative carried."""

import copy
import json
import re

import pytest
from conftest import ROOT

from renderers import prose_renderer
from renderers.anime_renderer import constraint_rows
from validators import prompt_validator

pytestmark = pytest.mark.unit
EXAMPLES = sorted(p for p in (ROOT / "examples").iterdir() if (p / "render.txt").exists())
SECTIONS = ("[SCENE]", "[MOVEMENT LANGUAGE]", "[LABAN STAFF – ", "[RULES]", "[NEGATIVES]")
LINE = re.compile(r"^\d+\.\d\d [A-Z]: SUPPORT ")


def load(folder):
    envelope = json.loads((folder / "envelope.json").read_text())
    return envelope, envelope["nodes"]["render"]["items"][0]


def staff(text):
    return [line for line in text.splitlines() if LINE.match(line)]


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_four_modes_with_sections_in_order_and_one_line_per_slot(folder):
    envelope, render = load(folder)
    assert set(render["prose"]) == set(prose_renderer.MODES)
    slots = len(envelope["nodes"]["motion"]["items"])
    for mode, row in render["prose"].items():
        text = row["text"]
        assert (folder / f"prose_{mode}.txt").read_text() == text
        positions = [text.index(s) for s in SECTIONS]
        assert positions == sorted(positions) and positions[0] == 0, mode
        assert len(staff(text)) == slots, mode


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_euler_blocks_sit_on_the_lines_each_mode_names(folder):
    _, render = load(folder)
    lines = {mode: staff(row["text"]) for mode, row in render["prose"].items()}
    assert not any("Root [" in line for line in lines["pure_staff"])
    assert all("Root [" in line and "Joints {" in line for line in lines["euler_heavy"])
    last = {}
    for i, line in enumerate(lines["pure_staff"]):
        last[line.split(":")[0].split(" ")[1]] = i
    first = {}
    for i, line in enumerate(lines["pure_staff"]):
        first.setdefault(line.split(":")[0].split(" ")[1], i)
    for i, line in enumerate(lines["pure_staff"]):
        strike = "[DOUBLE BOW + accent:" in line
        assert ("Root [" in lines["mixed"][i]) == (strike or i in first.values() or i in last.values())
        assert "Joints {" not in lines["mixed"][i]
        assert ("Joints {" in lines["upgraded_mixed"][i]) == (strike or i in last.values())
        assert lines["mixed"][i].startswith(line) and lines["euler_heavy"][i].startswith(line)


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_root_exact_only_in_lbn_and_every_other_rule_and_negative_in_the_prose(folder):
    envelope, render = load(folder)
    _, rows = constraint_rows(envelope, render["labels"])
    root_exact = {cid for _, _, cid, ref in rows if ref == prose_renderer.ROOT_EXACT}
    assert root_exact and "root exact" in render["text"]
    for mode, row in render["prose"].items():
        assert row["omitted_constraints"] == sorted(root_exact)
        assert "root exact" not in row["text"]
        body = row["text"]
        for section, text, _, ref in rows:
            if section in ("rules", "negative", "preface", "ax", "key") and ref != prose_renderer.ROOT_EXACT:
                if section == "key" and mode in ("pure_staff", "mixed"):
                    continue
                assert text in body, (mode, section, text)
        lead = ("Follow the SUPPORT column and the contact bows strictly" if mode == "pure_staff"
                else "Laban support and contacts are primary; Euler numbers are precision override only.")
        assert lead in body


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_every_entity_has_its_anchor_phrase_in_scene(folder):
    envelope, render = load(folder)
    scene = render["prose"]["mixed"]["text"].split("[MOVEMENT LANGUAGE]")[0]
    for entity in envelope["nodes"]["entities"]["items"]:
        assert f"{render['labels'][entity['id']]} = {entity['name']}: {entity['silhouette'].rstrip('.')}" in scene


def test_reference_strikes_are_the_impacts_on_other_bodies_and_free_props():
    _, render = load(ROOT / "examples" / "reference_fight")
    strikes = [line.split(" | ")[0].split(":")[0] for line in staff(render["prose"]["pure_staff"]["text"])
               if "[DOUBLE BOW + accent:" in line]
    assert {"2.50 A", "4.70 A"} <= set(strikes)
    # O93 (RV-10): the catch at 6.6 is a grasp plus a throw, and at 8.5 B is struck by A's kunai: neither is B's strike
    assert not {"6.60 B", "8.50 B"} & set(strikes)
    text = render["prose"]["pure_staff"]["text"]
    assert "[DOUBLE BOW + accent: R foot > kunai blade]" in text  # at its pose (O23, M9-02)
    assert "chain " in next(line for line in staff(text) if line.startswith("2.50 A"))


def test_the_prose_is_a_pure_function_of_the_envelope():
    envelope, render = load(ROOT / "examples" / "ugc_glasses_demo")
    again = prose_renderer.render_all(envelope, render["frame_parts"], render["labels"])
    assert again == render["prose"]
    assert "FACE:" in render["prose"]["pure_staff"]["text"]
    assert not re.search(r"\bAU\s?\d", render["prose"]["pure_staff"]["text"])  # faces in words only (owner F4)


GENRE_TITLES = {"anime": "[ANIME]", "ugc_ad": "[UGC]", "live_action": "[LIVE ACTION]"}


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_every_master_template_section_in_order(folder):
    envelope, render = load(folder)
    order = ["[SCENE]", "[MOVEMENT LANGUAGE]", "[LABAN STAFF – ", "[IMPLIED GUIDANCE]", "[MOTION CONTROL]",
             "[SPATIAL ANCHORS]"] + [f"[PROP STATE MACHINE – {p['name']}]" for p in envelope["nodes"]["props"]["items"]] + [
             "[CAUSAL LINKS]", "[CAMERA]", GENRE_TITLES[envelope["scene"]["genre"]], "[RULES]", "[NEGATIVES]"]
    for row in render["prose"].values():
        heads = [line for line in row["text"].splitlines() if line.startswith("[") and line.endswith("]")
                 and not line.startswith("[DOUBLE")]
        assert [h if not h.startswith("[LABAN STAFF – ") else "[LABAN STAFF – " for h in heads] == order
        assert "Render intent. Motion:" in row["text"].split("[MOVEMENT LANGUAGE]")[0]


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_every_gap_over_one_and_a_half_seconds_has_implied_guidance(folder):
    envelope, render = load(folder)
    text = render["prose"]["pure_staff"]["text"]
    guidance = text.split("[IMPLIED GUIDANCE]")[1].split("[MOTION CONTROL]")[0]
    times = {}
    for line in staff(text):
        stamp, label = line.split(":")[0].split(" ")
        times.setdefault(label, []).append(float(stamp))
    for label, ts in times.items():
        for a, b in zip(ts, ts[1:] + [envelope["scene"]["duration_s"]], strict=True):
            if b - a > 1.5 + 1e-6:
                assert f"- {label} {a:.2f}–{b:.2f} (" in guidance, (label, a, b)


@pytest.mark.parametrize("folder", EXAMPLES, ids=lambda p: p.name)
def test_props_causal_links_and_shots_are_all_carried(folder):
    envelope, render = load(folder)
    text = render["prose"]["mixed"]["text"]
    for prop in envelope["nodes"]["props"]["items"]:
        block = text.split(f"[PROP STATE MACHINE – {prop['name']}]")[1].split("\n\n")[0]
        assert "never duplicated, never in two hands at once, never lost" in block
    causal = text.split("[CAUSAL LINKS]")[1].split("\n\n")[0]
    beats = {b["id"]: b for b in envelope["nodes"]["beats"]["items"]}
    labels = render["labels"]

    def name(beat_id):
        return f"{labels[beats[beat_id]['actor']]} {beats[beat_id]['label'].replace('_', ' ')}"

    for edge in envelope["edges"]["causal"]["items"]:
        arrow = "→" if edge["causal_strength"] == "hard" else "⇢"
        assert f"{name(edge['from'])} {arrow} {name(edge['to'])}" in causal, edge["id"]
    camera = text.split("[CAMERA]")[1].split("\n\n")[0].splitlines()
    shots = [line for line in camera if line and not line.startswith(("Camera rules:", "Holds on hits:"))]
    assert len(shots) == len(envelope["nodes"]["camera"]["items"])


def test_reference_rules_bound_lasting_effects_spans_and_separate_strikes():
    _, render = load(ROOT / "examples" / "reference_fight")
    rules = render["prose"]["pure_staff"]["text"].split("[RULES]")[1].split("[NEGATIVES]")[0]
    assert "- From 9.00 to the end, B keeps condition down." in rules
    assert "- From 8.50 to the end, kunai stays embedded." in rules  # the drive lodges it at 8.5 (O93, RV-10)
    assert "- A L foot stays on the wooden pillar from 0.60 to 1.60: one continuous contact" in rules
    assert "- TWO SEPARATE STRIKES: A R foot > kunai blade and R leg > B torso" in rules
    # the pelvis lying (O72, S-027), 0.18 m aside since RV-49 (S-049) so A's feet stand clear of B's legs
    assert "End state: B at [0.96, 0.1, 5.48], condition down, support lying." in rules
    assert "Contact before effect: nothing reacts to a hit before the contact." in rules
    assert rules.index("Identity is immutable") > rules.index("Follow the SUPPORT column")  # laws in the rules layer


def test_hits_are_camera_holds_and_nothing_plays_slow():
    """Owner O92 (RV-09, F-083): the reference fight's four hits print as camera holds with both bodies in frame and
    every shot plays at normal x1; without the hold, or with a slowed shot, the prompt is refused (HIT_HOLD,
    PLAYBACK_RAMP)."""
    envelope, render = load(ROOT / "examples" / "reference_fight")
    text = render["prose"]["mixed"]["text"]
    assert ("Holds on hits: 2.50 impact: hold for 3 frames with BOTH bodies in frame (A and B), no close-up; 4.70 impact: "
            "hold for 3 frames with BOTH bodies") in text and "8.50 impact: hold for 4 frames with BOTH bodies" in text
    assert not re.search(r"; (slow|ramp|freeze) x", text)

    def fired(prompt):
        return {f["code"] for f in prompt_validator.check(prompt, envelope, "mixed")}
    assert not {"HIT_HOLD", "PLAYBACK_RAMP"} & fired(text)
    assert "HIT_HOLD" in fired(text.replace("2.50 impact: hold for 3 frames with", "2.50 impact: cut to", 1))
    assert "PLAYBACK_RAMP" in fired(text.replace("normal x1; shows A foot deflect kunai", "slow x0.25; shows A foot "
                                                 "deflect kunai", 1))


def test_the_printed_camera_rules_follow_o92():
    """F-160, F-177 (RV-60, RV-71b; owner O92): every example prints its genre card's camera rules word for word (the
    card's rules are checked where they are written), and a prompt that adds or alters one is refused (CAMERA_RULES),
    whatever its words. The test moved from word lists to the card with the check it pins (ADR-O102)."""
    for name in ("reference_fight", "wizard_vs_acrobat", "live_action_standoff", "ugc_glasses_demo"):
        envelope, render = load(ROOT / "examples" / name)
        for variant, prose in render["prose"].items():
            found = {f["code"] for f in prompt_validator.check(prose["text"], envelope, variant)}
            assert not {"CAMERA_RULES", "HIT_HOLD", "PLAYBACK_RAMP"} & found, (name, variant)
    envelope, render = load(ROOT / "examples" / "reference_fight")
    text = render["prose"]["mixed"]["text"]

    def fired(rule):
        prompt = text.replace("Camera rules: ", f"Camera rules: {rule} ", 1)
        return {f["code"] for f in prompt_validator.check(prompt, envelope, "mixed")}
    for rule in ("Cut close on the receiver after a blow lands.", "Slow motion only around the peak of an action.",
                 "Crash zoom onto the blow.", "Run the fall at half speed."):
        assert "CAMERA_RULES" in fired(rule), rule
    assert "CAMERA_RULES" in {f["code"] for f in prompt_validator.check(
        text.replace("between hits is followed by a tracking or whip move", "is followed by a crash zoom", 1), envelope, "mixed")}


def test_the_vanishing_actor_s_line_ends_its_support_and_walks_nowhere():
    """Owner O90 (F-163, RV-62): A's 3.70 line keeps its key's support for the instant and says it ends there, and no
    path walks A to where it reappears; a vanish line that carries either into the vanish is refused (VANISHED_BODY)."""
    envelope, render = load(ROOT / "examples" / "reference_fight")
    for prose in render["prose"].values():
        line = next(x for x in prose["text"].splitlines() if x.startswith("3.70 A: "))
        assert line.startswith("3.70 A: SUPPORT both feet place-mid [f:both], then none: A vanishes here until 4.40 | ")
        assert "path: " not in line
    text = render["prose"]["mixed"]["text"]

    def fired(prompt):
        return {f["code"] for f in prompt_validator.check(prompt, envelope, "mixed")}
    assert "VANISHED_BODY" not in fired(text)
    assert "VANISHED_BODY" in fired(text.replace("3.70 A: SUPPORT both feet place-mid [f:both], then none: A vanishes here "
                                                 "until 4.40", "3.70 A: SUPPORT steps left alternating [f:alt]", 1))


def test_the_prompt_owes_a_hold_at_every_hit_whatever_s17_holds():
    """F-155 (RV-57, owner O92): the prompt prints a camera hold at every hit the contacts give, and a prompt that drops
    one is refused even when S17's frame parts drop that hold too (HIT_HOLD)."""
    envelope, render = load(ROOT / "examples" / "reference_fight")
    text = render["prose"]["mixed"]["text"]
    unheld = copy.deepcopy(envelope)
    frame = unheld["nodes"]["render"]["items"][0]["frame_parts"]
    frame["holds"] = [h for h in frame["holds"] if abs(h["t"] - 4.7) > 1e-6]
    dropped = text.replace("4.70 impact: hold for 3 frames with BOTH bodies in frame (A and B), no close-up; ", "", 1)
    assert dropped != text and "HIT_HOLD" not in {f["code"] for f in prompt_validator.check(text, unheld, "mixed")}
    assert "HIT_HOLD" in {f["code"] for f in prompt_validator.check(dropped, unheld, "mixed")}


def test_the_vanished_body_is_gone_from_the_guidance():
    """Owners O18, O90 (F-176, RV-70): the guidance prints the vanish's own Effort at its instant (LBN-2.4's "in-place
    dissolve") and keeps nothing of A moving while it is gone; a prompt that does, or a vanish line whose support
    steps, is refused (VANISHED_BODY); a vanish that never returns says so and holds no sign."""
    envelope, render = load(ROOT / "examples" / "reference_fight")
    for prose in render["prose"].values():
        assert "- A at 3.70: vanishes with light weight, sudden time, indirect space, free flow (flick quality), in place; " \
               "gone until 4.40." in prose["text"] and "- A 3.70–4.00" not in prose["text"]
        assert "travels through space between positions, except while it is gone after a substitution" in prose["text"]
    text = render["prose"]["mixed"]["text"]

    def fired(prompt):
        return {f["code"] for f in prompt_validator.check(prompt, envelope, "mixed")}
    assert "VANISHED_BODY" not in fired(text)
    moving = text.replace("- A at 3.70: vanishes with", "- A 3.70–4.00: maintain", 1)
    assert moving != text and "VANISHED_BODY" in fired(moving)
    stepping = text.replace("3.70 A: SUPPORT both feet place-mid [f:both], then none", "3.70 A: SUPPORT steps left "
                            "alternating [f:alt], then none", 1)
    assert stepping != text and "VANISHED_BODY" in fired(stepping)
    assert prose_renderer.vanish_note(None) == "SUBSTITUTION: the decoy takes this place and the body does not return"
    assert "reappears at its next line" in prose_renderer.vanish_note(4.4)


def test_the_printed_hold_names_every_body_present():
    """F-177 (RV-71a, owner O92): the prompt's hold line names the bodies it holds, and one that leaves out a body present
    at the hit is refused (HIT_HOLD)."""
    envelope, render = load(ROOT / "examples" / "reference_fight")
    text = render["prose"]["mixed"]["text"]
    one = text.replace("2.50 impact: hold for 3 frames with BOTH bodies in frame (A and B)", "2.50 impact: hold for 3 "
                       "frames with BOTH bodies in frame (A)", 1)
    found = [f["message"] for f in prompt_validator.check(one, envelope, "mixed") if f["code"] == "HIT_HOLD"]
    assert one != text and found == ["The hold at 2.50 leaves out B"]
    assert not [f for f in prompt_validator.check(text, envelope, "mixed") if f["code"] == "HIT_HOLD"]

