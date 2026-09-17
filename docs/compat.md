# Skillkeel Starter: tested against Claude Code versions

Generated from the eval results in this repo (`evals/results/` for `claude plugin eval`, `evals/*/record-*.json` for the transcript runner); nothing in this table is typed by hand. Latest per case per run. Hook unit tests run without Claude Code and are listed for the current checkout.

Hook unit tests (`bash tests/test-hooks.sh`, current checkout): 64 passed, 0 failed.

| Claude Code | Date | Native eval cases | Transcript cases | Cost (USD) | Notes |
|---|---|---|---|---|---|
| 2.1.274 | 2026-09-17 | 3/3 | 5/5 | 1.05 |  |
| 2.1.271 | 2026-09-15 | 0/0 | 1/1 | 0.00 |  |
| 2.1.270 | 2026-09-14 | 2/4 | 0/0 | 0.92 | failed: changelog, commit-message |
| 2.1.270 | 2026-09-13 | 0/0 | 8/8 | 0.00 |  |

Last generated 2026-09-17 by tools/compat.py in the Skillkeel ops repo. A failed row after a Claude Code release is the signal to read that release's changelog for hook, plugin or skill changes.
