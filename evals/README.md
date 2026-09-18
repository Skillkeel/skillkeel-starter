# Evals

Every skill ships with an eval: a fixture, an expected outcome, and a transcript from a real Claude Code run.

- `<skill>/fixture.sh`: builds the minimal repo state the skill is run against.
- `<skill>/case.yaml` and `<skill>/graders/`: the native `claude plugin eval` case and its graders (tool_used, regex, file_exists, llm_judge).
- `<skill>/expected.md`: the same assertions in prose.
- `<skill>/transcript-<date>.md`: the session transcript, unedited, with a PASS/FAIL verdict per assertion; `transcript-<date>.raw.md` is the assistant text as captured.
- `<skill>/record-<date>.json` (since 0.1.3): the run record, written by `record.py` from the stream-json output: exit code, seconds, every tool call, skill invocations, last message, and the verdict of each grader that needs no model.

Run all: `bash evals/run.sh` (builds fixtures, runs each skill with `claude -p`, writes the records, then prints `cluster.py`).
Trigger prompts: `bash evals/run.sh --trigger` runs the same cases with the fixture's `trigger:` line, a request that never names the skill ("Commit the staged changes." instead of "Use the commit-message skill to commit the staged changes."). The `skill-fired` grader then tests whether the description triggers on a plain request; in the named run it only tests that the invocation path works. Records land as `record-<date>-trigger.json` with `"mode": "trigger"`, and docs/compat.md lists them in the Trigger prompts column.
`python3 evals/cluster.py [--date YYYY-MM-DD]` groups failed cases by their first mechanical mismatch, in this order: runner (exit code, timeout), skill not invoked, tool count, file, text, judge. It also reads native results under `results/`. Read a transcript only where the bucket says the skill itself did something wrong.
