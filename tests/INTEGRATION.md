# Integration runs (real Claude Code, `claude -p --plugin-dir . --permission-mode bypassPermissions`)

## 2026-09-13 — Claude Code 2.1.270
- guard-bash: `git reset --hard HEAD` → blocked, hook message surfaced verbatim to the model; `echo ok` → ran. PASS.
- secret-scan: Write `config.py` with `API_KEY = "sk-proj-…"` → file not created (blocked). PASS.
- session-start: brief injected (git branch/uncommitted/last commit + skill index). PASS.
