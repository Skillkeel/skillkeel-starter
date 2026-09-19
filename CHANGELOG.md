# Changelog

## Unreleased

- evals: `evals/record.py` records `escapes`, tool calls whose path (Read, Edit, Write, Glob, Grep) or Bash command before any heredoc names the plugin checkout, the home directory, a parent directory or a sibling case; one escape fails the case and `cluster.py` files it under runner as "reads outside the fixture". Text the run writes is not checked, so a CLAUDE.md that mentions `~/.claude` passes. The 0.1.6 claim (no transcript read the grader) was a grep; this makes it a record field. Today's eight records re-graded from their streams: 0 escapes. 30 record checks.

## 0.1.6 (2026-09-19)

- evals: trigger mode. `bash evals/run.sh --trigger` runs every case with the fixture's `trigger:` line, a request that never names the skill ("Commit the staged changes."), so the skill-fired grader tests the description and not only the invocation path; records carry `mode: trigger` and docs/compat.md has a Trigger prompts column. First run on 2.1.276: 8/8 fired. Two graders were stricter than the skill text and are fixed: claude-md-init `no-install-run` matched `pnpm install` inside the heredoc that wrote CLAUDE.md (now command position only); readme-refresh `deadlink-handled` demanded the dead link removed while the skill allows a `<!-- TODO: verify -->` marker (now accepts the marked form, before or on the same line as the link; the named rerun on 2.1.276 put it after the link). Named rerun on 2.1.276: 8/8. Found through the HN thread on skill triggering (item 49744398), no user report.
- evals: `evals/record.py` records the plugin list from the run's init event; any plugin besides skillkeel-starter fails the case as "not isolated" and `cluster.py` files it under runner with the plugin names. The 09-17 leak (a user-level hook loaded into every run while the suite stayed green) would have failed on the record line instead of in a transcript read. 25 record checks.
- Hooks and skill texts unchanged, 64 hook tests. No transcript in the 21 eval runs kept in this repo reads the grader, the fixture script or any path outside the fixture directory (checked 2026-09-19); the grader still sits within reach of the run through the plugin directory, so this is an observation, not a guarantee.

## 0.1.5 (2026-09-17)

- secret-audit: a note that a found value matches a known placeholder (the AWS docs example key) names the placeholder and keeps the masked form. On Claude Code 2.1.274 the skill masked the key in the findings table and then quoted it in full in a note; the masked grader caught it.
- pr-description: the body ends after the Risk / rollback section and carries no attribution line even when the harness asks for one; users who want attribution off everywhere are pointed to the includeCoAuthoredBy setting. On 2.1.274 the "Generated with Claude Code" footer came back (first seen and fixed 2026-09-13); the no-footer grader caught it.
- evals: dependency-audit grader `bumped` accepts `"lodash":"4.18.1"` without a space (npm writes compact JSON; the pattern expected a space, a grader fault); commit-message grader `no-trailer` matches the trailer form `Co-Authored-By:` and the footer link, not the words (the model's sentence "I omitted the Co-Authored-By trailer" had tripped it). `evals/run.sh` passes `--setting-sources project` so the maintainer's user-level plugins and hooks stay out of the run, and sets `GIT_CONFIG_GLOBAL=/dev/null` plus a fixture git identity so the model never sees or commits with the maintainer's; run records replace the case directory, the home directory and any global git identity with placeholders before they are written (a user-level "be terse" hook had turned a report into "Done."). `evals/record.py` reads the Claude Code version from the init event and judges regex graders with `trace` and `{source: file}` targets locally (19 checks).
- docs/compat.md: table "tested against Claude Code versions", generated from the eval results in this repo; the README links it. 2.1.274 (2026-09-17): 3/3 native git-free cases, 5/5 transcript cases after the two skill fixes above.
- Hooks unchanged, 64 tests.

## 0.1.4 (2026-09-17)

- guard-bash: git settings that make git run a command are now refused when set through `git config` or `git -c`: `core.fsmonitor`, `core.hooksPath`, `core.sshCommand`, `core.pager`, `core.editor`, `core.askPass`, `core.gitProxy`, `core.alternateRefsCommand`, `diff.external`, difftool and mergetool commands, merge drivers, filter clean/smudge/process, credential helpers, gpg programs, `sequence.editor`, uploadpack and receive hooks, and shell aliases (`alias.x '!...'`). Shell writes into a `.git/` path (`>> sub/.git/config`, `> .git/hooks/pre-commit`) and `mv`, `cp`, `ln` or `rsync` with a `.git` target are refused too. Reads (`--get`, `--list`, `cat .git/config`), `--unset`, and plain keys such as `user.email` or `core.autocrlf` pass. Prompted by accomplish.ai's Beltdown write-up (2026-09-11): a repo-planted `core.fsmonitor` in a nested `.git/config` ran outside the Claude Code sandbox because the harness runs its own git there (fixed upstream in 2.1.247). Before this release all five commands from that chain passed guard-bash.
- tests: 20 new guard cases (64 total).
- Known, on purpose: a `.git/config` edited through the Write or Edit tool is not covered by this hook; Claude Code's own file tools refuse `.git` writes.

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
