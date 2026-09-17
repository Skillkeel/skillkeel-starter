No `origin` remote is configured, so I diffed against local `main` (3 commits, 3 files). Note: `make test` currently fails in this environment because `pytest` isn't installed, and the repo has no test files yet.

**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders have no way to carry free-form customer/operator text. This adds an optional `note` field to orders: a new nullable `note TEXT` column on the `orders` table, and a `create_order(note=None)` entry point that rejects notes longer than 500 characters so unbounded input doesn't reach the database.

## Changes
- **Schema migration** — `migrations/0002_note.sql` adds a nullable `note TEXT` column to `orders`.
- **Order creation** — `orders.py` introduces `create_order(note=None)`, which raises `ValueError("note too long")` when the note exceeds 500 characters and otherwise returns the order payload with the note.
- **Docs** — `README.md` mentions that orders support notes.

## Test plan
- [ ] `make test` (`python -m pytest -q`): runs the suite. Not passing in this session — `pytest` is not installed and the repo contains no test files yet; consider adding cases for `create_order` with no note, a 500-char note, and a 501-char note.
- [ ] Apply `migrations/0002_note.sql` against a staging database and confirm `orders.note` exists and is nullable.
- [ ] Manually call `create_order(note="x" * 501)` and confirm it raises `ValueError`.

## Risk / rollback
- **Migration:** `0002_note.sql` alters the `orders` table. Adding a nullable column is low-risk and backwards-compatible, but there is no down migration — rolling back requires a manual `ALTER TABLE orders DROP COLUMN note`.
- The 500-character cap is enforced only in Python, not at the DB level; anything writing to `orders` outside `create_order` is unconstrained.
- Revert code with `git revert 675f6ab 5402f1a 3247433`, then drop the column as above.
```
