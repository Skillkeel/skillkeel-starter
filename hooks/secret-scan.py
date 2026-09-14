import json, os, re, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = d.get("tool_input", {}) or {}
path = ti.get("file_path", "") or ""
content = ti.get("content") or ti.get("new_string") or ""
if not content and isinstance(ti.get("edits"), list):
    content = "\n".join(e.get("new_string", "") for e in ti["edits"])
if os.environ.get("SKILLKEEL_ALLOW_SECRETS"):
    sys.exit(0)
low = path.lower()
if low.endswith((".md", ".example", ".sample")) or "/.secrets/" in low or low.startswith(".secrets/"):
    sys.exit(0)
PATTERNS = [
    ("AWS access key", r"AKIA[0-9A-Z]{16}"),
    ("OpenAI-style key", r"sk-(?:live|test|proj)-[A-Za-z0-9_-]{16,}"),
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("GitHub token", r"gh[pousr]_[A-Za-z0-9]{30,}"),
    ("Slack token", r"xox[abpr]-[A-Za-z0-9-]{10,}"),
    ("private key", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----"),
    ("JWT", r"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}"),
    ("hardcoded secret", r"(?i)\b(?:api[_-]?key|secret|password|passwd|token)\b[\"']?\s*[:=]\s*[\"'][A-Za-z0-9_\-/+=!@#$%^&*.]{12,}[\"']"),
]
hits = []
for i, line in enumerate(content.splitlines(), 1):
    for name, pat in PATTERNS:
        if re.search(pat, line):
            hits.append(f"  line {i}: {name}: {line.strip()[:80]}")
            break
if hits:
    sys.stderr.write(f"skillkeel secret-scan: refusing to write what looks like a credential into {path or '<file>'}:\n" + "\n".join(hits[:3]) +
                     "\nMove it to an env var or a gitignored .env file. Override for this session: SKILLKEEL_ALLOW_SECRETS=1.\n")
    sys.exit(2)
sys.exit(0)
