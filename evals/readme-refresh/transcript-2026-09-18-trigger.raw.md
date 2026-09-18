Applied the factual fixes; the diff above is what changed.

**Fixed**
- `npm run start` → `npm run dev` (the only run script in `package.json`).
- Added a minimal **Test** section using the existing `npm test` script.

**Flagged, not removed** (can't verify, so marked with `<!-- TODO: verify -->` rather than deleted)
- `docs/api.md` link — the file doesn't exist. Either add the doc or drop the section.
- "MIT" license — there's no `LICENSE` file and no `license` field in `package.json`. If MIT is intended, add a `LICENSE` file and `"license": "MIT"`.

I skipped an Install section since `package.json` declares no dependencies. Nothing is committed; let me know if you want a commit.
