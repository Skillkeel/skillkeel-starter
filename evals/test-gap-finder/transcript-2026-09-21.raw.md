Test layout: `tests/test_*.py` (pytest by convention; no runner config present, and `pytest`/`pytest-cov` aren't installed here, so no coverage numbers — the map below is from grep, not a coverage tool).

## Module → test map

| Module | Lines | Commits (90d) | Test files | Tests | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | 10 | 4 | — | 0 | yes (auth) |
| `pkg/payments.py` | 4 | 1 | — | 0 | yes (payments) |
| `pkg/utils.py` | 2 | 1 | `tests/test_utils.py` | 1 | no |
| `pkg/__init__.py` | 0 | 1 | — | — | empty, skip |

Ranking: **auth.py** first (highest churn, auth path, two functions), **payments.py** second (data/money path, untested). `utils.py` is already covered and trivial — not proposed. Only two modules qualify, so there are two proposals rather than five.

## Proposals (not written)

### 1. `tests/test_auth.py` — `pkg/auth.py`

`hash_password(p, salt)` → `sha256(salt + p).hexdigest()`; `verify(p, salt, h)` → equality against that.

- `test_hash_password_is_deterministic` — same `(p, salt)` twice yields identical 64-char hex; matches `hashlib.sha256((salt+p).encode()).hexdigest()` computed inline.
- `test_hash_password_salt_changes_output` — `hash_password("pw", "a") != hash_password("pw", "b")`.
- `test_hash_password_is_order_sensitive` — since concatenation is `salt + p`, `hash_password("ab", "c") != hash_password("c", "ab")` (guards against a refactor swapping the order and silently invalidating stored hashes).
- `test_verify_round_trip_and_rejects_wrong_password` — `verify("pw", "s", hash_password("pw", "s"))` is `True`; `verify("px", "s", same_hash)` and `verify("pw", "t", same_hash)` are `False`.
- `test_hash_password_rejects_non_string` (failure) — `hash_password(None, "s")` raises `TypeError` (`salt + p` fails); documents the current contract.

### 2. `tests/test_payments.py` — `pkg/payments.py`

`charge(amount_cents, currency="EUR")` → raises `ValueError` if `amount_cents <= 0`, else returns `{"amount", "currency"}`.

- `test_charge_returns_amount_and_default_currency` — `charge(1000) == {"amount": 1000, "currency": "EUR"}`.
- `test_charge_respects_explicit_currency` — `charge(500, currency="USD")["currency"] == "USD"`.
- `test_charge_boundary_one_cent_succeeds` — `charge(1)["amount"] == 1`.
- `test_charge_rejects_zero_and_negative` — `charge(0)` and `charge(-1)` both raise `ValueError` with message `"amount must be positive"` (`pytest.raises(..., match=...)`).

Not proposed: `pkg/utils.py` (already tested), `pkg/__init__.py` (empty).

I have not written any files. Say the word if you want either of these created and run.
