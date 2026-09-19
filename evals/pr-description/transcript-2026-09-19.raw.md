No remote is configured, so the base is local `main` (3 commits, 3 files). Here's the PR description:

---

**Title:** `feat(orders): add optional note field`

## Summary
Orders had no way to carry free-form customer or operator context. This adds an optional `note` to orders: a new nullable `note TEXT` column on the `orders` table, an `orders.create_order(note=None)` entry point that validates the note, and a README mention. Notes are capped at 500 characters — longer input raises `ValueError("note too long")` rather than being silently truncated.

## Changes
- **Schema:** new migration `migrations/0002_note.sql` — `ALTER TABLE orders ADD COLUMN note TEXT` (nullable, no default, no backfill).
- **`orders.py`:** new `create_order(note=None)` that rejects notes over 500 chars and returns the order dict with the note.
- **`README.md`:** one-line mention that orders support notes.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`): not run in this session. Note the repo currently has no test files, so this will collect zero tests — consider adding cases for `create_order()` with no note, a 500-char note, and a 501-char note before merging.
- [ ] Apply `migrations/0002_note.sql` against a copy of the database and confirm `orders.note` exists and existing rows read back with `note = NULL`.

## Risk / rollback
- **Migration:** adds a nullable column, so it is backward-compatible with existing rows and code that doesn't reference `note`. There is no down migration; rolling back the schema requires a manual `ALTER TABLE orders DROP COLUMN note`.
- **Validation:** the 500-char cap raises rather than truncates, so any caller passing longer notes will fail loudly.
- **Revert code:** `git revert 6805605 031b7ce 59d358b` (drop the schema column separately, as above).
