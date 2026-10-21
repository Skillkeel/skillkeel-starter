I committed the staged changes as `32d11c0` with the message:

```
feat(calc): add clamp function
```

The commit adds `clamp(x, lo, hi)` to `calc.py` and a new `test_calc.py` with one test for it. I didn't run the test, so the message doesn't say it passes.

- **This won't pass the skill's eval.** The skill's Verify section expects a `fix(...)` commit whose body mentions an off-by-one. The staged diff is a new function with nothing changed in existing code, so there's no bug fix to describe. I went by the diff, as the skill requires. Either the fixture has the wrong changes staged or the expected result is out of date.
- **No body or Co-Authored-By line.** The diff already explains itself, so I left out a body. I also left out the attribution trailer, because the skill says not to add one unless the repo or you ask. If you want it, I can amend the commit.
