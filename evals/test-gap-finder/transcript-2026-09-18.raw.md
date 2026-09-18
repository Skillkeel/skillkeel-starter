## Test gap report

**Layout:** `tests/test_*.py` → pytest (no runner config file; pytest isn't installed in this environment, so no coverage report was produced — no percentage claimed).

### Module → test map

| Module | Test files | Test count | Lines | Churn (90d commits) | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | — | 0 | 10 | **4** | yes — auth |
| `pkg/payments.py` | — | 0 | 4 | 1 | yes — payments |
| `pkg/utils.py` | `tests/test_utils.py` | 1 | 2 | 1 | no |
| `pkg/__init__.py` | — | — | 0 | 1 | (empty, skipped) |

### Ranking

1. **`pkg/auth.py`** — untested, 4× the churn of anything else (`fix(auth): tweak 1/2/3` in the last three commits), and it's the credential-verification path. Highest value.
2. **`pkg/payments.py`** — untested, money-handling, has an explicit validation branch that nothing exercises.
3. `pkg/utils.py` — already covered by `test_slugify`; not proposed.

Only two untested modules exist, so the "top 5" collapses to two proposals.

### Proposals

#### 1. `tests/test_auth.py` — `hash_password(p, salt)`, `verify(p, salt, h)`

- `test_hash_password_is_deterministic` — same `(p, salt)` twice → identical 64-char hex digest (sha256 hexdigest).
- `test_hash_password_salt_changes_digest` — `hash_password("pw", "a") != hash_password("pw", "b")`; guards the `salt + p` concatenation actually mixing salt in.
- `test_verify_round_trip` — `h = hash_password("pw", "s")`; `verify("pw", "s", h)` is `True`.
- `test_verify_rejects_wrong_password_or_salt` — `verify("PW", "s", h)` and `verify("pw", "t", h)` both `False`.
- `test_hash_password_known_vector` — boundary: `hash_password("", "")` equals `hashlib.sha256(b"").hexdigest()` (`e3b0c442…`); pins the exact algorithm so the next "tweak" commit can't silently change it. Worth noting: the concatenation is order-dependent (`salt + p`), so `hash_password("ab","c") != hash_password("cb","a")` but `hash_password("b","a") == hash_password("", "ab")` — a test asserting the known vector locks that in.

#### 2. `tests/test_payments.py` — `charge(amount_cents, currency="EUR")`

- `test_charge_happy_path` — `charge(1250)` → `{"amount": 1250, "currency": "EUR"}` (default currency applied).
- `test_charge_explicit_currency` — `charge(500, currency="USD")["currency"] == "USD"`.
- `test_charge_zero_raises` — `charge(0)` raises `ValueError("amount must be positive")` (boundary: `<= 0` includes zero).
- `test_charge_negative_raises` — `charge(-1)` raises `ValueError`.

No test files were written. Say the word and I'll add both files in the existing style (plain `pytest` functions, direct `from pkg.x import …`) and run them — you'd need `pip install pytest` first since it's not installed here.
