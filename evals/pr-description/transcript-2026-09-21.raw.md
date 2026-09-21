**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders currently have no way to carry free-text context from the caller. This adds an optional `note` to orders: a new nullable `note TEXT` column on the `orders` table and a `create_order(note=None)` entry point that accepts it. Notes are capped at 500 characters — anything longer raises `ValueError("note too long")` rather than being silently truncated.

## Changes
- **Migration** `migrations/0002_note.sql`: `ALTER TABLE orders ADD COLUMN note TEXT` (nullable, no default, no backfill).
- **`orders.py`**: new `create_order(note=None)` that validates length (≤ 500 chars) and returns the order dict with the note.
- **`README.md`**: one-line mention that orders support notes.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`): not run in this session. Note: the repo currently has no test files, so this will collect nothing until tests for `create_order` are added — suggested cases: `note=None`, a 500-char note (accepted), a 501-char note (raises `ValueError`).
- [ ] Apply `migrations/0002_note.sql` against a staging DB and confirm `orders.note` exists and existing rows read back with `note = NULL`.

## Risk / rollback
- **Schema change:** adds a column to `orders`. Additive and nullable, so existing reads/writes are unaffected, but it is a migration and must be applied before the new code path is exercised in production. `ALTER TABLE` on a large `orders` table may lock briefly depending on the database.
- The 500-char cap is enforced only in `create_order`, not at the DB level (`TEXT` is unbounded); anything writing to the column outside this function bypasses the limit.
- **Rollback:** `git revert ff5cb54 da64647 d8d0c78`, then drop the column (`ALTER TABLE orders DROP COLUMN note`) if the migration was already applied. Dropping is safe as long as no rows have notes worth keeping.
```

Notes: the branch has no upstream and there is no `origin` remote, so I diffed against local `main`. Attribution footer omitted per the skill's rules.
