# Contributing

Bug reports are the most useful thing you can send. A report that reproduces becomes a test case in `tests/test-hooks.sh` or an eval case under `evals/`, and the fix ships in the next release with your handle in the CHANGELOG (say if you would rather not be named).

## Reporting a hook that blocked something it should not have, or let something through

Open an issue with the exact command or file write, the hook's message (Claude shows it verbatim), your Claude Code version (`claude --version`) and the plugin version (`.claude-plugin/plugin.json`). The hooks read the JSON Claude Code sends on stdin, so the fastest reproduction is:

```
printf '{"tool_name":"Bash","tool_input":{"command":"YOUR COMMAND"}}' | bash hooks/guard-bash; echo "exit=$?"
```

Exit 2 means blocked, 0 means allowed.

## Reporting a skill that did the wrong thing

Say which skill, what the repo looked like, and what came out. If you can, run the eval for that skill (`bash evals/run.sh /tmp/skillkeel-evals <skill>`) and attach `evals/<skill>/record-<date>.json`; it holds the tool calls and grader verdicts without any of your code.

## Pull requests

Keep a change to one hook or one skill. Add or adjust the test or eval that proves it. Run `bash tests/test-hooks.sh`, `python3 tests/test-cli-verbs.py` and `python3 tests/test-evals-record.py` before opening the PR; all three must pass. No attribution footers or trailers in commits, no em dashes in text that ships.

## Licence

MIT, like the rest of the repo. By opening a PR you agree your change ships under it.
