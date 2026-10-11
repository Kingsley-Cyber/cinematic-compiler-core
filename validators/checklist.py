"""M8.10 per-prompt DAG checklist (owner 2026-10-11; rulings O13 and O14 in docs/plans/MASTER_PLAN.md).

Every prompt the compiler writes (render.txt, the LBN-2.4 projection, and the four prose_<mode>.txt) is judged against
all 84 checklist rows of kernel/knowledge_map.yaml: the 109 rows minus the 25 evidence rows, which are never enforced.
Each cell is PASS, FAIL, NOT CHECKED or N/A, with its evidence:

- PASS: the row is enforced and each of its semantic codes (validators/prompt_validator.py) passes on this prompt,
  which carries every section those codes read. An excluded row passes when its code finds the excluded thing absent,
  or an owner decision keeps it (O3: LBN-2.4 keeps 'root exact').
- FAIL: a code of the row fires, or the prompt lacks a section the code reads (silence is not a pass).
- NOT CHECKED: no code covers the row, or covers only part of it (partial and missing rows, rows checked on the graph
  only, menus nothing selects yet, open owner questions).
- N/A: only by owner O14: T3 and T4 (superseded by T5 in the DAG), and menu rows that another mode or genre selects
  (C11, C14-C17). C26's 14 unnamed states are N/A inside C26, which checks the two the DAG names.

O13: the five prompts are fragments of one complete prompt (one content set in the DAG's template, the mode as a
setting), so the Any column is their union: PASS if any prompt passes, else NOT CHECKED if any is unchecked, else
FAIL. A prompt is a deliverable only with no FAIL and no NOT CHECKED row; `--gate` refuses the rest. The tables sit
next to the prompts (examples/<name>/checklist.md); tests/test_checklist.py keeps them current.

    python -m validators.checklist           # report every prompt; exit 1 if a checklist.md is stale
    python -m validators.checklist --write   # rewrite them
    python -m validators.checklist --gate    # also exit 1 unless every prompt is a deliverable
"""

import hashlib
import json
import sys

import yaml

from compiler.examples import EXAMPLES, render_text
from planner.dependency_graph import ROOT
from validators import prompt_validator

PASS, FAIL, OPEN, NA = "PASS", "FAIL", "NOT CHECKED", "N/A"
RESULTS = (PASS, FAIL, OPEN, NA)
PROMPTS = (("LBN", "render.txt", "euler_heavy"), ("Pure", "prose_pure_staff.txt", "pure_staff"),
           ("Mixed", "prose_mixed.txt", "mixed"), ("Upgr", "prose_upgraded_mixed.txt", "upgraded_mixed"),
           ("Euler", "prose_euler_heavy.txt", "euler_heavy"))
LBN_EXEMPT = {"ROOT_EXACT_PRESENT": "owner O3 keeps 'root exact' in LBN-2.4"}
MESSAGE_CHARS = 120
FINDINGS_DOC = "docs/reports/2026-10-11-renders-and-dag-adherence.md"
RENDERED = ("reference_fight",)
EVERY = ("reference_fight", "live_action_standoff", "wizard_vs_acrobat", "ugc_glasses_demo")
# The findings doc, section 3: per finding, the examples it holds for (renders R1-R5 were all of the reference fight; F1
# found placeholder causes in live_action_standoff too; F2 holds for every prose prompt), the checklist rows it
# implicates, and the codes that now catch it (a test reproduces what was seen and the code fails it). A finding that
# no code of a row catches turns that row's PASS into NOT CHECKED: a render contradicts it (owner, 2026-10-11:
# "harden the 16 pass rows"). F2 no longer names V8: stacking two graphs is not what F2 saw (reasons unprinted).
FINDINGS = {
    "F1": (("reference_fight", "live_action_standoff"), ("C6", "T9", "C21", "C26", "C27"), ("CAUSE_REASON",)),
    "F2": (EVERY, ("C6", "V7"), ("CAUSE_REASON",)),
    "F3": (("reference_fight", "live_action_standoff"), ("M4",), ()),
    "F4": (RENDERED, ("C10", "C11", "C25", "V3", "V6"), ()),
    "F5": (RENDERED, ("C10", "C12", "C25"), ()),
    "F6": (RENDERED, ("C2", "C3", "C4"), ()),
    "F7": (RENDERED, ("BIO", "T7", "C5"), ("AIRBORNE_PICKUP",)),
    "F8": (RENDERED, ("C5", "C7", "C31"), ("PROP_LINE_MISSING", "DOUBLED_WORD")),
    "F9": (RENDERED, ("C5", "C23"), ("PROP_FIRST_STATE",)),
    "F10": (RENDERED, ("M1", "C9"), ()),
    "F11": (RENDERED, ("C5", "C24"), ("PROP_FIRST_STATE",)),
    "F12": (RENDERED, ("C5", "NEG"), ("COUNT_CONTRADICTION",)),
    "F13": (RENDERED, ("C9", "C23"), ()),
    "F14": (RENDERED, ("C1", "C2"), ()),
    "F15": (RENDERED, ("C12", "C25"), ()),
}


def rows():
    """The 84 checklist rows of the map, in map order."""
    data = yaml.safe_load((ROOT / "kernel" / "knowledge_map.yaml").read_text(encoding="utf-8"))
    return [row for row in data["rows"] if row["class"] != "evidence"]


def _short(text, limit=MESSAGE_CHARS):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def gist(note, limit=170):
    """The note's first sentence, shortened."""
    text = " ".join(note.split())
    cut = text.find(". ", 40)
    return _short(text if cut < 0 else text[:cut + 1], limit)


def _lbn_graphs(text, envelope):
    """The LBN-2.4 fields that embed a graph other than a prop track: per-performer keys, camera and Laban phrases."""
    fields = json.JSONDecoder().raw_decode(text[text.index('{"variant"'):])[0]
    graphs = set(envelope["nodes"]["render"]["items"][0]["labels"].values()) | {"cam", "laban"}
    return [key for key in fields if key in graphs]


def fired(text, envelope, mode, lbn):
    """{code: [messages]}: the codes that fire on this prompt, and those it cannot pass (a section they read is absent)."""
    out = {}
    for finding in prompt_validator.check(text, envelope, mode):
        out.setdefault(finding["code"], []).append(finding["message"])
    if lbn:
        for code in LBN_EXEMPT:
            out.pop(code, None)
        out.pop("PROSE_STALE", None)  # the prose check; LBN-2.4 is compared with its own projection
        if text != render_text(envelope):
            out["PROSE_STALE"] = ["render.txt differs from the envelope's LBN-2.4 projection"]
        stacked = _lbn_graphs(text, envelope)
        if stacked:
            out["STACKED_GRAPHS"] = [f"LBN-2.4 embeds the {', '.join(stacked)} graphs as JSON fields; the DAG stacks two "
                                     "(causal links, prop state)"]
    for code, missing in prompt_validator.unread(text, envelope, mode).items():
        more = f" (+{len(missing) - 2} more)" if len(missing) > 2 else ""
        out[code] = [f"cannot pass: the prompt has no {', '.join(missing[:2])}{more}"] + out.get(code, [])
    return out


def judge(row, found, mode, genre, lbn):
    """(result, evidence) for one checklist row on one prompt, given the codes `found` on it."""
    if "not_applicable" in row:
        return NA, row["not_applicable"]
    when = row.get("applies_when", {})
    if "mode" in when and when["mode"] != mode:
        return NA, f"menu (DAG §2.14, O14): the {when['mode']} mode's row; this prompt is {mode}"
    if "genre" in when and genre not in when["genre"]:
        return NA, f"O14: applies to {', '.join(when['genre'])}; this example is {genre}"
    codes = row.get("codes", [])
    failed = [code for code in codes if code in found]
    if failed:
        return FAIL, "; ".join(f"{code} ×{len(found[code])}: {_short(found[code][0])}" for code in failed)
    if "selection" in when:
        return OPEN, f"menu (O14): no {when['selection']} is selected for this example yet"
    passed = "pass: " + ", ".join(code + (f" ({LBN_EXEMPT[code]})" if lbn and code in LBN_EXEMPT else "")
                                  for code in codes)
    if codes and row["status"] in ("enforced", "excluded"):
        return PASS, passed
    if row["status"] == "enforced":
        graph = sorted({loc["code"] for loc in row.get("enforced_by", []) if "code" in loc})
        return OPEN, f"checked on the graph only ({', '.join(graph)} at {row['step']}); the prompt text is not checked"
    lead = passed + "; " if codes else ""
    if row.get("gaps"):
        return OPEN, lead + "not built: " + ", ".join(row["gaps"])
    return OPEN, lead + ("owner question open: " if row["status"] == "clashes_with_repo" else "not checked: ") + gist(
        row["note"])


def findings_for(name, row):
    """[(finding, caught)] for a row on an example: caught when one of the row's codes catches what the render saw."""
    codes = set(row.get("codes", []))
    return [(f, bool(codes & set(caught))) for f, (where, ids, caught) in sorted(FINDINGS.items(), key=lambda i: int(i[0][1:]))
            if name in where and row["id"] in ids]


def contested(cell, open_findings):
    """A PASS that a render contradicts, with no code checking what the render saw, is NOT CHECKED."""
    result, evidence = cell
    if result != PASS or not open_findings:
        return cell
    return OPEN, f"{evidence}, but render finding {', '.join(open_findings)} contradicts it and no code here checks what it saw"


def union(results):
    """The Any column (O13): PASS if one prompt passes, else NOT CHECKED if one is unchecked, else FAIL."""
    applicable = [r for r in results if r != NA]
    if not applicable:
        return NA
    return next(r for r in (PASS, OPEN, FAIL) if r in applicable)


def deliverable(results):
    return all(r in (PASS, NA) for r in results)


def evaluate(name):
    """{genre, columns: [{label, file, sha256, bytes, cells: [(result, evidence)]}], rows} for one example."""
    folder = EXAMPLES / name
    envelope = json.loads((folder / "envelope.json").read_text(encoding="utf-8"))
    genre, checklist = envelope["scene"]["genre"], rows()
    columns = []
    for label, file, mode in PROMPTS:
        data = (folder / file).read_bytes()
        lbn = file == "render.txt"
        found = fired(data.decode("utf-8"), envelope, mode, lbn)
        cells = [contested(judge(row, found, mode, genre, lbn), [f for f, caught in findings_for(name, row) if not caught])
                 for row in checklist]
        columns.append({"label": label, "file": file, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                        "cells": cells})
    return {"genre": genre, "columns": columns, "rows": checklist}


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def _evidence(columns, i):
    groups = {}
    for column in columns:
        groups.setdefault(column["cells"][i][1], []).append(column["label"])
    if len(groups) == 1:
        return next(iter(groups))
    return " — ".join(f"**{', '.join(labels)}:** {text}" for text, labels in groups.items())


def _counts(results):
    return [sum(r == kind for r in results) for kind in RESULTS]


def markdown(name, result=None):
    result = result or evaluate(name)
    columns, checklist = result["columns"], result["rows"]
    any_column = [union([c["cells"][i][0] for c in columns]) for i in range(len(checklist))]
    out = [f"# DAG checklist: {name}", "",
           "Generated by `python -m validators.checklist --write`; do not edit. Rows: the "
           f"{len(checklist)} checklist rows of [kernel/knowledge_map.yaml](../../kernel/knowledge_map.yaml) (the 25 "
           "evidence rows are never checked). Rules and the owner's rulings O13 and O14: "
           "[validators/checklist.py](../../validators/checklist.py). Findings: F-numbers in "
           f"[the 2026-10-11 findings]({'../../' + FINDINGS_DOC}), section 3; '(caught)' = a code of the row now fails "
           "what that render saw, otherwise the finding turns a PASS into NOT CHECKED.", "",
           f"Genre: {result['genre']}. LBN-2.4 is read against the DAG's Master Template (O13), so many of its FAIL "
           "cells are layout gaps: it keeps rules, negatives, props and shots in its own JSON fields. A prompt is a "
           "deliverable only with no FAIL and no NOT CHECKED row; Any is the union of the five (O13).", "",
           "| Prompt | File | sha256 | Bytes | PASS | FAIL | NOT CHECKED | N/A | Deliverable |",
           "|---|---|---|---|---|---|---|---|---|"]
    for column in columns:
        results = [r for r, _ in column["cells"]]
        counts = _counts(results)
        out.append(f"| {column['label']} | `{column['file']}` | `{column['sha256']}` | {column['bytes']} | "
                   + " | ".join(map(str, counts)) + f" | {'yes' if deliverable(results) else 'no'} |")
    counts = _counts(any_column)
    out += ["| Any | union of the five | | | " + " | ".join(map(str, counts))
            + f" | {'yes' if deliverable(any_column) else 'no'} |", "",
            "| Row | Name | Class | " + " | ".join(c["label"] for c in columns) + " | Any | Findings | Evidence |",
            "|---|---|---|" + "---|" * len(columns) + "---|---|---|"]
    for i, row in enumerate(checklist):
        seen = ", ".join(f + (" (caught)" if caught else "") for f, caught in findings_for(name, row))
        out.append(f"| {row['id']} | {_cell(row['name'])} | {row['class']} | "
                   + " | ".join(c["cells"][i][0] for c in columns)
                   + f" | {any_column[i]} | {seen} | {_cell(_evidence(columns, i))} |")
    return "\n".join(out) + "\n"


def names():
    return sorted(p.name for p in EXAMPLES.iterdir() if (p / "render.txt").exists())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    stale, refused, total = [], 0, 0
    for name in names():
        result = evaluate(name)
        text, path = markdown(name, result), EXAMPLES / name / "checklist.md"
        if "--write" in argv:
            path.write_text(text, encoding="utf-8")
        elif not path.exists() or path.read_text(encoding="utf-8") != text:
            stale.append(name)
        report = []
        for column in result["columns"]:
            results = [r for r, _ in column["cells"]]
            total += 1
            refused += not deliverable(results)
            report.append(f"{column['label']} {'/'.join(map(str, _counts(results)))}")
        print(f"{name}: " + " · ".join(report) + "  (PASS/FAIL/NOT CHECKED/N/A)")
    print(f"deliverable prompts: {total - refused} of {total}")
    if stale:
        print("stale checklist.md (run python -m validators.checklist --write): " + ", ".join(stale))
        return 1
    return 1 if "--gate" in argv and refused else 0


if __name__ == "__main__":
    sys.exit(main())
