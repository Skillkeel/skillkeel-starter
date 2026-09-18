Done. Summary of changes to `README.md`:

- **`npm run start` → `npm run dev`** — `package.json` has no `start` script; `dev` runs `node server.js`.
- **Added a minimal `## Test` section** with `npm test` — the script exists and I confirmed it runs cleanly (`node --test`, exit 0).
- **`docs/api.md` link** — the file doesn't exist. Per the skill rules I didn't delete the section; it's marked with a `<!-- TODO: verify -->` comment. Either create `docs/api.md` or drop the Docs section — your call.

Flagged but not changed:
- **License: MIT** — there's no `LICENSE` file in the repo. Worth adding one if MIT is intended.
- No Install section was added: the project has no dependencies or lockfile, so there's nothing to install beyond having Node available.

Rest of the prose is untouched. Nothing is committed — say the word if you'd like a commit.
