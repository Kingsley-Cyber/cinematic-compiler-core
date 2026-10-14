"""The test budget (ADR-O119, R-37, R-38): at most 20 tests and 200 lines per test file, at most 100 ms per test, and
every check code the compiler raises named by a test. What was over it on 2026-10-13 is in tests/budget_baseline.json,
which may only shrink: a file or test over budget and not listed fails, a listed one that grew fails, and a listed one
back within budget fails until it is removed (so the list cannot go stale; a slow test once it takes under half the
budget, so timing noise at the line does not flap).

    python scripts/test_budget.py              # check (reads .test_durations.json, written by the last full pytest run)
    python scripts/test_budget.py --baseline   # rewrite the baseline (only to shrink it; the diff shows what left)
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests" / "budget_baseline.json"
DURATIONS = ROOT / ".test_durations.json"
MAX_TESTS, MAX_LINES, MAX_SECONDS = 20, 200, 0.1
CODE = re.compile(r'''(?:"code":\s*|_finding\(\s*|add\(\s*|ContractError\(\s*|StepFailed\(\s*)"([A-Z][A-Z0-9_]{3,})"''')


def measure():
    out = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-n", "0"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    tests = Counter(line.split("::")[0] for line in out.splitlines() if "::" in line)
    files = {f"tests/{p.name}": {"tests": tests.get(f"tests/{p.name}", 0), "lines": len(p.read_text().splitlines())}
             for p in sorted((ROOT / "tests").glob("test_*.py"))}
    durations = json.loads(DURATIONS.read_text(encoding="utf-8")) if DURATIONS.exists() else {}
    source = [p for d in ("compiler", "validators", "solver", "planner") for p in (ROOT / d).rglob("*.py")]
    codes = {m.group(1) for p in source for m in CODE.finditer(p.read_text(encoding="utf-8"))}
    named = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").glob("*.py"))
    return {"files": {f: v for f, v in files.items() if v["tests"] > MAX_TESTS or v["lines"] > MAX_LINES},
            "slow": sorted(t for t, s in durations.items() if s > MAX_SECONDS),
            "untested_codes": sorted(c for c in codes if c not in named)}, durations


def alone(tests):
    """The tests still over budget when timed by themselves (one worker): six workers' load is not a test's cost."""
    tests = sorted(tests)
    if not tests:
        return []
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-n", "0", "-p", "no:cacheprovider", "--durations=0",
                          "--durations-min=0", *tests], cwd=ROOT, capture_output=True, text=True).stdout
    timed = {m.group(2): float(m.group(1)) for m in re.finditer(r"([0-9.]+)s call\s+(\S+)", out)}
    return [t for t in tests if timed.get(t, MAX_SECONDS + 1) > MAX_SECONDS]


def problems(now, held, durations):
    out = []
    for f, v in now["files"].items():
        base = held["files"].get(f)
        if base is None:
            out.append(f"{f}: {v['tests']} tests, {v['lines']} lines (budget {MAX_TESTS} and {MAX_LINES})")
        elif v["tests"] > base["tests"] or v["lines"] > base["lines"]:
            out.append(f"{f} grew past its baseline: {v} > {base}")
    out += [f"{f} is back within budget: remove it from the baseline" for f in held["files"] if f not in now["files"]]
    out += [f"{t} takes over {MAX_SECONDS * 1000:g} ms on its own" for t in alone(t for t in now["slow"]
                                                                                if t not in held["slow"])]
    out += [f"{t} now takes under {MAX_SECONDS * 500:g} ms: remove it from the baseline" for t in held["slow"]
            if durations.get(t, MAX_SECONDS) < MAX_SECONDS / 2]  # half the budget: no flapping at the line
    out += [f"check code {c} is named by no test" for c in now["untested_codes"] if c not in held["untested_codes"]]
    out += [f"check code {c} is now tested: remove it from the baseline" for c in held["untested_codes"]
            if c not in now["untested_codes"]]
    return out


def main():
    now, durations = measure()
    if "--baseline" in sys.argv:
        BASELINE.write_text(json.dumps(now, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {BASELINE.relative_to(ROOT)}: {len(now['files'])} files, {len(now['slow'])} slow tests, "
              f"{len(now['untested_codes'])} untested codes")
        return 0
    if not durations:
        print("test budget: no .test_durations.json (run the full pytest first)")
        return 1
    found = problems(now, json.loads(BASELINE.read_text(encoding="utf-8")), durations)
    for line in found:
        print("TEST BUDGET", line)
    print(f"test budget: {'PASS' if not found else f'{len(found)} problem(s)'}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
