# test-gap-finder — expected
Fixture: `pkg/utils.py` tested; `pkg/auth.py` untested with 3 recent commits; `pkg/payments.py` untested.
1. Map/table shows utils.py as tested, auth.py and payments.py as untested.
2. auth.py ranked at or near top (churn), payments.py flagged as critical path.
3. ≥ 2 concrete test cases per proposal, referencing real functions (`hash_password`, `verify`, `charge` with amount ≤ 0).
4. utils.py not proposed for new tests.
5. No test files written.
