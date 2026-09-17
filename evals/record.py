#!/usr/bin/env python3
"""Run record for one transcript case: the mechanical facts of a `claude -p` run, graded without a model.

evals/run.sh calls this after each case with the stream-json output. It writes
  evals/<case>/record-<date>.json   exit code, seconds, every tool call (name + input summary),
                                    tool counts, skill invocations, last message, and the verdict
                                    of each grader in evals/<case>/graders/ that can be judged from
                                    the record (tool_used, regex on last_message, file_exists).
  evals/<case>/transcript-<date>.raw.md   the assistant text, as the text runner wrote it before.
llm_judge graders are listed as "unjudged"; they need a model run and are not what this step is for.

Usage: python3 evals/record.py <case> <stream.jsonl> <exit_code> <seconds> <workdir> [date]
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(os.environ.get("SKILLKEEL_EVAL_ROOT") or Path(__file__).resolve().parent.parent)


HOME = str(Path.home())
PLUGIN = str(Path(__file__).resolve().parent.parent)


def scrub(s):
    """No machine paths in a shipped record: the plugin checkout and the home directory become placeholders."""
    return s.replace(PLUGIN, "<plugin>").replace(HOME, "~")


def parse_stream(path):
    tools, texts, result = [], [], {}
    for line in Path(path).read_text().splitlines():
        line = scrub(line.strip())
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        t = ev.get("type")
        if t == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools.append({"name": c.get("name", ""), "input": json.dumps(c.get("input", {}), sort_keys=True)})
                elif c.get("type") == "text" and c.get("text"):
                    texts.append(c["text"])
        elif t == "result":
            result = ev
    return tools, texts, result


def front_matter(md):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", md, re.S)
    if not m:
        return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v[:1] in "'\"" and v[-1:] == v[:1]:
                v = v[1:-1]
            meta[k.strip()] = v
    return meta, m.group(2)


def grade(g, tools, last_message, workdir):
    """(passed | None, detail) for one grader front matter."""
    typ = g.get("type")
    if typ == "tool_used":
        pat = re.compile(g["input_match"]) if g.get("input_match") else None
        hits = [t for t in tools if t["name"] == g.get("tool") and (pat is None or pat.search(t["input"]))]
        n, lo, hi = len(hits), int(g.get("min", 1)), g.get("max")
        ok = n >= lo and (hi is None or n <= int(hi))
        return ok, f"{g.get('tool')} calls matching: {n} (min {lo}" + (f", max {hi}" if hi is not None else "") + ")"
    if typ == "regex" and g.get("target", "last_message") == "last_message":
        flags = re.I if "i" in g.get("flags", "") else 0
        found = re.search(g["pattern"], last_message, flags) is not None
        ok = found if g.get("match", "contains") == "contains" else not found
        return ok, f"pattern {g['pattern']!r} {'found' if found else 'not found'} in last message ({g.get('match', 'contains')})"
    if typ == "file_exists":
        exists = bool(list(Path(workdir).glob(g["path"])))  # plain path or glob, as the native grader takes it
        want = str(g.get("exists", "true")).lower() != "false"
        return exists == want, f"{g['path']} {'exists' if exists else 'missing'} (want {'present' if want else 'absent'})"
    return None, f"{typ}: needs a model run"


def main():
    case, stream, exit_code, seconds, workdir = sys.argv[1:6]
    date = sys.argv[6] if len(sys.argv) > 6 else __import__("datetime").date.today().isoformat()
    tools, texts, result = parse_stream(stream)
    last = result.get("result") or (texts[-1] if texts else "")
    counts = {}
    for t in tools:
        counts[t["name"]] = counts.get(t["name"], 0) + 1
    skills = [t["input"] for t in tools if t["name"] == "Skill"]
    graders = []
    gdir = ROOT / "evals" / case / "graders"
    for gf in sorted(gdir.glob("*.md")) if gdir.exists() else []:
        meta, _ = front_matter(gf.read_text())
        passed, detail = grade(meta, tools, last, workdir)
        graders.append({"name": gf.stem, "type": meta.get("type"), "tool": meta.get("tool"), "weight": int(meta.get("weight", 1)), "passed": passed, "detail": detail})
    exit_code = int(exit_code)
    rec = {
        "case": case, "date": date, "workdir": scrub(workdir),
        "claude_version": result.get("version") or "",
        "exit": exit_code, "seconds": float(seconds), "turns": result.get("num_turns"),
        "result_subtype": result.get("subtype"), "is_error": bool(result.get("is_error")),
        "tool_counts": counts, "tools": [{"name": t["name"], "input": t["input"][:200]} for t in tools],
        "skills": skills, "last_message": last,
        "graders": graders,
        "passed": exit_code == 0 and not result.get("is_error") and all(g["passed"] is not False for g in graders),
    }
    out = ROOT / "evals" / case
    (out / f"record-{date}.json").write_text(json.dumps(rec, indent=1) + "\n")
    (out / f"transcript-{date}.raw.md").write_text("\n\n".join(texts) + ("\n" if texts else ""))
    verdicts = " ".join(f"{g['name']}={'PASS' if g['passed'] else 'FAIL' if g['passed'] is False else '?'}" for g in graders)
    print(f"   exit={exit_code} turns={rec['turns']} tools={sum(counts.values())} {verdicts} -> {'PASS' if rec['passed'] else 'FAIL'}")


if __name__ == "__main__":
    main()
