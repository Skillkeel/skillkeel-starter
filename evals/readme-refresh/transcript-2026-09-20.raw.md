Done. Two factual fixes applied, one section added, one item left for you:

- **`npm run start` → `npm run dev`** — `package.json` only defines `dev` and `test`.
- **`docs/api.md` link removed** — no `docs/` directory exists. I kept the `## Docs` heading with a `<!-- TODO: verify -->` comment rather than deleting the section, per the skill's rules. If you'd rather drop the section entirely or add the docs file, say so.
- **Added `## Test`** with `npm test` (verified: `node --test`).
- **License: MIT** — not changed, but flagged: there's no `LICENSE` file and no `license` field in `package.json`. Worth adding one or the other so the claim is backed by something.

Title, description, and License prose are untouched. Nothing is committed.
