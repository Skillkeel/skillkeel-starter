# pr-description: expected
Fixture: branch `feat/orders` vs `main`, 3 commits (feat, fix, docs), adds `migrations/0002_note.sql`; repo has `make test`.
1. Output has Summary / Changes / Test plan / Risk sections.
2. Migration explicitly called out under Risk (or Changes) as schema change.
3. Test plan uses the repo's real command (`make test` or `python -m pytest`), not an invented `npm test`.
4. Title ≤ 70 chars, starts with `feat`.
5. Does not claim tests passed unless it ran them.
