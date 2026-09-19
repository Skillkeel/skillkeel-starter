`pytest` isn't installed in this environment, so no coverage tool ran — the map below is from grep/import analysis only, not a measured percentage.

## Coverage map

| Module | Lines | Test files | Tests | Churn (90d commits) | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | 10 | — | 0 | **4** | yes (auth) |
| `pkg/payments.py` | 4 | — | 0 | 1 | yes (payments) |
| `pkg/utils.py` | 2 | `tests/test_utils.py` | 1 | 1 | no |
| `pkg/__init__.py` | 0 | — | — | 1 | skip (empty) |

Runner: no `pyproject.toml`/`pytest.ini`/`setup.cfg`; layout is `tests/test_*.py` with plain `assert`, so pytest is the implied runner.

## Ranking

1. **`pkg/auth.py`** — untested, highest churn (3 of 4 commits touch it), auth critical path.
2. **`pkg/payments.py`** — untested, payments critical path, contains the only branching/error logic in the package.

`utils.py` is already covered and trivial; nothing proposed there. Only two modules qualify, so this is a top-2 rather than a top-5.

## Proposed tests

### 1. `tests/test_auth.py` — `hash_password(p, salt)` and `verify(p, salt, h)`

- `test_hash_password_is_deterministic` — same `(p, salt)` twice → identical 64-char hex string.
- `test_hash_password_salt_changes_output` — `hash_password("pw", "a") != hash_password("pw", "b")`.
- `test_hash_password_matches_sha256_of_salt_plus_password` — pins the concatenation order: result equals `hashlib.sha256(b"saltpw").hexdigest()` for `("pw", "salt")`. Guards against a future refactor swapping to `p + salt`, which would silently invalidate every stored hash.
- `test_verify_round_trip` — `verify(p, salt, hash_password(p, salt))` is `True`.
- `test_verify_rejects_wrong_password_or_salt` — wrong password → `False`; correct password with a different salt → `False`.
- `test_hash_password_rejects_non_str` (failure) — `hash_password(None, "s")` raises `TypeError` (from `salt + p`); documents that there's no input validation.

### 2. `tests/test_payments.py` — `charge(amount_cents, currency="EUR")`

- `test_charge_returns_amount_and_default_currency` — `charge(500)` → `{"amount": 500, "currency": "EUR"}`.
- `test_charge_respects_explicit_currency` — `charge(500, "USD")["currency"] == "USD"`.
- `test_charge_boundary_one_cent` — `charge(1)` succeeds (smallest positive value).
- `test_charge_zero_raises` — `charge(0)` raises `ValueError` matching `"amount must be positive"` (the `<= 0` boundary).
- `test_charge_negative_raises` — `charge(-100)` raises `ValueError`.

Per your instruction, no test files were written. Say the word if you'd like me to create either file.
