No remote is configured, so I compared against local `main` (3 commits, 3 files). Note the repo has no test files yet, so `make test` will collect nothing — I've flagged that in the test plan rather than claiming coverage.

**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders had no way to carry free-text context from the customer or operator. This adds an optional `note` field to orders: a new nullable `note` column on the `orders` table, a `create_order(note=None)` entry point in `orders.py` that accepts it, and a 500-character cap so unbounded text can't be stored.

## Changes
- **Schema / migration** — `migrations/0002_note.sql` adds a nullable `note TEXT` column to `orders`. Must be applied before deploying the code change.
- **`orders.py`** — new `create_order(note=None)` that returns the order payload with the note; raises `ValueError("note too long")` when the note exceeds 500 characters.
- **`README.md`** — mentions that orders support notes.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`): not run in this session. The repo currently has no test files, so this will collect zero tests — consider adding cases for `create_order()` with no note, a 500-char note, and a 501-char note before merging.
- [ ] Apply `migrations/0002_note.sql` against a dev database and confirm `orders.note` exists and is nullable.
- [ ] Manual: call `create_order(note="x" * 501)` and confirm it raises `ValueError`.

## Risk / rollback
- Schema change: adds a nullable column, so it is backward-compatible with existing rows and older code. Rollback of the column requires a manual `ALTER TABLE orders DROP COLUMN note` — there is no down migration in this PR.
- The 500-char limit is enforced only in `create_order`; nothing prevents longer values being written through other paths or directly in SQL.
- Code rollback: `git revert 7636fb5 8b7c1c1 c2579fb`.
```
