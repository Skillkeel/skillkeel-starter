No remote is configured, so the base is local `main`. Three commits, 6 added lines across `orders.py`, `migrations/0002_note.sql`, and `README.md`. The repo's only test entrypoint is `make test` (`python -m pytest -q`); there are no test files on the branch and I didn't run it.

**Title:** `feat(orders): add optional note field`

```markdown
## Summary
Orders can now carry a free-text note. This adds a nullable `note` column to the `orders` table, a `create_order(note=None)` entrypoint in `orders.py` that accepts the note, and a length cap (500 chars) so arbitrarily large notes are rejected before they hit the database. README updated to mention the feature.

## Changes
- `migrations/0002_note.sql`: new migration, `ALTER TABLE orders ADD COLUMN note TEXT` (nullable, no default, no backfill).
- `orders.py`: new `create_order(note=None)`; raises `ValueError("note too long")` when the note exceeds 500 characters.
- `README.md`: one-line mention that orders support notes.

## Test plan
- [ ] `make test`: runs `python -m pytest -q`. Not run in this session; note the branch adds no test files, so `create_order` length-cap behaviour (500 accepted, 501 rejected, `None` accepted) is currently unverified.
- [ ] Apply `migrations/0002_note.sql` against a dev database and confirm `orders.note` exists and is nullable.
- [ ] Manually call `create_order(note="x" * 501)` and confirm `ValueError`.

## Risk / rollback
- **Schema change**: `0002_note.sql` is additive (nullable column), so existing rows and readers are unaffected, but it must be applied before the new code is deployed.
- The 500-char cap is enforced only in Python, not in the schema (`TEXT` has no length constraint); direct DB writes can bypass it.
- Rollback: `git revert 7b56368 923706d f42804f`, then drop the column (`ALTER TABLE orders DROP COLUMN note`) if the migration has already been applied.
```
