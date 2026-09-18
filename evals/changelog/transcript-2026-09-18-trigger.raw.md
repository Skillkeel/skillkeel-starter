Five commits since `v0.1.0`; no existing CHANGELOG.md, so I'll create one. Only the `chore` commit is omitted.

Created `CHANGELOG.md` with everything since `v0.1.0` under `## [Unreleased]`:

| Commit | Entry |
|---|---|
| `c288883` feat!: drop Node 16 support | **BREAKING:** Dropped support for Node 16 (listed first) |
| `82c93a9` feat(api): add /health endpoint | `/health` API endpoint |
| `7dff441` feat: add export to CSV (#12) | Export to CSV (#12) |
| `c515a57` fix: handle empty rows in import | Empty rows handled during import |
| `0ccb889` chore: bump eslint | omitted (not user-visible) |

One assumption to flag: the breaking entry says "Node 18 or later is now required" — that's inferred from dropping Node 16, not stated in the commit. Tweak it if the actual minimum differs. The file is left uncommitted; if you want to cut a version rather than leave this under `[Unreleased]`, tell me the number and I'll rename the heading and propose the tag command.
