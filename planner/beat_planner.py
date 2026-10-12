"""S04 beat planner (the plan's LLM call #1): build the hash-bound packet a beat plan is written from."""

from compiler.authoring import seal
from kernel import kernel_files
from planner import library_vocab, modality
from planner.dependency_graph import ROOT
from planner.vocabulary import resolve
from solver import forward_kinematics

PROMPT = ROOT / "planner" / "prompts" / "beat_planning.txt"
SCHEMA_ID = "urn:cinematic-compiler:schema:beat_plan:1.6"


def given_duration(intent):
    rows = intent["evidence"].get("duration_s", [])
    value = intent["parsed"]["duration_s"]
    return (value, "flag" if rows and rows[0]["source"] == "flag" else "user") if value is not None else (None, None)


def prepare(envelope):
    scene, nodes = envelope["scene"], envelope["nodes"]
    entities, props, surfaces = (nodes[k]["items"] for k in ("entities", "props", "surfaces"))
    duration, _ = given_duration(envelope["intent"])
    targets = {}
    for row in envelope["edges"]["constraint_application"]["items"]:
        targets.setdefault(row["constraint_id"], []).append(row["target"])
    packet = {
        "step_id": "S04", "band": "L1", "kind": "beat_plan", "schema": SCHEMA_ID,
        "instructions": PROMPT.read_text(encoding="utf-8"),
        "modality": {"genre": scene["genre"], "guidance": modality.guidance(scene["genre"]), "fps": scene["fps"],
                     "duration_s": duration,
                     "duration_budget_s": None if duration is not None else modality.duration_budget(scene["genre"])},
        "scene": {key: scene[key] for key in ("genre", "fps", "world", "setting", "style_reference", "ax")},
        "entities": [{key: e[key] for key in ("id", "name", "description", "parts", "capabilities", "modes")} for e in entities],
        "props": [{key: p[key] for key in ("id", "name", "description", "parts", "states", "affordances", "grips")}
                  for p in props],
        "surfaces": [{**{key: s[key] for key in ("id", "kind", "description")}, "ax": s.get("ax")} for s in surfaces],
        "constraints": [{"id": c["id"], "rule": c["rule"], "applies_to": targets.get(c["id"], [])}
                        for c in nodes["constraints"]["items"]],
        "vocabulary": resolve(entities, props, surfaces, kernel_files.load("state_vocabulary")),
        "contact_types": ["touch", "possess", "support", "release"],
        "combat_verbs": {kind: rule["values"] for kind, rule in library_vocab.load("combat_verbs")["fields"].items()},
        "standing_leg_m": forward_kinematics.standing_leg(forward_kinematics.segments(scene["genre"])),  # O85
        "event_types": ["action", "hold", "transition", "substitution"]}
    if scene.get("chained_from"):  # M5.5: what this clip continues (end states, open contacts, unresolved causes)
        packet["chained_from"] = scene["chained_from"]
    return seal(packet)
