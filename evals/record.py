#!/usr/bin/env python3
"""Run record for one transcript case: the mechanical facts of a `claude -p` run, graded without a model.

evals/run.sh calls this after each case with the stream-json output. It writes
  evals/<case>/record-<date>.json   exit code, seconds, every tool call (name + input summary),
                                    tool counts, skill invocations, last message, and the verdict
                                    of each grader in evals/<case>/graders/ that can be judged from
                                    the record (tool_used, regex on last_message, file_exists),
                                    and the plugins the init line says were loaded: anything besides
                                    the plugin under test means the run was not isolated, and fails.
  evals/<case>/transcript-<date>.raw.md   the assistant text, as the text runner wrote it before.
llm_judge graders are listed as "unjudged"; they need a model run and are not what this step is for.

Usage: python3 evals/record.py <case> <stream.jsonl> <exit_code> <seconds> <workdir> [date]
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(os.environ.get("SKILLKEEL_EVAL_ROOT") or Path(__file__).resolve().parent.parent)


HOME = str(Path.home())
PLUGIN = str(Path(__file__).resolve().parent.parent)
PLUGIN_NAME = "skillkeel-starter"
WORKDIR = [""]


def git_identity():
    """The maintainer's global git name and email, so a run that picked them up is scrubbed generically."""
    import subprocess
    out = []
    for k in ("user.name", "user.email"):
        v = subprocess.run(["git", "config", "--global", k], capture_output=True, text=True).stdout.strip()
        if len(v) > 3:
            out.append(v)
    return out


IDENTITY = git_identity()


def scrub(s):
    """No machine paths or personal identity in a shipped record: the plugin checkout, the case workdir, the home
    directory (also in its dashed form, as temp dirs encode it) and the maintainer's git identity become placeholders."""
    if WORKDIR[0]:
        s = s.replace(WORKDIR[0], "<workdir>")
    s = s.replace(PLUGIN, "<plugin>").replace(HOME, "~").replace(HOME.strip("/").replace("/", "-"), "~")
    for v in IDENTITY:
        s = s.replace(v, "<git user>")
    return s


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
        if t == "system" and ev.get("subtype") == "init":
            result["version"] = ev.get("claude_code_version") or ev.get("version") or ""
            result["plugins"] = [p.get("name", "") for p in ev.get("plugins", []) if isinstance(p, dict)]
        elif t == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools.append({"name": c.get("name", ""), "input": json.dumps(c.get("input", {}), sort_keys=True)})
                elif c.get("type") == "text" and c.get("text"):
                    texts.append(c["text"])
        elif t == "result":
            result = {**result, **ev}
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


def regex_target(g, tools, texts, last_message, workdir):
    """Text a regex grader runs against: last_message, trace (every tool input and assistant text),
    a file in the workdir ({source: file, path: X}), or None when the target is not judged here."""
    t = g.get("target", "last_message")
    if t == "last_message":
        return last_message
    if t == "trace":
        return "\n".join([x["input"] for x in tools] + texts)
    m = re.match(r"\{\s*source:\s*file\s*,\s*path:\s*([^}]+?)\s*\}", t)
    if m:
        p = Path(workdir) / m.group(1).strip("'\"")
        return p.read_text(errors="replace") if p.exists() else ""
    return None


def grade(g, tools, last_message, workdir, texts=()):
    """(passed | None, detail) for one grader front matter."""
    typ = g.get("type")
    if typ == "tool_used":
        pat = re.compile(g["input_match"]) if g.get("input_match") else None
        hits = [t for t in tools if t["name"] == g.get("tool") and (pat is None or pat.search(t["input"]))]
        n, lo, hi = len(hits), int(g.get("min", 1)), g.get("max")
        ok = n >= lo and (hi is None or n <= int(hi))
        return ok, f"{g.get('tool')} calls matching: {n} (min {lo}" + (f", max {hi}" if hi is not None else "") + ")"
    if typ == "regex":
        text = regex_target(g, tools, list(texts), last_message, workdir)
        if text is None:
            return None, f"regex target {g.get('target')!r}: not judged here"
        flags = re.I if "i" in g.get("flags", "") else 0
        found = re.search(g["pattern"], text, flags) is not None
        ok = found if g.get("match", "contains") == "contains" else not found
        return ok, f"pattern {g['pattern']!r} {'found' if found else 'not found'} in {g.get('target', 'last_message')} ({g.get('match', 'contains')})"
    if typ == "file_exists":
        exists = bool(list(Path(workdir).glob(g["path"])))  # plain path or glob, as the native grader takes it
        want = str(g.get("exists", "true")).lower() != "false"
        return exists == want, f"{g['path']} {'exists' if exists else 'missing'} (want {'present' if want else 'absent'})"
    return None, f"{typ}: needs a model run"


def main():
    case, stream, exit_code, seconds, workdir = sys.argv[1:6]
    WORKDIR[0] = str(Path(workdir).resolve())
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
        passed, detail = grade(meta, tools, last, workdir, texts)
        graders.append({"name": gf.stem, "type": meta.get("type"), "tool": meta.get("tool"), "weight": int(meta.get("weight", 1)), "passed": passed, "detail": detail})
    exit_code = int(exit_code)
    plugins = result.get("plugins") or []
    extra = [p for p in plugins if p != PLUGIN_NAME]
    rec = {
        "case": case, "date": date, "workdir": scrub(workdir),
        "claude_version": result.get("version") or "",
        "exit": exit_code, "seconds": float(seconds), "turns": result.get("num_turns"),
        "result_subtype": result.get("subtype"), "is_error": bool(result.get("is_error")),
        "tool_counts": counts, "tools": [{"name": t["name"], "input": t["input"][:200]} for t in tools],
        "skills": skills, "last_message": last,
        "plugins": plugins, "extra_plugins": extra,
        "graders": graders,
        "passed": exit_code == 0 and not result.get("is_error") and not extra and all(g["passed"] is not False for g in graders),
    }
    out = ROOT / "evals" / case
    (out / f"record-{date}.json").write_text(json.dumps(rec, indent=1) + "\n")
    (out / f"transcript-{date}.raw.md").write_text("\n\n".join(texts) + ("\n" if texts else ""))
    verdicts = " ".join(f"{g['name']}={'PASS' if g['passed'] else 'FAIL' if g['passed'] is False else '?'}" for g in graders)
    leak = f" extra plugins={','.join(extra)}" if extra else ""
    print(f"   exit={exit_code} turns={rec['turns']} tools={sum(counts.values())} {verdicts}{leak} -> {'PASS' if rec['passed'] else 'FAIL'}")


if __name__ == "__main__":
    main()
