Done mapping. No pytest/pytest-cov installed, so no coverage run, no percentage claimed. Layout: `tests/test_*.py`, pytest-style.

**Coverage map**

| module | test files | tests | churn (90d) | lines | critical path |
|---|---|---|---|---|---|
| `pkg/auth.py` | none | 0 | 4 commits | 10 | yes (auth) |
| `pkg/payments.py` | none | 0 | 1 commit | 4 | yes (payments) |
| `pkg/utils.py` | `tests/test_utils.py` | 1 | 1 commit | 2 | no |
| `pkg/__init__.py` | skip | – | – | 0 | empty |

Ranking: auth first (untested, 4 commits in 90 days, auth path). Payments second (untested, money path). Utils covered, not proposed. Only two candidates worth tests, so list stops at two, not five.

**Proposal 1: `tests/test_auth.py`**

Functions: `hash_password(p, salt)`, `verify(p, salt, h)`.

- `test_hash_password_is_deterministic`: same `p` + `salt` twice gives same hex digest. Digest length 64 (sha256 hexdigest).
- `test_hash_password_salt_changes_output`: same `p`, different `salt`, digests differ. Guards against salt being ignored.
- `test_hash_password_matches_known_sha256`: `hash_password("pw", "s")` equals `hashlib.sha256(b"spw").hexdigest()`. Pins concat order `salt + p`. Order swap in future tweak would break this.
- `test_verify_round_trip`: `verify(p, salt, hash_password(p, salt))` is `True`.
- `test_verify_rejects_wrong_password_or_salt`: wrong `p` gives `False`. Wrong `salt` gives `False`.
- `test_hash_password_non_ascii`: `p="pässwörd"` works. Code calls `.encode()` default UTF-8, so no crash expected. Boundary case.

**Proposal 2: `tests/test_payments.py`**

Function: `charge(amount_cents, currency="EUR")`.

- `test_charge_happy_path`: `charge(1000)` returns `{"amount": 1000, "currency": "EUR"}`. Pins default currency.
- `test_charge_custom_currency`: `charge(500, "USD")` returns `currency == "USD"`.
- `test_charge_zero_raises`: `charge(0)` raises `ValueError` with message `"amount must be positive"`. Boundary at `<= 0`.
- `test_charge_negative_raises`: `charge(-1)` raises `ValueError`.
- `test_charge_minimum_amount`: `charge(1)` succeeds. Boundary just above zero.

No test files written. To proceed: say which proposals to write, and install pytest first (`pip install pytest`).
