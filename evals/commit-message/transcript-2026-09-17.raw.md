The staged diff adds a `clamp` helper to `calc.py` plus a unit test for it in `test_calc.py`. Both pieces belong to one feature, so a single `feat(calc)` commit fits (no need to split).

Committed as `ad849ba`:

```
feat(calc): add clamp function with test
```

- `calc.py`: adds `clamp(x, lo, hi)` returning `max(lo, min(x, hi))`
- `test_calc.py`: new `test_clamp` asserting `clamp(5, 0, 3) == 3`

No body was needed — the *why* is evident from the diff. Per the skill's rules, I did not add a `Co-Authored-By` trailer, and the message makes no claim about tests passing since I didn't run them.
