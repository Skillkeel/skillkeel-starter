No remote, so base = local `main`. Diff: 3 commits, 3 files, new migration, no test files in repo. Tests not run.

**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders can now carry an optional free-text `note`. This adds the `note` column to the `orders` table, a `create_order` helper that accepts and validates the note (max 500 chars, longer input raises `ValueError`), and a README mention. No linked issue.

## Changes
- `migrations/0002_note.sql` — **new migration**: `ALTER TABLE orders ADD COLUMN note TEXT;` (nullable, no default, no backfill).
- `orders.py` — new `create_order(note=None)`; rejects notes over 500 characters with `ValueError("note too long")`.
- `README.md` — one-line mention that orders support notes.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`) — **not run in this session**. Note: the repo currently has no test files, so this will collect zero tests; consider adding a test for the 500-char cap and the `None` default before merge.
- [ ] Apply `migrations/0002_note.sql` against a dev DB and confirm `orders.note` exists and is nullable.
- [ ] Manual: call `create_order(note="x" * 501)` and confirm it raises; `create_order()` returns `{"note": None}`.

## Risk / rollback
- **Schema change**: adds a nullable `TEXT` column to `orders`. Additive and backward-compatible for existing rows, but on large tables `ALTER TABLE` may lock depending on the database engine. There is no down migration; rolling back requires a manual `ALTER TABLE orders DROP COLUMN note;`.
- Length cap is enforced only in `create_order`, not at the DB level. Any other write path can still store notes over 500 chars.
- Code rollback: `git revert 12c9e85 fcc7c3b e6978ff`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
