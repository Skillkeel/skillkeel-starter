## Test gap report

**Layout:** `pkg/` source, `tests/test_*.py` (pytest-style). No runner config and `pytest` isn't installed, so no coverage run — the numbers below are from grepping, not a coverage tool.

| Module | Test files | Test count | 90-day churn | Lines | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | — | 0 | 4 commits | 10 | yes (auth) |
| `pkg/payments.py` | — | 0 | 1 commit | 4 | yes (payments) |
| `pkg/utils.py` | `tests/test_utils.py` | 1 | 1 commit | 2 | no |
| `pkg/__init__.py` | — | — | 1 commit | 0 | empty, skip |

**Ranking:** `auth.py` first (highest churn, auth), `payments.py` second (money, raises on bad input). `utils.py` is already covered and not on a critical path — not proposed. Only two modules qualify, so the "top 5" is a top 2.

## Proposals

### 1. `tests/test_auth.py` — `pkg/auth.py`

Signatures: `hash_password(p, salt) -> str`, `verify(p, salt, h) -> bool`.

- `test_hash_password_is_deterministic` — same `(p, salt)` twice returns identical 64-char hex digest.
- `test_hash_password_salt_changes_digest` — `hash_password("pw", "a") != hash_password("pw", "b")`.
- `test_hash_password_matches_sha256_of_salt_plus_password` — pin the layout: equals `hashlib.sha256(b"saltpw").hexdigest()` for `("pw", "salt")`. Guards against silently reordering to `p + salt`, which would invalidate every stored hash.
- `test_verify_round_trip` — `verify("pw", "s", hash_password("pw", "s")) is True`.
- `test_verify_rejects_wrong_password_and_wrong_salt` — both `verify("nope", "s", h)` and `verify("pw", "t", h)` return `False`.
- `test_hash_password_unicode_input` — boundary: non-ASCII `p`/`salt` doesn't raise (`.encode()` defaults to UTF-8).

### 2. `tests/test_payments.py` — `pkg/payments.py`

Signature: `charge(amount_cents, currency="EUR") -> dict`.

- `test_charge_returns_amount_and_default_currency` — `charge(1000) == {"amount": 1000, "currency": "EUR"}`.
- `test_charge_respects_explicit_currency` — `charge(500, "USD")["currency"] == "USD"`.
- `test_charge_rejects_zero` — `charge(0)` raises `ValueError` matching `"amount must be positive"` (boundary of the `<= 0` check).
- `test_charge_rejects_negative` — `charge(-1)` raises `ValueError`.
- `test_charge_minimum_amount` — `charge(1)` succeeds (smallest valid value).

Nothing was written. Note that running these needs `pytest` installed (`pip install pytest`) and an empty `tests/__init__.py` or `pythonpath` config so `pkg` imports resolve. Say the word if you want me to write either file.
