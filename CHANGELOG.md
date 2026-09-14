# Changelog

## 0.1.0 — 2026-09-13
- Hooks: `guard-bash` (blocks destructive shell commands), `secret-scan` (blocks credentials in file writes), `session-start` (short project brief).
- Skills: `commit-message`, `pr-description`, `claude-md-init`, `changelog`, `readme-refresh`, `dependency-audit`, `secret-audit`, `test-gap-finder` — each with a fixture, assertions and a real-run transcript under `evals/`.
- Tests: `tests/test-hooks.sh` (37 cases).
