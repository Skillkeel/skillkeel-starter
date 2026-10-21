I didn't write any test files. This repo has only three source modules, so instead of five there are two proposals: one for `pkg/auth.py` and one for `pkg/payments.py`.

**Setup:** The tests are pytest-style, in `tests/` as `test_*.py`, with no runner config file. I didn't get a coverage percentage because pytest isn't installed (`No module named pytest`). The "covered" column below comes from checking which modules the tests import.

## Module → test map

| Rank | Module | Lines | Changes in last 90 days | Test files | Tests | Critical path |
|---|---|---|---|---|---|---|
| 1 | `pkg/auth.py` | 10 | **4** (initial + 3 "fix(auth)" tweaks) | none | 0 | **auth** |
| 2 | `pkg/payments.py` | 4 | 1 | none | 0 | **payments** |
| — | `pkg/utils.py` | 2 | 1 | `tests/test_utils.py` | 1 | no |
| — | `pkg/__init__.py` | 0 | 1 | — | — | empty, skip |

`utils.slugify` is already tested and very simple, so I'm not proposing anything for it.

## Proposals

### 1. `tests/test_auth.py`: `hash_password(p, salt)`, `verify(p, salt, h)`
`auth.py` changes the most of any file and sits on the auth path, yet nothing tests it.

- `test_hash_password_is_deterministic`: the same `p` and `salt` always give the same digest.
- `test_hash_password_matches_sha256_of_salt_plus_password`: the result equals `hashlib.sha256((salt + p).encode()).hexdigest()` and is 64 hex characters. This pins the salt-before-password order, so a future tweak can't silently break existing stored hashes.
- `test_hash_password_differs_by_salt`: the same password with two different salts gives two different digests.
- `test_verify_accepts_correct_password`: `verify("pw", "s", hash_password("pw", "s"))` returns `True`.
- `test_verify_rejects_wrong_password_or_salt`: a wrong password returns `False`, and so does the right password with the wrong salt.

### 2. `tests/test_payments.py`: `charge(amount_cents, currency="EUR")`
This is on the payments path and is untested, including its only error check.

- `test_charge_returns_amount_and_default_currency`: `charge(100)` returns `{"amount": 100, "currency": "EUR"}`.
- `test_charge_custom_currency`: `charge(250, "USD")` returns `currency` as `"USD"`.
- `test_charge_minimum_positive_amount`: `charge(1)` succeeds, which tests the boundary just above 0.
- `test_charge_rejects_zero_and_negative`: `charge(0)` and `charge(-5)` raise `ValueError` with the message "amount must be positive" (use `pytest.raises(..., match=...)`).

## Code issues the tests would expose
- **`auth.py:4`:** passwords are hashed with a single SHA-256 pass, which is fast and weak for stored passwords. A slow algorithm like `hashlib.scrypt`, bcrypt or argon2 would be safer.
- **`auth.py:7`:** `verify` compares hashes with `==`, which can leak timing information. `hmac.compare_digest` avoids that.
- **`payments.py`:** `charge` checks only that the amount is positive. It accepts non-integer amounts (e.g. `1.5`) and any currency string. Decide whether that's intended before writing tests that lock it in.

To write and run these, install pytest first (`pip install pytest pytest-cov`). Tell me if you want me to go ahead.
