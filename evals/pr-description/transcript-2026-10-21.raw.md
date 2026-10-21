**Title:** `feat(orders): add optional note field to orders`

```markdown
## Summary
Orders can now carry an optional free-text note. A migration adds a nullable `note` column to `orders`, and `create_order` accepts a `note` argument and rejects anything over 500 characters. No linked issue.

## Changes
- `migrations/0002_note.sql`: **schema change**, `ALTER TABLE orders ADD COLUMN note TEXT;` (nullable, no default)
- `orders.py`: `create_order(note=None)` returns the note on the order and raises `ValueError("note too long")` when `len(note) > 500`
- `README.md`: notes that orders support notes

## Test plan
- [ ] `make test` (runs `python -m pytest -q`): not run. The branch adds no tests, so add cases for `note=None`, a 500-character note (accepted) and a 501-character note (`ValueError`)
- [ ] Apply `migrations/0002_note.sql` to a copy of the database and check that existing rows get `note = NULL`

## Risk / rollback
- **Migration:** `ADD COLUMN` on `orders` is nullable with no default, so it should be cheap on most engines. Still, check lock behaviour on a large table before deploying. Reverting the code does not drop the column. If a full rollback is needed, write a down migration (`ALTER TABLE orders DROP COLUMN note;`).
- The 500-character limit is only enforced in `create_order`, not in the database. Writes that skip this function can still store longer notes.
- Code rollback: `git revert cb819e3 d25bdca b576c77`.
```

I compared against local `main` because the repo has no `origin` remote, so I couldn't fetch first. The only test command in the repo is `make test`, and I didn't run it. I left off the "Generated with Claude Code" footer because the pr-description skill says not to add one.
