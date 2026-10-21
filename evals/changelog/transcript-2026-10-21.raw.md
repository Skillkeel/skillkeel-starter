I created `CHANGELOG.md`, since the repo didn't have one. It covers the 5 commits since the last tag, `v0.1.0`:

```markdown
## [Unreleased]

### Added
- **BREAKING:** Node 16 is no longer supported.
- `/health` endpoint in the API.
- Export to CSV (#12).

### Fixed
- Importing data with empty rows no longer fails.
```

- **Skipped:** `chore: bump eslint` isn't something users would notice, so I left it out.
- **Breaking change:** `feat!: drop Node 16 support` has the **BREAKING:** prefix and comes first. It's under "Added" because the skill puts `feat` commits there, but it fits "Removed" better. Say if you want it moved.
- **Not done:** I didn't commit the file or create a version or tag. If you're cutting a release, tell me the version number and I'll rename `[Unreleased]` to that version with today's date.
