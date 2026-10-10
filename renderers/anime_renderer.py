"""S16 renderer: deterministic projection of a built envelope into the full LBN-2.x layout (anime target).

Uncompressed and model-agnostic: no length budget, no model-specific formatting. Every node group item and every
applied constraint is rendered (owner invariant no_render_compression) and `coverage` proves it item by item.
Kernel controls written for the reference actors and props are regenerated from this scene's data (labels,
facings, props); scene-wide kernel controls are printed as written; card invariants and beat actions go to rules.
Layout: preface text, then one JSON object: variant, fps, dur, ax, key, lma_legend, negative, laban, one track per
actor label, one track per prop, set (surfaces), cam, anime (frame-part directives), rules.
"""

import hashlib
import json
import math

from planner import library_vocab

VARIANT = "LBN-2.4-ADV-LMA"
TARGET = "lbn-2.x"
NUMBERS = ("ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE")
CUES = ("balance", "loading", "bracing", "yielding", "weight_transfer", "tension", "release", "strain", "restraint", "breathing")
# Kernel controls written for the reference cast, regenerated for this scene (kernel item id -> section, scope, text).
GENERATED = {
    "k_ax_01": ("ax", "actor", "{label} faces {facing}"),
    "k_negative_06": ("negative", "scene", "no extra fighters beyond {labels}"),
    "k_negative_07": ("negative", "actor", "no cloned {label}"),
    "k_negative_08": ("negative", "prop", None),
    "k_negative_09": ("negative", "prop", None),
    "k_negative_10": ("negative", "prop", None),
    "k_negative_11": ("negative", "prop", None),
    "k_rules_00": ("rules", "actor", "slerp {label} joints"),
    "k_rules_01": ("rules", "actor", "{label} root exact"),
    "k_rules_23": ("rules", "scene", "{count} fighter identities {labels} never merge or duplicate"),
    "k_rules_24": ("rules", "prop_scene", "{count} props tracked separately,never merged:{ids}"),
}
PRINTED = ("preface", "ax", "key", "negative", "rules")
ENFORCED = ("owner",)  # owner render controls are enforced by this module's coverage, not printed to the model


def _num(value):
    return int(value) if float(value).is_integer() else value


def _join(labels):
    return labels[0] if len(labels) == 1 else ", ".join(labels[:-1]) + " and " + labels[-1]


def _facing(vector):
    for axis, index in (("X", 0), ("Y", 1), ("Z", 2)):
        if abs(vector[index]) >= 0.999 * max(1e-9, sum(v * v for v in vector) ** 0.5):
            return ("+" if vector[index] > 0 else "-") + axis
    return f"heading {round(math.degrees(math.atan2(vector[0], vector[2])), 1)}deg"


def _items(envelope, kind, group):
    return envelope.get(kind, {}).get(group, {}).get("items", [])


class _Coverage:
    def __init__(self, envelope):
        self.groups = {g: {i["id"] for i in envelope["nodes"][g]["items"]} for g in envelope["nodes"] if g != "render"}
        self.seen = {g: set() for g in self.groups}

    def mark(self, group, identity):
        if group in self.seen:
            self.seen[group].add(identity)

    def report(self, applied, rendered, enforced):
        groups = {g: {"items": len(ids), "rendered": len(ids & self.seen[g]), "missing": sorted(ids - self.seen[g])}
                  for g, ids in sorted(self.groups.items())}
        missing = sorted(applied - rendered - enforced)
        complete = all(not row["missing"] for row in groups.values()) and not missing
        return {"groups": groups, "constraints": {"applied": len(applied), "rendered": len(applied & rendered),
                                                  "enforced_by_renderer": sorted(applied & enforced), "missing": missing},
                "complete": complete}


def render(envelope, frame_parts):
    cover = _Coverage(envelope)
    scene = envelope["scene"]
    entities = _items(envelope, "nodes", "entities")
    props = _items(envelope, "nodes", "props")
    labels = {e["id"]: chr(ord("A") + i) for i, e in enumerate(entities)}
    for e in entities:
        cover.mark("entities", e["id"])
    beats = sorted(_items(envelope, "nodes", "beats"), key=lambda b: (b["t"], b["id"]))
    first_facing = {}
    for beat in beats:
        for entity, vector in beat["facing"].items():
            first_facing.setdefault(entity, vector)
    constraints = {c["id"]: c for c in _items(envelope, "nodes", "constraints")}
    applications = _items(envelope, "edges", "constraint_application")
    applied = {a["constraint_id"] for a in applications}
    targets = {}
    for a in applications:
        targets.setdefault(a["constraint_id"], []).append(a["target"])
    sections = {name: [] for name in PRINTED}
    rendered, enforced = set(), set()

    def emit(section, text, constraint_id=None):
        if text not in sections[section]:
            sections[section].append(text)
        if constraint_id:
            rendered.add(constraint_id)
            cover.mark("constraints", constraint_id)

    prop_cards = {p["id"]: p for p in props}
    for cid in sorted(applied, key=lambda c: list(constraints).index(c)):
        constraint = constraints[cid]
        ref = constraint["source"]["ref"]
        if constraint["field"] in ENFORCED:
            enforced.add(cid)
            cover.mark("constraints", cid)
        elif ref in GENERATED:
            section, scope, template = GENERATED[ref]
            actors = [labels[t["id"]] for t in targets[cid] if t["kind"] == "entity"]
            if scope == "actor":
                for target in targets[cid]:
                    if target["kind"] == "entity":
                        emit(section, template.format(label=labels[target["id"]],
                                                      facing=_facing(first_facing.get(target["id"], [0, 0, 1]))), cid)
            elif scope == "scene":
                every = [labels[e["id"]] for e in entities] or actors
                emit(section, template.format(labels=_join(every), count=NUMBERS[len(every)]), cid)
            elif scope == "prop":
                for target in targets[cid]:
                    if target["kind"] == "prop":
                        card = prop_cards[target["id"]]
                        if card.get("count", 1) > 1:
                            text = (f"no duplicated {card['unit_name']} beyond the declared {card['group_name']} "
                                    f"of {card['count']}")
                        else:
                            text = f"no duplicated {card['name']}"
                        emit(section, text, cid)
            else:
                emit(section, template.format(count=NUMBERS[len(props)], ids=",".join(p["id"] for p in props)), cid)
        elif constraint["field"] in PRINTED:
            emit(constraint["field"], constraint["rule"], cid)
        else:
            emit("rules", constraint["rule"], cid)

    preface = envelope["provenance"]["source_prompt"].strip()
    for text in sections["preface"]:
        if text not in preface:
            preface += f" {text}."
    convention = scene["ax"]["rotation_convention"]
    ax = sections["ax"] + [f"Euler {convention['euler_order']} {convention['kind']} {convention['handedness']}-handed "
                           f"{convention['units']},+X performer's left"]
    for surface in _items(envelope, "nodes", "surfaces"):
        cover.mark("surfaces", surface["id"])
        if surface.get("ax"):
            ax.append(surface["ax"])

    spec = {"variant": VARIANT, "fps": _num(scene["fps"]), "dur": float(scene["duration_s"]), "ax": ",".join(ax),
            "key": " ".join(sections["key"]), "lma_legend": _legend(), "negative": ",".join(sections["negative"]),
            "laban": _laban(envelope, beats, entities, labels, cover)}
    states = _items(envelope, "nodes", "states")
    for entity in entities:
        spec[labels[entity["id"]]] = _actor_rows(envelope, entity["id"], labels, cover)
    for prop in props:
        cover.mark("props", prop["id"])
        spec[prop["id"]] = _subject_rows(envelope, "prop", prop["id"], states, labels, cover)
    spec["set"] = {s["id"]: _subject_rows(envelope, "surface", s["id"], states, labels, cover)
                   for s in _items(envelope, "nodes", "surfaces")}
    for entity in entities:
        _subject_rows(envelope, "entity", entity["id"], states, labels, cover)
    spec["cam"] = _camera_rows(envelope, labels, cover)
    spec["anime"] = _anime(frame_parts, labels)
    for beat in beats:
        cover.mark("beats", beat["id"])
    spec["rules"] = ";".join(sections["rules"] + [b["action"] for b in beats])
    text = preface + " " + json.dumps(spec, ensure_ascii=False, separators=(",", ":"))
    return {"target": TARGET, "variant": VARIANT, "labels": labels, "text": text,
            "sha256": "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "coverage": cover.report(applied, rendered, enforced)}


def _legend():
    laban = library_vocab.load("laban_vocabulary")["fields"]
    body = library_vocab.load("bartenieff_vocabulary")["fields"]

    def values(fields, name):
        return "|".join(fields[name]["values"])

    return (f"BODY={{connectivity:{values(body, 'connectivity')}, pattern:{values(body, 'developmental_pattern')}, "
            f"initiation:part|core, follow:parts, mode:{values(body, 'body_mode')}}}. "
            f"EFFORT={{weight:{values(laban, 'effort.weight')}, time:{values(laban, 'effort.time')}, "
            f"space:{values(laban, 'effort.space')}, flow:{values(laban, 'effort.flow')}, "
            f"action:{values(laban, 'effort_action')}}}. "
            f"SHAPE={{quality:{values(laban, 'shape.quality')}, mode:{values(laban, 'shape.mode')}}}. "
            f"SPACE={{reach:{values(laban, 'space.kinesphere')}, pathway:{values(laban, 'space.pathway')}, "
            f"plane:{values(laban, 'space.plane')}}}. cpcs: values are labelled extensions, not LMA terms")


def _effort_words(e):
    effort = e["effort"]
    action = "" if e["effort_action"] == "none" else f" {e['effort_action']}"
    return f"{effort['weight']},{effort['time']},{effort['space']},{effort['flow']}{action}"


def _laban(envelope, beats, entities, labels, cover):
    efforts = sorted(_items(envelope, "nodes", "efforts"), key=lambda e: (e["t"], e["id"]))
    slots = {n["id"] for n in _items(envelope, "nodes", "motion")}
    laban = {}
    for entity in entities:
        sequence = [b["label"].replace("_", " ") for b in beats if f"{entity['id']}@{b['id']}" in slots]
        own = [e for e in efforts if e["actor"] == entity["id"]]
        for e in own:
            cover.mark("efforts", e["id"])
        laban[labels[entity["id"]]] = ">".join(sequence) + "; " + ">".join(_effort_words(e) for e in own)
    return laban


def _actor_rows(envelope, entity, labels, cover):
    kinematic = {n["id"]: n for n in _items(envelope, "nodes", "kinematic")}
    bartenieff = {n["id"]: n for n in _items(envelope, "nodes", "bartenieff")}
    states = {s["id"]: s for s in _items(envelope, "nodes", "states")}
    efforts = _items(envelope, "nodes", "efforts")
    contacts = _items(envelope, "nodes", "contacts")
    rows = []
    keys = [k for k in _items(envelope, "nodes", "motion") if k["entity"] == entity]
    for key in sorted(keys, key=lambda k: (k["t"], k["id"])):
        slot, beat = key["id"], key["beat"]
        for group in ("motion", "kinematic", "bartenieff"):
            cover.mark(group, slot)
        k, b = kinematic[slot], bartenieff[slot]
        parts = ["support=" + (",".join(k["support"]) or "none airborne"),
                 "KIN:" + ",".join(f"{c}={k[c]}" for c in CUES)]
        ext = " [labelled extension]" if b["extensions"] else ""
        parts.append(f"BODY:{b['connectivity']}{ext} connectivity,{b['developmental_pattern']} pattern,{b['initiation']} "
                     f"initiates,follow {'>'.join(b['follow_through'])},{b['body_mode']} mode,intent {b['intent']}")
        effort = next(e for e in efforts if e["actor"] == entity and beat in e["beats"])
        parts.append(f"EFFORT:{_effort_words(effort)},intensity {effort['intensity']},{effort['effort_mode']} mode")
        parts.append(f"SHAPE:{effort['shape']['quality']},{effort['shape']['mode']}")
        parts.append(f"SPACE:{effort['space']['kinesphere']} reach,{effort['space']['pathway']} pathway,"
                     f"{effort['space']['plane']} plane")
        state = states[slot]
        parts.append("STATE:" + ",".join(f"{p}={v}" for p, v in sorted(state["conditions"].items())))
        touching = [c for c in contacts if c["beat"] == beat and c["a"]["id"] == entity]
        for c in touching:
            cover.mark("contacts", c["id"])
        if touching:
            parts.append("CONTACT:" + ";".join(f"{c['contact_type']} {c['body_part']}->{c['b']['id']}"
                                               f"{'.' + c['b']['part'] if c['b'].get('part') else ''} at {_num(c['t'])}"
                                               for c in touching))
        if key["turn"] != "none":
            parts.append(f"TURN:{key['turn']} about {key['axis_declaration']}")
        rows.append([_num(key["t"]), key["name"], key["pos"], key["rot"], key["bones"],
                     "; ".join(parts) + "; " + key["description"]])
    return rows


def _subject_rows(envelope, kind, identity, states, labels, cover):
    """Initial conditions, then each change at the end of the beat that caused it, then contacts on this subject."""
    own = sorted((s for s in states if s["subject"] == {"kind": kind, "id": identity}), key=lambda s: (s["t"], s["id"]))
    ends = {b["id"]: round(b["t"] + b["dur"], 6) for b in _items(envelope, "nodes", "beats")}
    caused = {e["to_state"]: max(ends[b] for b in e["trigger_event"]) for e in _items(envelope, "edges", "state_transition")
              if e["trigger_event"]}
    rows = []
    previous = None
    for snapshot in own:
        cover.mark("states", snapshot["id"])
        if previous is None:
            rows.append(f"{_num(snapshot['t'])} " + ",".join(f"{p}={v}" for p, v in sorted(snapshot["conditions"].items())))
        else:
            changes = [f"{p} {previous['conditions'].get(p)}->{v}" for p, v in sorted(snapshot["conditions"].items())
                       if previous["conditions"].get(p) != v]
            if changes:
                rows.append(f"{_num(caused.get(snapshot['id'], snapshot['t']))} " + ",".join(changes))
        previous = snapshot
    for c in _items(envelope, "nodes", "contacts"):
        if c["b"]["kind"] == kind and c["b"]["id"] == identity:
            cover.mark("contacts", c["id"])
            who = labels.get(c["a"]["id"], c["a"]["id"])
            rows.append(f"{_num(c['t'])} {c['contact_type']} by {who} {c['body_part']}")
    return sorted(rows, key=lambda r: float(r.split(" ", 1)[0]))


def _camera_rows(envelope, labels, cover):
    rows = []
    for s in _items(envelope, "nodes", "camera"):
        cover.mark("camera", s["id"])
        d, name = s["derived"], (lambda x: labels.get(x, x))
        framing, angle, position, lens, focus = s["framing"], s["angle"], s["position"], s["lens"], s["focus"]
        quality, relation, composition = s["movement_quality"], s["relation_to_action"], s["composition"]
        detail = f" insert on {framing['detail']}" if framing["detail"] else ""
        cross = " across the axis" if s["editing"]["axis"] == "cross" else ""
        placement = ",".join(f"{name(k)} {v}" for k, v in sorted(composition["placement"].items()))
        parts = [
            f"{_num(s['t'])}-{_num(round(s['t'] + s['dur'], 6))} {s['id']} {s['editing']['transition_in']}{cross} to "
            f"{framing['scale']}{detail} on {','.join(name(x) for x in framing['subjects'])}: {framing['visible_action']}",
            f"angle elev {_num(angle['elevation_deg'])} az {_num(angle['azimuth_deg'])} roll {_num(angle['roll_deg'])}",
            f"position {name(position['target'])} {_num(position['distance_m'])}m {position['side']} side "
            f"camera {d['camera_pos']}",
            f"lens {_num(lens['focal_length_mm'])}mm {lens['perspective']} fov{d['fov_deg'][0]}x{d['fov_deg'][1]}",
            f"focus {name(focus['target'])} {focus['depth_of_field']} {focus['transition']}",
            f"movement {s['movement']['kind']}: {s['movement']['path']}",
            f"quality {quality['easing']},{quality['stability']},{quality['texture']}",
            f"rig {s['support']['rig']}",
            f"relation {relation['mode']} {name(relation['subject'])}: {relation['note']}",
            f"composition {placement},depth {composition['depth_anchor'] or 'none'},"
            f"negative space {composition['negative_space']}",
            f"playback {s['playback']['treatment']} x{_num(s['playback']['speed'])}",
            f"blur {s['blur']['motion_blur']} {','.join(s['blur']['affected'])}",
            f"eyeline {s['editing']['eyeline']}", f"intent {s['intent']}",
            f"motivation {s['motivation']['kind']}:{s['motivation']['ref']}"]
        rows.append("; ".join(parts))
    return rows


def _anime(frame_parts, labels):
    def who(subject):
        return labels.get(subject, subject)

    def span(item):
        return f"{_num(item['t0'])}-{_num(item['t1'])}"

    return {"impact": [_num(t) for t in frame_parts["impact"]],
            "smear": [f"{span(s)} {who(s['subject'])}{' ' + s['part'] if s['part'] else ''} only,{s['note']}"
                      for s in frame_parts["smear"]],
            "speedlines": [f"{span(s)} {who(s['subject'])}" for s in frame_parts["speedlines"]],
            "holds": [[_num(h["t"]), h["frames"]] for h in frame_parts["holds"]],
            "fx": ";".join(f"{_num(f['t'])}{'-' + str(_num(f['t_end'])) if f['t_end'] is not None else ''} {f['text']}"
                           for f in frame_parts["fx"]),
            "ink": frame_parts["ink"]}
