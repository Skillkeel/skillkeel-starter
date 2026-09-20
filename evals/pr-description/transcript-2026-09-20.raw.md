No remote is configured, so I diffed against local `main` (3 commits, 3 files). No test files exist yet; `make test` is the repo's only test entry point.

**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders had no way to carry free-text context from the caller. This adds an optional `note` to `create_order`, backed by a new nullable `note` column on the `orders` table, and caps the note at 500 characters so unbounded text can't be stored.

## Changes
- `orders.py`: new `create_order(note=None)`; raises `ValueError("note too long")` when the note exceeds 500 characters.
- `migrations/0002_note.sql`: `ALTER TABLE orders ADD COLUMN note TEXT;` (nullable, no default, no backfill).
- `README.md`: one-line mention that orders support notes.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`): not run — there are currently no test files in the repo, so this passes vacuously. A test for the >500-char rejection and the `None` default would be worth adding before merge.
- [ ] Apply `migrations/0002_note.sql` against a staging database and confirm existing rows read back with `note = NULL`.
- [ ] Manual: call `create_order(note="x" * 501)` and confirm `ValueError`; `create_order()` returns `{"note": None}`.

## Risk / rollback
**Schema change:** this PR adds a migration (`0002_note.sql`). The column is nullable `TEXT`, so it is additive and safe for existing rows, but the migration must be applied before deploying code that writes `note`. The 500-char cap is enforced only in Python, not in the schema.

Rollback: `git revert 178544f 7ba8b86 c6baf7e`, then drop the column (`ALTER TABLE orders DROP COLUMN note;`) if the migration was already applied.
```
