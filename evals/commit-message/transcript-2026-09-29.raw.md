I committed the staged changes as `9e3046c` with the message `feat(calc): add clamp helper with test`.

- **What went in:** a `clamp(x, lo, hi)` function in `calc.py`, and a new `test_calc.py` that checks `clamp(5, 0, 3) == 3`.
- **Commit type:** I used `feat` for both files, since the test only covers the new function.
- **No body:** the diff is small and self-explanatory. I didn't run the test, and the message doesn't say it passes.
- **No Co-Authored-By line:** the commit-message skill says to leave out tool attribution unless you or the repo ask for it. That overrode the default Claude Code attribution. If you want the line, I can amend the commit to add it.
