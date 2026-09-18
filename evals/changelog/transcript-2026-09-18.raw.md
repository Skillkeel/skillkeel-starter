Last tag is `v0.1.0`; five commits since. Subjects are all clear, so no diffs needed. No CHANGELOG.md exists yet, so I'll create one with the Keep a Changelog header.

Created `CHANGELOG.md` from the 5 commits in `v0.1.0..HEAD`:

- `9a516b5 feat!: drop Node 16 support` → **BREAKING**, listed first under Added
- `7442058 feat(api): add /health endpoint` → Added
- `19cf1f0 feat: add export to CSV (#12)` → Added
- `18ce6ea fix: handle empty rows in import` → Fixed
- `e711e31 chore: bump eslint` → omitted (not user-visible)

One assumption to flag: I wrote "Node 18 or later is now required" — the commit only says Node 16 was dropped, so adjust that if the actual minimum is different.

The file is uncommitted. If you want to cut a release instead of leaving it under `[Unreleased]`, tell me the version (the breaking change suggests `v0.2.0` under 0.x semver) and I'll rename the heading and propose the tag command.
