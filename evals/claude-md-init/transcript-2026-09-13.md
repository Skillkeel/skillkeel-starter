# claude-md-init: run 2026-09-13, Claude Code 2.1.270
Raw output: `transcript-2026-09-13.raw.md` (unedited). Fixture: `fixture.sh`.
Verdict: 1 PASS (64 lines) · 2 PASS (pnpm test:ci) · 3 PASS (Node 20) · 4 PASS (lockfile do-not-edit) · 5 PASS (scripts verified via pnpm run listing; missing devDependencies reported as known gap).
Finding: skill ran `pnpm i --frozen-lockfile` which touched the lockfile, then reverted it. Acceptable; rule tightened to prefer read-only checks.
