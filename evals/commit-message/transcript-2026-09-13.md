# commit-message — run 2026-09-13, Claude Code 2.1.270, `claude -p --plugin-dir`
Prompt: "use the commit-message skill to commit the staged changes"
Result: commit `3d2d826` — subject `feat: add calc modules with add and sub` (40 chars). Two files, four insertions.
Notes from the run: first commit attempt failed on missing git identity; the skill retried with one-off `-c user.name/-c user.email` and did not change global config. Trailer omitted per skill rule.
Verdict: 1 PASS, 2 PASS, 3 PASS, 4 PASS.
