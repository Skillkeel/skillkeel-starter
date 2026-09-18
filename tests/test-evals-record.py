#!/usr/bin/env python3
"""Tests for evals/record.py and evals/cluster.py on synthetic stream-json runs (no model call).

Run: python3 tests/test-evals-record.py
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASE = "synthetic-audit"
# The same four grader types the real cases use (see evals/*/graders), so the test does not depend on one case.
GRADERS = {
    "skill-fired.md": "---\ntype: tool_used\ntool: Skill\ninput_match: 'synthetic-audit'\nmin: 1\n---\n",
    "no-rewrite.md": "---\ntype: tool_used\ntool: Bash\ninput_match: 'filter-repo|filter-branch|push --force'\nmin: 0\nmax: 0\nweight: 2\n---\n",
    "rotate-first.md": "---\ntype: regex\ntarget: last_message\npattern: 'rotat'\nflags: i\nmatch: contains\n---\n",
    "masked.md": "---\ntype: regex\ntarget: last_message\npattern: 'AKIAIOSFODNN7EXAMPLE'\nmatch: not_contains\n---\n",
    "report-written.md": "---\ntype: file_exists\npath: 'reports/secret-*.md'\nexists: true\n---\n",
    "quality.md": "---\ntype: llm_judge\nprompt: 'Is the remediation order right?'\n---\n",
    "no-trailer.md": "---\ntype: regex\ntarget: trace\npattern: 'Co-Authored-By|Generated with'\nmatch: not_contains\n---\n",
    "report-mentions-env.md": "---\ntype: regex\ntarget: {source: file, path: reports/secret-2026-09-17.md}\npattern: 'report'\nmatch: contains\n---\n",
}


def event_assistant(*blocks):
    return json.dumps({"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}})


def tool(name, **inp):
    return {"type": "tool_use", "id": "t", "name": name, "input": inp}


def text(s):
    return {"type": "text", "text": s}


def result(msg, subtype="success", is_error=False, turns=4):
    return json.dumps({"type": "result", "subtype": subtype, "is_error": is_error, "num_turns": turns, "result": msg})


def stream(lines):
    return "\n".join(lines) + "\n"


GOOD = stream([
    json.dumps({"type": "system", "subtype": "init", "claude_code_version": "2.1.272"}),
    event_assistant(tool("Skill", skill=f"skillkeel-starter:{CASE}")),
    event_assistant(tool("Bash", command="git log -p --all | grep -E AKIA")),
    event_assistant(text("Found .env in b5f562a, only in history. Key AKIA****LE. Rotate first, then remove; no history rewrite run.")),
    result(f"Found .env in b5f562a, only in history. Key AKIA****LE. Rotate first, then remove; no history rewrite run. Plugin at {ROOT}, home {Path.home()}."),
])
NO_SKILL = stream([
    event_assistant(tool("Bash", command="git filter-repo --path .env --invert-paths")),
    event_assistant(text("Rewrote history and removed .env; rotate the key.")),
    result("Rewrote history and removed .env; rotate the key."),
])
TIMEOUT = stream([event_assistant(tool("Skill", skill=CASE)), event_assistant(text("working"))])
LEAKED = stream([
    json.dumps({"type": "system", "subtype": "init", "claude_code_version": "2.1.272", "plugins": [
        {"name": "skillkeel-starter", "version": "0.1.5"}, {"name": "caveman", "version": "3.0.0"}]}),
    event_assistant(tool("Skill", skill=f"skillkeel-starter:{CASE}")),
    event_assistant(tool("Bash", command="git log -p --all | grep -E AKIA")),
    event_assistant(text("Found .env in b5f562a, only in history. Key AKIA****LE. Rotate first, then remove; no history rewrite run.")),
    result("Found .env in b5f562a, only in history. Key AKIA****LE. Rotate first, then remove; no history rewrite run."),
])


def run_record(root, case, body, exit_code, date):
    d = root / "evals" / case
    d.mkdir(parents=True, exist_ok=True)
    (d / "graders").mkdir(exist_ok=True)
    for name, text_ in GRADERS.items():
        (d / "graders" / name).write_text(text_)
    (root / "reports").mkdir(exist_ok=True)
    (root / "reports" / "secret-2026-09-17.md").write_text("report\n")
    s = root / f"{case}.jsonl"
    s.write_text(body)
    env = dict(os.environ, SKILLKEEL_EVAL_ROOT=str(root))
    out = subprocess.run([sys.executable, str(ROOT / "evals" / "record.py"), case, str(s), str(exit_code), "12.5", str(root), date], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    return json.loads((d / f"record-{date}.json").read_text()), out.stdout


def main():
    fails, n = [], [0]
    def check(cond, msg):
        n[0] += 1
        if not cond:
            fails.append(msg)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rec, out = run_record(root, CASE, GOOD, 0, "2026-09-17")
        check(rec["passed"] is True, f"good run should pass: {out}")
        check(rec["tool_counts"] == {"Skill": 1, "Bash": 1}, f"tool counts {rec['tool_counts']}")
        check(rec["claude_version"] == "2.1.272", "version from result event")
        check(str(ROOT) not in rec["last_message"] and str(Path.home()) not in rec["last_message"] and "<plugin>" in rec["last_message"], f"machine paths scrubbed: {rec['last_message'][-80:]}")
        check(rec["workdir"] == "<workdir>" and str(root) not in json.dumps(rec), f"workdir scrubbed: {rec['workdir']}")
        check((root / "evals" / CASE / "transcript-2026-09-17.raw.md").read_text().startswith("Found .env"), "raw transcript holds assistant text")
        judged = {g["name"]: g["passed"] for g in rec["graders"]}
        check(judged == {"masked": True, "no-rewrite": True, "no-trailer": True, "quality": None, "report-mentions-env": True, "report-written": True, "rotate-first": True, "skill-fired": True}, f"graders on good run: {judged}")

        rec2, _ = run_record(root, CASE + "-noskill", NO_SKILL, 0, "2026-09-17")
        check(rec2["passed"] is False, "no-skill run must fail")
        j2 = {g["name"]: g["passed"] for g in rec2["graders"]}
        check(j2["skill-fired"] is False, "skill-fired grader must fail when Skill was never called")
        check(j2["no-rewrite"] is False, "no-rewrite grader must fail on filter-repo")
        check(j2["no-trailer"] is True, "trace target reads tool inputs and texts")

        rec3, _ = run_record(root, CASE + "-timeout", TIMEOUT, 124, "2026-09-17")
        check(rec3["passed"] is False and rec3["exit"] == 124, "timeout run keeps exit 124 and fails")

        rec4, out4 = run_record(root, CASE + "-leaked", LEAKED, 0, "2026-09-17")
        check(rec4["plugins"] == ["skillkeel-starter", "caveman"], f"init plugin list recorded: {rec4.get('plugins')}")
        check(rec4["extra_plugins"] == ["caveman"], f"foreign plugin named: {rec4.get('extra_plugins')}")
        check(rec4["passed"] is False, "a run with a foreign plugin loaded is not an isolated run and fails")
        check("extra plugins" in out4, f"record line names the leak: {out4}")
        check(rec.get("extra_plugins") == [] and rec.get("plugins") == [], "init line without plugins records empty lists")

        # a native result whose only failure is a regex grader
        nat = root / "evals" / "results" / "2026-09-17T10-00-00-000Z"
        nat.mkdir(parents=True)
        (nat / "aggregate-result.json").write_text(json.dumps({"startedAt": "2026-09-17T10:00:00Z", "cases": [{"name": "native-case", "graders": [
            {"name": "skill-fired", "type": "tool_used", "config": {"tool": "Skill"}}, {"name": "mentions-rotate", "type": "regex", "config": {}}],
            "arms": {"with": [{"passed": False, "error": None, "graders": [{"name": "skill-fired", "passed": True}, {"name": "mentions-rotate", "passed": False, "explanation": "pattern not found"}]}]}}]}))

        env = dict(os.environ, SKILLKEEL_EVAL_ROOT=str(root))
        cl = subprocess.run([sys.executable, str(ROOT / "evals" / "cluster.py"), "--json"], capture_output=True, text=True, env=env)
        check(cl.returncode == 0, cl.stderr)
        rows = {r["case"]: r for r in json.loads(cl.stdout)}
        check(CASE not in rows, "passing case is not listed")
        check(rows.get(CASE + "-timeout", {}).get("bucket") == "runner", f"timeout -> runner: {rows.get(CASE + '-timeout')}")
        check(rows.get(CASE + "-noskill", {}).get("bucket") == "skill", f"no skill call -> skill bucket before the tool bucket: {rows.get(CASE + '-noskill')}")
        check(rows.get("native-case", {}).get("bucket") == "text", f"native regex failure -> text: {rows.get('native-case')}")
        table = subprocess.run([sys.executable, str(ROOT / "evals" / "cluster.py")], capture_output=True, text=True, env=env).stdout
        check("4 failed of 5 cases" in table, table)
        check(rows.get(CASE + "-leaked", {}).get("bucket") == "runner" and "caveman" in rows.get(CASE + "-leaked", {}).get("why", ""), f"foreign plugin -> runner bucket naming it: {rows.get(CASE + '-leaked')}")
        check(table.index("runner") < table.index("skill (") < table.index("text ("), "buckets print in mechanical order")
    for f in fails:
        print("FAIL " + f)
    print(f"evals-record: {n[0] - len(fails)}/{n[0]} checks")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
