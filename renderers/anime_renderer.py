"""S17 renderer: deterministic projection of a built envelope into the full LBN-2.x layout (anime target).

Uncompressed and model-agnostic: no length budget, no model-specific formatting. Every node group item and every
applied constraint is rendered (owner invariant no_render_compression) and `coverage` proves it item by item.
Kernel controls written for the reference actors and props are regenerated from this scene's data (labels,
facings, props); scene-wide kernel controls are printed as written; card invariants and beat actions go to rules.
Layout: preface text, then one JSON object: variant, fps, dur, ax, key, lma_legend, negative, laban (each fighter's
own moves, the beats it acts in, then its efforts: F-091, RV-16), one track per actor label (rows with named fields
{t, label, pos, rot, joints, desc}, owner O9), one track per prop, set (surfaces), cam, the genre block (here: anime
frame-part directives), rules.
`project` is shared with renderers/ugc_renderer.py.
"""

import hashlib
import json
import math

from planner import library_vocab
from renderers import prop_samples

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


def inbetweens(envelope):
    """The in-between keys S13's follows edges carry (ADR-O109, RV-59i), in time order."""
    return sorted((b for e in _items(envelope, "edges", "motion") for b in e.get("inbetweens", [])),
                  key=lambda b: (b["t"], b["id"]))


def inbetweens_turning(envelope):
    """The ids of the in-between keys inside a declared turn: those whose entity's key before declares one, the turn
    each carries (ADR-O109, RV-59k; solver/interpolation.py), so a prose line prints its root as mid-turn (W3)."""
    keys = sorted(_items(envelope, "nodes", "motion"), key=lambda k: k["t"])
    out = set()
    for between in inbetweens(envelope):
        before = [k for k in keys if k["entity"] == between["entity"] and k["t"] < between["t"]]
        if before and before[-1].get("turn", "none") != "none":
            out.add(between["id"])
    return out


class _Coverage:
    def __init__(self, envelope):
        self.groups = {g: {i["id"] for i in envelope["nodes"][g]["items"]} for g in envelope["nodes"] if g != "render"}
        if inbetweens(envelope):  # ADR-O109 (RV-59i): every in-between key is printed
            self.groups["inbetweens"] = {b["id"] for b in inbetweens(envelope)}
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
    return project(envelope, frame_parts, "anime", lambda labels, cover: _anime(frame_parts, labels))


def first_facings(envelope):
    first = {}
    for beat in sorted(_items(envelope, "nodes", "beats"), key=lambda b: (b["t"], b["id"])):
        for entity, vector in beat["facing"].items():
            first.setdefault(entity, vector)
    return first


def constraint_rows(envelope, labels):
    """Every applied constraint as (section, text, constraint id, kernel ref), in constraint order.

    Kernel controls written for the reference cast are regenerated for this scene (GENERATED); owner render controls
    come back with section None (enforced by coverage, never printed). Shared with renderers/prose_renderer.py.
    """
    entities, props = _items(envelope, "nodes", "entities"), _items(envelope, "nodes", "props")
    first_facing = first_facings(envelope)
    constraints = {c["id"]: c for c in _items(envelope, "nodes", "constraints")}
    applications = _items(envelope, "edges", "constraint_application")
    applied = {a["constraint_id"] for a in applications}
    targets = {}
    for a in applications:
        targets.setdefault(a["constraint_id"], []).append(a["target"])
    prop_cards = {p["id"]: p for p in props}
    rows = []
    for cid in sorted(applied, key=lambda c: list(constraints).index(c)):
        constraint = constraints[cid]
        ref = constraint["source"]["ref"]
        if constraint["field"] in ENFORCED:
            rows.append((None, None, cid, ref))
        elif ref in GENERATED:
            section, scope, template = GENERATED[ref]
            actors = [labels[t["id"]] for t in targets[cid] if t["kind"] == "entity"]
            if scope == "actor":
                for target in targets[cid]:
                    if target["kind"] == "entity":
                        rows.append((section, template.format(label=labels[target["id"]], facing=_facing(
                            first_facing.get(target["id"], [0, 0, 1]))), cid, ref))
            elif scope == "scene":
                every = [labels[e["id"]] for e in entities] or actors
                rows.append((section, template.format(labels=_join(every), count=NUMBERS[len(every)]), cid, ref))
            elif scope == "prop":
                for target in targets[cid]:
                    if target["kind"] == "prop":
                        card = prop_cards[target["id"]]
                        if card.get("count", 1) > 1:
                            text = (f"no duplicated {card['unit_name']} beyond the declared {card['group_name']} "
                                    f"of {card['count']}")
                        else:
                            text = f"no duplicated {card['name']}"
                        rows.append((section, text, cid, ref))
            else:
                rows.append((section, template.format(count=NUMBERS[len(props)], ids=",".join(p["id"] for p in props)),
                             cid, ref))
        elif constraint["field"] in PRINTED:
            rows.append((constraint["field"], constraint["rule"], cid, ref))
        else:
            rows.append(("rules", constraint["rule"], cid, ref))
    return applied, rows


def project(envelope, frame_parts, block_key, genre_block):
    """The shared LBN projection; `genre_block(labels, cover)` builds the genre's own block (placed before rules)."""
    cover = _Coverage(envelope)
    scene = envelope["scene"]
    entities = _items(envelope, "nodes", "entities")
    props = _items(envelope, "nodes", "props")
    labels = {e["id"]: chr(ord("A") + i) for i, e in enumerate(entities)}
    for e in entities:
        cover.mark("entities", e["id"])
    beats = sorted(_items(envelope, "nodes", "beats"), key=lambda b: (b["t"], b["id"]))
    applied, rows = constraint_rows(envelope, labels)
    sections = {name: [] for name in PRINTED}
    rendered, enforced = set(), set()
    for section, text, cid, _ in rows:
        cover.mark("constraints", cid)
        if section is None:
            enforced.add(cid)
            continue
        if text not in sections[section]:
            sections[section].append(text)
        rendered.add(cid)

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
    if scene.get("chained_from"):
        spec["chained_from"] = _chained(scene["chained_from"], envelope, labels, cover)
    spec["cam"] = _camera_rows(envelope, labels, cover)
    spec[block_key] = genre_block(labels, cover)
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
    """{label: "move>move; effort>effort"}: each fighter's own moves, the beats it acts in, in time order, as the 2.4
    source chains them (F-091, RV-16: a beat it only takes part in is the actor's move, not its own), then its own
    efforts; "none" for a fighter that acts in no beat."""
    efforts = sorted(_items(envelope, "nodes", "efforts"), key=lambda e: (e["t"], e["id"]))
    laban = {}
    for entity in entities:
        sequence = [b["label"].replace("_", " ") for b in beats if b["actor"] == entity["id"]]
        own = [e for e in efforts if e["actor"] == entity["id"]]
        for e in own:
            cover.mark("efforts", e["id"])
        laban[labels[entity["id"]]] = (">".join(sequence) or "none") + "; " + ">".join(_effort_words(e) for e in own)
    return laban


def _actor_rows(envelope, entity, labels, cover):
    kinematic = {n["id"]: n for n in _items(envelope, "nodes", "kinematic")}
    bartenieff = {n["id"]: n for n in _items(envelope, "nodes", "bartenieff")}
    states = {s["id"]: s for s in _items(envelope, "nodes", "states")}
    efforts = _items(envelope, "nodes", "efforts")
    contacts = _items(envelope, "nodes", "contacts")
    facial = {n["id"]: n for n in _items(envelope, "nodes", "facial")}
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
        face = facial.get(slot)
        if face is not None:  # S14, live_action and ugc_ad: words only (owner F4)
            cover.mark("facial", slot)
            parts.append(_face_words(face, labels))
        rows.append({"t": _num(key["t"]), "label": key["name"], "pos": key["pos"], "rot": key["rot"],
                     "joints": key["bones"], "desc": "; ".join(parts) + "; " + key["description"]})
    between = [b for b in inbetweens(envelope) if b["entity"] == entity]
    for b in between:  # ADR-O109 (RV-59i): a pose the interpolation passes through, at its instant
        cover.mark("inbetweens", b["id"])
        rows.append({"t": _num(b["t"]), "label": b["name"], "pos": b["pos"], "rot": b["rot"], "joints": b["bones"],
                     "desc": "IN-BETWEEN key (no beat, no contact): the interpolation passes through this pose; "
                             + b["description"]})
    return sorted(rows, key=lambda row: float(row["t"])) if between else rows


def _face_words(face, labels):
    words = face["words"]
    target = face["gaze_target"]
    gaze = words["gaze"] if target in ("camera", "none") else f"eyes on {labels.get(target, target)}"
    lead = "FACE (carries the beat)" if face["salience"] == "carries_beat" else "FACE"
    text = f"{lead}: " + (", ".join(words["face"]) or "relaxed, no visible expression")
    if words["not"]:
        text += "; NOT: " + ", ".join(words["not"])
    return text + f"; feeling {words['feeling']}, {words['display']}; {gaze}; {face['description']}"


def _subject_rows(envelope, kind, identity, states, labels, cover):
    """Initial conditions, then each change at the instant S06 commits it, then contacts on this subject."""
    own = sorted((s for s in states if s["subject"] == {"kind": kind, "id": identity}), key=lambda s: (s["t"], s["id"]))
    caused = {e["to_state"]: {c["property"]: c["t"] for c in e["changes"]}  # each change's S06 instant (F-061, F-132)
              for e in _items(envelope, "edges", "state_transition")}
    rows = []
    previous = None
    for snapshot in own:
        cover.mark("states", snapshot["id"])
        if previous is None:
            rows.append(f"{_num(snapshot['t'])} " + ",".join(f"{p}={v}" for p, v in sorted(snapshot["conditions"].items())))
        else:
            changes = {}
            for p, v in sorted(snapshot["conditions"].items()):
                if previous["conditions"].get(p) != v:
                    changes.setdefault(caused.get(snapshot["id"], {}).get(p, snapshot["t"]), []).append(
                        f"{p} {previous['conditions'].get(p)}->{v}")
            rows += [f"{_num(t)} " + ",".join(texts) for t, texts in sorted(changes.items())]
        previous = snapshot
    for c in _items(envelope, "nodes", "contacts"):
        if c["b"]["kind"] == kind and c["b"]["id"] == identity:
            cover.mark("contacts", c["id"])
            who = labels.get(c["a"]["id"], c["a"]["id"])
            rows.append(f"{_num(c['t'])} {c['contact_type']} by {who} {c['body_part']}")
    if kind == "prop":  # owner O8: authored position and velocity samples
        rows += [text for _, text in prop_samples.rows(envelope, labels, identity, compact=True)]
    return sorted(rows, key=lambda r: float(r.split(" ", 1)[0]))


def _chained(chained, envelope, labels, cover):
    """M5.5: what this clip continues: carried end states, carried contacts, unresolved causes, the last shot."""
    carried = []
    for c in _items(envelope, "nodes", "contacts"):
        if c["beat"] == "chain":
            cover.mark("contacts", c["id"])
            part = "." + c["b"]["part"] if c["b"].get("part") else ""
            carried.append(f"{c['id']} {c['contact_type']} {labels.get(c['a']['id'], c['a']['id'])} {c['body_part']}->"
                           f"{labels.get(c['b']['id'], c['b']['id'])}{part} from t=0")
    return {"previous": chained["envelope_sha256"], "previous_prompt": chained["source_prompt"],
            "carried_states": [f"{labels.get(s['subject']['id'], s['subject']['id'])}: "
                               + ",".join(f"{p}={v}" for p, v in sorted(s["conditions"].items()))
                               for s in chained["end_states"]],
            "carried_contacts": carried,
            "unresolved_causes": [f"{b['id']} {b['label']}: {b['action']}" for b in chained["open_beats"]],
            "last_shot": chained["last_shot"]}


def _camera_rows(envelope, labels, cover):
    rows = []
    for s in _items(envelope, "nodes", "camera"):
        cover.mark("camera", s["id"])
        d, name = s["derived"], (lambda x: labels.get(x, x))
        framing, angle, position, lens, focus = s["framing"], s["angle"], s["position"], s["lens"], s["focus"]
        quality, relation, composition = s["movement_quality"], s["relation_to_action"], s["composition"]
        detail = (f" on {framing['detail']}" if framing["scale"] == "insert" else f" insert on {framing['detail']}") \
            if framing["detail"] else ""
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
