"""S17 renderer for ugc_ad: the shared LBN projection plus a `ugc` block that carries the UGC graphs.

The ugc block lists every hand-role interaction with its locked hands and grips, each object's internal state track,
every proven affordance (before -> after, grip, duration) and the enables links, then the frame parts. Like the anime
renderer it is uncompressed and every item is counted in coverage.
"""

from renderers.anime_renderer import _anime, _num, project


def render(envelope, frame_parts):
    return project(envelope, frame_parts, "ugc", lambda labels, cover: _ugc(envelope, frame_parts, labels, cover))


def _state(state):
    return "|".join(f"{p}:{v}" for p, v in sorted(state.items()))


def _conditions(rows):
    return ",".join(f"{c['property']} in {'|'.join(c['values'])}" for c in rows) or "none"


def _ugc(envelope, frame_parts, labels, cover):
    nodes, edges = envelope["nodes"], envelope["edges"]
    roles = []
    for i in nodes["hand_role"]["items"]:
        cover.mark("hand_role", i["id"])
        roles.append(f"{_num(i['t'])}-{_num(i['end'])} {i['id']} {i['verb']} {i['object']}: agent {labels[i['actor']]} "
                     f"{i['agent_hand']} {i['agent_grip']}, support {i['support_hand']} {i['support_grip']}, "
                     f"{i['role_template']}; {i['role_invariant']}")
    states = {}
    for s in nodes["object_state"]["items"]:
        cover.mark("object_state", s["id"])
        states.setdefault(s["object"], []).append(f"{_num(s['t'])} {s['state_name']}"
                                                  f"{' during ' + s['interaction'] if s['interaction'] else ''}")
    for e in edges["object_state_transition"]["items"]:
        changes = ",".join(f"{c['property']} {c['from']}->{c['to']}" for c in e["changes"])
        states[e["to"].split("@")[0]].append(f"change {changes} from {e['from']} to {e['to']} in {e['trigger_beat']} by "
                                             f"{e['trigger_contact']} ({e['interaction']})")
    proven = []
    for a in nodes["affordance"]["items"]:
        cover.mark("affordance", a["id"])
        proven.append(f"{a['id']} {a['action']} {a['object']}: before {_state(a['before'])} -> after {_state(a['after'])}; "
                      f"pre "
                      f"{_conditions(a['preconditions'])}; post {_conditions(a['postconditions'])}; grip {a['required_grip']}; "
                      f"agent grip {a['agent_grip']}; {_num(a['duration'])}s in "
                      f"{a['duration_range'][0]}-{a['duration_range'][1]}s; proven")
    handoffs = [f"{e['from']} -> {e['to']}: agent hand {'changes' if e['agent_hand_changed'] else 'stays'}, support hand "
                f"{'changes' if e['support_hand_changed'] else 'stays'}" for e in edges["hand_role_transition"]["items"]]
    return {"hand_roles": roles, "handoffs": handoffs, "object_states": states, "affordances": proven,
            "enables": [f"{e['from']} enables {e['to']} via {','.join(e['via'])}"
                        for e in edges["affordance_dependency"]["items"]],
            "frames": _anime(frame_parts, labels)}
