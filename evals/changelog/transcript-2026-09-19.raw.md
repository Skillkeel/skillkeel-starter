No CHANGELOG.md exists, so I'll create it with the Keep a Changelog header. The `chore: bump eslint` commit isn't user-visible, so it's omitted.

Created `CHANGELOG.md` (none existed) with entries for the 5 commits since `v0.1.0`:

```markdown
## [Unreleased]

### Added
- **BREAKING:** Drop support for Node 16; Node 18 or later is now required.
- Add `/health` API endpoint.
- Add export to CSV (#12).

### Fixed
- Handle empty rows when importing.

## [0.1.0]
```

Notes:
- `869eaf9 chore: bump eslint` was omitted as not user-visible.
- The breaking change (`fb03fb6 feat!`) is listed first with the **BREAKING:** prefix. I assumed "Node 18 or later" as the new minimum since the commit doesn't state it — adjust if the actual floor is different.
- The `[0.1.0]` heading is a placeholder with no entries, since there's no prior changelog to preserve. Left uncommitted and no version bumped; say the word if you want to cut a release (`[Unreleased]` → `[0.2.0] - 2026-09-19` plus a proposed `git tag`).
