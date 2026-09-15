# Changelog

## 0.1.1 (2026-09-15)

- guard-bash: recursive `rm` behind `find -exec`, `-execdir` or `xargs` is now refused. The path never appears as an argument in those forms, so the old rule never saw it. Reported by u/Far_Business4773 on r/ClaudeCode. `find -delete` and `-exec rm {}` on single files still pass.
- tests: 7 new guard cases (44 total).
- Known, on purpose: `git stash` and `git checkout <rev> -- <dir>` are not blocked.

## 0.1.0 (2026-09-13)
- Hooks: `guard-bash` (blocks destructive shell commands), `secret-scan` (blocks credentials in file writes), `session-start` (short project brief).
- Skills: `commit-message`, `pr-description`, `claude-md-init`, `changelog`, `readme-refresh`, `dependency-audit`, `secret-audit`, `test-gap-finder`, each with a fixture, assertions and a real-run transcript under `evals/`.
- Tests: `tests/test-hooks.sh` (37 cases).
