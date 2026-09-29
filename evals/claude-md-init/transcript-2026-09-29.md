# claude-md-init: run 2026-09-29, Claude Code 2.1.284
Raw output: `transcript-2026-09-29.raw.md` (unedited). Record: `record-2026-09-29.json`. Fixture: `fixture.sh`.
Rerun 1 FAILED on not-npm-test, a grader fault: CLAUDE.md listed `pnpm test:ci` and had one line ruling out `npm test` ("There is no `test` script, so `npm test` / `pnpm test` will not work"); the old pattern matched any `npm test`. Fix in 0.1.11: a line that names `npm test` next to no, not, never, don't, instead of or avoid passes; any other line still fails (checked against that CLAUDE.md and four lines that recommend `npm test`).
Rerun 2 FAILED on the escape check: one Bash call ran `ls ~/.cache/node/corepack` to look for a cached pnpm. All graders passed; the record counts any `~/` path as a read outside the fixture, so the case fails. Not a skill change.
Rerun 3: file-written PASS · no-install-run PASS · not-npm-test PASS · pnpm-test-ci PASS · skill-fired PASS · escapes none. Verdict: PASS.
