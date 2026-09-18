Now verifying the scripts list (read-only) rather than running them — there are no `node_modules`, so `vite`/`vitest`/`eslint` binaries aren't installed, and installing would write to the tree.

Wrote `CLAUDE.md` (46 lines) at the repo root.

**What it's based on** (all read from the repo, nothing invented):
- `package.json` scripts: `dev`, `build`, `test:ci`, `lint` — confirmed via `npm run` listing. Note there's no plain `test` script, so the file points at `pnpm test:ci`, matching what `.github/workflows/ci.yml` actually runs.
- `.nvmrc` → Node 20; `packageManager` → pnpm 9.0.0.
- `pnpm-lock.yaml` flagged as do-not-edit-by-hand.
- Git history is a single `chore: init` commit, so the convention note is Conventional Commits with no branch-naming rule yet.

**Two caveats on verification:**
- `pnpm` isn't on PATH in this environment and there's no `node_modules`, so I confirmed the script names/definitions but did not execute `vitest`, `eslint`, or `vite` themselves (that would have required an install, which writes to the tree).
- The "single test" example (`pnpm test:ci src/index.test.ts`) uses a file that doesn't exist yet — it's there to show the Vitest filter syntax. Adjust the path once you have real tests, or tell me to drop that row.
