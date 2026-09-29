No test files were written. Only two modules have no tests, `pkg/auth.py` and `pkg/payments.py`, so there are two proposals rather than five. I couldn't get a coverage number because pytest isn't installed here (`No module named pytest`). The table below is based on grepping the tests for imports, plus git churn and file size.

## Map

| Rank | Module | Lines | Commits (last 90 days) | Critical path | Tests |
|---|---|---|---|---|---|
| 1 | `pkg/auth.py` | 10 | 4 (the most in the repo: `feat: initial` plus 3× `fix(auth)`) | Yes (auth) | none |
| 2 | `pkg/payments.py` | 4 | 1 | Yes (payments) | none |
| — | `pkg/utils.py` | 2 | 1 | No | `tests/test_utils.py` (1 test) |
| — | `pkg/__init__.py` | 0 | 1 | — | empty file, skipped |

## Proposals

### 1. `tests/test_auth.py`: `hash_password(p, salt)` and `verify(p, salt, h)`
This is the highest priority: it's security-critical, it has changed four times with no tests, and the recent "tweak" commits could quietly change the hash output.

- **`test_hash_password_is_deterministic`**: the same `p` and `salt` should always give the same result.
- **`test_hash_password_matches_known_vector`**: `hash_password("pw", "salt")` should equal `hashlib.sha256(b"saltpw").hexdigest()`. This pins the salt-before-password order, so a future tweak that changes it fails the test.
- **`test_hash_password_salt_changes_output`**: the same password with two different salts should give different hashes.
- **`test_verify_accepts_correct_password`**: `verify("pw", "s", hash_password("pw", "s"))` should return `True`.
- **`test_verify_rejects_wrong_password_or_salt`**: a wrong password should return `False`, and so should a wrong salt.
- **`test_hash_password_empty_inputs`**: `hash_password("", "")` should return the SHA-256 of an empty string rather than raising an error.

While reading the code I noticed that `verify` compares with `==`, which isn't constant-time. `hmac.compare_digest` would be safer. That's a code fix rather than something to test, so I'm only mentioning it.

### 2. `tests/test_payments.py`: `charge(amount_cents, currency="EUR")`
- **`test_charge_returns_amount_and_default_currency`**: `charge(100)` should return `{"amount": 100, "currency": "EUR"}`.
- **`test_charge_custom_currency`**: `charge(100, "USD")["currency"]` should be `"USD"`.
- **`test_charge_minimum_positive_amount`**: `charge(1)` is the smallest valid amount and should succeed.
- **`test_charge_rejects_zero_and_negative`**: `charge(0)` and `charge(-1)` should each raise `ValueError` with the message `"amount must be positive"`. Parametrizing covers both.

`pkg/utils.py` already has a test and is tiny, so there's nothing to propose for it.

To run any of these you'd need pytest first (`pip install pytest pytest-cov`). Want me to write these two test files, following the plain-function style in `tests/test_utils.py`?
