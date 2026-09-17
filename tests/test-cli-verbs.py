#!/usr/bin/env python3
"""CLI verb gate: every `gitleaks|trufflehog|pip-audit|gh ...` command in the skill and agent texts
must use a subcommand and flags that the snapshot in tests/cli-verbs.json knows.

The snapshot is read from the latest release of each CLI (its own --help output), so a renamed or
removed subcommand fails this test on the commit that touches the skill, or on the snapshot refresh,
instead of surfacing in an eval transcript or a user report.

Run: python3 tests/test-cli-verbs.py           exit 1 on any finding
     python3 tests/test-cli-verbs.py --list    also print every command the gate checked
     python3 tests/test-cli-verbs.py --self    run the gate's own cases (the 0.1.1 gitleaks text must fail)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = json.loads((ROOT / "tests" / "cli-verbs.json").read_text())["clis"]
FILES = sorted(list(ROOT.glob("skills/*/SKILL.md")) + list(ROOT.glob("agents/*.md")))
CLI = re.compile(r"(?<![\w./-])(" + "|".join(re.escape(c) for c in SNAP) + r")(?=\s|$)")
# A command is text inside a code span or fenced block; quoted strings and $(...) are dropped first,
# then the text is split at shell separators so `a && gh pr list` yields `gh pr list`.
STRIP = [re.compile(r'"(?:[^"\\]|\\.)*"'), re.compile(r"'[^']*'"), re.compile(r"\$\([^)]*\)"), re.compile(r"<[^>]*>")]
SEP = re.compile(r"\s*(?:&&|\|\||[;|]|\n)\s*")
# A fallback for an old CLI version is allowed when the line says so.
OLD = re.compile(r"\bolder\b|\bdeprecated\b|\bbefore\b|\blegacy\b", re.I)


def snippets(text):
    """(line_no, code) for every code span and fenced block."""
    out, fence, buf, start = [], False, [], 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            if fence:
                out.append((start, "\n".join(buf))); buf = []
            fence, start = not fence, i
            continue
        if fence:
            buf.append(line)
        else:
            out += [(i, m.group(1)) for m in re.finditer(r"`([^`]+)`", line)]
    return out


def commands(code):
    for s in STRIP:
        code = s.sub(" ", code)
    for part in SEP.split(code):
        tokens = part.split()
        if len(tokens) > 1 and CLI.fullmatch(tokens[0]):  # a bare name in prose is not a command
            yield tokens


def check(tokens, line_text):
    cli, rest = tokens[0], tokens[1:]
    spec = SNAP[cli]
    verbs, hidden = spec["verbs"], spec["hidden"]
    words = [t for t in rest if not t.startswith("-")]
    verb = ""
    if verbs:
        if not words:
            return f"{cli}: no subcommand (snapshot {spec['version']})"
        two = " ".join(words[:2])
        if two in verbs:
            verb = two
        elif words[0] in verbs:
            verb = words[0]
        elif words[0] in hidden:
            if not OLD.search(line_text):
                return f"{cli} {words[0]}: not listed by {cli} {spec['version']} (still runs); only allowed as a documented fallback for older versions"
            verb = words[0]
        else:
            return f"{cli} {words[0]}: not a subcommand of {cli} {spec['version']}"
    known = set(spec["flags"].get("", [])) | set(spec["flags"].get(verb, []))
    if verb and verb not in spec["flags"]:
        return None  # verb exists, flags for it not in the snapshot: verb-only check
    for t in rest:
        if t.startswith("-") and t != "-":
            flag = t.split("=")[0]
            if flag not in known:
                return f"{cli} {verb}: flag {flag} unknown to {cli} {spec['version']}"
    return None


SELF = [  # (code, line text, expect a finding)
    ("gitleaks detect --source .", "1. Tooling: prefer `gitleaks detect --source .`", True),  # Starter 0.1.1 text
    ("gitleaks detect --source .", "on an older gitleaks use `gitleaks detect --source .`", False),
    ("gitleaks git --report-format json .", "", False),
    ("gitleaks scan .", "", True),
    ("gitleaks git --sources .", "", True),
    ("trufflehog git file://. --json", "", False),
    ("trufflehog filesystem . --jsonl", "", True),
    ("pip-audit -f json", "", False),
    ("pip-audit --json", "", True),
    ("gh pr create --title x --body y", "", False),
    ("gh pr open --title x", "", True),
    ("gh issue list --label bug --state open", "", False),
    ("gh release create v1 --notes-file n.md", "", False),
    ("gh release create v1 --notes-path n.md", "", True),
    ("command -v gitleaks", "", None),  # not a command of the gated CLI
    ("git log | gh pr list --json title", "", False),
]


def selftest():
    bad = 0
    for code, line, expect in SELF:
        found = [check(t, line) for t in commands(code)]
        got = None if not found else bool(found[0])
        if got != expect:
            bad += 1
            print(f"SELF FAIL: {code!r} -> {found} (expected finding={expect})")
    print(f"cli-verbs self-test: {len(SELF) - bad}/{len(SELF)} cases")
    sys.exit(1 if bad else 0)


def main():
    if "--self" in sys.argv:
        selftest()
    listing = "--list" in sys.argv
    findings, checked = [], 0
    for f in FILES:
        text = f.read_text()
        lines = text.splitlines()
        for line_no, code in snippets(text):
            for tokens in commands(code):
                checked += 1
                rel = f.relative_to(ROOT)
                if listing:
                    print(f"  {rel}:{line_no}: {' '.join(tokens)}")
                err = check(tokens, lines[line_no - 1] if line_no - 1 < len(lines) else "")
                if err:
                    findings.append(f"{rel}:{line_no}: {err}")
    for x in findings:
        print("FAIL " + x)
    vers = ", ".join(f"{c} {SNAP[c]['version']}" for c in SNAP)
    print(f"cli-verbs: {checked} commands checked in {len(FILES)} files against {vers} (snapshot {json.loads((ROOT / 'tests' / 'cli-verbs.json').read_text())['updated']}); {len(findings)} findings")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
