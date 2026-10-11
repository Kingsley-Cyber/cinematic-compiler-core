"""M8.4 DAG conformance (owner O6): the test prompts run through every graph and layer, and the final prompts meet the
DAG map's mandatory and required rows, each checked by its semantic codes (validators/prompt_validator.py).

- Test prompts: every example (request.json + authored plans), compiled from its query, not read from envelope.json.
  Between them they build every step S01-S17 across anime, ugc_ad and live_action (S18 waits for M7).
- Every structured-prose prompt returns no finding. KNOWN would list findings the owner chooses to keep, each with its
  reason (never silent; an entry that stops occurring fails the test); owner O10 keeps it empty.
- Every code fires on a prompt broken in that one way (BREAKS), so no code is decorative.
"""

import copy
import re

import pytest
import yaml
from conftest import ROOT

from compiler.examples import EXAMPLES, compile_example
from planner.dependency_graph import active_nodes, load
from validators import prompt_validator
from validators.envelope_validator import validate_envelope

pytestmark = pytest.mark.integration
NAMES = sorted(p.name for p in EXAMPLES.iterdir() if (p / "request.json").exists())
MODES = ("pure_staff", "mixed", "upgraded_mixed", "euler_heavy")
KNOWN = {}  # owner O10: the golden passes with nothing set aside (its 'dust ring' fx now read 'dust burst')


@pytest.fixture(scope="module")
def compiled():
    return {name: compile_example(EXAMPLES / name) for name in NAMES}


def _resolve(envelope, pointer):
    node = envelope
    for part in pointer.strip("/").split("/"):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def test_the_test_prompts_build_every_graph_and_layer(compiled):
    order = load()
    built = set()
    for name, envelope in compiled.items():
        assert validate_envelope(envelope) == {"ok": True, "complete": True, "findings": []}, name
        assert envelope["nodes"]["render"]["items"][0]["coverage"]["complete"], name
        for node in order["nodes"]:
            if node["id"] in active_nodes(order, envelope["scene"]["genre"]) and node["id"] != "post_generation":
                for pointer in node["writes"]:
                    assert _resolve(envelope, pointer) is not None, (name, node["id"], pointer)
                built.add(node["step_id"])
    assert built == {n["step_id"] for n in order["nodes"] if n["id"] != "post_generation"}


def test_every_final_prompt_meets_the_dag_map(compiled):
    seen = set()
    for name, envelope in compiled.items():
        for mode in MODES:
            text = envelope["nodes"]["render"]["items"][0]["prose"][mode]["text"]
            for finding in prompt_validator.check(text, envelope, mode):
                assert (name, finding["code"]) in KNOWN, (name, mode, finding)
                seen.add((name, finding["code"]))
    assert seen == set(KNOWN), "a KNOWN finding no longer occurs: remove it"


def _line(pattern):
    """Delete the first line matching `pattern`."""
    return lambda text, env: (re.sub(rf"(?m)^{pattern}.*\n", "", text, count=1), env)


def _replace(old, new):
    return lambda text, env: (text.replace(old, new, 1), env)


def _staff_first(edit):
    def apply(text, env):
        lines = text.split("\n")
        i = next(i for i, line in enumerate(lines) if re.match(r"^\d+\.\d\d [A-Z]: SUPPORT ", line))
        lines[i] = edit(lines[i])
        return "\n".join(lines), env
    return apply


def _swap_rules_and_negatives(text, env):
    return text.replace("[RULES]", "[TMP]").replace("[NEGATIVES]", "[RULES]").replace("[TMP]", "[NEGATIVES]"), env


def _grounded_to_airborne(text, env):
    lines = text.split("\n")
    i = next(i for i, line in enumerate(lines) if re.match(r"^\d+\.\d\d [A-Z]: SUPPORT (?!NO SUPPORT)", line))
    lines[i] = re.sub(r"SUPPORT [^|]*\|", "SUPPORT NO SUPPORT |", lines[i], count=1)
    return "\n".join(lines), env


def _first_line_of_a_airborne(text, env):
    lines = text.split("\n")
    i = next(i for i, line in enumerate(lines) if re.match(r"^1\.60 A: SUPPORT ", line))
    lines[i] = re.sub(r"SUPPORT [^|]*\|", "SUPPORT NO SUPPORT |", lines[i], count=1)
    return "\n".join(lines), env


def _strip_maintain(label):
    return lambda text, env: (re.sub(rf"(?m)^- {label} \d+\.\d\d–\d+\.\d\d: maintain .*\n", "", text), env)


def _custody(text, env):
    env = copy.deepcopy(env)
    for state in env["nodes"]["states"]["items"]:
        if state["subject"]["id"] == "glasses":
            state["conditions"]["holder"] = "ugc_creator"
    return text, env


def _react_early(text, env):
    env = copy.deepcopy(env)
    beats = {b["id"]: b for b in env["nodes"]["beats"]["items"]}
    edge = next(e for e in env["edges"]["causal"]["items"] if e["causal_strength"] == "hard" and any(
        c["beat"] == e["from"] and c["contact_type"] in ("touch", "possess") for c in env["nodes"]["contacts"]["items"]))
    touch = min(c["t"] for c in env["nodes"]["contacts"]["items"] if c["beat"] == edge["from"])
    beats[edge["to"]]["t"] = round(touch - 0.5, 6)
    return text, env


def _drop_causal_threads(text, env):
    head, rest = text.split("[CAUSAL LINKS]\n", 1)
    legend, after = rest.split("\n", 1)
    return head + "[CAUSAL LINKS]\n" + legend + "\n\n" + after.split("\n\n", 1)[1], env


BREAKS = [
    ("SECTION_MISSING", "wizard_vs_acrobat", "mixed", _line(r"\[MOTION CONTROL\]")),
    ("SECTION_ORDER", "wizard_vs_acrobat", "mixed", _swap_rules_and_negatives),
    ("STACKED_GRAPHS", "wizard_vs_acrobat", "mixed", _replace("[RULES]", "[SCENE GRAPH]\nA parented to the pillar\n\n[RULES]")),
    ("PROSE_STALE", "wizard_vs_acrobat", "mixed", lambda text, env: (text + " ", env)),
    ("ROOT_EXACT_PRESENT", "wizard_vs_acrobat", "mixed", _replace("[RULES]\n", "[RULES]\n- A root exact\n")),
    ("KEY_LINE_MISSING", "wizard_vs_acrobat", "mixed", _line(r"\d+\.\d\d [A-Z]: SUPPORT ")),
    ("STAFF_FORMAT", "wizard_vs_acrobat", "mixed", _staff_first(lambda line: line.replace(" | ", " ; ", 1))),
    ("SUPPORT_MISMATCH", "wizard_vs_acrobat", "mixed", _grounded_to_airborne),
    ("AIRBORNE_UNBOOKENDED", "wizard_vs_acrobat", "mixed", _first_line_of_a_airborne),
    ("GESTURE_MISMATCH", "wizard_vs_acrobat", "mixed", _staff_first(lambda line: re.sub(r"L arm \S+,", "L arm back-high,", line,
                                                                                         count=1))),
    ("EULER_MODE_MISMATCH", "wizard_vs_acrobat", "mixed", _staff_first(lambda line: re.sub(r" · Root \[.*$", "", line))),
    ("SKELETON_KEY_MISSING", "wizard_vs_acrobat", "euler_heavy", _line("Skeleton key:")),
    ("EFFORT_UNDECLARED", "wizard_vs_acrobat", "mixed", _strip_maintain("A")),
    ("KINETIC_CHAIN_MISSING", "wizard_vs_acrobat", "mixed", lambda text, env: (re.sub(r"; chain [^;|·]*", "", text, count=1),
                                                                               env)),
    ("KEY_GAP_UNGUIDED", "ugc_glasses_demo", "mixed", lambda text, env: (re.sub(r"(?m)^- A .* s without a line\).*\n", "",
                                                                               text), env)),
    ("IMPLIED_GUIDANCE_MISSING", "wizard_vs_acrobat", "mixed", _line("- A: secondary motion")),
    ("INTERPOLATION_UNDECLARED", "wizard_vs_acrobat", "mixed", _line("Interpolation:")),
    ("CONVENTION_MISSING", "wizard_vs_acrobat", "mixed", _replace("joints local to their parent", "joints")),
    ("SPATIAL_ANCHOR_MISSING", "wizard_vs_acrobat", "mixed", _line("A starts at")),
    ("PROP_TRACK_MISSING", "ugc_glasses_demo", "mixed",
     lambda text, env: (re.sub(r"\[PROP STATE MACHINE – glasses\]\n.*?\n\n", "", text, flags=re.S), env)),
    ("PROP_STATE_ORDER", "ugc_glasses_demo", "mixed", _replace("holder none -> A", "holder none -> B")),
    ("PROP_INVARIANT_MISSING", "ugc_glasses_demo", "mixed", _line("ONE glasses only")),
    ("CUSTODY_RULE_MISSING", "ugc_glasses_demo", "mixed", _custody),
    ("PROP_FIRST_STATE", "ugc_glasses_demo", "mixed", _replace("temples folded until", "temples until")),
    ("PROP_LINE_MISSING", "reference_fight", "mixed", _replace(" · 8.00 one line from A L hand to B torso", "")),
    ("DOUBLED_WORD", "wizard_vs_acrobat", "mixed", _replace("Props at the start:", "Props at the the start:")),
    ("COUNT_CONTRADICTION", "reference_fight", "mixed", _replace("TWO fighters, FIVE props", "TWO fighters, FOUR props")),
    ("VANISHED_BODY", "reference_fight", "mixed", _line(r"- A is gone from")),
    ("TURN_LABEL", "reference_fight", "mixed", _replace("ONE backflip about", "ONE spin to the left about")),
    # W1-W4, the probe wording rules (owner O47-O49): each break restores a wording a probe render refused
    ("BODY_HOLD_FRAMES", "reference_fight", "mixed", _replace("Impact frames:", "Holds: 0.60 for 3 frames.\nImpact frames:")),
    ("EMPTY_HAND_UNSTATED", "reference_fight", "mixed", _replace("; B's right hand is empty from 2.50", "")),
    ("ROTATION_ANGLES_PRINTED", "reference_fight", "mixed", _replace(
        "ONE backflip about the side-to-side axis (sagittal plane), 5.10–5.50",
        "backflip: 0 degrees at 5.10, -180 degrees at 5.30, -360 degrees at 5.50")),
    ("HIDDEN_PHRASING", "reference_fight", "mixed", _replace("substitution log (on the ground, deployment standing until 4.00)",
                                                             "substitution log (hidden in A's coat until 3.70)")),
    ("CAUSAL_LIST_MISSING", "wizard_vs_acrobat", "mixed", _drop_causal_threads),
    ("CAUSE_REASON", "wizard_vs_acrobat", "mixed", _replace(": The crouch loads the legs for the vault.", ": It goes on.")),
    ("REACTION_WITHOUT_CAUSE", "ugc_glasses_demo", "mixed", _react_early),
    ("CAUSAL_RULE_MISSING", "wizard_vs_acrobat", "mixed", _line(r"- From \d+\.\d\d to the end, ")),
    ("CONSERVATION_RULE_MISSING", "wizard_vs_acrobat", "mixed", _line("- Momentum is conserved")),
    ("SPAN_RULE_MISSING", "reference_fight", "mixed", lambda text, env: (re.sub(r"(?m)^- A . foot stays on the .*\n", "",
                                                                                text), env)),
    ("EVENT_SEPARATION_MISSING", "reference_fight", "mixed", _line("- TWO SEPARATE STRIKES: A")),
    ("RULES_MISSING", "wizard_vs_acrobat", "mixed", _line("- slerp A joints")),
    ("NEGATIVES_MISSING", "wizard_vs_acrobat", "mixed", _replace("; no halo", "")),
    ("DISCONNECTED_CAMERA_MOTION", "wizard_vs_acrobat", "mixed", _replace("; motivated by ", "; ")),
    ("ANCHOR_PHRASE_MISSING", "wizard_vs_acrobat", "mixed", _replace("A = wizard:", "A wizard:")),
    ("RENDER_INTENT_MISSING", "wizard_vs_acrobat", "mixed", _replace("Choreography:", "Plan:")),
    ("END_STATE_MISSING", "wizard_vs_acrobat", "mixed", _line("- End state: A")),
    ("PRECEDENCE_RULE_MISSING", "wizard_vs_acrobat", "mixed", _line("- Laban support and contacts are primary")),
    ("PROMPT_CONTRADICTION", "ugc_glasses_demo", "mixed", _replace("1.50 held by A R hand", "1.50 held by B R hand")),
]


@pytest.mark.parametrize("code, example, mode, edit", BREAKS, ids=[b[0] for b in BREAKS])
def test_each_code_fires_on_a_prompt_broken_that_way(code, example, mode, edit, compiled):
    envelope = compiled[example]
    text, broken = edit(envelope["nodes"]["render"]["items"][0]["prose"][mode]["text"], envelope)
    assert text != envelope["nodes"]["render"]["items"][0]["prose"][mode]["text"] or broken is not envelope, code
    assert code in {f["code"] for f in prompt_validator.check(text, broken, mode)}


def test_every_code_has_a_break_and_every_map_code_is_real():
    assert sorted(b[0] for b in BREAKS) == sorted(prompt_validator.CODES)  # one break per code, no code left out
    rows = yaml.safe_load((ROOT / "kernel" / "knowledge_map.yaml").read_text(encoding="utf-8"))["rows"]
    used = {code for row in rows for code in row.get("codes", [])}
    assert used == set(prompt_validator.CODES)
    gaps = {code for row in rows for code in row.get("gaps", [])}
    assert not gaps & set(prompt_validator.CODES)
