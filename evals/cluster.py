#!/usr/bin/env python3
"""Group failed eval cases by their first mechanical mismatch, before anyone reads a transcript.

Reads the latest run record per case (evals/<case>/record-<date>.json, written by evals/record.py) and the
latest native result per case (evals/results/<stamp>/aggregate-result.json from `claude plugin eval`),
then buckets every failed case by the first thing that went wrong in this order:

  runner       the run itself failed: non-zero exit, timeout, max turns, error
  skill        the skill was never invoked (a tool_used grader on the Skill tool)
  tool         another tool call count was off (tool_used)
  file         an expected file is missing or present (file_exists)
  text         the final answer failed a regex
  judge        only a model-judged grader failed

A bucket with several cases and one grader name is usually one bug in the grader or the runner, not in
the skill; a case that fails at "runner" has nothing to read yet. Idea from u/EvalRaccoonDev's 228-failure
audit (r/ClaudeCode, 2026-09-16).

Usage: python3 evals/cluster.py [--date YYYY-MM-DD] [--json]
       python3 evals/cluster.py --show <case>      # the latest run record of one case: tools, graders, verdict
"""
import json, os, sys
from pathlib import Path

ROOT = Path(os.environ.get("SKILLKEEL_EVAL_ROOT") or Path(__file__).resolve().parent.parent)
ORDER = ["runner", "skill", "tool", "file", "text", "judge"]
TYPE_BUCKET = {"tool_used": "tool", "file_exists": "file", "regex": "text"}


def bucket_of(grader):
    t = grader.get("type")
    if t == "tool_used" and grader.get("tool") == "Skill":
        return "skill"
    return TYPE_BUCKET.get(t, "judge")


def from_records(date):
    out = {}
    for f in ROOT.glob("evals/*/record-*.json"):
        r = json.loads(f.read_text())
        if date and r["date"] != date:
            continue
        if r["case"] not in out or r["date"] > out[r["case"]]["date"]:
            out[r["case"]] = r
    return out


def native_cases(date):
    """Latest native result per case: (case, run dict, grader configs)."""
    out = {}
    for f in sorted(ROOT.glob("evals/results/*/aggregate-result.json")):
        d = json.loads(f.read_text())
        stamp = d.get("startedAt", "")[:10]
        if date and stamp != date:
            continue
        for c in d.get("cases", []):
            for run in c.get("arms", {}).get("with", []):
                out[c["name"]] = (stamp, run, {g["name"]: g for g in c.get("graders", [])})
    return out


def first_mismatch_record(r):
    if r["exit"] != 0 or r.get("is_error") or (r.get("result_subtype") not in (None, "success")):
        return "runner", f"exit {r['exit']}" + (f", {r['result_subtype']}" if r.get("result_subtype") else "")
    failed = [g for g in r["graders"] if g["passed"] is False]
    if not failed:
        return None, None
    g = sorted(failed, key=lambda g: ORDER.index(bucket_of(g)))[0]
    return bucket_of(g), f"{g['name']}: {g['detail']}"


def first_mismatch_native(run, cfg):
    if run.get("error"):
        return "runner", str(run["error"])[:120]
    failed = [g for g in run.get("graders", []) if g.get("passed") is False]
    if not failed:
        return None, None
    def bucket(g):
        c = cfg.get(g["name"], {})
        return bucket_of({"type": c.get("type"), "tool": c.get("config", {}).get("tool")})
    g = sorted(failed, key=lambda g: ORDER.index(bucket(g)))[0]
    return bucket(g), f"{g['name']}: {(g.get('explanation') or '')[:120]}"


def show(case):
    recs = sorted(ROOT.glob(f"evals/{case}/record-*.json"))
    if not recs:
        print(f"no run record for {case}"); return
    r = json.loads(recs[-1].read_text())
    print(f"{case} on Claude Code {r['claude_version']} ({r['date']}): exit {r['exit']}, {r['turns']} turns, {r['seconds']:.0f} s, tools {r['tool_counts']}")
    for g in r["graders"]:
        print(f"  {('PASS' if g['passed'] else 'FAIL' if g['passed'] is False else '?'):<4} {g['name']:<18} {g['detail'][:70]}")
    print("  ->", "PASS" if r["passed"] else "FAIL")


def main():
    if "--show" in sys.argv:
        show(sys.argv[sys.argv.index("--show") + 1]); return
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else None
    rows, total = [], 0
    for case, r in from_records(date).items():
        total += 1
        b, why = first_mismatch_record(r)
        if b:
            rows.append((b, case, f"record {r['date']}", why))
    for case, (stamp, run, cfg) in native_cases(date).items():
        total += 1
        b, why = first_mismatch_native(run, cfg)
        if b:
            rows.append((b, case, f"native {stamp}", why))
    if "--json" in sys.argv:
        print(json.dumps([{"bucket": b, "case": c, "source": s, "why": w} for b, c, s, w in rows], indent=1))
        return
    print(f"== {len(rows)} failed of {total} cases" + (f" on {date}" if date else "") + ", grouped by first mechanical mismatch")
    for b in ORDER:
        group = [x for x in rows if x[0] == b]
        if not group:
            continue
        names = {x[3].split(":")[0] for x in group}
        hint = "  <- one grader across cases, check the grader first" if len(group) > 1 and len(names) == 1 else ""
        print(f"\n{b} ({len(group)}){hint}")
        for _, case, src, why in group:
            print(f"  {case:<20} {src:<20} {why}")
    if not rows:
        print("nothing to read.")


if __name__ == "__main__":
    main()
