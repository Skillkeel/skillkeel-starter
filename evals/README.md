# Evals

Every skill ships with an eval: a fixture, an expected outcome, and a transcript from a real Claude Code run.

- `<skill>/fixture/`: minimal repo state the skill is run against (created by `fixture.sh`).
- `<skill>/expected.md`: observable assertions (what the output must contain / must not contain).
- `<skill>/transcript-<date>.md`: the actual session transcript, unedited, with a PASS/FAIL verdict per assertion.

Run all: `bash evals/run.sh` (builds fixtures, prints the checklist to verify manually inside Claude Code).
