Staged diff is a single `feat`: a new `clamp` helper in `calc.py` plus its test. Committing with:

```
feat(calc): add clamp helper with test
```

Committed `dec98e8` on `main`:

```
feat(calc): add clamp helper with test

 calc.py      | 3 +++
 test_calc.py | 4 ++++
```

No body was needed — the diff is self-explanatory (adds `clamp(x, lo, hi)` and a test asserting the upper bound). Per the skill's rules I omitted the Co-Authored-By trailer; say the word if you'd like it added.
