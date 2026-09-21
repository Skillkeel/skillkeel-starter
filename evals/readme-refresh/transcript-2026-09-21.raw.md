Done. Changes to `README.md`:

- **`npm run start` → `npm run dev`** — `package.json` only defines `dev` and `test` scripts.
- **Dead `docs/api.md` link** — replaced with a `<!-- TODO -->` marker; the `## Docs` heading is kept so you can fill it in or drop the section.
- **Added a minimal `## Test` section** with `npm test` (the `test` script exists: `node --test`).

Not changed, but worth noting:
- **`## License: MIT`** — there's no `LICENSE` file in the repo. I left the claim as-is since I can't verify it; add a `LICENSE` file if MIT is intended.
- I skipped an Install section: `package.json` has no dependencies, so `npm install` would be a no-op.

All other prose is untouched. Nothing has been committed.
