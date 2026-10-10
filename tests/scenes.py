"""Small authored scenes for step tests. Each plan is sealed against the packet of its own envelope."""

import copy
import json

from conftest import ROOT

from compiler import pipeline
from planner.beat_planner import prepare

COURTYARD = ROOT / "examples" / "wizard_vs_acrobat"
COURTYARD_QUERY = json.loads((COURTYARD / "request.json").read_text())["query"]
COURTYARD_PLAN = json.loads((COURTYARD / "plans" / "temporal.json").read_text())
CUP_QUERY = "6 seconds live action: wizard vs knight, wizard holding a coffee cup in a castle"


def courtyard_plans():
    return {path.stem: json.loads(path.read_text()) for path in sorted((COURTYARD / "plans").glob("*.json"))}


def courtyard(until, **overrides):
    return pipeline.run(COURTYARD_QUERY, until=until, plans={**courtyard_plans(), **overrides})


def _fact(kind, sid, prop, value):
    return {"subject": {"kind": kind, "id": sid}, "property": prop, "value": value}


def cup_plan(envelope):
    cup, hand = {"kind": "prop", "id": "coffee_cup"}, {"kind": "entity", "id": "wizard", "part": "right_hand"}
    anchor = {"pos": {"wizard": [0, 0, 0]}, "facing": {"wizard": [0, 0, 1]}}
    beats = [
        {"id": "b01", "t": 0.0, "dur": 1.5, "event_type": "action", "actor": "wizard", "label": "lift_cup",
         "participants": [cup], "modes": {"wizard": "calm_casting"}, **copy.deepcopy(anchor),
         "action": "Wizard lifts the cup by its handle.", "requires": [_fact("prop", "coffee_cup", "holder", "none"),
                                                                     _fact("prop", "coffee_cup", "fill", "full")],
         "effects": [_fact("prop", "coffee_cup", "holder", "wizard"), _fact("entity", "wizard", "possession", "coffee_cup")],
         "contacts": [{"contact_type": "possess", "a": hand, "b": {**cup, "part": "handle"}}],
         "causes": [{"to": "b02", "causal_strength": "hard", "why": "Holding the cup lets the wizard sip."}]},
        {"id": "b02", "t": 1.5, "dur": 2.0, "event_type": "action", "actor": "wizard", "label": "sip",
         "participants": [cup], "modes": {"wizard": "calm_casting"}, **copy.deepcopy(anchor),
         "action": "Wizard sips; the coffee level drops.", "requires": [_fact("prop", "coffee_cup", "holder", "wizard")],
         "effects": [_fact("prop", "coffee_cup", "fill", "partly_full")], "contacts": [],
         "causes": [{"to": "b03", "causal_strength": "soft", "why": "Done drinking, the wizard sets it down."}]},
        {"id": "b03", "t": 3.5, "dur": 1.5, "event_type": "action", "actor": "wizard", "label": "set_down",
         "participants": [cup, {"kind": "surface", "id": "ground"}], "modes": {"wizard": "calm_casting"},
         **copy.deepcopy(anchor), "action": "Wizard sets the cup on the ground and lets go.",
         "requires": [_fact("prop", "coffee_cup", "holder", "wizard")],
         "effects": [_fact("prop", "coffee_cup", "holder", "none"), _fact("prop", "coffee_cup", "location", "ground"),
                     _fact("entity", "wizard", "possession", "none")],
         "contacts": [{"contact_type": "release", "a": hand, "b": {**cup, "part": "handle"}},
                      {"contact_type": "support", "a": {"kind": "entity", "id": "wizard", "part": "right_foot"},
                       "b": {"kind": "surface", "id": "ground", "part": None}}],
         "causes": []}]
    return {"step_id": "S04", "band": "L1", "packet_sha256": prepare(envelope)["packet_sha256"],
            "author": {"host": "test fixture", "model": "none"}, "attempt": 1, "beats": beats}


def cup(until, edit=None):
    envelope = pipeline.run(CUP_QUERY, until="constraint")
    plan = cup_plan(envelope)
    if edit:
        edit(plan)
    return pipeline.run(CUP_QUERY, until=until, plans={"temporal": plan})
