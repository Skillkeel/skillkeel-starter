## Test gap map

Layout: `tests/test_*.py`, pytest-style (bare `assert`). No pytest config and pytest isn't installed here, so I didn't run coverage — the map below is from grepping test imports.

| Module | Test files | Tests | Churn (90d) | Lines | Critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | — | 0 | **4 commits** | 10 | yes (auth) |
| `pkg/payments.py` | — | 0 | 1 | 4 | yes (payments) |
| `pkg/utils.py` | `tests/test_utils.py` | 1 | 1 | 2 | no |
| `pkg/__init__.py` | — | — | 1 | 0 | skip (empty) |

Only two modules are untested, so the "top 5" collapses to two proposals. `utils.slugify` is already covered and not worth expanding right now.

## 1. `tests/test_auth.py` — highest priority

Touched in 4 of the last 4 commits (`fix(auth): tweak 1–3`) with zero tests guarding it. `hash_password(p, salt)` and `verify(p, salt, h)` in `pkg/auth.py:3-7`.

- `test_hash_password_is_deterministic` — same `(p, salt)` twice → identical hex digest; pins the algorithm so the next "tweak" can't silently change it.
- `test_hash_password_is_sha256_of_salt_then_password` — assert against `hashlib.sha256((salt + p).encode()).hexdigest()` computed inline. The concatenation order (`salt + p`, not `p + salt`) is the exact thing a refactor would flip.
- `test_different_salt_changes_hash` — same password, two salts → different digests.
- `test_verify_round_trip` — `verify(p, salt, hash_password(p, salt))` is `True`.
- `test_verify_rejects_wrong_password_and_wrong_salt` — `verify("other", salt, h)` and `verify(p, "othersalt", h)` are both `False`.
- Boundary: `test_hash_password_empty_strings` — `hash_password("", "")` returns the known SHA-256 of `b""` (`e3b0c442…b855`); documents that empty input is currently accepted rather than rejected.

## 2. `tests/test_payments.py`

`charge(amount_cents, currency="EUR")` at `pkg/payments.py:1-4`.

- `test_charge_returns_amount_and_default_currency` — `charge(500)` → `{"amount": 500, "currency": "EUR"}`.
- `test_charge_respects_explicit_currency` — `charge(500, currency="USD")` → currency `"USD"`.
- `test_charge_rejects_zero` — `charge(0)` raises `ValueError` matching `"amount must be positive"` (the `<= 0` boundary, not just negatives).
- `test_charge_rejects_negative` — `charge(-1)` raises `ValueError`.

Not derivable from the code, so not proposed: currency validation and non-int amounts — `charge(1.5)` and `charge(5, currency="xyz")` currently pass through untouched. If that's unintended, that's a code change first, then a test.

Want me to write either of these files? I'd match the existing style in `tests/test_utils.py` (plain functions, direct `from pkg.x import ...`).
