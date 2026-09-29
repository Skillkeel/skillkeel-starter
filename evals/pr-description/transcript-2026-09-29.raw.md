Here's the PR description. I used local `main` as the base because the repo has no remote or upstream configured, so I didn't run `git fetch`. I didn't run the tests either.

**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders can now carry an optional free-text note. This PR adds a nullable `note` column to the `orders` table and accepts a `note` argument in `create_order`. Notes longer than 500 characters are rejected.

## Changes
- **Schema migration:** `migrations/0002_note.sql` adds `note TEXT` to `orders`. The column is nullable and has no default.
- `orders.py`: new `create_order(note=None)`, which raises `ValueError("note too long")` if `note` is over 500 characters.
- `README.md`: mentions note support.

## Test plan
- [ ] `make test` (runs `python -m pytest -q`). Not run. The repo has no test files yet, so this proves nothing about the new code until tests are added.
- [ ] Manual: apply `migrations/0002_note.sql` to a dev DB and check that `orders.note` exists and is nullable.
- [ ] Manual: `create_order()` returns `{"note": None}`, `create_order("x" * 500)` succeeds, and `create_order("x" * 501)` raises `ValueError`.

## Risk / rollback
- **Migration:** the `ALTER TABLE ... ADD COLUMN` is additive and nullable, so it shouldn't affect existing rows. There is no down migration. Reverting the code (`git revert 4b5ad6c 1f4d0ca 09dd35b`) leaves the column in place. To remove it, run `ALTER TABLE orders DROP COLUMN note;` by hand.
- The 500-character limit only exists in `create_order`. The database doesn't enforce it, so writes that bypass `create_order` can store longer notes.
- An empty string is falsy, so `note=""` skips the length check. That's harmless, but callers will get `""` back rather than `None`.
```

I left off the "Generated with Claude Code" footer because the pr-description skill says not to add one unless you or the repo asks for it. Tell me if you want it added.
