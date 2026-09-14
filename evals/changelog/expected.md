# changelog — expected
Fixture: tag v0.1.0 then 5 commits: 2 feat, 1 fix, 1 chore, 1 `feat!:` breaking.
1. CHANGELOG.md created with `## [Unreleased]`.
2. `chore: bump eslint` omitted.
3. Breaking change present, prefixed **BREAKING:**, listed first in its section.
4. `(#12)` reference preserved on the CSV export entry.
5. Exactly 4 user-facing entries (2 Added + 1 Fixed + 1 Added/BREAKING) — no invented ones.
