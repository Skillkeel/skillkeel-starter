No CHANGELOG.md yet, so I'll create one.

The repo had no `CHANGELOG.md`, so I created one in the Keep a Changelog format. It covers the 5 commits since the last tag, `v0.1.0`. The new entries are all under `## [Unreleased]`:

```markdown
## [Unreleased]

### Added

- **BREAKING:** Node 16 is no longer supported.
- `/health` API endpoint.
- Export to CSV (#12).

### Fixed

- Importing no longer fails on empty rows.
```

- **Breaking change:** `d2e792d feat!: drop Node 16 support` is first under Added with a **BREAKING:** prefix. The skill files every `feat` under Added, though dropping support would arguably fit better under a "Removed" section. I can move it if you prefer.
- **Left out:** `57b9e21 chore: bump eslint`, because it doesn't change anything for users.

The file isn't committed and I didn't tag a version. If you want to cut a release, I can turn `[Unreleased]` into a version number with today's date and suggest the `git tag` command.
