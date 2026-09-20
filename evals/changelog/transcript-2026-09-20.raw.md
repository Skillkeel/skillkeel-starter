No CHANGELOG.md exists, so I'll create one with the Keep a Changelog header. Range is `v0.1.0..HEAD` (5 commits; the eslint chore is omitted as not user-visible).

One correction: the commit only says Node 16 was dropped — there's no `package.json` to confirm the new minimum, so I'll drop the "Node 18" inference rather than invent it.

Created `CHANGELOG.md` (it didn't exist) covering `v0.1.0..HEAD`:

```markdown
## [Unreleased]

### Added

- **BREAKING:** Dropped support for Node 16.
- Added `/health` API endpoint.
- Added export to CSV (#12).

### Fixed

- Empty rows are now handled correctly during import.

## [0.1.0]
```

Traceability:
- `1082556 feat!: drop Node 16 support` → BREAKING, listed first
- `77dcecc feat(api): add /health endpoint` → Added
- `a4023fd feat: add export to CSV (#12)` → Added
- `5547b8c fix: handle empty rows in import` → Fixed
- `b3d0542 chore: bump eslint` → omitted (not user-visible)

The file is untracked and uncommitted. If you want to cut a release, say the version and I'll rename `[Unreleased]` to `[X.Y.Z] - 2026-09-20` and propose the tag command (given the breaking change, `0.2.0` would be the conventional bump for a pre-1.0 project).
