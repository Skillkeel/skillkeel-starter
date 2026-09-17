No coverage tool is installed (`pytest` is missing), so no coverage percentage is claimed below — the map is built from grepping test imports.

## Source → test map

| Module | Test files | Test count | 90-day churn (commits) | Lines | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | — | 0 | 4 | 10 | yes (auth) |
| `pkg/payments.py` | — | 0 | 1 | 4 | yes (payments) |
| `pkg/utils.py` | `tests/test_utils.py` | 1 | 1 | 2 | no |
| `pkg/__init__.py` | — | — | 1 | 0 | skipped (empty) |

Layout: `tests/` with `test_*.py`, pytest-style plain `assert` functions and no runner config. `utils.slugify` already has a test and isn't proposed.

## Ranked proposals

Only two untested modules exist, so the "top 5" collapses to two modules with 5 proposed test functions total. Ranked: `auth.py` first (4 of the 5 commits touch it, and it's the auth path), `payments.py` second (money path, untested).

### 1. `pkg/auth.py` → `tests/test_auth.py`

`hash_password(p, salt)` returns `sha256(salt + p).hexdigest()`; `verify(p, salt, h)` compares that against `h`.

- `test_hash_password_is_deterministic_and_hex_sha256`
  - Same `(p, salt)` twice → identical output; output is 64 lowercase hex chars.
  - Pin one known vector: `hash_password("pw", "s")` == `hashlib.sha256(b"spw").hexdigest()` (guards against someone silently swapping the `salt + p` concatenation order — the three recent "tweak" commits make this the most likely regression).
- `test_hash_password_salt_changes_output`
  - `hash_password("pw", "a") != hash_password("pw", "b")`.
  - Boundary: empty salt `""` still works and equals plain `sha256("pw")`.
- `test_verify_round_trip`
  - Happy path: `verify("pw", "s", hash_password("pw", "s")) is True`.
  - Failure: wrong password → `False`; wrong salt with correct password → `False`; tampered hash (flip one char) → `False`.
- `test_hash_password_rejects_non_string` *(documents current behaviour)*
  - `hash_password(None, "s")` and `hash_password("pw", None)` raise `TypeError` (from `salt + p` / `.encode()`); worth pinning so a future refactor doesn't start silently hashing `"None"`.

### 2. `pkg/payments.py` → `tests/test_payments.py`

`charge(amount_cents, currency="EUR")` raises `ValueError("amount must be positive")` when `amount_cents <= 0`, else returns `{"amount": ..., "currency": ...}`.

- `test_charge_returns_amount_and_currency`
  - Happy path: `charge(1250)` → `{"amount": 1250, "currency": "EUR"}` (checks the default currency).
  - Explicit currency: `charge(500, "USD")["currency"] == "USD"`.
  - Boundary: `charge(1)` succeeds (smallest positive amount).
- `test_charge_rejects_non_positive_amount`
  - `charge(0)` raises `ValueError` matching `"amount must be positive"` (exact boundary of the `<= 0` check).
  - `charge(-1)` raises `ValueError`.
  - Currency isn't validated at all today — no test proposed for that since there's no behaviour to assert; flagging it as a gap in the code rather than the tests.

## Not proposed
- `pkg/utils.py` — already covered by `tests/test_utils.py`.
- `pkg/__init__.py` — empty.

No test files were written. If you want any of these, say which and I'll add them in the existing `tests/test_*.py` style and run them (you'll need `pip install pytest` first — it's not available in this environment).
