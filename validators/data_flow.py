"""The data flow (owner, 2026-10-13: "the graphs need to be a cog wheel"): which fields each layer reads and writes,
measured by running every layer on the envelope as it stood before that layer and tracking every key it touches.

`trace(envelope, plans)` re-runs each layer of a finished envelope on that envelope with the layer's own writes and
every later layer's taken away. A computed layer runs whole; an authored layer runs whole when its plan is given, and
otherwise only its packet is built (what the author is sent). Every `group.field` a layer touches is a read; a read of
a key the item does not hold is an absent read (the layer looks for it and falls back). `report(trace)` then names:

- phantom inputs: fields a layer reads that no layer writes (where a layer guesses);
- dead outputs: fields a layer writes that no later layer reads (and that are not the prompt itself);
- dormant inputs (`dormant(...)`): fields a layer reads whose value does not change what it writes.

The contract (kernel/data_flow.yaml) declares, per layer, its reads, writes, checks and the fields it passes
downstream; `contract_problems()` is the gate's check that the four examples still flow exactly as declared.
`python -m validators.data_flow [envelope.json] [--plans DIR] [--dormant]` prints the report;
`python -m validators.data_flow --write-contract` rewrites the contract from the examples.
"""

import argparse
import copy
import json
import sys
from pathlib import Path

import yaml

from kernel.canonical import ContractError, canonical_json
from planner.dependency_graph import ROOT, load, node_index
from validators.graph_map import EXAMPLES, MAP, _items_schema, _schema

CONTRACT = ROOT / "kernel" / "data_flow.yaml"
GROUPS = [".".join(where) for _, _, where in MAP] + ["scene", "intent"]
OUTPUT = {"nodes.render"}  # the prompt itself: written for the reader, not for a later layer


class _Tracked(dict):
    """A dict that logs every key read from it as (group, key, held)."""

    def __init__(self, data, log, group):
        super().__init__(data)
        self._log, self._group = log, group

    def _mark(self, key, held=None):
        self._log.add((self._group, key, dict.__contains__(self, key) if held is None else held))

    def __getitem__(self, key):
        self._mark(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        self._mark(key)
        return super().get(key, default)

    def __contains__(self, key):
        self._mark(key)
        return super().__contains__(key)

    def __iter__(self):
        return super().__iter__()

    def keys(self):
        return super().keys()

    def items(self):
        for key in super().keys():
            self._mark(key, True)
        return super().items()

    def values(self):
        for key in super().keys():
            self._mark(key, True)
        return super().values()

    def __deepcopy__(self, memo):  # a copy is not a read: the copy keeps logging into the same log
        return _Tracked({key: copy.deepcopy(value, memo) for key, value in super().items()}, self._log, self._group)

    def copy(self):
        return _Tracked(dict(super().items()), self._log, self._group)


def _holder(envelope, group):
    parts = group.split(".")
    holder = envelope
    for key in parts[:-1]:
        holder = holder.get(key, {})
    return holder, parts[-1]


def _wrap(envelope, log):
    envelope = copy.deepcopy(envelope)
    for group in GROUPS:
        holder, key = _holder(envelope, group)
        value = holder.get(key)
        if group in ("scene", "intent"):
            if isinstance(value, dict):
                holder[key] = _Tracked(value, log, group)
            continue
        if value is None:
            continue
        nested = isinstance(value, dict) and "items" in value
        items = [_Tracked(i, log, group) if isinstance(i, dict) else i for i in (value["items"] if nested else value)]
        if nested:
            value["items"] = items
        else:
            holder[key] = items
    return envelope


def _plain(envelope):
    return json.loads(canonical_json(envelope))


def _owner(order):
    """{envelope path: node} from the layer order's `writes`; the most specific path wins."""
    return {path: node["id"] for node in order["nodes"] for path in node.get("writes", [])}


def _group_of(path):
    """'/nodes/beats' -> 'nodes.beats'; '/scene/duration_s' -> ('scene', 'duration_s'); '/scene' -> 'scene'."""
    parts = path.strip("/").split("/")
    if parts[0] in ("nodes", "edges"):
        return ".".join(parts[:2]), None
    return parts[0], (parts[1] if len(parts) > 1 else None)


def _writes(envelope, order, node_id):
    """The `group.field`s a layer wrote into the finished envelope."""
    owners = _owner(order)
    out = set()
    for path, owner in owners.items():
        if owner != node_id:
            continue
        group, field = _group_of(path)
        if group == "validation":
            continue
        if field:
            if field in envelope.get(group, {}):
                out.add(f"{group}.{field}")
            continue
        holder, key = _holder(envelope, group)
        value = holder.get(key)
        if group in ("scene", "intent"):
            carved = {_group_of(p)[1] for p, o in owners.items() if o != node_id and _group_of(p)[0] == group}
            out |= {f"{group}.{k}" for k in (value or {}) if k not in carved}
            continue
        items = value.get("items") if isinstance(value, dict) and "items" in value else value
        out |= {f"{group}.{k}" for i in (items or []) if isinstance(i, dict) for k in i}
    return out


def _strip(envelope, order, sequence, node_id):
    """The envelope as it stood before `node_id`: its writes and every later layer's taken away."""
    out = copy.deepcopy(envelope)
    later = set(sequence[sequence.index(node_id):])
    for path, owner in sorted(_owner(order).items(), key=lambda p: -len(p[0])):
        if owner not in later:
            continue
        group, field = _group_of(path)
        if group == "validation":
            continue
        if field:
            out.get(group, {}).pop(field, None)
        elif group == "invariants":
            out["invariants"] = []
        elif group in ("scene", "intent"):
            out.pop(group, None)
        else:
            holder, key = _holder(out, group)
            holder.pop(key, None)
    history = out.get("provenance", {})
    steps = {node_index(order)[n]["step_id"] for n in later}
    if history:
        history["authored"] = [a for a in history.get("authored", []) if a["step_id"] not in steps]
        history["pass_history"] = [p for p in history.get("pass_history", []) if f"S{p['pass'][1:3]}" not in steps]
    return out


def _sequence(envelope):
    return [p["pass"].split("_", 1)[1] for p in envelope["provenance"]["pass_history"]]


def _render_plan(envelope, before):
    """S17's document rebuilt from the render node (its frame parts are the only authored field)."""
    from compiler.passes.derived import p17_render

    render = envelope["nodes"]["render"]["items"][0]
    packet = p17_render.prepare(before)
    return {"step_id": "S17", "band": "L6", "packet_sha256": packet["packet_sha256"],
            "author": {"host": "data-flow trace", "model": "rebuilt"}, "attempt": 1, "frame_parts": render["frame_parts"]}


def run_layer(node_id, before, envelope, plans, order, *, cards=None, untracked=None):
    """Run one layer on `before`; returns (envelope after, mode). `envelope` is the finished one (query, render plan);
    `untracked`, the same input without tracking, rebuilds the render plan so its hashing is not counted as reads."""
    from compiler import pipeline
    from compiler.passes.derived import p09_object_state, p10_affordance
    from compiler.passes.mandatory import p01_intent, p02_brief, p03_constraint, p05_causal, p06_state, p07_contact

    query = envelope["provenance"]["source_prompt"]
    computed = {
        "intent": lambda env: p01_intent.run(env, query, genre=envelope["intent"]["flags"]["genre"],
                                             duration_s=envelope["intent"]["flags"]["duration_s"], order=order),
        "brief": lambda env: p02_brief.run(env, cards=cards, order=order),
        "constraint": lambda env: p03_constraint.run(env, cards=cards, order=order),
        "causal": lambda env: p05_causal.run(env, order=order),
        "state": lambda env: p06_state.run(env, order=order),
        "contact": lambda env: p07_contact.run(env, order=order),
        "object_state": lambda env: p09_object_state.run(env, order=order),
        "affordance": lambda env: p10_affordance.run(env, order=order),
    }
    if node_id in computed:
        return computed[node_id](before), "computed"
    module = pipeline.AUTHORED[node_id]
    plan = (plans or {}).get(node_id)
    if plan is None and node_id == "render":
        plan = _render_plan(envelope, _plain(untracked if untracked is not None else before))
    if plan is None:
        module.prepare(before)
        return None, "packet only"
    after, _ = module.run(before, plan, order=order)
    return after, "authored"


def trace(envelope, plans=None, *, cards=None):
    """{node: {step, mode, reads, absent, writes, reproduced, error}} for every layer the envelope ran."""
    order = load()
    index = node_index(order)
    sequence = _sequence(envelope)
    out = {}
    for node_id in sequence:
        log = set()
        before = _strip(envelope, order, sequence, node_id)
        row = {"step": index[node_id]["step_id"], "writes": _writes(envelope, order, node_id), "error": None,
               "reproduced": None}
        try:
            after, row["mode"] = run_layer(node_id, _wrap(before, log), envelope, plans, order, cards=cards,
                                           untracked=before)
            seen = set(log)  # before the comparison below reads the copies
            if after is not None:
                after = _plain(after)
                row["reproduced"] = all(_holder(after, g)[0].get(_holder(after, g)[1]) ==
                                        _holder(envelope, g)[0].get(_holder(envelope, g)[1])
                                        for g in {w.rsplit(".", 1)[0] for w in row["writes"]} if g not in ("scene",))
        except ContractError as refused:
            row["mode"], row["error"] = "refused", f"{refused.code}: {str(refused)[:160]}"
        except Exception as crashed:  # noqa: BLE001 - a layer that cannot run on its own input is a finding
            row["mode"], row["error"] = "crashed", f"{type(crashed).__name__}: {str(crashed)[:160]}"
        if row["error"]:
            seen = set(log)
        row["reads"] = {f"{g}.{k}" for g, k, held in seen if held}
        row["absent"] = {f"{g}.{k}" for g, k, held in seen if not held} - row["reads"]
        out[node_id] = row
    return out


def declared_fields():
    """{group: fields its schema section declares} for every graph group."""
    out = {}
    for name, section, where in MAP:
        item = _items_schema(_schema(name), section)
        out[".".join(where)] = set(item.get("properties", {})) if isinstance(item, dict) else set()
    return out


def report(rows, order=None, written_anywhere=None):
    """{node: {phantom, unexercised, optional, early, dead, passes_downstream}} from a trace.

    phantom: read, declared by no schema and written by no layer in this envelope nor in any of `written_anywhere` (the
    code looks for what nothing produces: there the layer guesses); unexercised: the same, but its schema declares it
    (an optional field no envelope traced fills); optional: written in another envelope, not in this one; early: written
    only by a later layer; dead: written and read by no later layer (an `id` is identity, not data, and the prompt
    itself is the end of the line)."""
    order = order or load()
    declared = {_group_of(p)[0] for p in _owner(order)}
    sequence = list(rows)
    written = {}
    for node_id in sequence:
        for field in rows[node_id]["writes"]:
            written.setdefault(field, node_id)
    anywhere = set(written) | set(written_anywhere or ())
    schema = declared_fields()
    out = {}
    for i, node_id in enumerate(sequence):
        row = rows[node_id]
        earlier = set(sequence[:i])
        phantom, unexercised, optional, early = set(), set(), set(), set()
        for field in (row["reads"] | row["absent"]) - row["writes"]:
            if field.rsplit(".", 1)[0] not in declared or written.get(field) in earlier:
                continue
            if field in written:
                early.add(field)
            elif field in anywhere:
                optional.add(field)
            else:
                group, key = field.rsplit(".", 1)
                (unexercised if key in schema.get(group, ()) else phantom).add(field)
        later = [rows[n]["reads"] | rows[n]["absent"] for n in sequence[i + 1:]]
        later_reads = set().union(*later) if later else set()
        dead = {f for f in row["writes"]
                if f not in later_reads and f.rsplit(".", 1)[0] not in OUTPUT and not f.endswith(".id")}
        out[node_id] = {"phantom": sorted(phantom), "unexercised": sorted(unexercised), "optional": sorted(optional),
                        "early": sorted(early),
                        "dead": sorted(dead), "passes_downstream": sorted(row["writes"] - dead)}
    return out


def written_in(named_rows):
    """Every `group.field` some layer writes in any of the traced envelopes."""
    return {f for rows in named_rows.values() for row in rows.values() for f in row["writes"]}


def _mutate(value):
    """A different value of the same shape: numbers nudged, strings suffixed, lists and dicts changed inside."""
    if isinstance(value, bool):
        return not value
    if isinstance(value, (int, float)):
        return value + 0.37
    if isinstance(value, str):
        return value + "_x"
    if isinstance(value, list):
        if value and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value):
            return [v + 0.37 for v in value]
        return [_mutate(v) for v in value] if value else ["x"]
    if isinstance(value, dict):
        return {k: _mutate(v) for k, v in value.items()} if value else {"x": "x"}
    return "x"


def dormant(envelope, plans=None, *, cards=None, rows=None):
    """{node: [fields]}: held reads whose value, changed on every item, leaves the layer's writes the same.

    Authored layers run without the packet binding (the packet changes with the field); a layer that refuses or
    crashes on the changed value uses it."""
    from compiler import authoring

    order = load()
    sequence = _sequence(envelope)
    rows = rows or trace(envelope, plans, cards=cards)
    bind = authoring.bind
    authoring.bind = lambda packet, document: None
    out = {}
    try:
        for node_id in sequence:
            row = rows[node_id]
            if row["mode"] not in ("computed", "authored"):
                continue
            before = _strip(envelope, order, sequence, node_id)
            groups = sorted({w.rsplit(".", 1)[0] for w in row["writes"]})
            base, _ = run_layer(node_id, copy.deepcopy(before), envelope, plans, order, cards=cards)
            base = canonical_json({g: _holder(_plain(base), g)[0].get(_holder(base, g)[1]) for g in groups})
            out[node_id] = []
            for field in sorted(row["reads"]):
                if all(_same(node_id, before, field, scope, base, groups, envelope, plans, order, cards)
                       for scope in ("every", "first")):
                    out[node_id].append(field)
    finally:
        authoring.bind = bind
    return out


def _same(node_id, before, field, scope, base, groups, envelope, plans, order, cards):
    """Whether the layer writes the same with `field` changed on every item (`every`) or on the first (`first`)."""
    group, key = field.rsplit(".", 1)
    changed = copy.deepcopy(before)
    holder, name = _holder(changed, group)
    value = holder.get(name)
    if group in ("scene", "intent"):
        value[key] = _mutate(value[key])
    else:
        items = [i for i in (value["items"] if isinstance(value, dict) and "items" in value else value) if key in i]
        for item in items if scope == "every" else items[:1]:
            item[key] = _mutate(item[key])
    try:
        after = _plain(run_layer(node_id, changed, envelope, plans, order, cards=cards)[0])
    except Exception:  # noqa: BLE001 - refusing or crashing on the change is using the field
        return False
    return canonical_json({g: _holder(after, g)[0].get(_holder(after, g)[1]) for g in groups}) == base


def _example(name):
    folder = ROOT / "examples" / name
    return (json.loads((folder / "envelope.json").read_text(encoding="utf-8")),
            {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((folder / "plans").glob("*.json"))})


def _example_rows():
    return {name: trace(*_example(name)) for name in EXAMPLES}


def contract_from(example_rows):
    """The contract the four examples show: per layer, its reads, writes, checks and fields passed downstream."""
    order = load()
    index = node_index(order)
    layers = {}
    anywhere = written_in(example_rows)
    for rows in example_rows.values():
        flow = report(rows, order, anywhere)
        for node_id, row in rows.items():
            layer = layers.setdefault(node_id, {"step": row["step"], "reads": set(), "writes": set(),
                                                "validates": list(index[node_id].get("validated_by", [])),
                                                "passes_downstream": set()})
            layer["reads"] |= row["reads"] | row["absent"]
            layer["writes"] |= row["writes"]
            layer["passes_downstream"] |= set(flow[node_id]["passes_downstream"])
    ordered = sorted(layers.items(), key=lambda kv: kv[1]["step"])
    return {"version": 1, "status": "draft", "measured_on": list(example_rows),
            "about": "Per layer: the graph fields it reads (held or looked for), writes, checks it runs (the layer "
                     "order's validated_by) and passes downstream (written and read by a later layer). Measured by "
                     "validators/data_flow.py on the examples; the gate refuses any layer that flows otherwise.",
            "layers": [{"id": n, "step": v["step"], "reads": sorted(v["reads"]), "writes": sorted(v["writes"]),
                        "validates": v["validates"], "passes_downstream": sorted(v["passes_downstream"])}
                       for n, v in ordered]}


def contract_problems(example_rows=None, declared=None):
    """[{code, layer, message}]: DATA_FLOW_CONTRACT for a layer that reads or writes other than it declares, or runs
    other than whole on an example; DATA_FLOW_PHANTOM for a read no layer writes."""
    declared = declared or yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    example_rows = example_rows or _example_rows()
    found = contract_from(example_rows)
    index = node_index(load())
    out = []
    want = {layer["id"]: layer for layer in declared["layers"]}
    for layer in found["layers"]:
        node_id, have = layer["id"], want.get(layer["id"])
        if have is None:
            out.append({"code": "DATA_FLOW_CONTRACT", "layer": node_id, "message": f"{node_id} has no contract"})
            continue
        for key in ("reads", "writes", "passes_downstream"):
            extra, missing = set(layer[key]) - set(have[key]), set(have[key]) - set(layer[key])
            if extra or missing:
                out.append({"code": "DATA_FLOW_CONTRACT", "layer": node_id,
                            "message": f"{node_id} {key}: undeclared {sorted(extra)}, declared but not seen {sorted(missing)}"})
        if have["validates"] != list(index[node_id].get("validated_by", [])):
            out.append({"code": "DATA_FLOW_CONTRACT", "layer": node_id,
                        "message": f"{node_id} validates {have['validates']}, the layer order says "
                                   f"{index[node_id].get('validated_by', [])}"})
    for name, rows in example_rows.items():
        for node_id, row in rows.items():
            if row["mode"] not in ("computed", "authored") or row["reproduced"] is False:
                out.append({"code": "DATA_FLOW_CONTRACT", "layer": node_id,
                            "message": f"{name}: {node_id} does not turn on its own input ({row['mode']}, "
                                       f"reproduced {row['reproduced']}, {row['error']})"})
        for node_id, flow in report(rows, written_anywhere=written_in(example_rows)).items():
            if flow["phantom"]:
                out.append({"code": "DATA_FLOW_PHANTOM", "layer": node_id,
                            "message": f"{name}: {node_id} reads what no layer writes: {flow['phantom']}"})
    return out


def markdown(name, rows, flow, quiet=None):
    out = [f"## {name}", "", "| Step | Layer | Mode | Reads | Writes | Phantom | Optional or unexercised | Read too early | "
           "Dead | Dormant |", "|---|---|---|---|---|---|---|---|---|---|"]
    for node_id, row in rows.items():
        f = flow[node_id]
        q = (quiet or {}).get(node_id)
        out.append(f"| {row['step']} | {node_id} | {row['mode']}{' (' + row['error'] + ')' if row['error'] else ''} | "
                   f"{len(row['reads'])} | {len(row['writes'])} | {', '.join(f['phantom']) or '—'} | "
                   f"{', '.join(f['unexercised'] + f['optional']) or '—'} | "
                   f"{', '.join(f['early']) or '—'} | {', '.join(f['dead']) or '—'} | "
                   f"{'—' if q is None else (', '.join(q) or 'none')} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m validators.data_flow")
    parser.add_argument("envelope", nargs="?")
    parser.add_argument("--plans")
    parser.add_argument("--dormant", action="store_true")
    parser.add_argument("--write-contract", action="store_true")
    args = parser.parse_args(argv)
    if args.write_contract:
        CONTRACT.write_text(yaml.safe_dump(contract_from(_example_rows()), sort_keys=False, width=120), encoding="utf-8")
        print("wrote", CONTRACT.relative_to(ROOT))
        return
    if args.envelope:
        targets = {Path(args.envelope).parent.name: (json.loads(Path(args.envelope).read_text(encoding="utf-8")),
                   {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(args.plans).glob("*.json"))}
                   if args.plans else None)}
    else:
        targets = {name: _example(name) for name in EXAMPLES}
    traced = {name: trace(envelope, plans) for name, (envelope, plans) in targets.items()}
    anywhere = written_in(traced) | (written_in(_example_rows()) if args.envelope else set())
    for name, (envelope, plans) in targets.items():
        quiet = dormant(envelope, plans, rows=traced[name]) if args.dormant else None
        print(markdown(name, traced[name], report(traced[name], written_anywhere=anywhere), quiet))


if __name__ == "__main__":
    sys.exit(main())
