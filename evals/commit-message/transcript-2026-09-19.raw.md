Committed as `71e84cd`:

```
feat(calc): add clamp helper with test
```

- `calc.py`: adds `clamp(x, lo, hi)` returning `max(lo, min(x, hi))`
- `test_calc.py`: new file with `test_clamp` asserting `clamp(5, 0, 3) == 3`

No body was added since the *why* is evident from the diff. I did not run the test, so the message makes no claim about it passing. One note: the skill's own eval description expects a `fix(...)` subject mentioning an off-by-one, but the actual staged diff contains no bug fix — only a new function — so per the skill's rule ("never describe changes that are not in the staged diff") I classified it as `feat`.
