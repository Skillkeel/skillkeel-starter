# Changelog

## 0.1.3 (2026-09-17)

- tests: CLI verb gate. `tests/cli-verbs.json` records the subcommands and flags that the latest releases of gitleaks, trufflehog, pip-audit and gh accept, read from each binary's own help output. `python3 tests/test-cli-verbs.py` greps every `<cli> <verb> --flag` out of the skill texts and fails on anything the snapshot does not know, so a renamed subcommand (gitleaks `detect` in 0.1.1) fails on the commit that touches the skill instead of in a transcript. Shape from u/EvalRaccoonDev on r/ClaudeCode.
- evals: run record. `evals/run.sh` now keeps the stream-json output of each run and writes `record-<date>.json` per case (exit code, seconds, every tool call, skill invocations, last message) with the verdict of each grader that needs no model (tool_used, regex, file_exists). `evals/cluster.py` groups failed cases by their first mechanical mismatch (runner, skill not invoked, tool count, file, text, judge) before anyone opens a transcript. Also from the thread with u/EvalRaccoonDev.
- Hooks and skills unchanged, 44 hook tests; 17 checks for the record and cluster tools; the verb gate checks 6 commands in 8 files. Run records scrub the plugin path and the home directory before they are written.

## 0.1.2 (2026-09-15)

- secret-audit: the gitleaks commands are now `gitleaks git --report-format json --report-path <file> .` and, for the pre-commit hook, `gitleaks git --pre-commit --staged .`. gitleaks deprecated `detect` and `protect` in v8.19.0; the old forms are noted for older installs. Found by the upstream watch, no user report.
- Docs: plain punctuation in the skill eval notes and this changelog; README hook test count corrected to 44.
- Hooks unchanged, 44 tests.

## 0.1.1 (2026-09-15)

- guard-bash: recursive `rm` behind `find -exec`, `-execdir` or `xargs` is now refused. The path never appears as an argument in those forms, so the old rule never saw it. Reported by u/Far_Business4773 on r/ClaudeCode. `find -delete` and `-exec rm {}` on single files still pass.
- tests: 7 new guard cases (44 total).
- Known, on purpose: `git stash` and `git checkout <rev> -- <dir>` are not blocked.

## 0.1.0 (2026-09-13)
- Hooks: `guard-bash` (blocks destructive shell commands), `secret-scan` (blocks credentials in file writes), `session-start` (short project brief).
- Skills: `commit-message`, `pr-description`, `claude-md-init`, `changelog`, `readme-refresh`, `dependency-audit`, `secret-audit`, `test-gap-finder`, each with a fixture, assertions and a real-run transcript under `evals/`.
- Tests: `tests/test-hooks.sh` (37 cases).
